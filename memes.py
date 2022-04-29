import config
import random as rand
import requests

memes_array = []

def sa_url(thread, page = 0, sa_token=config.sa_token):
    if page > 0:
        return (f'https://api.fyad.club/threaddata/{thread}?token={sa_token}&page={page}')
    else:
        return (f'https://api.fyad.club/threaddata/{thread}?token={sa_token}')

def random_img(thread):
    response = requests.get(sa_url(thread))
    response.raise_for_status()
    img_json = response.json()
    total_pages = int(img_json['total_pages'])
    random_page_int = rand.randrange(total_pages+1)
    response = requests.get(sa_url(thread, random_page_int))
    img_json = response
    img_array = []
    for post in img_json:
        images = img_json[f'{post}']['imgs']
        img_array.append(images)
    while("" in img_array):
        img_array.remove("")
    
    return rand.randomchoice(img_array)
def random_meme():
    return random_img(3813092)
def random_funny():
    return random_img(3811995)
def random_curse():
    return random_img(3833370)
def random_cute():
    return random_img(3769444)