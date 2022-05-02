from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
import requests
import random

def sa_url(thread, page = 0):
    if page > 0:
        return f"https://forums.somethingawful.com/showthread.php?threadid={thread}&userid=0&perpage=40&pagenumber={page}"
    else:
        return f"https://forums.somethingawful.com/showthread.php?threadid={thread}&userid=0&perpage=40&pagenumber=1"
def get_random_page(thread):
    r = requests.get(sa_url(thread))
    soup = bs(r.text, features="html.parser")
    pages = int(soup.find(class_="pages top").find(title="Last page").string[:4])
    return random.randint(1, pages)

def random_img(thread):
    r = requests.get(sa_url(thread, get_random_page(thread)))
    posts = SoupStrainer(class_='postbody')
    soup = bs(r.text, parse_only=posts, features="html.parser")
    #for tag in posts.find_all:
    images = []
    for tag in soup.find_all('img'):
        if "somethingawful.com" in tag['src']:
            continue
        else:
            images.append(tag['src'])
    if len(images = 0):
        random_img(thread)
    else:
        return random.choice(images)

def random_meme(thread):
    return random_img(thread)
