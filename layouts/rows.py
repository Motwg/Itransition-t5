import dash_bootstrap_components as dbc
import pandas as pd

from layouts.aggrids import get_aggrid


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
