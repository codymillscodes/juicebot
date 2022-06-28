#!/usr/bin/env python
#import youtube_dl
import config, debrid, memes, tv_movies, recipe, puzzle, chatbot
import datetime, random, requests, json, loki, db
import discord
import asyncio, subprocess
import wikipediaapi as wiki
from bs4 import BeautifulSoup
from hurry.filesize import size
import io
import aiohttp
import logging

#define discord client
intents = discord.Intents().all()
client = discord.Client(intents=intents)
# logging config
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@client.event
async def on_ready():
    log_channel = await client.fetch_channel(config.log_channel)
    loki.log('info', 'on_ready()', f"Logged in as {client.user.name} log_channel: {config.log_channel}")
    await log_channel.send("[BOT ACTIVATED]")

waffle_emoji = '\N{WAFFLE}'
#define commands
wordlist_recs = ["!addrec", "!getrec", "!addalias"]
wordlist_cats = ["!cat", "!catgif", "!neb", 'catfact']
wordlist_dogs = ['!dog']
wordlist_debrid = ["!search", "!status", '!lstatus', '!unlock ']
wordlist_waffle = ["!waffle", f"!{waffle_emoji}", f"!{':w:'}", "!chat", "!gptprompt"]
wordlist_search = ["!wiki", "!movie", "!tv", "!regret"]
wordlist_insult = ["!insult"]
wordlist_comp = ["!comp"]
wordlist_weather = ["!weather"]
wordlist_help = ['!help']
wordlist_system = ["!restartbot", "!git-update", "!media", "!users"]
wordlist_sa = ['!meme', '!curse', '!funny', '!cute', '!osha', '!badfood', '!schad', '!gif', '!rassle']
wordlist_puzzle = ['!prompt', '!setprompt']
wordlist_recipes = ['!recipe']
not_ready_magnets = []

list_roles_system = ['967697785304526879']

