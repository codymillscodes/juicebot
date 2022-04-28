import json
import requests
import config
import numpy as np
import random

memes_array = []
response = requests.get(f'https://api.fyad.club/threaddata/3813092?token={config.sa_token}')
response.raise_for_status()
jsonResponse = response.json()
thread_pages = int(jsonResponse['total_pages'])
def memes_compile():
    try:
        for i in range(1, thread_pages):
            response = requests.get(f'https://api.fyad.club/threaddata/3813092?token={config.sa_token}&page={i}')
            jsonResponse = response.json()
            for post in jsonResponse:
                images = jsonResponse[f'{post}']['imgs']
                #print(images)
                memes_array.append(images)
    except (TypeError, KeyError):
        pass
    while("" in memes_array):
        memes_array.remove("")

 #   np.savetxt('meme_links.txt', memes_array)

def random_meme():
    return random.choice(memes_array)