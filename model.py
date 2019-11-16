import json # se encarga de leer archivos tipo json, o sea, diccionarios
import os # se encarga de llamar funciones del sistema
import requests
import urllib.request
import urllib.parse
import re
import http.client
import config
import matplotlib.pyplot as plt
import nltk
import random

from wordcloud import WordCloud
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tools import TwitterClient


def get_movies_filmaffinity():
    """"
        Esta funcion sirve para extraer datos de la pagina
        filmaffinity. Es decir, peliculas y sus datos.

    """
    label = 'filmaffinity'

    if config.mongo_activated:
        from pymongo import MongoClient # Libreria que se conecta al mongodb. Instalar mongodb previamente.
        client = MongoClient('localhost', 27017)

        db = client.test_database # El nomnbre de la base de datos, en este caso,  peliculas

        # movie_collections = list(db['filmaffinity'].find().sort('_id', 1).limit(10)) # Son como las tablas.
        movie_collections = list(db['filmaffinity'].find().sort('_id', 1).limit(10)) # Son como las tablas.

        # try: # Primera vez no entregara ningun lista
        #     movie_collections = random.sample(movie_collections, 8) # Son como las tablas.
        # except:
        #     pass

        # Esta parte inserta los valores al mongo por primera vez.
        if len(movie_collections) == 0: #  Significa no hay ninguna pelicula guarda. Entonces escribir en mongo
            movies = _get_movies_filmaffinity() # Llama al scrapping en tiempo real, porque no hay ningun documento.
            db['filmaffinity'].insert_many(movies) # Inserta las peliculas al mongo en la tabla filmaffinity.

            return movies
        else:
            print(f'Datos de filmaffinity ya guardados en MongoDB')
            return movie_collections

    else: # Si mongo no esta activado se usa archivos locales
        file_path = f"{os.path.join('local', label)}.json" # Aqui se guardaran los datos de cada pelicula
        if os.path.isfile(file_path):# Verifica si existe el archivo, sino lo crea de nuevo
            print(f'{file_path} ya existe en local.')
            with open(file_path, 'r') as fp:
                movies = json.load(fp)

            return movies

        else: # lo crea de nuevo
            movies = _get_movies_filmaffinity()
            print(f'{file_path} guardado en local.')

            with open(file_path, 'w') as fp:
                json.dump(movies, fp)

            return movies


def _get_movies_filmaffinity():
    """

        Scrapping. Se encarga de conectarse en tiempo real con filmaffinity y descargar os datos de las peoliculas.

    """
    # La pagina que quiero scrappear.
    url = 'https://www.filmaffinity.com/es/topcat.php?id=new_th_es'

    page = urlopen(url) # descarga la pagina de filmaffinity
    soup = BeautifulSoup(page, 'html.parser') # Declara un buscador. Todavia no lo usa, solo declaracion.

    # picture = soup.find_all('div', attrs={'class': 'mc-left'})
    picture = soup.find_all('div', attrs={'class': 'mc-poster'}) # me ubico en el poster para descargar las fotos
    rating = soup.find_all('div', attrs={'class': 'avg-rating'})# descargo los avg scores
    rating_count = soup.find_all('div', attrs={'class': 'rat-count'})# descargo los scores

    movies = []
    # Se encarga de guardar los descargado a un dictionario
    # que luego se guardara en mongodb
    for div1, div2, div3 in zip(picture, rating, rating_count): # zip une las tres busquedas en solo for.
        # for a in div:
        # titles.append(div.a)
        d = dict()
        d['img'] = div1.a.img['src']#.replace('https://', 'http://')
        d['rating'] = div2.getText() # obtener texto de ese div.
        d['rating_count'] = div3.getText().replace('\n', '').replace('.', '') # replace limpia la data.
        d['name'] = div1.a['title'].strip().lower() # strip quita espacios que no usan y lower pasa a minusculas.
        # movies[div1.a['title']] = d

        # Guardar fotos de las peliculas
        url = d['img']
        name = d['name']
        # path_mv_relative = os.path.join('/assets', 'images', f'wc_{name}.png')
        # path_mv = os.path.join(os.getcwd(), 'assets','images', f"mv_{name}.jpg")

        path_mv_relative = os.path.join('assets','images', f'mv_{name}.jpg')
        path_mv = os.path.join(os.getcwd(), path_mv_relative)
        urllib.request.urlretrieve(url, path_mv)
        d['img'] = path_mv_relative

        movies.append(d) # pongo las pelicuas en una lista movies.

    return movies[:10]


