from typing import Any, override

import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State, callback, dcc, html

from config import pdf_config
from db import DB
from detectors import available_detectors
from layouts.rows import get_bottom_row, get_upper_row
from pages.page import Page
from pdf.pdfcreator import PDFCreator
from plots import available_plots


@callback(
    Output('download', 'data'),
    [Input('to-pdf', 'n_clicks'), State('anomalies', 'figure')],
    prevent_initial_call=True,
)
def to_pdf(_: int, fig_data: dict[str, Any]) -> dict[str, Any]:
    writer = PDFCreator(pdf_config()['font'])
    writer.add_title(pdf_config()['main_title'], size=pdf_config()['main_title_size'])
    writer.add_title('Daily output')
    writer.add_table(DB()['mines'])
    writer.add_title('Summary')
    writer.add_table(DB()['indicators'])
    writer.add_title('Anomalies')
    writer.add_figure(fig_data)
    return dcc.send_bytes(writer.get_writer(), f'{pdf_config()["pdf_filename"]}.pdf')


@callback(
    Output('anomalies', 'figure'),
    [
        Input('mine-selection', 'value'),
        Input('detector-selection', 'value'),
        Input('chart-selection', 'value'),
        Input('degree', 'value'),
    ]
    + [Input(f'parameter-{d.lower()}', 'value') for d in available_detectors()],
)
def find_anomalies(
    mines: list[str],
    det_names: list[str],
    chart: str,
    degree: int,
    *args: float,
) -> go.Figure:
    data = DB()['mines']
    outliers = pd.DataFrame()
    detectors = {
        k: (det, arg) for (k, det), arg in zip(available_detectors().items(), args, strict=True)
    }
    for mine in mines:
        if len(det_names) > 0:
            temp_outliers = pd.concat(
                [detectors[d_name][0](data[mine], detectors[d_name][1]) for d_name in det_names]
            ).astype(float)
            outliers[mine] = temp_outliers.drop_duplicates()
    outliers['Day'] = data['Day'][outliers.index]
    return available_plots().get(chart)(data[[*mines, 'Day']], outliers, degree)


class HomePage(Page):
    def __init__(self, path: str) -> None:
        super().__init__(path)

    @override
    def render(self) -> html.Div:
        indicators = DB()['indicators']
        return html.Div(
            [
                get_upper_row(DB()['mines'], indicators),
                html.Hr(),
                get_bottom_row(
                    list(indicators['source']),
                    list(available_detectors()),
                    list(available_plots()),
                ),
            ],
            className='p-3 bg-light rounded-3',
        )
