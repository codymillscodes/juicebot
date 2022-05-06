import config
import requests
import json
import html
# https://api.edamam.com/api/recipes/v2?type=public&q=vegan%20pinwheels&app_id=4c039cbf&app_key=8f91e662ec47301394e327972a4ec6c7&imageSize=SMALL&field=uri&field=label&field=image&field=source&field=url&field=yield&field=healthLabels&field=totalTime

def recipe_url(query, hits = 5):
    url = f'https://api.edamam.com/api/recipes/v2?type=public&q={html.escape(query)}&app_id={config.edamam_id}&app_key={config.edamam_key}&imageSize=SMALL&field=label&field=image&field=source&field=url&field=yield&field=healthLabels&field=totalTime'
    recipe_json = json.loads(requests.get(url).text)['hits']
    if len(recipe_json) == 0:
        return 0
    return recipe_json[:hits]
