import os
import json
import tweepy
import requests

from decouple import config
from emojis import sad_emoji, happy_emoji

#Coleta os dados para acessar o twitter
consumer_key = config('consumer_key')
consumer_secret = config('consumer_secret')
access_token = config('access_token')
access_token_secret = config('access_token_secret')

#Realiza a conexão ao twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
user = api.me()

#Abre o arquivo de configuração
config_file = open('config.json', 'r')
config = json.load(config_file)
config_file.close()

#Abre os dados sobre os pokemons
pokemons_file = open('pokedex.json', 'r')
pokemon = json.load(pokemons_file)

#Recebe a cotação do dolar
uol_quote = requests.get('http://cotacoes.economia.uol.com.br/cambioJSONChart.html?type=d&cod=BRL&mt=off')
dolar_json = json.loads(uol_quote.content)
dolar_real = "{:.2f}".format(dolar_json[1][-1]['ask'])

#criação de variaveis auxiliares
data = {}
subiu = False
first_tweet = False
data['exchange'] = dolar_real

#verifica se já existe uma cotação na config
if 'exchange' in config:
    #se a cotação atual for igual a antiga não há tweet
    if config['exchange'] == dolar_real:
        tweet = False
    else:
        tweet = True
        #verifica se alteração do valor foi positiva ou negativa
        if float(config['exchange']) < float(dolar_real):
            subiu = True
        data['exchange'] = dolar_real #linha desnecessária?

#Se não existir a config, é o primeiro tweet
else:
    tweet = True
    first_tweet = True

#caso seja para twittar
if tweet:
    #Coleta o numero da dex, muda o formato do ponto decimal e coleta o nome do pkm
    pokeid = int(dolar_real.replace('.',''))
    dolar_real = dolar_real.replace('.', ',')
    name = pokemon[pokeid-1]['name']['english']
    
    imagepath = 'pokemon_img/{}.png'.format(pokeid)
    emoji = ''
    if not first_tweet:
        #seleciona um template de relação com a cotação anterior, será incluido o valor, emoji, numero da dex e nome
        if subiu:
            status_template = "O dólar subiu para R${} {}\n\n #{} - {}"
            emoji = sad_emoji()
        else:
            status_template = "O dólar caiu para R${} {}\n\n #{} - {}"
            emoji = happy_emoji()
    else:
        #template do tweet inicial
        status_template = "quanto tá o pokédólar? R${}\n\n #{} - {}"
    
    #realiza o tweet e salva a navoa cotação
    status = status_template.format(dolar_real, emoji, pokeid, name)
    api.update_with_media(imagepath, status)
    config_file = open('config.json', 'w')
    json.dump(data, config_file)
else:
    #caso não seja realizado um tweet a última leitura será salva e printada no console
    config_file = open('config.json', 'w')
    
    last_read = "{}".format(dolar_json[1][-1]['ask'])

    data['last_read'] = last_read
    json.dump(data, config_file)

    print("Não mudou {}".format(data['exchange']))