def get_movies_kinepolis():
    """"
        Esta funcion sirve para extraer datos de la pagina
        kinepolis

    """
    # file_path = 'movies_kinepolis.json'

    label = 'kinepolis'

    if config.mongo_activated:
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017)

        db = client.test_database

        movie_collections = list(db[{label}].find().sort('_id', -1).limit(10))

        if len(movie_collections) == 0: # Entonces escribir en mongo
            movies = _get_movies_kinepolis()
            db[label].insert_many(movies)

            return movies
        else:
            print(f'Data kinepolis ya existe en MongoDB')
            return movie_collections
    else:
        file_path = f"{os.path.join('local', label)}.json" # Aqui se guardaran los datos de cada pelicula
        if os.path.isfile(file_path):
            print(f'{file_path} ya existe en local.')
            with open(file_path, 'r') as fp:
                movies = json.load(fp)

            return movies

        else:
            movies = _get_movies_kinepolis()
            print(f'{file_path} guardado en local.')
            with open(file_path, 'w') as fp:
                json.dump(movies, fp)

        return movies


def _get_movies_kinepolis():
    url = 'https://kinepolis.es/cines/kinepolis-madrid-ciudad-de-la-imagen?main-section=presales'

    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    # regex = re.compile(r'^movie-container-[0-9]+')
    # regex = re.compile(r'^movie')

    movies = []
    # movie = soup2.find_all('div', attrs={'id': regex})
    raw_data = soup.find_all('div', attrs={'class': 'movie-overview-title'})

    for movie in raw_data:
        d = dict()
        d['name'] = movie.getText().strip().lower()
        url_t = urljoin('https://kinepolis.es', movie.a['href'])
        # print(url_t)
        page_t = urlopen(url_t)
        soup_t = BeautifulSoup(page_t, 'html.parser')
        score = soup_t.find_all('span', attrs={'class': 'movie-visitor-score-score'})

        try:
            if not score[0].is_empty_element:
                for s in score:
                    # print(s.getText())
                    d['score'] = s.getText()
                    # print(score[0].getText())
        except:
            d['score'] = -1

        movies.append(d)

    return movies


def get_weather():
    """"
        Esta funcion sirve para el clima de madrid

    """
    label = 'weather'

    if config.mongo_activated:
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017)

        db = client.test_database

        # time_collections = list(db[f'{label}'].find().sort('_id', -1).limit(10))
        time_collections = list(db[f'{label}'].find().sort('_id', 1).limit(10))

        if len(time_collections) == 0: # Entonces escribir en mongo
            # days = _get_weather()
            try:
                days = _get_weather()
                db[f'{label}'].insert_many(days)
                return days
            except:
                print('Error weather')
                return None

        else:
            print(f'Data {label} ya existe en  MongoDB')
            return time_collections
    else:
        file_path = f"{os.path.join('local', label)}.json" # Aqui se guardaran los datos de cada pelicula
        if os.path.isfile(file_path):
            print(f'{file_path} ya existe en local.')
            with open(file_path, 'r') as fp:
                movies = json.load(fp)

            return movies

        else:
            days = _get_weather()
            print(f'{file_path} guardado en local.')
            with open(file_path, 'w') as fp:
                json.dump(days, fp)

            return days


def _get_weather():
    url = 'https://weather.com/es-ES/tiempo/10dias/l/c2825b2b1eab60a3eb6bad36bd2facdb4a886cfc284c90755c59ebd1b34781d1'
    page = requests.get(url)

    # page = urlopen(url) # descarga la pagina de filmaffinity
    soup=BeautifulSoup(page.content,"html.parser")
    # soup=BeautifulSoup(page,"html.parser")

    all=soup.find("div",{"class":"locations-title ten-day-page-title"}).find("h1").text
    table=soup.find_all("table",{"class":"twc-table"})
    days=[]
    for items in table:
        for i in range(len(items.find_all("tr"))-1):
            d = {}
            d["day"]=items.find_all("span",{"class":"date-time"})[i].text
            d["date"]=items.find_all("span",{"class":"day-detail"})[i].text
            d["desc"]=items.find_all("td",{"class":"description"})[i].text
            d["temp"]=items.find_all("td",{"class":"temp"})[i].text
            d["precip"]=items.find_all("td",{"class":"precip"})[i].text
            d["wind"]=items.find_all("td",{"class":"wind"})[i].text
            d["humidity"]=items.find_all("td",{"class":"humidity"})[i].text
            days.append(d)

    return days


