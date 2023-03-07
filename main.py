from webuiapi import webuiapi
from datetime import datetime

import env
from custom_api import CustomAPI


def print_hi(name):
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def generateImage(model):
    checkPointName = model.split('/')[-1].split('.')[0]
    api.util_set_model(model)
    api.util_wait_for_ready()
    result = api.txt2img(
        prompt=f"((({checkPointName}))),film style, the most outstanding photo in the world, Asian beauty, mesmerizing eyes, (((narrow face))), (((narrow nose bridge))), full and inviting lips, flawless skin, (few natural freckles:0.7), (((colorful hair in the wind))), (((rim light on the face))), slim figure, sexy and cute girl, pronounced feminine feature, amazing body, street in sunset, neon lights, intricate, highly detailed, extremely hyper aesthetic, masterpiece, highest quality, lens flare, dramatic lighting, sharp focus, photorealism, HDR, 8K, mannerism, cinematography, by Adrian Zingg and johnson ting",
        negative_prompt="(low quality, worst quality:1.4),",
        seed=-1,
        styles=["anime"],
        cfg_scale=7,
        sampler_index='DPM++ SDE Karras',
        steps=33,
        batch_size=4
        # enable_hr=True,
        # hr_scale=2,
        # hr_upscaler=webuiapi.HiResUpscaler.Latent,
        # hr_second_pass_steps=20,
        # hr_resize_x=1536,
        # hr_resize_y=1024,
        # denoising_strength=0.4,
    )
    for image in result.images:
        image.save(f'/Users/toto/Desktop/{checkPointName}_{datetime.now()}.jpg')


def checkPointMerger(model):
    primaryModel = model.split('/')[-1]
    secondaryModel = 'dreamshaper_331BakedVae.ckpt'
    result = cus_api.checkpointMerger(primary_model_name=primaryModel,
                                      secondary_model_name=secondaryModel,
                                      tertiary_model_name="v1-5-pruned.ckpt",
                                      interp_method="Add difference",
                                      multiplier=1,
                                      save_as_half=False,
                                      custom_name=f"AutoMerge/{secondaryModel}/{primaryModel}",
                                      checkpoint_format="ckpt",
                                      config_source=0,
                                      bake_in_vae=None,
                                      discard_weights="")
    print(result)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cus_api = CustomAPI()
    api = webuiapi.WebUIApi(host=env.host, port=env.port)
    api.set_auth('toto', '123456')
    models = api.util_get_model_names()
    femaleModels = [model for model in models if 'female' in model]
    maleModels = [model for model in models if 'male' in model]
    for femaleModels in femaleModels:
        checkPointMerger(femaleModels)
    for femaleModel in femaleModels:
        generateImage(femaleModel)
