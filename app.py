import flask
import dash
import dash_bootstrap_components as dbc
# import dash_auth
import dash_html_components as html

# VALID_USERNAME_PASSWORD_PAIRS = [
#     ['hello', 'world']
# ]

server = flask.Flask(__name__) # Declara un servidor de Flask
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.SANDSTONE]) # Pasa el servidor Flask a Dash
# app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.DARKLY])

# auth = dash_auth.BasicAuth(
#     app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )

# current_path = os.getcwd()
# external_css = [
#     os.path.join(current_path, 'assets/stylesheet-oil-and-gas.css'),
#     os.path.join(current_path, 'assets/all.css'),
#     # os.path.join(current_path, 'assets/loading.css'),
#     os.path.join(current_path, 'assets/dash_crm.css')
#     # 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css'
# ]
#
# for css in external_css:
#     app.css.append_css({"external_url": css})

app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True
# app.config.requests_pathname_prefix = ''