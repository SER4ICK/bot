import requests
from pyexpat.errors import messages

from config import API_KEY, API_KEY_IMAGE
def gpt(text):
    url = "https://api.air.fail/public/text/chatgpt"
    data = {"model": "gpt-4" , "content": text, "info": {"temperature": 0.5}}
    headers = {"Autorization": API_KEY}
    response = requests.post(url, json=data , headers=headers)
    return response.json()[0]["content"]
def image(text):
    url = "https://api.air.fail/public/image"
    data = {"model": "gpt-4" , "content": text, "info": {"temperature": 0.5}}
    headers = {"Autorization": API_KEY_IMAGE}
    response = requests.post(url, json=data , headers=headers)
    return response.json()[0]["file"], response.json()[0]["content"]