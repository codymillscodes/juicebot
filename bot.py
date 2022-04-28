#!/usr/bin/env python
#import youtube_dl
import config
import debrid
import datetime
import discord
import asyncio
import requests
import json
import random
import wikipediaapi as wiki
from bs4 import BeautifulSoup
from hurry.filesize import size

print(config.discord_application_id)

#define discord client
client = discord.Client()

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")

#define commands
wordlist_cats = ["!cat", "!catgif", "!neb", 'catfact']
wordlist_debrid = ["!search", "!status", '!lstatus']
wordlist_waffle = ["!waffle"]
wordlist_wiki = ["!wiki"]
wordlist_insult = ["!insult"]
wordlist_comp = ["!comp"]
wordlist_weather = ["!weather"]
wordlist_help = ['!help']

not_ready_magnets = []

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

#check if string can be converted to int
def check_int(potential_int):
    try:
        int(potential_int)
        return True
    except ValueError:
        return False

async def update_debrid_status():
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
    if message.author == client.user: #Don't respond to my own messages
        return
    #if str(message.author.id) in config.discord_ignored_ids: #Don't respond to these user ids
        return
    #if str(message.channel.id) in config.discord_ignored_channel_ids: #Don't respond to these channel ids
        return
    em_footer = f"{message.author} | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" #default embed footer
#weather
    if any(message.content.startswith(word) for word in wordlist_weather):
        if(check_int(message.content[9:])):
            arg = f'zip={message.content[9:]}'
        else:
            arg = f'q={message.content[9:]}'
        weather = json.loads(requests.get(f"https://api.openweathermap.org/data/2.5/weather?{arg}&appid={config.owm_auth}&units=imperial").text)
        em_weather = discord.Embed()
        em_weather.set_footer(text=em_footer)
        em_weather.set_author(name=weather['name'])
        em_weather.description = f"Temp: {weather['main']['temp']}F | {weather['weather'][0]['description']}\nWind: {weather['wind']['speed']} | Humidity: {weather['main']['humidity']}%"
        await message.channel.send(embed=em_weather)
#cats
    if any(message.content.startswith(word) for word in wordlist_cats): 
        if message.content.startswith('!neb'):
            cat_search = f"https://api.thecatapi.com/v1/images/search?breed_ids=nebe&api_key={config.cat_auth}"
            cat_pic = json.loads(requests.get(cat_search).text)[0]["url"]
            await message.channel.send(cat_pic)
        elif message.content.startswith('!catgif'):
            cat_search = f"https://api.thecatapi.com/v1/images/search?mime_types=gif&api_key={config.cat_auth}"
            cat_pic = json.loads(requests.get(cat_search).text)[0]["url"]
            await message.channel.send(cat_pic)
        elif message.content.startswith('!catfact'):
            cat_fact = json.loads(requests.get('https://meowfacts.herokuapp.com').text)["data"]
            fact = ((str(cat_fact)).strip("'[]'"))
            await message.channel.send(fact)
        elif message.content.startswith('!cat'):
            cat_search = f"https://api.thecatapi.com/v1/images/search?api_key={config.cat_auth}"
            cat_pic = json.loads(requests.get(cat_search).text)[0]["url"]
            await message.channel.send(cat_pic)
#random waffle command
    if any(message.content.startswith(word) for word in wordlist_waffle):
        waffles = 'https://randomwaffle.gbs.fm/'
        image = BeautifulSoup(requests.get(waffles).content, 'html.parser').find('img').attrs['src']
        await message.channel.send(waffles+image)
#insults
    if any(message.content.startswith(word) for word in wordlist_insult):
        a = random.choice(insult_words['A'])
        b = random.choice(insult_words['B'])
        c = random.choice(insult_words['C'])
        d = random.choice(insult_words['D'])
        e = random.choice(insult_words['E'])
        f = random.choice(insult_words['F'])
        
        await message.channel.send(f"{message.content[8:]} is {a} {b} {c} and a {d} {e} {f}.")
#compliments
    if any(message.content.startswith(word) for word in wordlist_comp):
        a = random.choice(praise['A'])
        b = random.choice(praise['B'])
        c = random.choice(praise['B'])
        d = random.choice(praise['C'])
        
        await message.channel.send(f"{message.content[6:]}, you {b.lower()}, {d.lower()} and {c.lower()} {a.lower()}.")
#wiki
    if any(message.content.startswith(word) for word in wordlist_wiki):
        wiki_search = wiki.Wikipedia('en')
        page = wiki_search.page(f'{message.content[6:]}')

        if page.exists():
            wiki_embed = discord.Embed()
            wiki_embed.set_footer(text=em_footer)
            wiki_embed.description = f"[**{page.title}**]({page.fullurl})\n{page.summary[0:500]}..."
            await message.channel.send(embed=wiki_embed)
        else:
            await message.channel.send("Pretty sure you made that up.")
#debrid
    if any(message.content.startswith(word) for word in wordlist_debrid):
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
    if any(message.content.startswith(word) for word in wordlist_debrid):
        if message.content.startswith('!search'):
            results = debrid.search1337(message.content[8:])['items'][:5]
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

client.loop.create_task(update_debrid_status())

client.run(config.discord_bot_token)