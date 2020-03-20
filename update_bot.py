import os
import json
import tweepy
import requests

from decouple import config
from emojis import sad_emoji, happy_emoji

consumer_key = config('consumer_key')
consumer_secret = config('consumer_secret')
access_token = config('access_token')
access_token_secret = config('access_token_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
user = api.me()

config_file = open('config.json', 'r')
config = json.load(config_file)
config_file.close()

pokemons_file = open('pokedex.json', 'r')
pokemon = json.load(pokemons_file)


uol_quote = requests.get('http://cotacoes.economia.uol.com.br/cambioJSONChart.html?type=d&cod=BRL&mt=off')
dolar_json = json.loads(uol_quote.content)
dolar_real = "{:.2f}".format(dolar_json[1][-1]['ask'])

data = {}
subiu = False
first_tweet = False
data['exchange'] = dolar_real
if 'exchange' in config:
    
    if config['exchange'] == dolar_real:
        tweet = False
    else:
        tweet = True
        if float(config['exchange']) < float(dolar_real):
            subiu = True
        data['exchange'] = dolar_real

else:
    tweet = True
    first_tweet = True
if tweet:
    pokeid = int(dolar_real.replace('.',''))
    dolar_real = dolar_real.replace('.', ',')
    name = pokemon[pokeid-1]['name']['english']
    
    imagepath = 'pokemon_img/{}.png'.format(pokeid)
    emoji = ''
    if not first_tweet:
        if subiu:
            status_template = "O dólar subiu para R${} {}\n\n #{} - {}"
            emoji = sad_emoji()
        else:
            status_template = "O dólar caiu para R${} {}\n\n #{} - {}"
            emoji = happy_emoji()
    else:
        status_template = "quanto tá o pokédólar? R${}\n\n #{} - {}"
    
    
    status = status_template.format(dolar_real, emoji, pokeid, name)
    api.update_with_media(imagepath, status)
    config_file = open('config.json', 'w')
    json.dump(data, config_file)
else:
    config_file = open('config.json', 'w')
    
    last_read = "{}".format(dolar_json[1][-1]['ask'])

    data['last_read'] = last_read
    json.dump(data, config_file)

    print("Não mudou {}".format(data['exchange']))