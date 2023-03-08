from webuiapi import webuiapi

from custom_api import CustomAPI

def delete_api():
    cus_api.delete_model()

def merge_api():
    cus_api.check_point_merge(primary_model_name=human_model, secondary_model_name=style_model, tertiary_model_name=base_model, custom_name=save_model_name)

if __name__ == '__main__':
    cus_api = CustomAPI(host="44.213.210.2", port="7860")
    webui_api = webuiapi.WebUIApi(host="44.213.210.2", port="7860")
    models = webui_api.util_get_model_names()
    style_model = 'style/elldrethsLucidMix_v10.ckpt'
    base_model = [model for model in models if '1-5-pruned.ckpt' in model][0]
    human_models = [model for model in models if 'female' in model.split('/')]
    human_model = human_models[0]
    human_model_cut = human_model.split('/')[-1].split('.')[0]
    style_model_cut = style_model.split('/')[-1].split('.')[0]
    save_model_name = f"AutoMerge/{style_model_cut}_{human_model_cut}"
    merge_api()
