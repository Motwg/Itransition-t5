from typing import Any, override

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State, callback, dcc, html

from layouts.rows import get_upper_row
from pages.page import Page


@callback(
    Output('anomalies', 'children'),
    [
        Input('mine-selection', 'value'),
        Input('detector-selection', 'value'),
        Input('desc-table', 'rowData'),
        State('data-table', 'rowData'),
    ],
)
def find_anomalies(
    mines: list[str],
    detectors: list[str],
    desc: list[dict[str, Any]],
    data: list[dict[str, Any]],
) -> dag.AgGrid:
    x = pd.DataFrame(data)
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
    desc: pd.DataFrame

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.desc = pd.DataFrame()

    @override
    def render(self) -> html.Div:
        return html.Div(
            [
                get_upper_row(self.data, self.desc),
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
                                            mines := list(self.desc['source']),
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

    @override
    def update(self, data: pd.DataFrame) -> None:
        super().update(data)
        desc = data.loc[:, data.columns != 'Day'].describe().transpose()
        desc['source'] = desc.index
        cols = list(desc.columns)
        self.desc = desc[cols[-1:] + cols[:-1]]
        # z-score roznica w odchylenia
        # def count_z_score(mean)
