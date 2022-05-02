from tmdbapis import TMDbAPIs
from tmdbapis import exceptions
#import tvdb_v4_official
import config

v4_access_token = None
#with open("access_token.txt") as text_file:
#    v4_access_token = text_file.readline()

tmdb = TMDbAPIs(config.tmdb_api) #v4_access_token=v4_access_token

def get_movie_info(query):
    try:
        results = tmdb.movie_search(query)
    except(exceptions.NotFound):
        return 0
    return results

def get_tv_info(query):
    try:
        results = tmdb.tv_search(query)
    except(exceptions.NotFound):
        return 0
    return results