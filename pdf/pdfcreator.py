import io
from collections.abc import Callable
from functools import partial
from typing import Any

import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF


class PDFCreator:
    pdf: FPDF
    font: str

    def __init__(self, font: str) -> None:
        """Initialize the PDF creator."""
        self.pdf = FPDF()
        self.pdf.add_page()
        self.font = font
        self.pdf.add_font('DejaVuSansCondensed', fname='font/DejaVuSansCondensed.ttf')
        self.pdf.add_font('DejaVuSansCondensed', style='B', fname='font/DejaVuSansCondensed.ttf')

    def add_title(self, title: str, size: int = 16) -> None:
        """Add the title to the PDF."""
        self.pdf.set_font(self.font, style='B', size=size)
        _ = self.pdf.cell(0, 10, title, ln=True, align='C')
        self.pdf.ln(10)

    def add_table(self, data: pd.DataFrame) -> None:
        """Add the table from the DataFrame to the PDF."""
        self.pdf.set_font(self.font, size=12)
        rounded = data.round(decimals=2)
        with self.pdf.table() as table:
            row = table.row()
            for column in data.columns.tolist():
                row.cell(column)

            for _, data_row in rounded.iterrows():
                row = table.row()
                for item in data_row:
                    _ = row.cell(str(item))
        self.pdf.ln(10)

    def add_figure(self, fig_data: dict[str, Any]) -> None:
        """Add the image of figure to the PDF."""
        fig = go.Figure(fig_data)
        image_data = fig.to_image(format='png', engine='kaleido')
        _ = self.pdf.image(io.BytesIO(image_data), w=self.pdf.epw)

    def get_writer(self) -> Callable[[Any], None]:
        return partial(self.pdf.output, dest='S')
