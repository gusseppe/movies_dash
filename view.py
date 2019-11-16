import os
import config
import dash # libreria que se encarga de mostrar el dashboard
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import model # Es el modelo de nuestra apliccion
import controller # El controlador de nuestra aplicacion

from app import app #
from dash.dependencies import Input, Output, State


def header(title='Some title', intro='intro', body='body'):
    """"
        Se encarga de mostrar la parte superior de la vista (titulos, dropdown)
    """
    _header = dbc.Container(
        [
            dbc.Jumbotron(
                [
                    dbc.Container(
                        [
                            html.H1(title,
                                    className="text-center text-info"),
                        ],
                        fluid=True,
                    ),
                ],
                fluid=True,
            )
        ],
        className="mt-5",
        fluid=True,
    )

    return _header


def navbar(title='mi_titulo_navbar', repo_site='#'):
    """"
        Se encarga de mostrar los nombres del equipo en un dropdown
    """
    _navbar = dbc.NavbarSimple(
        children=[
            # dbc.NavItem(dbc.NavLink("Bitbucket", href=repo_site)),
            # html.A('Refresh', href='/'),
            # dbc.NavItem(dbc.NavLink("¡Tendré suerte!", href="/")),
            dbc.NavItem(dbc.Button(html.A('¡Tendré suerte!', href='/'))),
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Equipo",
                children=[
                    dbc.DropdownMenuItem(d['name'], href=d['site']) for d in config.team
                ],
            ),
        ],
        brand=title,
        brand_href="/",
        sticky="top",
    )
    return _navbar


def card(d_info, _id=1):
    _card = dbc.Card(
        [
            dbc.CardImg(
                # src='assets/images/thumbs-down.png',
                src=d_info['img'],
                # src=(
                #     "https://placeholdit.imgix.net/~text?"
                #     "txtsize=33&txt=318%C3%97180&w=318&h=180"
                # )
                # style={"max-width": "320px",
                #        "height": '6rem',
                #        # 'width': '100%',
                #        'object-fit': 'cover'},
                style={
                    "height": '20rem',
                },
                top=True
            ),
            dbc.CardBody(
                [
                    html.H4(d_info['name'].capitalize(), className="card-title"), # Nombre de la pelicual. E.g, Joker
                    html.P(
                        f"Rating: {d_info['rating']}", # Rating
                        className="card-text",
                    ),
                    dbc.Button("Magic", color="primary", id=f"collapse-button-{_id}"),
                    html.Hr(),
                    dbc.Collapse([
                        html.H4('Sentiment Twitter'),
                        dbc.Progress(
                            [
                                dbc.Progress(value=d_info['sentiment'][0] * 100,
                                             color="success", bar=True, style={"height": "1px"},
                                             children=f"Positivo: {d_info['sentiment'][0] * 100}"),
                                dbc.Progress(value=d_info['sentiment'][1] * 100,
                                             color="danger", bar=True,
                                             children=f"Negativo: {d_info['sentiment'][1] * 100}"),
                                dbc.Progress(value=d_info['sentiment'][2] * 100,
                                             color="warning", bar=True,
                                             children=f"Neutro: {d_info['sentiment'][2] * 100}"),
                            ],
                            style={"height": "30px"},
                            multi=True,
                        ),
                        html.Hr(),
                        dcc.Markdown(d_info['collapse']),
                        dbc.CardImg(
                            src=d_info['wordcloud'],
                            style={
                                "height": '15rem',
                            },
                            top=True
                        ),
                        html.Hr(),
                        html.P(d_info['update']),

                    ],
                        id=f"collapse-{_id}",
                    ),
                ]
            ),
        ],
        style={"max-width": "320px"},
    )
    return _card


def body():
    """"
        Lista todas las peliculas en la pagina usando contenedores tipo Card.
    """

    body = dbc.Container(
        [
            dbc.Row( # En una sola fila, aunque puede ajustarse al ancho de la pantalla
                    controller.show_cards() # Llama al controlador par aque se encargue de mostrar las peliculas
                , justify='center'
            )
        ],
        className="mt-4",
        fluid=True,
    )

    return body


# @app.callback(
#     Output("collapse-1", "is_open"),
#     [Input("collapse-button-1", "n_clicks")],
#     [State("collapse-1", "is_open")],
# )
# def toggle_collapse(n, is_open):
#     """"
#         Se encargara del evento de aparecer informacion cuando se hace click en un boton
#     """
#     if n:
#         print('hola')
#         return not is_open
#     return is_open

@app.callback(
    [Output(f"collapse-{i}", "is_open") for i in range(0, config.number_of_movies)],
    [Input(f"collapse-button-{i}", "n_clicks") for i in range(0, config.number_of_movies)],
    [State(f"collapse-{i}", "is_open") for i in range(0, config.number_of_movies)],
)
def toggle_collapse(n0, n1, n2, n3,
                    is_open0, is_open1, is_open2, is_open3):
    ctx = dash.callback_context

    if not ctx.triggered:
        return ""
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "collapse-button-0" and n0:
        return not is_open0, False, False, False
    elif button_id == "collapse-button-1" and n1:
        return False, not is_open1, False, False
    elif button_id == "collapse-button-2" and n2:
        return False, False, not is_open2, False
    elif button_id == "collapse-button-3" and n3:
        return False, False, False, not is_open3
    return False, False, False, False

# @app.callback(
#     [Output(f"collapse-{i}", "is_open") for i in range(0, config.number_of_movies)],
#     [Input(f"collapse-button-{i}", "n_clicks") for i in range(0, config.number_of_movies)],
#     [State(f"collapse-{i}", "is_open") for i in range(0, config.number_of_movies)],
# )
# def toggle_collapse(n0, n1, n2, n3, n4,
#                      is_open0, is_open1, is_open2, is_open3,
#                      is_open4):
#     ctx = dash.callback_context
#
#     if not ctx.triggered:
#         return ""
#     else:
#         button_id = ctx.triggered[0]["prop_id"].split(".")[0]
#
#     if button_id == "collapse-button-0" and n0:
#         return not is_open0, False, False, False, False
#     elif button_id == "collapse-button-1" and n1:
#         return False, not is_open1, False, False, False
#     elif button_id == "collapse-button-2" and n2:
#         return False, False, not is_open2, False, False
#     elif button_id == "collapse-button-3" and n3:
#         return False, False, False, not is_open3, False
#     elif button_id == "collapse-button-4" and n4:
#         return False, False, False, False, not is_open4
#     return False, False, False, False, False