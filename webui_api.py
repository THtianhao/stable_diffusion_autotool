import requests

class WebuiAPI:
    def __init__(self):
        self.simple_txt2img = None
        self.url_txt2img = None

    def setUp(self):
        self.url_txt2img = "http://44.213.210.2:7860/sdapi/v1/txt2img"
        self.simple_txt2img = {
            "enable_hr": False,
            "denoising_strength": 0,
            "firstphase_width": 0,
            "firstphase_height": 0,
            "prompt": "example prompt",
            "styles": [],
            "seed": -1,
            "subseed": -1,
            "subseed_strength": 0,
            "seed_resize_from_h": -1,
            "seed_resize_from_w": -1,
            "batch_size": 1,
            "n_iter": 1,
            "steps": 3,
            "cfg_scale": 7,
            "width": 64,
            "height": 64,
            "restore_faces": False,
            "tiling": False,
            "negative_prompt": "",
            "eta": 0,
            "s_churn": 0,
            "s_tmax": 0,
            "s_tmin": 0,
            "s_noise": 1,
            "sampler_index": "Euler a"
        }

    def test_txt2img_simple_performed(self):
        response = requests.post(self.url_txt2img, json=self.simple_txt2img)
        print(response)

    def test_txt2img_with_negative_prompt_performed(self):
        self.simple_txt2img["negative_prompt"] = "example negative prompt"
        response = requests.post(self.url_txt2img, json=self.simple_txt2img)
        print(response)
