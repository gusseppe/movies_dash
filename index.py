import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import view

from app import app

server = app.server

navbar = view.navbar('CINES MADRID') # Pone un titulo

header = view.header('¿Qué película escoger?') # Pone un subtitulo

body = view.body() # Pone un body

app.layout = html.Div([navbar, header, body]) # Junta todo los componentes


if __name__ == "__main__":
    app.run_server(host='0.0.0.0') # Levanta un servidor web
