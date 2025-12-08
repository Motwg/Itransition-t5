import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate

from config import get_config, obs_config
from layouts.errors import err_handler
from layouts.sidebar import render_sidebar
from layouts.styles import get_style
from observer import DataObserver
from pages.home import HomePage

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
content = html.Div(id='page-content', style=get_style('content'))
pages = {p.path: p for p in [HomePage('/home')]}
app.layout = html.Div(
    [
        dcc.Location(id='url'),
        dcc.Interval(
            id='pull-interval',
            interval=get_config('reload_time'),
            n_intervals=0,
        ),
        render_sidebar(pages.keys()),
        content,
    ],
)


@callback(Input('url', 'pathname'))
async def start_observer(_: str) -> None:
    await DataObserver().connect(**obs_config()).start()


@callback(
    Output('page-content', 'children', allow_duplicate=True),
    [State('url', 'pathname'), Input('pull-interval', 'n_intervals')],
    prevent_initial_call='initial_duplicate',
)
@err_handler
def refresh_content(pathname: str, _: int) -> html.Div:
    page = pages[pathname]
    if page.is_new_content:
        page.refresh()
        return page.render()
    raise PreventUpdate


@callback(
    Output('page-content', 'children', allow_duplicate=True),
    Input('url', 'pathname'),
    prevent_initial_call='initial_duplicate',
)
@err_handler
def render_page_content(pathname: str) -> html.Div:
    return pages[pathname].render()


if __name__ == '__main__':
    obs = DataObserver()
    for page in pages.values():
        obs.add_subscriber(page)
    app.run(debug=False)