string_restartdiscord = "Restarting myself..."
string_updatebot = "Pulling from git and restarting..."
string_no_restart= "Ask an adult for permission."
#wordlists for commands to use
insult_words = {
            'A': ['a confoundedly', 'a conspicuously', 'a cruelly', 'a deucedly', 'a devilishly', 'a dreadfully', 'a frightfully', 'a grievously', 'a lamentably', 'a miserably', 'a monstrously', 'a piteously', 'a precociously', 'a preposterously', 'a shockingly', 'a sickly', 'a wickedly', 'a woefully', 'an abominably', 'an egregiously', 'an incalculably', 'an indescribably', 'an ineffably', 'an irredeemably', 'an outrageously', 'an unconscionably', 'an unequivocally', 'an unutterably'],
            'B': ['appalling', 'babbling', 'backward', 'bantering', 'blabbering', 'blighted', 'boorish', 'contemptible', 'corpulent', 'cretinous', 'debauched', 'decadent', 'demented', 'depraved', 'detestable', 'dissolute', 'execrable', 'fiendish', 'foolish', 'foul', 'gluttonous', 'grotesque', 'gruesome', 'hermaphroditic', 'hideous', 'ignominious', 'ignorant', 'ill-bred', 'ill-mannered', 'incompetent', 'incorrigible', 'indecent', 'inept', 'insignificant', 'insufferable', 'insufferable', 'lascivious', 'lecherous', 'licentious', 'loathsome', 'maladjusted', 'malignant', 'minuscule', 'miserable', 'myopic', 'naive', 'narcissistic', 'nonintuitive', 'obese', 'obtuse', 'offensive', 'parasitic', 'pedestrian', 'perverted', 'petty', 'primitive', 'promiscuous', 'reprehensible', 'repugnant', 'repulsive', 'revolting', 'salacious', 'subliterate', 'sybaritic', 'uncivilized', 'uncouth', 'unseemly', 'unsightly', 'vile', 'vulgar', 'witless'],
            'C': ['barbarian', 'cannibal', 'coccydynia', 'cretin', 'degenerate', 'delinquent', 'derelict', 'dingleberry', 'dolt', 'dullard', 'dunce', 'fiend', 'filcher', 'glutton', 'half-wit', 'heathen', 'hemorrhoid', 'idiot', 'ignoramus', 'imbecile', 'lackey', 'lecher', 'libertine', 'loafer', 'lout', 'malefactor', 'menace', 'microphallus', 'miscreant', 'misdemeanant', 'moron', 'narcissist', 'neanderthal', 'nincompoop', 'ninny', 'nose picker', 'oaf', 'onanist', 'parasite', 'peon', 'pervert', 'pick pocket', 'plebeian', 'polisson', 'prostitute', 'rapscallion', 'reprobate', 'reprobate', 'reptile', 'rogue', 'ruffian', 'scoundrel', 'simpleton', 'slattern', 'sphincter', 'subhuman', 'swine', 'sycophant', 'sycophant', 'troglodyte', 'trollop', 'twit', 'varmint', 'vermin', 'wretch'],
            'D': ['belligerent', 'catatonic', 'corrupt', 'dastardly', 'debased', 'debauched', 'decadent', 'decrepit', 'degenerate', 'demented', 'deplorable', 'depraved', 'disgusting', 'fecal', 'feculent', 'fiendish', 'flaccid', 'flagitious', 'flagrant', 'frightful', 'gaudy', 'glaring', 'gluttonous', 'gross', 'grotesque', 'heinous', 'hopeless', 'horribly atrocious', 'infamous', 'loathsome', 'ludicrous', 'maladjusted', 'malingering', 'malingering', 'malodorous', 'maniacal', 'maniacal', 'masturbatory', 'miscreant', 'miserable', 'monstrous', 'myopic', 'myopic', 'naive', 'narcissistic', 'narcissistic', 'nefarious', 'nefarious', 'outrageous', 'perverse', 'perverted', 'petty', 'preposterous', 'preposterous', 'primitive', 'primitive', 'putrid', 'putrid', 'rank', 'reprehensible', 'repugnant', 'revolting', 'rotten', 'vacuous', 'vapid', 'villainous', 'wearisome'],
            'E': ['acidly acrimonious', 'air-polluting', 'all-befouling', 'all-defiling', 'armpit-licking', 'blood-curdling', 'blood-freezing', 'bug-eyed', 'buttock-rimming', 'cantankerously-caterwauling', 'chromosome deficient', 'chronically flatulent', 'cold-hearted', 'coma-inducing', 'congenitally clueless', 'dandruff-eating', 'disease-ridden', 'dull-witted', 'enema-addicted', 'feces-collecting', 'feeble-minded', 'flea-infested', 'flesh-creeping', 'foul-smelling', 'gossip-mongering', 'grudge-festering', 'halitosis-infested', 'heart-sickening', 'Internet-addicted', 'irredeemably boring', 'maliciously malodorous', 'mattress-soiling', 'monotonous solitaire playing', 'mucous-eating', 'nose-picking', 'nostril-offending', 'odiously suffocating', 'one dimensional', 'orgasm faking', 'scruffy-looking', 'sheep-molesting', 'simple-minded', 'small-minded', 'snake-eyed', 'sock-sucking', 'soul-destroying', 'stench-emitting', 'thick-headed', 'toe-sucking', 'urine-reeking'],
            'F': ['aberration of nature', 'abomination of humanity', 'abomination to all the senses', 'abomination to all the senses', 'acrid smog of oppressively caustic oral effluvium', 'amalgamation of loathsome repulsiveness', 'arbitrary dereliction of genetics', 'assault on the ocular senses', 'blight upon society', 'buggering buttock bandit', 'cacophonous catastrophe', 'cesspool of putrid effluvium', 'cesspool of sub-human filth', 'cheap Internet loiterer', 'chromosome-deficient test tube experiment', 'conglomerate of intellectual constipation', 'conglomerate of intellectual constipation', 'delinquent who has delusions of adequacy', 'deplorable calamity of birth', 'depraved orgy of subhuman indecency', 'depravity of genetics', 'display of indecency', 'dreg of the Internet', 'derelict whose birth certificate is an apology from the condom factory', 'derelict whose birth certificate is an apology from the condom factory', 'evangelical crusader of sub-mediocrity', 'evangelical crusader of sub-mediocrity', 'excrement stain on a Sumo Wrestler\'s underpants', 'glob of grease', 'grotesque visual experience', 'grudge-festering haggard', 'gruesome vista to all eyes assaulted by the sight of you', 'hysterical mass of warbling inanity', 'lamentable mistake by your parent\'s reckless exchange of genetic material', 'leach on humanity', 'malfunctioning little twerp', 'malodorous heathen', 'malodorous marinade of sweat and fear', 'manifestation of contraceptive personality', 'mass of existential impotence', 'mass of loathsome repulsiveness', 'mass of neuroses and complexes', 'mass of neuroses and pathologies', 'mass of neuroses and pathologies', 'mean-spirited poltroon', 'mediocrity afflicted with mental retardation', 'menace to, not only society, but all living creatures', 'mental midget with the natural grace of an intoxicated beluga whale', 'molester of small furry animals', 'molester of small old men', 'moving stench of leprosy', 'mutilation of decency', 'nauseating assault on the senses', 'nauseating assault on the senses', 'nefarious vermin', 'obfuscation of all that is good', 'object of execration', 'ocular depravity to all of discrimination', 'odious leach-covered blob of quivering slime', 'odious leach-covered glob of quivering slime', 'offense to all of good taste and decency', 'oppressive orgy of perversion', 'orgy of indecency', 'orgy of indignity', 'parasite on the states resources', 'personification of vulgarity', 'piece of excrement attached to a dogs posterior', 'pitiful sideshow freak', 'plague of sighing and grief', 'plague upon humanity', 'plot-less melodrama of uneventful life', 'plot-less melodrama of uneventful life', 'practitioner of bestiality', 'proof that evolution can go in reverse', 'proof that test tube experiments can go horribly wrong', 'pulp of stultifying inanity', 'putrid waste of flesh', 'repulsive polisson', 'sadistic hippophilic necrophile', 'scourge of decency', 'sexual assaulter of barnyard animals', 'shameless exhibition of genetic deficiency', 'shameless exhibition of genetic deficiency', 'sideshow freak whose word is as valuable as an aging cow paddy', 'spawn from a lunatics rectum', 'spawn of a mad scientist and a disastrous test tube experiment', 'sub-literate simple minded mental midget', 'tainted spawn of a syphilitic swamp rat', 'tainted spawn of a syphilitic swamp hog', 'tasteless amalgam of dross', 'toll on the nerves of those with good taste and decency', 'unfortunate occurrence of unprotected intercourse', 'unspeakably offensive barbarian', 'vulgarity to all and sundry', 'wretched horror to all who encounter you']	
        }
