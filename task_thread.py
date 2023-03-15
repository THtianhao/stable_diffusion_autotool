import shutil
import traceback
from datetime import datetime

from PyQt5.QtCore import QThread, pyqtSignal
from webuiapi import webuiapi

from api.feishu_api import FeishuApi
from bean.result_bean import ResultBean
from bean.task_bean import *
from config import *
from api.custom_api import CustomAPI
from log_utils import LogUtils

class TaskThread(QThread):
    printSignal = pyqtSignal(str)

    def __init__(self, ui, tasks: TasksBean, config):
        super().__init__()
        self.config: ConfigBean = config
        self.should_stop = False
        self.ui = ui
        self.tasks: TasksBean = tasks
        self.cus_api = CustomAPI(host=config.host, port=config.port)
        self.webui_api = webuiapi.WebUIApi(host=config.host, port=config.port)
        self.log_utils: LogUtils = ui.log_utils
        self.feishu_api = FeishuApi()
        self.printSignal.connect(self.ui.print_log)
        self.result = ResultBean()
        print("init finished")

    def run(self) -> None:
        try:
            if self.config.upload_feishu == 1:
                if not self.check_feishu():
                    return
            self.log_utils.sys(f"total task is  {len(self.tasks.tasks)}")
            for index, taskjson in enumerate(self.tasks.tasks):
                self.log_utils.separator()
                self.log_utils.sys(f"start Tasks {index + 1} of {len(self.tasks.tasks)}")
                task = TaskBean()
                task.__dict__ = taskjson
                models = None
                try:
                    models = self.webui_api.util_get_model_names()
                except Exception as e:
                    self.log_utils.e(f"connect server error : {e}")
                    return
                base_models = [model for model in models if task.base_model_flag in model]
                if len(base_models) == 0:
                    self.log_utils.e("can not find base models")
                    return
                base_model = base_models[0]
                human_models = [model for model in models if task.human_model_dir_flag in model.split('/')]
                if len(human_models) == 0:
                    self.log_utils.e("can not find human models")
                    return
                style_model = task.style_model
                style_model_cut = style_model.split('/')[-1].split('.')[0]
                style = [model for model in models if style_model in model][0]
                for index_human, human_model in enumerate(human_models):
                    human_model_cut = human_model.split('/')[-1].split('.')[0]
                    save_model_name = f"AutoTool/{style_model_cut}/{style_model_cut}_{human_model_cut}"
                    filter_model = [model for model in models if f"{save_model_name}.ckpt" in model]
                    if len(filter_model) == 0:
                        self.check_point_merger(human_model, style, base_model, save_model_name, task.task_merge)
                        if self.__check_need_stop():
                            return
                    else:
                        self.log_utils.e(f"{save_model_name}.ckpt already have")
                    if self.config.operation == 1:
                        images = self.generate_image(save_model_name, human_model_cut, style_model_cut, task.task_txt_img)
                        if self.config.upload_feishu == 1:
                            self.create_feishu_sheet(index_human, style_model_cut)
                            self.upload_feishu(index_human, task, human_model_cut)
                            self.upload_images(index_human, images)
                            if index_human == len(human_models) - 1:
                                self.at_when_finished(index_human + 3)
                        if self.__check_need_stop(): return
                        if task.delete_after_merge:
                            self.__delete_models(style_model_cut)

                self.log_utils.separator()
            self.log_utils.sys("====All Task complete====")
            for url in self.result.links:
                self.log_utils.sys(f"文档地址 :{url}")
        except:
            self.log_utils.e(traceback.format_exc())

    def at_when_finished(self, line):
        if len(self.config.at_email) == 0:
            return
        test_value = {
            "valueRange": {
                "range": f"{self.sheet_id}!A{line}:A{line}",
                "values": [
                    [
                        {
                            "type": "mention",
                            "text": f"{self.config.at_email}",
                            "textType": "email",
                            "notify": True,
                            "grantReadPermission": True
                        }
                    ]
                ]
            }
        }
        self.feishu_api.qut_sheet(self.file_token, test_value)

    def create_feishu_sheet(self, human_index, style_model_cut):
        if human_index == 0:
            time_format = datetime.now().strftime("%H:%M:%S")
            feishu_folder_name = f'{style_model_cut}_{time_format}'
            root_token = self.feishu_api.get_root_token()
            sheet = self.feishu_api.create_sheet(feishu_folder_name, root_token)
            self.file_token = sheet['spreadsheet_token']
            self.result.links.append(sheet['url'])
            self.sheet_id = self.feishu_api.query_sheetId(self.file_token)
            self.feishu_create_title(self.file_token, self.sheet_id)

    def feishu_create_title(self, file_token, sheet_id):
        title = {
            "valueRange": {
                "range": f"{sheet_id}!A1:M1",
                "values": [
                    [
                        "效果图1", "效果图2", "效果图3", "效果图4", "人物资源", "风格资源", "提示词", "反向提示词", "采样方式", "采样步数", "CFG Scale", "seed", "Checkpoint Multiplier"
                    ]
                ]
            }
        }
        self.feishu_api.qut_sheet(file_token, title)

    def upload_images(self, index, images):
        for image_index, image in enumerate(images):
            column_flag = ""
            if image_index == 0:
                column_flag = "A"
            elif image_index == 1:
                column_flag = "B"
            elif image_index == 2:
                column_flag = "C"
            elif image_index == 3:
                column_flag = "D"
            self.feishu_api.post_image(self.file_token, f"{self.sheet_id}!{column_flag}{index + 2}:{column_flag}{index + 2}", image)

    def upload_feishu(self, index, task, human_model_cut):
        if self.file_token is not None:
            line = {
                "valueRange": {
                    "range": f"{self.sheet_id}!E{index + 2}:M{index + 2}",
                    "values": [
                        [
                            human_model_cut,
                            task.style_model,
                            task.task_txt_img['prompt'],
                            task.task_txt_img['negative_prompt'],
                            task.task_txt_img['sampler_index'],
                            task.task_txt_img['steps'],
                            task.task_txt_img['cfg_scale'],
                            task.task_txt_img['seed'],
                            task.task_merge['multiplier']
                        ]
                    ]
                }
            }
            self.feishu_api.qut_sheet(self.file_token, line)

    def check_feishu(self):
        response = self.feishu_api.getToken('cli_a483ea8b94e3100e', 'UhJeWk7YxAgzhbc6mOz6xh7Gkfwu6eGS')
        if response is not None:
            if self.config.refresh_token is not None and len(self.config.refresh_token) != 0:
                refreshResult = self.feishu_api.refresh_user_access_token(self.config.refresh_token)
                if refreshResult is not None:
                    self.config.refresh_token = refreshResult.refresh_token
                    write_config(self.config.__dict__)
                    return True
            else:
                userResult = self.feishu_api.get_user_access_token(self.config.feishu_code)
                if userResult is not None:
                    self.config.refresh_token = userResult.refresh_token
                    write_config(self.config.__dict__)
                    return True
        else:
            self.log_utils.e("access token error")
        return False

    def stop(self):
        self.should_stop = True
        self.log_utils.sys("Waiting for stop tasks...")

    def __check_need_stop(self) -> bool:
        if self.should_stop:
            self.log_utils.sys("All tasks stopped")
            return True
        return False

    def __delete_all_models(self):
        self.log_utils.i("delete all merge models")
        deleteResult = self.cus_api.delete_model()
        self.log_utils.i(f"delete result = {deleteResult.content}")

    def __delete_models(self, path):
        self.log_utils.i(f"delete  models {path}")
        deleteResult = self.cus_api.delete_model(path)
        self.log_utils.i(f"delete result = {deleteResult.content}")

    def generate_image(self, model, primary_model_cut, secondary_model_cut, task_txt_img_json):
        self.log_utils.sys("start txt2img")
        task_txt_img = TaskTxt2Img()
        task_txt_img.__dict__ = task_txt_img_json
        self.webui_api.util_set_model(model)
        self.webui_api.util_wait_for_ready()
        prompt = f"({primary_model_cut}:{task_txt_img.human_weight}),{task_txt_img.prompt}"
        self.log_utils.sys(f'prompt = {prompt}')
        result = self.webui_api.txt2img(
            prompt=prompt,
            negative_prompt=f"{task_txt_img.negative_prompt}",
            seed=task_txt_img.seed,
            styles=["anime"],
            cfg_scale=task_txt_img.cfg_scale,
            sampler_index=task_txt_img.sampler_index,
            steps=task_txt_img.steps,
            batch_size=task_txt_img.batch_size
            # enable_hr=True,
            # hr_scale=2,
            # hr_upscaler=webuiapi.HiResUpscaler.Latent,
            # hr_second_pass_steps=20,
            # hr_resize_x=1536,
            # hr_resize_y=1024,
            # denoising_strength=0.4,
        )
        style_dir = f"{env.globalRootPath}/{secondary_model_cut}/{primary_model_cut}"
        if os.path.exists(style_dir):
            shutil.rmtree(style_dir)
        if not os.path.exists(style_dir):
            os.makedirs(style_dir)
        for index, image in enumerate(result.images):
            image.save(f'{style_dir}/{primary_model_cut}_{secondary_model_cut}_{index}.jpg')
        self.log_utils.sys("end txt2img")
        return result.images

    def check_point_merger(self, primary_model, secondary_model, base_model, save_name, task_merge_json):
        self.log_utils.i(f"start merge : {primary_model} + {secondary_model}")
        task_merge = TaskMerge()
        task_merge.__dict__ = task_merge_json
        result = self.cus_api.check_point_merge(primary_model_name=primary_model,
                                                secondary_model_name=secondary_model,
                                                tertiary_model_name=base_model,
                                                interp_method=task_merge.interp_method,
                                                multiplier=task_merge.multiplier,
                                                save_as_half=False,
                                                custom_name=save_name,
                                                checkpoint_format=task_merge.checkpoint_format,
                                                config_source=0,
                                                bake_in_vae=None,
                                                discard_weights="")
        self.log_utils.i(f"merge result {result.content}")
