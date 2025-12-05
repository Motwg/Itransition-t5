import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate

from config import obs_config
from layouts.errors import er_404
from layouts.sidebar import render_sidebar
from layouts.styles import get_style
from observer import DataObserver
from pages.charts import Charts
from pages.home import HomePage
from pages.page import Page

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
content = html.Div(id='page-content', style=get_style('content'))
pages = {p.path: p for p in [Page('/help'), HomePage('/home'), Charts('/charts')]}
app.layout = html.Div(
    [
        dcc.Location(id='url'),
        dcc.Interval(
            id='pull-interval',
            interval=5000,
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
def refresh_content(pathname: str, _: int) -> html.Div:
    try:
        page = pages[pathname]
        if page.is_new_content:
            page.refresh()
            return page.render()
        raise PreventUpdate
    except KeyError:
        return er_404(pathname)


@callback(
    Output('page-content', 'children', allow_duplicate=True),
    Input('url', 'pathname'),
    prevent_initial_call='initial_duplicate',
)
def render_page_content(pathname: str) -> html.Div:
    try:
        return pages[pathname].render()
    except KeyError:
        return er_404(pathname)


if __name__ == '__main__':
    obs = DataObserver()
    for page in pages.values():
        obs.add_subscriber(page)
    app.run(debug=True)