praise = {
            'A': ["alpaca","antelope", "armadillo","badger","bat", "beaver", "bee", "buffalo", "butterfly", "camel", "caribou", "cat", "cheetah", "chimpanzee", "chinchilla", "coyote", "deer", "dolphin", "donkey", "duck", "elk", "ferret", "fox", "giraffe", "goldfish", "gorilla keeper", "grasshopper", "grey wolf", "guinea pig", "hedgehog", "horse", "jellyfish", "kangaroo", "koala", "land-mermaid", "leopard", "lion", "llama", "macaw", "mallard", "manatee", "mannequin come to life", "mink", "moth", "muskox", "otter", "crime fighting oyster", "panda", "pig", "platypus", "porcupine", "porpoise", "prairie dog", "super pig", "rabbit", "raccoon", "reindeer", "salmon", "sardine", "sea", "seal", "shark", "space lion", "space unicorn", "spinster", "squirrel", "super pig", "sunflower", "sunfish", "sunken treasure", "sun goddess", "swan", "tiger", "tortoise", "tree shark", "tropical fish", "trout detective", "turtle wrangler", "wallaby", "wild pig", "wolf", "wombat", "zebra", "apple blossom", "buttercup", "daisy", "lilac", "lily", "orchid", "orange blossom", "poppy", "rose", "sacred lotus", "sweet pea", "tulip", "alligator chaser", "bear herder", "fixer-of-things", "nerd herder", "newborn baby", "nurse", "shakespearean actor", "underwear model", "supernova"],
            'B': ["Appetizing", "Delicious", "Juicy", "Palatable", "Peppery", "Pickled", "Ripe", "Savory", "Spicy", "Tart", "Tasty", "Toothsome", "Aromatic", "Fragrant", "Fruity", "Perfumed", "Beautiful", "Brawny", "Briny", "Clean", "Chestnut-haired", "Colorful", "Crystalline", "Cute", "Delicate", "Dew-flecked", "Flaming", "Flashy", "Floral", "Gleaming", "Glitter", "Glittering", "Glowing", "Iridescent", "Luminescent", "Lustrous", "Misty", "Opalescent", "Polished", "Polka-dotted", "Radiant", "Shimmering", "Shiny", "Sparkling", "Stupid Hot", "Tan", "Translucent", "Transparent", "Cooing", "Harmonious", "Melodic", "Melodious", "Humming", "Moaning", "Purring", "Resonant", "Reverberating", "Blazing-Hot", "Blistering-Hot", "Breezy", "Contoured", "Cuddly", "Curved", "Feathered", "Fluffy", "Gooey", "Jiggling", "Luscious", "Moist", "Petite", "Quivering", "Satiny", "Silky", "Sizzling", "Soft", "Tender", "Throbbing", "Undulating", "Vibrant", "Vibrating", "Elegant", "Exquisite", "Flexible", "Fresh", "Graceful", "Hot", "Lithe", "Medicinal", "Quaint", "Scorching", "Sunny", "Statuesque", "Sweet", "Young", "Youthful"],
            'C': ["Adventurous", "Affectionate", "Ambitious", "Amiable", "Amusing", "Brave", "Bright", "Brilliant", "Calm", "Charming", "Chatty", "Cheerful", "Clever", "Compassionate", "Considerate", "Convivial", "Cool", "Courageous", "Creative", "Cunning", "Decisive", "Dependable", "Determined", "Devious", "Diligent", "Diplomatic", "Dynamic", "Easy-going", "Effervescent", "Efficient", "Energetic", "Enthusiastic", "Fair-minded", "Fearless", "Friendly", "Funny", "Generous", "Giving", "Gregarious", "Hardworking", "Helpful", "Hilarious", "Honest", "Humorous", "Imaginative", "Impartial", "Independent", "Innocent", "Intuitive", "Inventive", "Kind", "Kooky", "Laid-back", "Likeable", "Loyal", "Modest", "Naive", "Noble", "Non-judgemental", "Observant", "Optimistic", "Organised", "Passionate", "Patient", "Perfect", "Persistent", "Pliable", "Plucky", "Poetic", "Polite", "Powerful", "Practical", "Proactive", "Quick-witted", "Reliable", "Resourceful", "Romantic", "Rule-breaking", "Sassy", "Self-disciplined", "Sincere", "Smart", "Sophisticated", "Straight-forward", "Sweet", "Sympathetic", "Talented", "Thoughtful", "Tidy", "Tricky", "Trustworthy", "Unassuming", "Understanding", "Versatile", "Vivacious", "Warmhearted", "Wicked", "Willing", "Witty"]
            }