def get_weather_api():
    """"
        Esta funcion sirve para el clima de madrid

    """
    label = 'weather_api'

    if config.mongo_activated:
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017)

        db = client.test_database

        # time_collections = list(db[f'{label}'].find().sort('_id', -1).limit(10))
        time_collections = list(db[f'{label}'].find().sort('_id', 1).limit(10))

        if len(time_collections) == 0: # Entonces escribir en mongo
            # days = _get_weather()
            try:
                days = _get_weather_api()
                # print(days)
                db[f'{label}'].insert_many(days)
                return days
            except:
                print('Error weather API')
                return None

        else:
            print(f'Data {label} ya existe en MongoDB')
            return time_collections
    else:
        file_path = f"{os.path.join('local', label)}.json" # Aqui se guardaran los datos de cada pelicula
        if os.path.isfile(file_path):
            print(f'{file_path} ya existe en local.')
            with open(file_path, 'r') as fp:
                movies = json.load(fp)

            return movies

        else:
            days = _get_weather_api()
            print(f'{file_path} guardado en local.')
            with open(file_path, 'w') as fp:
                json.dump(days, fp)

            return days


def _get_weather_api():
    conn = http.client.HTTPSConnection("opendata.aemet.es")

    headers = {
        'cache-control': "no-cache",
    }

    url = '/opendata/api/prediccion/ccaa/medioplazo/mad'
    # url = '/opendata/api/prediccion/ccaa/hoy/mad'
    # url = '/opendata/api/prediccion/ccaa/manana/mad'
    # url = '/opendata/api/prediccion/provincia/hoy/28'
    request_url = f"{url}?api_key={config.weather_api}"
    conn.request("GET", request_url, headers=headers)

    res = conn.getresponse()
    data = res.read().decode("utf-8")

    url_data = data.split()[9].replace('\"', '').replace(',','')
    raw_dataset = urlopen(url_data).read().decode('cp1252')
    raw_dataset = raw_dataset.replace('\r\r', '').replace('\n', '')
    clean_dataset = raw_dataset.split('DÍA ')[2:]
    clean_dataset = [e.strip() for e in clean_dataset]

    d_list = []
    for e in clean_dataset:
        d = dict()
        k = e.split(':')[0]
        v = e.split(':')[1]
        d['day'] = k
        d['pred'] = v
        d_list.append(d)

    # d_dataset = dict((e.split(':')) for e in clean_dataset)

    return d_list


def get_youtube(query):
    """"
        Esta funcion sirve para extraer datos de twitter

    """
    label = f'youtube_{query}'

    if config.mongo_activated:
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017)

        db = client.test_database

        tweets_collections = list(db[f'{label}'].find({'name': query}).sort('_id', -1).limit(10))

        if len(tweets_collections) == 0: # Entonces escribir en mongo
            link = _get_youtube(query)
            db[f'{label}'].insert(link)

            return link
        else:
            print(f'Data {label} ya existe en MongoDB')
            return tweets_collections
    else:
        file_path = f"{os.path.join('local', label)}.json" # Aqui se guardaran los datos de cada pelicula
        if os.path.isfile(file_path):
            print(f'{file_path} ya existe en local.')
            with open(file_path, 'r') as fp:
                link = json.load(fp)

            return link

        else:
            link = _get_youtube(query)
            print(f'{file_path} guardado en local.')
            with open(file_path, 'w') as fp:
                json.dump(link, fp)

            return link


def _get_youtube(query):
    """

        Se conecta a youtube y busca los trailer en espanol de la pelicula en cuestion.

    """
    # Codifica tu texto de lenguaje humano, a un texto entendible para las paginas.
    # por ejemplo, reemplazar los espacios por %20. O quitar tildes, las enhes.
    try:
        query_string = urllib.parse.urlencode({"search_query" : f'{query} trailer espanol'})
        # Descarga la pagina que pertenece a ese link.
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        # Obtiene de esa pagina, el url del video que deseas. El primero.
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        link_trailer = f'http://www.youtube.com/watch?v={search_results[0]}'

        d = {'name': query, 'link': link_trailer} # dictionario

        return d
    except:
        print('Error youtube scrapping')
        return None


def get_twitter(query):
    """"
        Esta funcion sirve para extraer datos de twitter

    """
    label = f'twitter_{query}'

    if config.mongo_activated:
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017)

        db = client.test_database

        tweets_collections = list(db[label].find({'name': query}).sort('_id', -1).limit(10))

        if len(tweets_collections) == 0: # Entonces escribir en mongo
            tweets = _get_twitter(query)
            db[label].insert_many(tweets)

            return tweets
        else:
            print(f'Data twitter ya existe en MongoDB')
            return tweets_collections
    else:
        # file_path = f'{label}_{query}.json'
        file_path = f"{os.path.join('local', label)}.json" # Aqui se guardaran los datos de cada pelicula
        if os.path.isfile(file_path):
            print(f'{file_path} ya existe en local.')
            with open(file_path, 'r') as fp:
                tweets = json.load(fp)

            return tweets

        else:
            tweets = _get_twitter(query)
            print(f'{file_path} guardado en local.')
            with open(file_path, 'w') as fp:
                json.dump(tweets, fp)

            return tweets


