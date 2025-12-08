from collections.abc import Callable
from typing import Concatenate, ParamSpec

from dash import html

P = ParamSpec('P')


def err_handler(
    fun: Callable[Concatenate[str, P], html.Div],
) -> Callable[Concatenate[str, P], html.Div]:
    def page_loader(pathname: str, *args: P.args, **kwargs: P.kwargs) -> html.Div:
        try:
            return fun(pathname, *args, **kwargs)
        except KeyError:
            return err_404(pathname)

    return page_loader


def err_404(pathname: str) -> html.Div:
    return html.Div(
        [
            html.H1('404: Not found', className='text-danger'),
            html.Hr(),
            html.P(f'The pathname {pathname} was not recognised...'),
        ],
        className='p-3 bg-light rounded-3',
    )
