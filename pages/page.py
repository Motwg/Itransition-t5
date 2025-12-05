from typing import override

import dash_ag_grid as dag
import pandas as pd
from dash import html

from observer import Subscriber


class Page(Subscriber):
    path: str
    is_new_content: bool = False
    data: pd.DataFrame | None = None

    def __init__(self, path: str) -> None:
        self.data = None
        self.path = path

    def render(self) -> html.Div:
        return html.Div(
            dag.AgGrid(
                rowData=self.data.to_dict('records'),
                columnDefs=[{'field': i} for i in self.data.columns],
                style={'height': 300},
            )
            if self.data is not None
            else html.Div(),
            className='p-3 bg-light rounded-3',
        )

    @override
    def update(self, data: pd.DataFrame) -> None:
        self.data = data
        self.is_new_content = True
        print(f'updating...{self.path}')

    def refresh(self) -> None:
        self.is_new_content = False
