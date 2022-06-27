import os

#Discord bot settings
discord_application_id = os.environ["discord_appid"]
discord_public_key = os.environ["discord_pubkey"]
discord_bot_name = 'waffle'
discord_bot_token = os.environ["discord_token"]
discord_oauth_id = os.environ["discord_oauthid"]
discord_oauth_secret = os.environ["discord_oauth_secret"]
log_channel = os.environ["log_channel"]
dl_channel = os.environ["dl_channel"]
puzzle_channel = os.environ["puzzle_channel"]
restart_role = os.environ["restart_role"]

#debrid settings
debrid_host = os.environ["debrid_host"]
debrid_key = os.environ["debrid_key"]
debrid_session = os.environ["debrid_session"]
#dog api
dog_auth = os.environ["dog_auth"]
#cat api key
cat_auth = os.environ["cat_auth"]
#weather api key
owm_auth = os.environ["owm_auth"]
#tmdb apis
tmdb_api = os.environ["tmdb_api"]
#openai key
openai_key = os.environ["openai_key"]
#loki
host = 'waffle'
loki_ip = os.environ["loki_ip"]
poop = True
#dbs
recommend_host = os.environ["recommend_host"]
recommend_dbname = os.environ["recommend_dbname"]
recommend_port = 5432
recommend_pass = os.environ["recommend_pass"]
recommend_user = os.environ["recommend_user"]

images_host = os.environ["images_host"]
images_dbname = os.environ["images_dbname"]
images_port = os.environ["images_port"]
images_pass = os.environ["images_pass"]
images_user = os.environ["images_user"]

#1337x cf cookie
cookie = os.environ["cookie"]