from typing import override

from dash import html

from pages.page import Page


class Charts(Page):
    def __init__(self, path: str) -> None:
        super().__init__(path)

    @override
    def render(self) -> html.Div:
        return html.Div(
            [],
            className='p-3 bg-light rounded-3',
        )
