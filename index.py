import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import view

from app import app

from textwrap import dedent
from dash.dependencies import Input, Output

# from dashboard.apps import define_front, \
#     analyze_front, model_front, tune_front, predict_front


navbar = view.navbar('CINES MADRID')

header = view.header('¿Qué película escoger?')

body = view.body()
# body = dbc.Container(
#     [
#         dbc.Row(
#             [
#                 dbc.Col(view.card('Hadoop', 'Hadoop benchmark',
#                                    '/hadoop', hadoop_image), width=3),
#                 dbc.Col(view.card('Spark', 'Spark benchmark',
#                                    '/spark', spark_image), width=3),
#             ],
#             justify='center'
#         )
#     ],
#     className="mt-4",
#     fluid=True,
# )

# app.layout = html.Div([html.Div(id="page_content", style={"margin": "2% 3%"}),
#                        navbar, header, body])

# app.layout = html.Div([html.Div(id="page_content", style={"margin": "2% 3%"}),
#                             dcc.Location(id='url', refresh=False)])

app.layout = html.Div([navbar, header, body])

# @app.callback(Output("page_content", "children"), [Input("url", "pathname")])
# def render_content(url):
#     if url == "/hadoop":
#         # app.layout = story.layout
#         # return story.layout
#         return html.Div([navbar, hadoop_front.layout])
#         # return define_front.layout
#     elif url=='/spark':
#         return html.Div([navbar, spark_front.layout])
#
#     else:
#         # pass
#         return html.Div([navbar, header, body])
#         # message = html.Div([
#         #     dcc.Markdown(
#         #         dedent(f'''
#         #         > #### Under development
#         #         > ###### Head to [pymach](http://www.github.com/gusseppe/pymach)
#         #
#         #     '''))
#         # ],className='two columns indicator')
#         # return message


if __name__ == "__main__":
    #app.run_server(host='0.0.0.0', debug=True, port=9051)
    app.run_server()
