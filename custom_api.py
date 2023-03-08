import time

import requests


class CustomAPI:

    def __init__(self, host, port):
        self.baseUrl = f"http://{host}:{port}/sdapi/v1"

    def delete_model(self):
        url = f"{self.baseUrl}/delete_models"
        response = requests.Session().get(url=url)
        if response.status_code != 200:
            pass
        return response

    def check_point_merge(self,
                          primary_model_name="",
                          secondary_model_name="",
                          tertiary_model_name="",
                          interp_method="Add difference",
                          multiplier=1,
                          save_as_half=False,
                          custom_name="",
                          checkpoint_format="ckpt",
                          config_source=0,
                          bake_in_vae=None,
                          discard_weights=""
                          ):
        url = f"{self.baseUrl}/checkpoint-merger"
        payload = {
            "id_task": int(time.time()),
            "primary_model_name": primary_model_name,
            "secondary_model_name": secondary_model_name,
            "tertiary_model_name": tertiary_model_name,
            "interp_method": interp_method,
            "multiplier": multiplier,
            "save_as_half": save_as_half,
            "custom_name": custom_name,
            "checkpoint_format": checkpoint_format,
            "config_source": config_source,
            "bake_in_vae": bake_in_vae,
            "discard_weights": discard_weights
        }
        response = requests.Session().post(url=url, json=payload)
        return response