#standalone_wordlist_all = wordlist_cats, wordlist_comp, wordlist_debrid, wordlist_insult, wordlist_waffle, wordlist_wiki

 #'\N{U+1F9C7}'
#check if string can be converted to int
def check_int(potential_int):
    loki.log('info', 'bot.check_int', f"Checking int for {potential_int}")
    try:
        int(potential_int)
        loki.log('info', 'bot.check_int', f"Congrats! It's an integer!")
        return True
    except ValueError:
        loki.log('info', 'bot.check_int', f"That's no int!")
        return False

async def update_debrid_status(): # log this stuff
    await client.wait_until_ready()
    while not client.is_closed():
        if len(not_ready_magnets) > 0:
            for magnet in not_ready_magnets:
                status = debrid.get_status(magnet_id=magnet)
                if status == 'ready':
                    filez = debrid.build_link_info(magnet)
                    em_links = discord.Embed()
                    #em_links.set_footer(text=em_footer)
                    for info in filez:
                        em_links.add_field(name=info["name"],value=f"{info['link']} | size: {info['size']}",inline=False)
                    dl_channel = client.get_channel(config.dl_channel)
                    not_ready_magnets.remove(magnet)
                    await dl_channel.send(embed=em_links)
                elif status == 404:
                    not_ready_magnets.remove(magnet)
        await asyncio.sleep(10)


# start event listener
@client.event
async def on_message(message):
    log_channel = client.get_channel(config.log_channel)
    if message.author == client.user: #Don't respond to my own messages
        return
    em_footer = f"{message.author} | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" #default embed footer
    #if str(message.author.id) in config.discord_ignored_ids: #Don't respond to these user ids
        #return
    #if str(message.channel.id) in config.discord_ignored_channel_ids: #Don't respond to these channel ids
        #return
    if any(message.content.startswith(word) for word in wordlist_help):
        loki.log('info', 'bot.on_message', f"{message.author}: {message.content}")
        em_help = discord.Embed()
        em_help.set_author(name="Help!")
        em_help.set_footer(text=em_footer)
        em_help.add_field(name="COMMANDS!", value="!search - Search for a torrent\n!status - which torrents are actively downloading?\n!cat, !catgif, !neb, !catfact - CATS!\n!waffle - roll the dice\n!wiki for wikipedia\n!movie for a movie search\n!tv for tv shows\n!insult, !comp - insult and compliment your subordinates\n!weather cause why not\n!meme, !curse, !funny, !cute - a bit buggy but MEMES!")
        loki.log('info', 'bot.help', f"Sending help embed to {message.author}")
        await message.channel.send(embed=em_help)
