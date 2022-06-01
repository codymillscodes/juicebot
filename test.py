import requests
import json

jackett_url = "http://192.168.1.78:9117/api/v2.0/indexers/all/results?apikey=thrz7pia9i3vagc5bpud1n4ljqo6bhfq&tracker=1337x,rarbg,torrentgalaxy&cat=1000,1010,1020,1030,1040,1050,1080,1090,1110,1180,2000,2010,2020,2030,2040,2045,2050,2060,2070,3000,3010,3020,3030,3040,3050,4000,4010,4020,4030,4040,4050,4060,4070,5000,5030,5040,5045,5050,5060,5070,5080,7000,7010,7020,7030,7040,8000,8010&query=aew all in 2019"

j = json.loads(requests.get(jackett_url).text)
print(j)