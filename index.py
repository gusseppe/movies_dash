import dash_html_components as html
import config
import view
import nltk
import json
import os
import tools
import time, threading

from datetime import datetime, timedelta
from app import app
# nltk.download('book')
nltk.download('stopwords')


server = app.server


# Actualizar cada x dias.
def update_database():
    if config.mongo_activated:
        tools.drop_mongo()
    tools.remove_local_files()
    print(f'Base de datos actualizada, siendo: {time.ctime()}')
    print(f'Se volvera a actualizar en: {config.interval_update/3600} horas')

    label = 'update'
    file_path = f"{os.path.join('local', label)}.json" # Aqui se guardaran los datos de cada pelicula
    next_update = datetime.now() + timedelta(hours=config.interval_update/3600)
    d_update = {'updated': f'{datetime.now().strftime("%Y-%m-%d %H:%M")}',
                'next_update': f'{next_update.strftime("%Y-%m-%d %H:%M")}'}
    with open(file_path, 'w') as fp:
        json.dump(d_update, fp)

    threading.Timer(config.interval_update, update_database).start()


if config.update_activated:
    update_database()


def serve_layout():
    navbar = view.navbar(config.title) # Pone un titulo

    # header = view.header(config.sub_title) # Pone un subtitulo

    body = view.body() # Pone un body

    # return html.Div([navbar, header, body])
    return html.Div([navbar, body])


app.layout = serve_layout# Junta todos los componentes
# app.layout = html.Div([navbar, header, body]) # Junta todos los componentes


if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=True) # Levanta un servidor web