#recommendations!
    if(any(message.content.startswith(word) for word in wordlist_recs)):
        if message.content.startswith("!addalias"):
            name = message.author.name
            if message.content[10:] == 'all':
                db.add_alias(name, name)
                db.add_alias(name, message.author)
                db.add_alias(name, f"<@{message.author.id}>")
                db.add_alias(name, 'everyone')
            elif len(message.content[10:]) > 0:
                db.add_alias(name, message.content[10:])
            else:
                await message.channel.send('Alias cannot be blank.') 
        if message.content.startswith("!addrec"):
            rec = message.content[8:].split(", ")
            db.add_rec(rec[0], message.author.name, rec[1], rec[2])
            await message.channel.send('Added.')
        if message.content.startswith("!getrec"):
            q = message.content[8:].split()
            if len(q) == 0:
                recs = db.get_recs(message.author.name)
            elif len(q) == 1:
                recs = db.get_recs(message.author.name, q[0])
            elif q[0] == 'for':
                recs = db.get_recs(' '.join(q[1:]))
            em_recs = discord.Embed()
            em_recs.set_author(name='Recommendations')
            #em_recs.set_footer(text=em_footer)
            for rec in recs:
                em_recs.add_field(name=f"{rec[0]}", value= f"{rec[1]} | {rec[2]}", inline = False)
            await message.channel.send(embed=em_recs)
#recipe search
    if any(message.content.startswith(word) for word in wordlist_recipes):
        loki.log('info', 'bot.on_message', f"{message.author}: {message.content}")
        em_recipe = discord.Embed()
        em_recipe.set_footer(text=em_footer)
        recipes = recipe.recipe_url(message.content[8:])
        loki.log('info', 'bot.recipes', f"Searching recipes for: {message.author}")
        if recipes == 0:
            loki.log('info', 'bot.recipes', f"Got no results for {message.content[8:]}.")
            await message.channel.send('This is not a food.')
        else:
            loki.log('info', 'bot.recipes', f"Got {len(recipes)} results for {message.content[8:]}.")    
            for r in recipes:
                em_recipe.add_field(name=r['recipe']['label'], value=r['recipe']['url'], inline=False)
            loki.log('info', 'bot.recipes', f"Sending recipe embed.") 
            await message.channel.send(embed=em_recipe)
#sa stuff
    if any(message.content.startswith(word) for word in wordlist_sa):
        loki.log('info', 'bot.on_message', f"{message.author}: {message.content}")
        loki.log('info', 'bot.sa', f"Grabbing a meme for {message.author}")
        request = message.content.split()[0]
        meme = db.get_img(str(request[1:]))
        #async with aiohttp.ClientSession() as session:
         # async with session.get(meme) as resp:
          #    if resp.status != 200:
            #     return await message.channel.send('404')
          #    data = io.BytesIO(await resp.read())
           
        await message.channel.send(meme)
        
        # if message.content.startswith('!meme'):
        #     loki.log('info', 'bot.sa', f"Sending !meme to {message.author}")
        #     await message.channel.send(db.get_img(meme))
        # if message.content.startswith('!funny'):
        #     loki.log('info', 'bot.sa', f"Sending !funny to {message.author}")
        #     await message.channel.send(db.get_img(meme))
        # if message.content.startswith('!curse'):
        #     loki.log('info', 'bot.sa', f"Sending !curse to {message.author}")
        #     await message.channel.send(db.get_img(meme))
        # if message.content.startswith('!cute'):
        #     loki.log('info', 'bot.sa', f"Sending !cute to {message.author}")
        #     await message.channel.send(db.get_img(meme))
        # if message.content.startswith('!osha'):
        #     loki.log('info', 'bot.sa', f"Sending !osha to {message.author}")
        #     await message.channel.send()
        # if message.content.startswith('!badfood'):
        #     loki.log('info', 'bot.sa', f"Sending !badfood to {message.author}")
        #     await message.channel.send()
        # if message.content.startswith('!schad'):
        #     loki.log('info', 'bot.sa', f"Sending !schad to {message.author}")
        #     await message.channel.send()
