from typing import Any, override

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State, callback, dcc, html

from db import DB
from layouts.rows import get_upper_row
from pages.page import Page


@callback(
    Output('anomalies', 'children'),
    [
        Input('mine-selection', 'value'),
        Input('detector-selection', 'value'),
    ],
)
def find_anomalies(
    mines: list[str],
    detectors: list[str],
) -> dag.AgGrid:
    db = DB()
    x = db['mines']
    return dag.AgGrid(
        style={'height': 300},
        rowData=x.to_dict('records'),
        columnDefs=[
            {
                'field': i,
                'type': 'rightAligned',
                'width': 80,
                'valueFormatter': {
                    'function': "d3.format('(.2f')(params.value)",
                },
            }
            if i != 'Day'
            else {'field': i, 'width': 120}
            for i in x.columns
        ],
    )


class HomePage(Page):
    def __init__(self, path: str) -> None:
        super().__init__(path)

    @override
    def render(self) -> html.Div:
        return html.Div(
            [
                get_upper_row(DB()['mines'], DB()['indicators']),
                html.Hr(),
                dbc.Row(
                    justify='evenly',
                    children=[
                        dbc.Col(
                            width=6,
                            children=[
                                dbc.Stack(
                                    direction='vertical',
                                    gap=1,
                                    children=[
                                        dcc.Dropdown(
                                            mines := list(DB()['indicators']['source']),
                                            mines,
                                            multi=True,
                                            closeOnSelect=False,
                                            id='mine-selection',
                                        ),
                                        dcc.Dropdown(
                                            ['IQR', 'Z-score', 'Distance', 'Grubb'],
                                            ['IQR', 'Z-score', 'Distance', 'Grubb'],
                                            multi=True,
                                            closeOnSelect=False,
                                            id='detector-selection',
                                        ),
                                    ],
                                ),
                                html.Div(id='anomalies'),
                            ],
                        ),
                        dbc.Col(
                            width=6,
                            children=dbc.Stack(
                                direction='vertical',
                                gap=1,
                                children=[
                                    dcc.Dropdown(
                                        mines,
                                        mines,
                                        id='mine-selector',
                                        multi=True,
                                        closeOnSelect=False,
                                    ),
                                    dcc.Dropdown(
                                        ['IQR', 'Z-score', 'Distance', 'Grubb'],
                                        ['IQR', 'Z-score', 'Distance', 'Grubb'],
                                        multi=True,
                                        closeOnSelect=False,
                                        id='detector-selector',
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ],
            className='p-3 bg-light rounded-3',
        )