def _get_twitter(query):
    """
        Se conectara al API de twitter. No es un scrapping.
    """
    api = TwitterClient()
    tweets = api.get_tweets(query=query, count=config.number_of_tweets)
    # tweets = api.get_tweets(query=query, count=100)

    return tweets


def get_sentiment_twitter(query):

    tweets = get_twitter(query)

    # Filtra a los tweets positivos, negativos  y neutros y los guarda en cada lista.
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    neutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']

    # Calcula la cantidad de elementos de cada lista.
    p_score = len(ptweets)/len(tweets)
    neg_score = len(ntweets)/len(tweets)
    neu_score = len(neutweets)/len(tweets)

    return p_score, neg_score, neu_score


def get_wordcloud(query):
    """"
        Esta funcion sirve para crear el word_cloud

    """
    label = f'wordcloud_{query}'

    if config.mongo_activated:
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017)

        db = client.test_database

        tweets_collections = list(db[f'{label}'].find({'name': query}).sort('_id', -1).limit(10))

        if len(tweets_collections) == 0: # Entonces escribir en mongo
            wc = _get_wordcloud(query)
            db[f'{label}'].insert(wc)

            return wc
        else:
            print(f'Data {label} ya existe en MongoDB')
            return tweets_collections
    else:
        file_path = f"{os.path.join('local', label)}.json" # Aqui se guardaran los datos de cada pelicula
        if os.path.isfile(file_path):
            print(f'{file_path} ya existe en local.')
            with open(file_path, 'r') as fp:
                wc = json.load(fp)

            return wc

        else:
            wc = _get_wordcloud(query)
            print(f'{file_path} guardado en local.')
            with open(file_path, 'w') as fp:
                json.dump(wc, fp)

            return wc


def _get_wordcloud(query=None, max_words=50):
    tweets = get_twitter(query)
    tweets = [d['text_cleaned'] for d in tweets]
    # stopwords significa palabras que no son releveantes para el analisis. P.e, la, el, los, las, etc.
    # Te entrega todas las palabras para luego no tomarlas en cuenta en el grafico
    stopwords = nltk.corpus.stopwords.words('spanish') # NLTK es una libreria de lenguaje natural para procesar datos.

    # Tu puedes crear tus propias palabras que no quieres que aparezcan en tu graficos. Personalizadas.
    words_yunk = ['pelicula', 'bottom',
                  'rt', 'pel', 'cula', query]

    if query is None:
        # Si no pones nunca pelicula
        all_words = ' '.join([text.lower() for text in tweets])
    else:
        # si ingresas una pelicula va borrar las palabras que has definido antes.
        all_words = [text.lower() for text in tweets]
        all_words = ' '.join([text for text in all_words if text not in words_yunk])
        for w in words_yunk:
            all_words = all_words.replace(w, '') # Reemplaza las palabras por un vacio.

    # Funcion que realiza el grafico.
    # Cuenta el numero de ocurrencia de cada palabra.
    # La palabra que aparece mas se muestra mas grande, y la que aparece aparece mas chico.
    # Te da a entender que estas palabras son relevantes, la gente mucho lo usa para describir esa pelicula.
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        width=600,
        height=600,
        random_state=21,
        colormap='jet',
        max_words=max_words,
        max_font_size=200).generate(all_words)

    # plt.figure(figsize=(12, 10))
    plt.axis('off')
    plt.imshow(wordcloud, interpolation="bilinear");
    path_wc_relative = os.path.join('assets','images', f'wc_{query}.png')
    path_wc = os.path.join(os.getcwd(), path_wc_relative)
    # path_wc = os.path.join('/assets', 'images', f'wc_{query}.png')
    plt.savefig(path_wc)
    d = {'name': query, 'path': path_wc_relative}

    return d


def get_update_db():
    label = 'update'
    file_path = f"{os.path.join('local', label)}.json" # Aqui se guardaran los datos de cada pelicula
    with open(file_path, 'r') as fp:
        d_update = json.load(fp)

    result = f"Próxima actualización: {d_update['next_update']}"

    return result

