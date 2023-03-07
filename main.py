import os
import sys

from webuiapi import webuiapi
from datetime import datetime

import env
from custom_api import CustomAPI


def print_hi(name):
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def generateImage(keyWord, model, primaryModelCut, secondaryModelCut):
    api.util_set_model(model)
    api.util_wait_for_ready()
    result = api.txt2img(
        prompt=f"({keyWord}),by Alice Pasquini and alena aenami, ((%s)), punk girl, purple hair, wild hair, leather jacket, concert lights",
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
    style_dir = f"{auto_dir}/{secondaryModelCut}/{primaryModelCut}"
    if not os.path.exists(style_dir):
        os.makedirs(style_dir)
    for index, image in enumerate(result.images):
        image.save(f'{style_dir}/{primaryModelCut}_{secondaryModelCut}_{index}.jpg')


def checkPointMerger(primaryModel, secondaryModel, saveName):
    result = cus_api.checkpointMerger(primary_model_name=primaryModel,
                                      secondary_model_name=secondaryModel,
                                      tertiary_model_name=baseModel,
                                      interp_method="Add difference",
                                      multiplier=0.9,
                                      save_as_half=False,
                                      custom_name=saveName,
                                      checkpoint_format="ckpt",
                                      config_source=0,
                                      bake_in_vae=None,
                                      discard_weights="")
    print(result.content)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cus_api = CustomAPI()
    api = webuiapi.WebUIApi(host=env.host, port=env.port)
    desktop_dir = os.path.expanduser('~/Desktop')
    auto_dir = f"{desktop_dir}/AutoTool/"
    if not os.path.exists(auto_dir):
        os.makedirs(auto_dir)
    models = api.util_get_model_names()
    baseModel = [model for model in models if 'v1-5-pruned.ckpt' in model][0]
    femaleModels = [model for model in models if 'female' in model]
    maleModels = [model for model in models if 'male' in model]
    #==========
    for mainModel in femaleModels:
        secondaryModel = 'style/cp_1366_elldrethsLucidMix_v10.safetensors'
        primaryModelCut = mainModel.split('/')[-1].split('.')[0]
        secondaryModelCut = secondaryModel.split('/')[-1].split('.')[0]
        saveModelName = f"AutoMerge/{primaryModelCut}/{primaryModelCut}_{secondaryModelCut}"
        checkPointMerger(mainModel, secondaryModel, saveModelName)
        generateImage(primaryModelCut, saveModelName, primaryModelCut, secondaryModelCut)
    cus_api.deleteModel()
