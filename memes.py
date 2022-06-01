from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
import requests
import random
import loki

def sa_url(thread, page = 0):
    if page > 0:
        return f"https://forums.somethingawful.com/showthread.php?threadid={thread}&userid=0&perpage=40&pagenumber={page}"
    else:
        return f"https://forums.somethingawful.com/showthread.php?threadid={thread}&userid=0&perpage=40&pagenumber=1"

def get_random_page(thread):
    r = requests.get(sa_url(thread))
    loki.log('info', 'memes.get_random_page', f"Finding random page for {thread}")
    soup = bs(r.text, features="html.parser")
    pages = int(soup.find(class_="pages top").find(title="Last page").string[:4])
    loki.log('info', 'memes.get_random_page', f"Got total pages: {pages}")
    return random.randint(1, pages)

def random_img(thread):
    page = get_random_page(thread)
    loki.log('info', 'memes.random_img', f"Scraping page {page} of thread {thread}")
    r = requests.get(sa_url(thread, page))
    posts = SoupStrainer(class_='postbody')
    soup = bs(r.text, parse_only=posts, features="html.parser")
    loki.log('info', 'memes.random_img', f"Made soup out of posts.")
    #for tag in posts.find_all:
    images = []
    for tag in soup.find_all('img'):
        loki.log('info', 'memes.random_img', f"Scanning tags for images.")
        if "somethingawful.com" in tag['src']:
            loki.log('info', 'memes.random_img', f"Found SA link, skipping.")
            continue
        else:
            images.append(tag['src'])
    if len(images) == 0:
        loki.log('info', 'memes.random_img', f"Page had zero images. Attempting another search.")
        random_img(thread)
    else:
        image = random.choice(images)
        loki.log('info', 'memes.random_img', f"Got images. Sending: {image}")
        return image

def random_meme(thread):
    loki.log('info', 'memes.random_meme', f"MEMES!")
    return random_img(thread)
