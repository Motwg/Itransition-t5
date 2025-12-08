import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html

from layouts.aggrids import get_aggrid
from layouts.utils import num_input


def get_upper_row(data: pd.DataFrame, desc: pd.DataFrame) -> dbc.Row:
    default = {
        'height': 250,
        'first_col_width': 120,
        'col_width': 80,
    }
    return dbc.Row(
        [
            dbc.Col(width=7, children=get_aggrid(desc, 'desc-table', **default)),
            dbc.Col(
                width=5,
                children=get_aggrid(data, 'data-table', **default),
            ),
        ],
    )


def get_bottom_row(
    mine_names: list[str],
    det_names: list[str],
    plot_names: list[str],
) -> dbc.Row:
    return dbc.Row(
        justify='evenly',
        children=[
            dbc.Col(
                width=7,
                children=[
                    dcc.Graph(
                        id='anomalies',
                        style={'height': 500},
                    ),
                ],
            ),
            dbc.Col(
                width=5,
                children=dbc.Stack(
                    direction='vertical',
                    gap=2,
                    children=[
                        html.H4('Chart options'),
                        dcc.Dropdown(
                            mine_names,
                            mine_names,
                            multi=True,
                            closeOnSelect=False,
                            id='mine-selection',
                        ),
                        dcc.Dropdown(
                            det_names,
                            det_names,
                            multi=True,
                            closeOnSelect=False,
                            id='detector-selection',
                        ),
                        dcc.Dropdown(
                            plot_names,
                            plot_names[-1],
                            id='chart-selection',
                        ),
                        html.Hr(),
                        html.H4('Outliers options'),
                        dbc.Stack(
                            [
                                num_input(
                                    'IQR threshold',
                                    id='parameter-iqr',
                                    min=1.0,
                                    max=5.0,
                                    value=1.5,
                                ),
                                num_input(
                                    'Z-score threshold',
                                    'σ',
                                    id='parameter-zscore',
                                    min=1.0,
                                    max=3.0,
                                    value=3.0,
                                ),
                            ],
                            gap=1,
                            direction='horizontal',
                        ),
                        dbc.Stack(
                            [
                                num_input(
                                    'Grubb alpha',
                                    id='parameter-grubb',
                                    min=0.05,
                                    max=10.0,
                                    value=0.15,
                                    step=0.05,
                                ),
                                num_input(
                                    'Distance from avg',
                                    '%',
                                    id='parameter-distance',
                                    min=5.0,
                                    max=100.0,
                                    value=30.0,
                                ),
                            ],
                            gap=1,
                            direction='horizontal',
                        ),
                        html.Hr(),
                        dbc.Stack(
                            [
                                dbc.InputGroupText('Degree'),
                                dcc.Dropdown(list(range(1, 5)), 2, id='degree'),
                            ],
                            gap=1,
                            direction='horizontal',
                        ),
                        html.Button('Export as PDF', id='to-pdf'),
                        dcc.Download(id='download'),
                    ],
                ),
            ),
        ],
    )
