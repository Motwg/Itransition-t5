from typing import override

import dash_ag_grid as dag
from dash import Input, Output, callback, dcc, html

from pages.page import Page


@callback(Output('live-update-text', 'children'), Input('dropdown-selection', 'value'))
def table(selection: str) -> str:
    return f'Selection: {selection}'


class Charts(Page):
    def __init__(self, path: str) -> None:
        super().__init__(path)

    @override
    def render(self) -> html.Div:
        return html.Div(
            [
                html.Div(id='live-update-text'),
                dcc.Dropdown(['a', 'vav', 'vfff'], 'Canada', id='dropdown-selection')
                if self.data is not None
                else html.Div(),
            ],
            className='p-3 bg-light rounded-3',
        )
