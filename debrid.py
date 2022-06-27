import config
import json
import requests
import time
import loki
from hurry.filesize import size
from py1337x import py1337x

torrents = py1337x(proxy="1337x.to", backend='memory')

plus = "%2B"

def debrid_url(domain, action, arg):
    loki.log('info', 'debrid.debrid_url', f"Sending URL for {domain} {action}")
    loki.log('debug', 'debrid.debrid_url', f"Argument: {arg}")
    return str(f"https://api.alldebrid.com/v4/{domain}/{action}?agent={config.debrid_host}&apikey={config.debrid_key}&{arg}")

def add_magnet(magnet):
    url = debrid_url("magnet", "upload", "magnets[]=") + magnet
    j = json.loads(requests.get(url).text)['data']['magnets'][0]
    ready_bool = j['ready']
    name = j['name']
    magnet_id = j['id']
    loki.log('info', 'debrid.add_magnet', f"Adding magnet. m_id: {magnet_id} |Name: {name} |Ready? {ready_bool}")
    return ready_bool, name, magnet_id #returns ready bool, filename and magnet id

def unlock_magnet(link):
    url = debrid_url("link", "unlock", "link=") + link
    j = json.loads(requests.get(url).text)["data"]
    loki.log('info', 'debrid.unlock_magnet', f"Unlocking: {link}")
    loki.log('debug', 'debrid.unlock_magnet', f"{j}")
    return j

def get_unhosted_links(magnet_id):
    url = debrid_url("magnet", "status", "id=") + str(magnet_id)
    t = json.loads(requests.get(url).text)["data"]["magnets"]["links"]
    loki.log('info', 'debrid.get_unhosted_links', f"Getting links for {magnet_id}")
    loki.log('debug', 'debrid.get_unhosted_links', f"{t}")
    return t

def build_link_info(magnet_id):
    links = get_unhosted_links(magnet_id)
    link_info = []
    for link in links:
        unlockedLink = unlock_magnet(link=link["link"])
        link_info.append(
            {"name": unlockedLink["filename"], "link": unlockedLink["link"], "size": size(int(unlockedLink["filesize"]))}
        )
    loki.log('info', 'debrid.build_link_info', f"Built link info for {magnet_id}")
    loki.log('debug', 'debrid.build_link_info', f"link_info: {link_info}")
    return link_info

def search1337(query):
    loki.log('info', 'debrid.search1337x', f"Searching 1337x for {query}")
    results = torrents.search(query, sortBy="seeders", order="desc")
    loki.log('info', 'debrid.search1337x', f"Found {len(results)} results.")
    return results

def magnet_info(torrent_id):
    loki.log('info', 'debrid.magnet_info', f"Getting magnet info for torrent id: {torrent_id}")
    m_link = torrents.info(torrentId=torrent_id)['magnetLink']
    loki.log('debug', 'debrid.magnet_info', f"Got magnet link: {m_link}")
    return m_link

def get_status(magnet_id=0, all=False):
    if all:
        loki.log('info', 'debrid.get_status', f"Getting status for all active torrents.")
        return json.loads(requests.get(debrid_url('magnet', 'status', 'status=active')).text)['data']
    else:    
        loki.log('info', 'debrid.get_status', f"Getting status for magnet_id: {magnet_id}")
        magnet_json = json.loads(requests.get(debrid_url('magnet', 'status', f'id={magnet_id}')).text)
        if 'data' in magnet_json.keys():
            if magnet_json['data']['magnets']['status'].lower() == 'ready':
                loki.log('info', 'debrid.get_status', f"Magnet ready.")
                status = 'ready'
                return status
            else:
                loki.log('info', 'debrid.get_status', f"Magnet not ready.")
                status = 'not ready'
                return status
        else:
            loki.log('warning', 'debrid.get_status', f"Got no result for status.")
            status = 404
            return status

def unlock_link(link, ext=''):
    loki.log('info', 'debrid.unlock_link', f"Unlocking link: {link}")
    url = debrid_url("link", "unlock", "link=") + link
    j = json.loads(requests.get(url).text)
    if j['data']['link'] == '':
        link_id = j['data']['id']
        loki.log('info', 'debrid.unlock_link', f"Got link id: {link_id}")
        print(link_id)
        if ext == 'mp3': #140 add some logs here too
            url = debrid_url("link", "streaming", f"id={link_id}")
            mp3_url = url+"&stream=140"
            print(mp3_url)
            j = json.loads(requests.get(mp3_url).text)
            if 'delayed' in j['data']:
                link = delayed_link_loop(j['data']['delayed'])
                return link['link']
        else:
            print(j)
            for stream in j['data']['streams']:
                print(stream['ext'])
                if stream['ext'] == 'mp4':
                    ext = stream['id']
                    print(ext)
                    break
            if '+' in ext:
                ext = ext.replace('+', plus)
            url = debrid_url("link", "streaming", f"id={link_id}")
            mp4_url = f"{url}&stream={ext}"
            print(mp4_url)
            j = json.loads(requests.get(mp4_url).text)
            print(j)
            if 'delayed' in j['data']:
                link = delayed_link_loop(j['data']['delayed'])
                return link['link']       
    else:
        loki.log('info', 'debrid.unlock_link', f"Sending link: {j['data']['link']}") 
        return j['data']['link']

def get_delayed_status(delayed_id):
    loki.log('info', 'debrid.get_delayed_status', f"Getting status for id: {delayed_id}")
    url = debrid_url("link", "delayed", f"id={delayed_id}")
    j = json.loads(requests.get(url).text)
    loki.log('info', 'debrid.get_delayed_status', f"Status is {j['data']['status']}")
    return j['data']['status']

def delayed_link_loop(delayed_id):
    time.sleep(1)
    while True:
        if get_delayed_status(delayed_id) == 1:
            loki.log('info', 'debrid.delayed_link_loop', f"Delayed status for {delayed_id} is 1.")
            time.sleep(5)
        else:
            loki.log('info', 'debrid.delayed_link_loop', f"Delayed status for {delayed_id} is not 1. lol")
            time.sleep(2)
            break
    url = debrid_url("link", "delayed", f"id={delayed_id}")
    j = json.loads(requests.get(url).text)['data']
    loki.log('debug', 'debrid.delayed_link_loop', f"Data: {j}")
    return j