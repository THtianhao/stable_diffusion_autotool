import time

import requests

import env


class CustomAPI:

    def __init__(self):
        self.baseUrl = f"http://{env.host}:{env.port}/sdapi/v1"

    def checkpointMerger(self,
                         primary_model_name="",
                         secondary_model_name="",
                         tertiary_model_name="",
                         interp_method="",
                         multiplier=0,
                         save_as_half=False,
                         custom_name="",
                         checkpoint_format="",
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
        if response.status_code != 200:
            pass
        return response
