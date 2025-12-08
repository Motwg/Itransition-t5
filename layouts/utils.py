from typing import Any

import dash_bootstrap_components as dbc
from dash import html


def card_content(header: str, title: str, body: str) -> list[dbc.CardHeader | dbc.CardBody]:
    return [
        dbc.CardHeader(header),
        dbc.CardBody(
            [
                html.H5(title, className='card-title'),
                html.P(
                    body,
                    className='card-text',
                ),
            ],
        ),
    ]


def num_input(
    text: str,
    extra: str = '',
    **in_params: Any,
) -> dbc.InputGroup:
    return dbc.InputGroup(
        [
            dbc.InputGroupText(text),
            dbc.Input(
                type='number',
                **in_params,
            ),
            dbc.InputGroupText(extra) if extra else html.Div(),
        ],
    )
