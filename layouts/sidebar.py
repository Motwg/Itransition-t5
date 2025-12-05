from collections.abc import Iterable

import dash_bootstrap_components as dbc
from dash import html

from layouts.styles import get_style


def render_sidebar(pages: Iterable[str]) -> html.Div:
    return html.Div(
        [
            html.H2('Itransition', id='project', title='', className='display-6'),
            html.Hr(),
            html.P('Dashboard', className='lead'),
            dbc.Nav(
                [
                    dbc.NavLink(
                        f'{page.split("/")[-1].capitalize()}', href=f'{page}', active='exact'
                    )
                    for page in pages
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=get_style('sidebar'),
    )
