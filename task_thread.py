from PyQt5.QtCore import QThread, pyqtSignal
from webuiapi import webuiapi

from bean.task_bean import *
from config import *
from custom_api import CustomAPI
from log_utils import LogUtils

class TaskThread(QThread):
    printSignal = pyqtSignal(str)

    def __init__(self, ui, tasks: TasksBean, config):
        super().__init__()
        self.ui = ui
        self.tasks: TasksBean = tasks
        self.cus_api = CustomAPI(host=config.host, port=config.port)
        self.webui_api = webuiapi.WebUIApi(host=config.host, port=config.port)
        self.log_utils: LogUtils = ui.log_utils
        self.printSignal.connect(self.ui.print_log)

    def run(self) -> None:
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
                self.print_ui_log(f"connect server error : {e}")
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
                self.check_point_merger(human_model, style_model, base_model, save_model_name, task.task_merge)
                self.generate_image(save_model_name, human_model_cut, style_model_cut, task.task_txt_img)
            deleteResult = self.cus_api.delete_model()
            self.log_utils.i(f"delete result = {deleteResult.content}")
            self.log_utils.separator()


    def print_ui_log(self, log):
        self.printSignal.emit(log)

    def generate_image(self, model, primary_model_cut, secondary_model_cut, task_txt_img_json):
        self.log_utils.sys("start txt2img")
        task_txt_img = TaskTxt2Img()
        task_txt_img.__dict__ = task_txt_img_json
        self.webui_api.util_set_model(model)
        self.webui_api.util_wait_for_ready()
        result = self.webui_api.txt2img(
            prompt=f"({primary_model_cut}),{task_txt_img.prompt}",
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
        if not os.path.exists(style_dir):
            os.makedirs(style_dir)
        for index, image in enumerate(result.images):
            image.save(f'{style_dir}/{primary_model_cut}_{secondary_model_cut}_{index}.jpg')
        self.log_utils.i("end txt2img")

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