#weather
    if any(message.content.startswith(word) for word in wordlist_weather):
        loki.log('info', 'bot.on_message', f"{message.author}: {message.content}")
        loki.log('info', 'bot.weather', f"Getting weather for {message.author}")
        city = message.content[9:]
        if ' ' in city:
            city = city.replace(' ', '+')
        weather = f"https://wttr.in/{city}_nQ1_background=36393f.png"
        try:
          async with aiohttp.ClientSession() as session:
            async with session.get(weather) as resp:
                if resp.status != 200:
                    return await channel.send('Something broke')
                data = io.BytesIO(await resp.read())
                await message.channel.send(file=discord.File(data, f'weather_{city}.png'))
        except Exception as e:
          await message.channel.send(e)
#puzzle
    if any(message.content.startswith(word) for word in wordlist_puzzle):
        loki.log('info', 'bot.on_message', f"{message.author}: {message.content}")
        if message.content.startswith('!setprompt'):
            puzzle.set_prompt(message.content[11:])
            prompt = puzzle.get_prompt()
            await message.channel.send(f'Prompt set:\n```{prompt}```')
        elif message.content.startswith('!prompt'):
            prompt = puzzle.get_prompt()
            await message.channel.send(f'```{prompt}```')
#cats
    if any(message.content.startswith(word) for word in wordlist_cats): 
        loki.log('info', 'bot.on_message', f"{message.author}: {message.content}")
        if message.content.startswith('!neb'):
            loki.log('info', 'bot.cats', f"Getting !neb for {message.author}")
            cat_search = f"https://api.thecatapi.com/v1/images/search?breed_ids=nebe&api_key={config.cat_auth}"
            cat_pic = json.loads(requests.get(cat_search).text)[0]["url"]
            loki.log('info', 'bot.cats', f"Sending cat_pic: {cat_pic}")
            await message.channel.send(cat_pic)
        elif message.content.startswith('!catgif'):
            loki.log('info', 'bot.cats', f"Getting !catgif for {message.author}")
            cat_search = f"https://api.thecatapi.com/v1/images/search?mime_types=gif&api_key={config.cat_auth}"
            cat_pic = json.loads(requests.get(cat_search).text)[0]["url"]
            loki.log('info', 'bot.cats', f"Sending cat_pic: {cat_pic}")
            await message.channel.send(cat_pic)
        elif message.content.startswith('!catfact'):
            loki.log('info', 'bot.cats', f"Getting !catfact for {message.author}")
            cat_fact = json.loads(requests.get('https://meowfacts.herokuapp.com').text)["data"]
            fact = ((str(cat_fact)).strip("'[]'"))
            loki.log('info', 'bot.cats', f"Sending cat_fact: {fact}")
            await message.channel.send(fact)
        elif message.content.startswith('!cat'):
            loki.log('info', 'bot.cats', f"Getting !cat for {message.author}")
            cat_search = f"https://api.thecatapi.com/v1/images/search?api_key={config.cat_auth}"
            cat_pic = json.loads(requests.get(cat_search).text)[0]["url"]
            loki.log('info', 'bot.cats', f"Sending cat_pic: {cat_pic}")
            await message.channel.send(cat_pic)
#dog
    if any(message.content.startswith(word) for word in wordlist_dogs):
        loki.log('info', 'bot.on_message', f"{message.author}: {message.content}")
        loki.log('info', 'bot.dogs', f"Getting !dog for {message.author}")
        dog_search = f"https://api.thedogapi.com/v1/images/search?api_key={config.dog_auth}"
        dog_pic = json.loads(requests.get(dog_search).text)[0]["url"]
        loki.log('info', 'bot.dogs', f"Sending dog_pic: {dog_pic}")
        await message.channel.send(dog_pic)
#random waffle command
    if any(message.content.startswith(word) for word in wordlist_waffle):
        loki.log('info', 'bot.on_message', f"{message.author}: {message.content}")
        waffles = 'https://randomwaffle.gbs.fm/'
        image = BeautifulSoup(requests.get(waffles).content, 'html.parser').find('img').attrs['src']
        loki.log('info', 'bot.waffle', f"Sending waffle! to {message.author}: {waffles+image}")
        await message.channel.send(waffles+image)
#insults
    if any(message.content.startswith(word) for word in wordlist_insult):
        loki.log('info', 'bot.on_message', f"{message.author}: {message.content}")
        a = random.choice(insult_words['A'])
        b = random.choice(insult_words['B'])
        c = random.choice(insult_words['C'])
        d = random.choice(insult_words['D'])
        e = random.choice(insult_words['E'])
        f = random.choice(insult_words['F'])
        loki.log('info', 'bot.insult', f"{message.author} is insulting {message.content[8:]}.")
        await message.channel.send(f"{message.content[8:]} is {a} {b} {c} and a {d} {e} {f}.")
