import json # se encarga de leer archivos tipo json, o sea, diccionarios
import os # se encarga de llamar funciones del sistema

from urllib.request import urlopen # sirve
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_movies_filmaffinity():
    """"
        Esta funcion sirve para extraer datos de la pagina
        filmaffinity

    """
    file_path = 'movies_filmaffinity.json' # Aqui se guardaran los datos de cada pelicula
    if os.path.isfile(file_path):# Verifica si existe el archivo, sino lo crea de nuevo
        print(f'{file_path} already exists.')
        with open(file_path, 'r') as fp:
            movies = json.load(fp)

        return movies

    else: # lo crea de nuevo
        url = 'https://www.filmaffinity.com/es/topcat.php?id=new_th_es'

        page = urlopen(url) # descarga la pagina de filmaffinity
        soup = BeautifulSoup(page, 'html.parser') # declaro un parser, beautiful soap

        # picture = soup.find_all('div', attrs={'class': 'mc-left'})
        picture = soup.find_all('div', attrs={'class': 'mc-poster'}) # me ubico en el poster para descargar las fotos
        rating = soup.find_all('div', attrs={'class': 'avg-rating'})# descargo los avg scores
        rating_count = soup.find_all('div', attrs={'class': 'rat-count'})# descargo los scores

        movies = []
        # Se encarga de guardar los descargado a un dictionario
        # que luego se guardara en mongodb
        for div1, div2, div3 in zip(picture, rating, rating_count):
            # for a in div:
            # titles.append(div.a)
            d = dict()
            d['img'] = div1.a.img['src']
            d['rating'] = div2.getText()
            d['rating_count'] = div3.getText().replace('\n', '').replace('.', '')
            d['name'] = div1.a['title'].strip().lower()
            # movies[div1.a['title']] = d
            movies.append(d)

        with open(file_path, 'w') as fp:
            json.dump(movies, fp)

        return movies


def get_movies_kinepolis():
    """"
        Esta funcion sirve para extraer datos de la pagina
        kinepolis

    """
    file_path = 'movies_filmaffinity.json'

    if os.path.isfile(file_path):
        print(f'{file_path} already exists.')
        with open(file_path, 'r') as fp:
            movies = json.load(fp)

        return movies

    else:
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

        with open(file_path, 'w') as fp:
            json.dump(movies, fp)

    return movies


def list_team():
    team = [
        {'name': 'Ricardo Lesevic',
     'site': 'wwww.google.com'},
        {'name': 'Julissa Gutierrez',
     'site': 'wwww.google.com'},
        {'name': 'Carlos Ninaquispe',
     'site': 'wwww.google.com'},
    ]

    return team