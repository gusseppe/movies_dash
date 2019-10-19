import os
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import model
import controller

from app import app

from dash.dependencies import Input, Output, State


def header(title='Some title', intro='intro', body='body'):
    _header = dbc.Container(
        [
            dbc.Jumbotron(
                [
                    dbc.Container(
                        [
                            html.H1(title,
                                    className="text-center text-info"),
                            # html.H5(
                            #     # "DeployML is a framework that aims to sum up the results and track the health "
                            #     # "of a Machine Learning model.",
                            #     intro,
                            #     className="mt-4",
                            # ),
                            # dbc.Button("More info", id="collapse-button", className="mb-3"),
                            # dbc.Collapse(
                            #     #dbc.Card(dbc.CardBody("This content is hidden in the collapse")),
                            #     dcc.Markdown(body),
                            #     id="collapse",
                            # ),
                        ],
                        fluid=True,
                    )
                ],
                fluid=True,
            )
        ],
        className="mt-4",
        fluid=True,
    )

    return _header


def navbar(title='DeployML', repo_site='#'):
    _navbar = dbc.NavbarSimple(
        children=[
            # dbc.NavItem(dbc.NavLink("Bitbucket", href=repo_site)),
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Equipo",
                children=[
                    dbc.DropdownMenuItem(d['name'], href=d['site']) for d in model.list_team()
                    # dbc.DropdownMenuItem("Entry 2"),
                    # dbc.DropdownMenuItem(divider=True),
                    # dbc.DropdownMenuItem("Logout"),
                ],
            ),
        ],
        brand=title,
        brand_href="/",
        sticky="top",
    )
    return _navbar


def card(title='DeployML',
         description='some brief description regarding the app',
         href='#', image_path=''):
    _card = dbc.Card(
        [
            dbc.CardImg(
                src=image_path,
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
            # dbc.CardBody(
            #     # [dbc.CardTitle(title), dbc.CardSubtitle("Card subtitle")]
            #     # [dbc.CardTitle(title)]
            #     [html.H5(title, className="card-title")]
            # ),
            dbc.CardBody(
                [
                    # dbc.CardText(description),
                    # dbc.CardLink("Go to app", href=href),
                    # dbc.CardLink("Another link", href="#"),

                    html.H4(title, className="card-title"),
                    html.P(
                        description,
                        className="card-text",
                    ),
                    dbc.Button("Go somewhere", color="primary"),
                    ]
            ),
        ],
        style={"max-width": "320px"},
    )
    return _card


def body():

    body = dbc.Container(
        [
            dbc.Row(
                [

                    dbc.Col(card(d['name'], f"Score: {d['rating']}",
                                 '#', d['img']), width=3)
                    for d in model.get_movies_filmaffinity()[:5]

                    # dbc.Col(card('Hadoop', 'Hadoop benchmark',
                    #                   '/hadoop', hadoop_image), width=3),
                    # dbc.Col(card('Spark', 'Spark benchmark',
                    #                   '/spark', spark_image), width=3),
                ],
                justify='center'
            )
        ],
        className="mt-4",
        fluid=True,
    )

    return body


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