#compliments
    if any(message.content.startswith(word) for word in wordlist_comp):
        loki.log('info', 'bot.on_message', f"{message.author}: {message.content}")
        a = random.choice(praise['A'])
        b = random.choice(praise['B'])
        c = random.choice(praise['B'])
        d = random.choice(praise['C'])
        loki.log('info', 'bot.comp', f"{message.author} is complimenting {message.content[8:]}.")
        await message.channel.send(f"{message.content[6:]}, you {b.lower()}, {d.lower()} and {c.lower()} {a.lower()}.")
#searchin stuff
    if any(message.content.startswith(word) for word in wordlist_search):
        loki.log('info', 'bot.on_message', f"{message.author}: {message.content}")
        if message.content.startswith('!wiki'):
            loki.log('info', 'bot.search', f"{message.author} is searching wiki for {message.content[6:]}")
            wiki_search = wiki.Wikipedia('en')
            page = wiki_search.page(f'{message.content[6:]}')

            if page.exists():
                wiki_embed = discord.Embed()
                wiki_embed.set_footer(text=em_footer)
                wiki_embed.description = f"[**{page.title}**]({page.fullurl})\n{page.summary[0:500]}..."
                loki.log('info', 'bot.search', f"Found wiki page and built embed.")
                await message.channel.send(embed=wiki_embed)
            else:
                loki.log('info', 'bot.search', f"No wiki results.")
                await message.channel.send("Pretty sure you made that up.")
        if message.content.startswith('!movie'):
            loki.log('info', 'bot.search', f"{message.author} is searching for !movie {message.content[7:]}")
            results = tv_movies.get_movie_info(message.content[7:])
            if results == 0:
                loki.log('info', 'bot.search', f"Got no results for the movie.")
                await message.channel.send("No results. You must've typed random shit.")
            else:
                movie = results[0]
                loki.log('info', 'bot.search', f"Found {movie}. Building embed.")
                em_movie = discord.Embed(description=movie.overview)
                em_movie.set_footer(text=f"{movie.genres[0].name}, {movie.genres[1].name} | {movie.original_language} | {movie.vote_average}% ({movie.vote_count})")
                em_movie.set_author(name=f"{movie.title} ({movie.release_date.year})", url="https://www.imdb.com/title/"+movie.imdb_id)
                em_movie.set_thumbnail(url=movie.poster_url)
                loki.log('info', 'bot.search', f"Sending movie embed.")
                await message.channel.send(embed=em_movie)

        if message.content.startswith('!tv'):
            loki.log('info', 'bot.search', f"{message.author} is searching for !tv {message.content[4:]}")
            results = tv_movies.get_tv_info(message.content[4:])
            if results == 0:
                loki.log('info', 'bot.search', f"Got no results for the show.")
                await message.channel.send("No results. You must've typed random shit.")
            else:
                tv = results[0]
                loki.log('info', 'bot.search', f"Found {tv}. Building embed.")
                em_tv = discord.Embed(description=tv.overview)
                em_tv.set_footer(text=f"{tv.genres[0].name}, {tv.genres[1].name} | {tv.vote_average}% ({tv.vote_count})")
                em_tv.set_author(name=f"{tv.title} ({tv.first_air_date.year})", url="https://www.imdb.com/title/"+tv.imdb_id)
                em_tv.set_thumbnail(url=tv.poster_url)
                loki.log('info', 'bot.search', f"Sending tv embed.")
                await message.channel.send(embed=em_tv)

#system commands
    #Restart stuff
    if any(message.content.startswith(word) for word in wordlist_system):
        loki.log('info', 'bot.on_message', f"{message.author}: {message.content}")
        #log_channel = client.get_channel(config.log_channel)
        valid_group = 0
        loki.log('info', 'bot.system', f"{message.author} has invoked a system command.")
        for role in message.author.roles:
                if str(role.id) in list_roles_system: #Needed role to restart shit
                    valid_group = 1
        if valid_group == 1:
            if message.content.startswith('!restartbot'):
                loki.log('info', 'bot.system', f"Restarting bot.")
                await log_channel.send(string_restartdiscord)
                subprocess.run('/waffle/scripts/restart.sh', shell=True)
            elif message.content.startswith('!users'):
                users = db.get_users()
                await message.channel.send(f"```{users}```")
            elif message.content.startswith('!media'):
                media = db.get_media()
                await message.channel.send(f"```{media}```")
            elif message.content.startswith('!git-update'):
                loki.log('info', 'bot.system', f"Pulling from git and then restarting.")
                await log_channel.send(string_updatebot)
                subprocess.run('/waffle/scripts/update.sh', shell=True)
        else:
            loki.log('warning', 'bot.system', f"{message.author} isn't auth'd for system commands.")
            await message.channel.send(string_no_restart)
