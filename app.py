

import flask
import dash
# import nltk
import dash_bootstrap_components as dbc


server = flask.Flask(__name__) # Declara un servidor de Flask tipo web
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.DARKLY]) # Tema oscuro

app.scripts.config.serve_locally = True # configuracion del servidor
app.config.suppress_callback_exceptions = True # configuracion del servidor
