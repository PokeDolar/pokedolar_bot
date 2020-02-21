import os
import json
import tweepy

from forex_python.converter import CurrencyRates
from decouple import config

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

currency_rates = CurrencyRates()
dolar_real = str(round(currency_rates.get_rate('USD','BRL'), 2))

data = {}
subiu = False
first_tweet = False
if 'exchange' in config:
    data['exchange'] = config['exchange']
    if data['exchange'] == dolar_real:
        tweet = False
    else:
        tweet = True
        if float(data['exchange']) < float(dolar_real):
            subiu = True
        data['exchange'] = dolar_real

else:
    data['exchange'] = dolar_real
    tweet = True
    first_tweet = True
if tweet:
    pokeid = int(dolar_real.replace('.',''))
    dolar_real = dolar_real.replace('.', ',')
    name = pokemon[pokeid-1]['name']['english']
    
    imagepath = 'pokemon_img/{}.png'.format(pokeid)
    if not first_tweet:
        if subiu:
            status_template = "O dólar subiu para R${} :(\n\n #{} - {}"
        else:
            status_template = "O dólar caiu para R${} :()\n\n #{} - {}"
    else:
        status_template = "quanto tá o pokédólar? R${}\n\n #{} - {}"
    
    
    status = status_template.format(dolar_real, pokeid, name)
    api.update_with_media(imagepath, status)
    config_file = open('config.json', 'w')
    json.dump(data, config_file)