#debrid
    if any(message.content.startswith(word) for word in wordlist_debrid):
        loki.log('info', 'bot.on_message', f"{message.author}: {message.content}")
        if message.content.startswith('!status'):
            magnet_status = debrid.get_status(all = True)
            if len(magnet_status['magnets']) > 0:
                #print(magnet_status['magnets'])
                #print(type(magnet_status['magnets']))
                em_status = discord.Embed()
                em_status.set_footer(text=em_footer)
                for magnet in magnet_status['magnets']:
                    if magnet['downloaded'] <= 0:
                        percent = 0
                    else:
                        percent = f"{'{0:.2f}'.format(100 * magnet['downloaded'] / magnet['size'])}"               
                    em_status.add_field(name=magnet['filename'], value=f"{percent}% | {magnet['status']} | Size: {size(magnet['size'])} | Speed: {size(magnet['downloadSpeed'])} | Seeders: {magnet['seeders']}", inline=False)
                await message.channel.send(embed=em_status)
            else:
                await message.channel.send('No active torrents, bud.')
        if message.content.startswith('!search'):
            results = debrid.search1337(message.content[8:])['items'][:5]
            loki.log('info', 'bot.search', results)
            if len(results) > 0:
                em_result = discord.Embed()
                em_result.set_footer(text=em_footer)
                x=1
                for torrent in results:
                    result_name = torrent["name"]
                    result_value = f"Seeders: {torrent['seeders']} | Leechers: {torrent['leechers']} | Size: {torrent['size']}"
                    em_result.add_field(name=f"{x}. {result_name}", value=result_value, inline=False)
                    x = x + 1
                em_result.add_field(name="----------------",value="You should pick the one with the most seeders and a reasonable filesize. Pay attention to the quality. You dont want a cam or TS.\n*!pick 1-5*",inline=False,)
                await message.channel.send(embed=em_result)

                def check(m):
                    return m.author == message.author and m.content.startswith("!pick")
                try:
                    msg = await client.wait_for("message", check=check, timeout=60)
                    pick = int(msg.content[6:])-1
                    if int(msg.content[6:]) > 5 or pick < 0:
                        await message.channel.send("WRONG")
                    else:
                        magnet_link = debrid.magnet_info(results[pick]["torrentId"])
                        ready_bool, name, magnet_id = debrid.add_magnet(magnet_link)
                        if ready_bool:
                            filez = debrid.build_link_info(magnet_id)
                            em_links = discord.Embed(description=f"{message.author.mention}")
                            em_links.set_footer(text=em_footer)
                            for info in filez:
                                em_links.add_field(name=info["name"],value=f"{info['link']} | size: {info['size']}",inline=False)
                            dl_channel = client.get_channel(config.dl_channel)
                            await dl_channel.send(embed=em_links)
                        else:
                            not_ready_magnets.append(magnet_id)
                            await message.channel.send("It aint ready. Try !status.")
                except asyncio.TimeoutError:
                    await message.channel.send("TOO SLOW")

            else:
                await message.channel.send("zero zero zero sesam street sesam street zero zero zero")
        if message.content.startswith('!unlock'):
            link = debrid.unlock_link(message.content[8:])
            await message.channel.send(link)
    if message.content.startswith('@waffle') or client.user.mention in message.content:
        loki.log('info', 'bot.on_message', f"{message.author}: {message.content}")
        input = message.content.split(maxsplit=1)[1]
        #print(input)
        #input = input[1]
        response = chatbot.get_response(input).strip()
        if response.startswith("Waffle: "):
            response = response.split(maxsplit=1)[1]
        if "Human:" in response:
            index = response.find("Human:")
            await message.channel.send(response[:index])
        else:
            await message.channel.send(response)
    if message.content.startswith("!gpt"):
        input = message.content.split(maxsplit=1)[1]
        response = chatbot.chat_response(input).strip()
        await message.channel.send(response)
    if message.content.startswith('!chatprompt'):
        chatbot.set_prompt(message.content.split(maxsplit=1)[1])
client.loop.create_task(update_debrid_status())

client.run(token=config.discord_bot_token, log_handler=handler, log_level=logging.DEBUG)
