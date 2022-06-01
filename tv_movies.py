from tmdbapis import TMDbAPIs
from tmdbapis import exceptions
#import tvdb_v4_official
import config
import loki

v4_access_token = None

tmdb = TMDbAPIs(config.tmdb_api) #v4_access_token=v4_access_token

def get_movie_info(query):
    try:
        results = tmdb.movie_search(query)
        loki.log('info', 'tv_movies.get_movie_info', f"Recv'd results for query: {query}")
        loki.log('info', 'tv_movies.get_movie_info', f"Results: {results.title}")
    except(exceptions.NotFound):
        loki.log('info', 'tv_movies.get_movie_info', f"Recv'd no results for {query}")
        return 0
    return results

def get_tv_info(query):
    try:
        results = tmdb.tv_search(query)
        loki.log('info', 'tv_movies.get_tv_info', f"Recv'd results for query: {query}")
        loki.log('info', 'tv_movies.get_tv_info', f"Results: {results.title}")
    except(exceptions.NotFound):
        loki.log('info', 'tv_movies.get_tv_info', f"Recv'd no results for {query}")
        return 0
    return results