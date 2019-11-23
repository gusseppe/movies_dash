"""
    El controlador sirve como intermediario entre la vista (view) y controlador (controller)
    Cada peticion de la vista, va para el controlador y esta llama al modelo.

"""
import model # Importa el archivo del modelo
import config # Importa a las configuraciones iniciales
import view # importa a la vista
import random
import dash_bootstrap_components as dbc # Componentes de dash

from textwrap import dedent # Sirve para mostrar el texto alineado dentro del boton magic, collapse.


def show_cards():
    # cards = [dbc.Col(view.card(title=d['name'].capitalize(),
    #                            subtitle=f"Rating: {d['rating']}",
    #                            collapse=d['collapse'],
    #                            image_path=d['img'], _id=i), width=3)
    #          for i, d in enumerate(show_info_card())]  # Muestra 5 peliculas
    cards = [dbc.Col(view.card(d_info, _id=i), width=3)
             for i, d_info in enumerate(show_info_card())]  # Muestra 5 peliculas

    return cards


def show_info_card():
    """
        Funcion que muestra informacion de cada pelicula,
        como por ejemplo, nombre, rating, collapse (twitter, tiempo, youtube, etc.)
        Esta funcion se conecta con el modelo para obtener todos estos datos.

    """
    list_movie_info = list()
    for d in random.sample(model.get_movies_filmaffinity(),
                           config.number_of_movies):
    # for d in model.get_movies_filmaffinity()[:config.number_of_movies]:
        d_info = dict()
        d_info.update(d)

        movies_kinepolis = model.get_movies_kinepolis()
        rating_kinepolis = [dk['score'] for dk in movies_kinepolis if dk['name'] in d['name']]
        rating_filmaff = float(d_info['rating'].replace(',', '.'))
        if len(rating_kinepolis) != 0: # Si existe el rating convertirlo a float
            rating_kinepolis = float(rating_kinepolis[0].replace(',', '.'))
        else: # Si no existe, solo considerar el filmaffinity
            rating_kinepolis = rating_filmaff

        rating_average = (rating_kinepolis + rating_filmaff) / 2

        d_info['rating'] = round(rating_average, 1)
        print('Rating Kinepolis', rating_kinepolis)
        print('Rating promedio', rating_average)
        print('NAME', d['name'])
        try:
            d_info['youtube'] = model.get_youtube(d['name'])[0]['link']
        except:
            d_info['youtube'] = 'Muy pronto link'
            # d_info['youtube'] = model.get_youtube(d['name'])['link']

        d_info['weather'] = model.get_weather()
        d_info['weather_api'] = model.get_weather_api()
        d_info['sentiment'] = model.get_sentiment_twitter(d['name'])
        try:
            print(model.get_wordcloud(d['name']))
            d_info['wordcloud'] = model.get_wordcloud(d['name'])[0]['path']
        except:
            print(model.get_wordcloud(d['name'])['path'])
            d_info['wordcloud'] = model.get_wordcloud(d['name'])['path']

        d_info['update'] = model.get_update_db()

        d_info['collapse'] = dedent(f"""
        
            **Tiempo**: \n
            - **Hoy**: {d_info['weather'][0]['date']} | {d_info['weather'][0]['desc'] } \n
            - **Mañana**: {d_info['weather'][1]['date']} | {d_info['weather'][1]['desc'] } \n
            
            **Prediccion Tiempo**: \n
            - **Dia**: {d_info['weather_api'][0]['day'] }\n
                {d_info['weather_api'][0]['pred'] }
                
            **Link**: {d_info['youtube'] } \n
            
            **Wordcloud** \n

        """)
        # **Trailer (youtube.com)**:\n
        # - **Link**: {d_info['youtube'][0]['link'] } \n
        # - **Dia**: {d_info['weather_api'][1]['day']}
        # {d_info['weather_api'][1]['pred'].split('.')[0] }
        # # ![]({d_info['wordcloud']['path']})
        list_movie_info.append(d_info)

        # ![Drag Racing]({d_info['wordcloud'][0]['path']})
    return list_movie_info
