from webuiapi import webuiapi

from custom_api import CustomAPI

def delete_api(path):
    cus_api.delete_model(path)

def merge_api():
    models = webui_api.util_get_model_names()
    style_model = 'style/elldrethsLucidMix_v10.ckpt'
    base_model = [model for model in models if '1-5-pruned.ckpt' in model][0]
    human_models = [model for model in models if 'female' in model.split('/')]
    human_model = human_models[0]
    human_model_cut = human_model.split('/')[-1].split('.')[0]
    style_model_cut = style_model.split('/')[-1].split('.')[0]
    save_model_name = f"AutoMerge/{style_model_cut}_{human_model_cut}"
    cus_api.check_point_merge(primary_model_name=human_model, secondary_model_name=style_model, tertiary_model_name=base_model, custom_name=save_model_name)

local_host = "127.0.0.1"
server_host = "44.213.210.2"

if __name__ == '__main__':
    cus_api = CustomAPI(host=local_host, port="7860")
    webui_api = webuiapi.WebUIApi(host=local_host, port="7860")
    delete_api('aaa')
    # merge_api()
