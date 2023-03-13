import os
import shutil
import traceback

from PyQt5.QtCore import QThread, pyqtSignal
from webuiapi import webuiapi

from api.feishu_api import FeishuApi
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
        print("init")
        self.ui = ui
        self.tasks: TasksBean = tasks
        self.cus_api = CustomAPI(host=config.host, port=config.port)
        self.webui_api = webuiapi.WebUIApi(host=config.host, port=config.port)
        self.log_utils: LogUtils = ui.log_utils
        self.feishu_api = FeishuApi(self.log_utils)
        self.printSignal.connect(self.ui.print_log)
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
                for human_model in human_models:
                    style_model = task.style_model
                    human_model_cut = human_model.split('/')[-1].split('.')[0]
                    style_model_cut = style_model.split('/')[-1].split('.')[0]
                    save_model_name = f"AutoTool/{style_model_cut}/{style_model_cut}_{human_model_cut}"
                    filter_model = [model for model in models if f"{save_model_name}.ckpt" in model]
                    style = [model for model in models if style_model in model][0]
                    if len(filter_model) == 0:
                        self.check_point_merger(human_model, style, base_model, save_model_name, task.task_merge)
                        if self.__check_need_stop():
                            return
                    else:
                        self.log_utils.e(f"{save_model_name}.ckpt already have")
                    if self.config.operation == 2:
                        self.generate_image(save_model_name, human_model_cut, style_model_cut, task.task_txt_img)
                        if self.__check_need_stop(): return
                        if task.delete_after_merge:
                            self.__delete_models(style_model_cut)
                self.log_utils.separator()
            self.log_utils.sys("====All Task complete====")
        except:
            self.log_utils.e(traceback.format_exc())

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
                userResult = self.feishu_api.getUserToken(self.config.feishu_code)
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
