# Author: Shahzain
# Credits: https://github.com/QIN2DIM/hcaptcha-challenger
import httpx
import capsolver
from io import BytesIO
import base64
import requests
import json


def image_url_to_base64(url):
    # Send a GET request to the image URL
    response = httpx.get(url)
    # Raise an exception if the request was unsuccessful
    response.raise_for_status()

    # Convert the image (response.content) to a Base64 string
    image_buffer = BytesIO(response.content)
    base64_bytes = base64.b64encode(image_buffer.getvalue())

    # Convert bytes to string
    base64_string = base64_bytes.decode("utf-8")

    return base64_string


def solve(images, example, question):
    apikey = "shahzain345-98fe324d-936f-c500-9930-f48d823f0f39"
    proapi = "https://pro.nocaptchaai.com/solve"

    base64_json = {
        "images": images,
        "target": question,
        "method": "hcaptcha_base64",  # method name
        "sitekey": "4c672d35-0701-42b2-88c3-78380b0db560",  # eg. b17a7-90bf-4070-9296-62679 from html page
        "site": "discord.com",  # url of the captcha page
        "ln": "en",  # "ru" for russian or  "ar" arabic | language of the captcha
        "examples": [],
    }

    headers = {
        "Content-type": "application/json",
        "apikey": apikey,
    }
    response = requests.post(proapi, headers=headers, data=json.dumps(base64_json))
    return response.json()


# def get_result(imgurls: list, label: str) -> bool:
#     solution = capsolver.solve(
#         {
#             "clientKey": "CAI-F53D11AC6BA3BD31DC284987881C28CB",
#             "type": "HCaptchaClassification",
#             "question": label,
#             "queries": queries,
#         }
#     )
#     return solution["solution"]["objects"]
