from PyQt5.QtCore import QThread, pyqtSignal
from webuiapi import webuiapi

from bean.task_bean import *
from config import *
from custom_api import CustomAPI

class TaskThread(QThread):
    printSignal = pyqtSignal(str)

    def __init__(self, ui, tasks: TasksBean):
        super().__init__()
        self.ui = ui
        self.tasks: TasksBean = tasks
        self.cus_api = CustomAPI()
        self.webui_api = webuiapi.WebUIApi(host=config.get(host_flag), port=config.get(port_flag))
        self.printSignal.connect(self.ui.print_log)

    def run(self) -> None:
        for task in self.tasks.tasks:
            models = self.webui_api.util_get_model_names()
            base_model = [model for model in models if task.base_model_flag in model][0]
            human_models = [model for model in models if task.human_model_dir_flag in model]
            for human_model in human_models:
                style_model = task.style_model
                human_model_cut = human_model.split('/')[-1].split('.')[0]
                style_model_cut = style_model.split('/')[-1].split('.')[0]
                save_model_name = f"AutoMerge/{style_model_cut}/{human_model_cut}_{style_model_cut}"
                self.check_point_merger(human_model, style_model, base_model, save_model_name, task.taskMerge)
                self.generate_image(save_model_name, human_model_cut, style_model_cut, task.taskTxt2Img)
            self.cus_api.delete_model()

    def printUILog(self, log):
        self.printSignal.emit(log)

    def generate_image(self, model, primary_model_cut, secondary_model_cut, taskTxt2Image):
        self.webui_api.util_set_model(model)
        self.webui_api.util_wait_for_ready()
        result = self.webui_api.txt2img(
            prompt=f"({primary_model_cut}),{taskTxt2Image.prompt}",
            negative_prompt=f"{taskTxt2Image.negative_prompt}",
            seed=taskTxt2Image.seed,
            styles=["anime"],
            cfg_scale=taskTxt2Image.cfg_scale,
            sampler_index=taskTxt2Image.sampler_index,
            steps=taskTxt2Image.steps,
            batch_size=taskTxt2Image.batch_size
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

    def check_point_merger(self, primary_model, secondary_model, base_model, save_name, taskMerge):
        result = self.cus_api.check_point_merge(primary_model_name=primary_model,
                                                secondary_model_name=secondary_model,
                                                tertiary_model_name=base_model,
                                                interp_method=taskMerge.interp_method,
                                                multiplier=taskMerge.multiplier,
                                                save_as_half=False,
                                                custom_name=save_name,
                                                checkpoint_format=taskMerge.checkpoint_format,
                                                config_source=0,
                                                bake_in_vae=None,
                                                discard_weights="")
        print(result.content)
