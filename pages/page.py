from typing import override

from dash import html

from observer import Subscriber


class Page(Subscriber):
    path: str
    is_new_content: bool = False

    def __init__(self, path: str) -> None:
        self.path = path

    def render(self) -> html.Div:
        return html.Div(
            className='p-3 bg-light rounded-3',
        )

    @override
    def update(self) -> None:
        self.is_new_content = True

    def refresh(self) -> None:
        self.is_new_content = False
