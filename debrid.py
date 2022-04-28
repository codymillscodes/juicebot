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

def get_status(magnet_id=0, all=False):
    if all:
        return json.loads(requests.get(debrid_url('magnet', 'status', 'status=active')).text)['data']
    else:    
        magnet_json = json.loads(requests.get(debrid_url('magnet', 'status', f'id={magnet_id}')).text)
        if 'data' in magnet_json.keys():
            if magnet_json['data']['magnets']['status'].lower() == 'ready':
                status = 'ready'
                return status
            else:
                status = 'not ready'
                return status
        else:
            status = 404
            return status