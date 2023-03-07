import codecs
import json
import os

from PyQt5.QtWidgets import QMainWindow
from webuiapi import webuiapi

import env
from custom_api import CustomAPI
from ui.main import Ui_MainWindow

class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.config = None
        self.host_tag = "host"
        self.port_tag = "port"
        self.file_tag = "chrome_config"
        self.setupUi(self)
        self.chromePathExploer.clicked.connect(self.saveConfig)

        self.cus_api = CustomAPI()
        self.api = webuiapi.WebUIApi(host=env.host, port=env.port)
        desktop_dir = os.path.expanduser('~/Desktop')
        self.auto_dir = f"{desktop_dir}/AutoTool/"
        if not os.path.exists(self.auto_dir):
            os.makedirs(self.auto_dir)
        models = self.api.util_get_model_names()
        self.baseModel = [model for model in models if 'v1-5-pruned.ckpt' in model][0]
        femaleModels = [model for model in models if 'female' in model]
        maleModels = [model for model in models if 'male' in model]
        for mainModel in femaleModels:
            secondaryModel = 'style/cp_1366_elldrethsLucidMix_v10.safetensors'
            primaryModelCut = mainModel.split('/')[-1].split('.')[0]
            secondaryModelCut = secondaryModel.split('/')[-1].split('.')[0]
            saveModelName = f"AutoMerge/{primaryModelCut}/{primaryModelCut}_{secondaryModelCut}"
            self.check_point_merger(mainModel, secondaryModel, saveModelName)
            self.generate_image(primaryModelCut, saveModelName, primaryModelCut, secondaryModelCut)
        self.cus_api.delete_model()

    def save_config(self):
        host = self.host.text()
        port = self.port.text()
        self.writeConfig(self.hostTag, host)
        self.writeConfig(self.portTag, port)

    def write_config(self, key, value):
        try:
            if self.config.get(key) is None or self.config[key] != value or len(self.config[key]) != 0:
                self.config[key] = value
                with open(env.getConfigPath(), 'w') as writeFile:
                    json.dump(self.config, writeFile)
        except Exception as e:
            self.print_log("json保存错误!" + str(e))

    def read_config(self):
        if not os.path.exists(env.getConfigPath()):
            with codecs.open(env.getConfigPath(), 'a+', encoding='utf-8') as f:
                f.write("{}")
                return
        try:
            with open(env.getConfigPath()) as f:
                self.config = json.load(f)
                host = self.config.get(self.host)
                port = self.config.get(self.port)
                self.metaPass.setText('' if host is None else host)
                self.chromePathEdit.setText('' if port is None else port)
        except Exception as e:
            print(e)

    def click_start(self):
        pass

    def delete_dir(self):
        pass

    def generate_image(self, keyword, model, primary_model_cut, secondary_model_cut):
        self.api.util_set_model(model)
        self.api.util_wait_for_ready()
        result = self.api.txt2img(
            prompt=f"({keyword}),by Alice Pasquini and alena aenami, ((%s)), punk girl, purple hair, wild hair, leather jacket, concert lights",
            negative_prompt="worst quality, low quality, medium quality, deleted, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, jpeg artifacts, signature, watermark, username, blurry",
            seed=-1,
            styles=["anime"],
            cfg_scale=7,
            sampler_index='DPM++ 2S a Karras',
            steps=22,
            batch_size=4
            # enable_hr=True,
            # hr_scale=2,
            # hr_upscaler=webuiapi.HiResUpscaler.Latent,
            # hr_second_pass_steps=20,
            # hr_resize_x=1536,
            # hr_resize_y=1024,
            # denoising_strength=0.4,
        )
        style_dir = f"{self.auto_dir}/{secondary_model_cut}/{primary_model_cut}"
        if not os.path.exists(style_dir):
            os.makedirs(style_dir)
        for index, image in enumerate(result.images):
            image.save(f'{style_dir}/{primary_model_cut}_{secondary_model_cut}_{index}.jpg')

    def check_point_merger(self, primary_model, secondary_model, save_name):
        result = self.cus_api.check_point_merge(primary_model_name=primary_model,
                                                secondary_model_name=secondary_model,
                                                tertiary_model_name=self.baseModel,
                                                interp_method="Add difference",
                                                multiplier=0.9,
                                                save_as_half=False,
                                                custom_name=save_name,
                                                checkpoint_format="ckpt",
                                                config_source=0,
                                                bake_in_vae=None,
                                                discard_weights="")
        print(result.content)
