import config
import json
import requests
from hurry.filesize import size
from py1337x import py1337x
import discord

torrents = py1337x(proxy="1337x.to", cache="cache", cacheTime=5000)

def debrid_url(domain, action, arg):
    return str(
        f"https://api.alldebrid.com/v4/{domain}/{action}?agent={config.debrid_host}&apikey={config.debrid_key}&{arg}"
    )

def add_magnet(magnet):
    url = debrid_url("magnet", "upload", "magnets[]=") + magnet
    j = json.loads(requests.get(url).text)['data']['magnets'][0]
    ready_bool = j['ready']
    name = j['name']
    magnet_id = j['id']
    return ready_bool, name, magnet_id #returns ready bool, filename and magnet id

def unlock_link(link):
    url = debrid_url("link", "unlock", "link=") + link
    j = json.loads(requests.get(url).text)["data"]
    return j

def get_unhosted_links(magnet_id):
    url = debrid_url("magnet", "status", "id=") + str(magnet_id)
    t = json.loads(requests.get(url).text)["data"]["magnets"]["links"]
    return t

def build_link_info(magnet_id):
    links = get_unhosted_links(magnet_id)
    link_info = []
    for link in links:
        unlockedLink = unlock_link(link=link["link"])
        link_info.append(
            {"name": unlockedLink["filename"], "link": unlockedLink["link"], "size": size(int(unlockedLink["filesize"]))}
        )
    return link_info

def search1337(query):
    results = torrents.search(query, sortBy="seeders", order="desc")
    return results

def magnet_info(torrent_id):
    return torrents.info(torrentId=torrent_id)['magnetLink']

def get_status():
    return json.loads(requests.get(debrid_url('magnet', 'status', 'status=active')).text)['data']

# def live_status(counter):
#     url = debrid_url('magnet', 'status', f'session={config.debrid_session}&counter={counter}')
#     live_status = json.loads(requests.get(url).text)["data"]
#     link_info = {}
#     counter = live_status["counter"]

#     if len(live_status['magnets']) <= 0:
#         return False
#     else:
#         updates = {}
#         for link in live_status["magnets"][:10]:
#             updates["id"] = link["id"] 
#             updates["downloaded"] = link["downloaded"] 
#             updates["dl_speed"] = link["downloadSpeed"]
#             print(updates)
#     link_info.update(updates)
#     print("link_info")
#     print(link_info)

#     return counter, link_info