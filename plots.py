from collections.abc import Callable
from functools import partial
from typing import Literal

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures


def available_plots() -> dict[str, Callable[[pd.DataFrame, pd.DataFrame, int], go.Figure]]:
    return {
        'line': plot_line,
        'bar stacked': partial(plot_bar, barmode='stack'),
        'bar grouped': partial(plot_bar, barmode='group'),
        'bar overlay': partial(plot_bar, barmode='overlay'),
        'violin': plot_violin,
    }


def plot_bar(
    data: pd.DataFrame,
    _: pd.DataFrame,
    degree: int,
    barmode: Literal['stack', 'group', 'overlay'],
) -> go.Figure:
    y = data.columns.drop(['Day'])
    return px.bar(
        data,
        x='Day',
        y=y,
        title='Anomalies',
        barmode=barmode,
        labels={
            'value': 'Daily output',
        },
    )


def plot_line(
    data: pd.DataFrame,
    outliers: pd.DataFrame,
    degree: int,
) -> go.Figure:
    y = data.columns.drop(['Day'])
    fig = px.line(
        data,
        x='Day',
        y=y,
        markers=True,
        labels={
            'value': 'Daily output',
        },
    )
    colors = [d.line.color for d in fig.data]
    fig = fig.update_traces(opacity=0.7)
    for column, color in zip(y, colors, strict=True):
        trendline = get_trendline(data[column], degree)
        fig = fig.add_traces(
            go.Scatter(x=data['Day'], y=trendline, name=f'Trend-{column}', line=dict(color=color))
        )
    return add_outliers(outliers, fig, 'Day')


def get_trendline(series: pd.Series, degree: int) -> np.ndarray:
    x = np.array(series.index).reshape(-1, 1)
    y = np.array(series.values).reshape(-1, 1)
    model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    model.fit(x, y)
    return model.predict(x).flatten()


def plot_violin(
    data: pd.DataFrame,
    outliers: pd.DataFrame,
    _: int,
) -> go.Figure:
    mines = data.loc[:, data.columns != 'Day']
    fig = go.Figure()
    for mine in mines:
        fig = fig.add_trace(
            go.Violin(
                y=mines[mine],
                name=mine,
                box_visible=True,
                meanline_visible=True,
                points='all',
                pointpos=0,
            )
        )

    out = outliers.loc[:, outliers.columns != 'Day']
    out = out.transpose()
    out['names'] = out.index
    return add_outliers(out, fig, 'names')


def add_outliers(outliers: pd.DataFrame, figure: go.Figure, x: str) -> go.Figure:
    fig = figure
    for i, col in enumerate(outliers.columns):
        fig = fig.add_trace(
            go.Scatter(
                x=outliers[x],
                y=outliers[col],
                name='outliers',
                mode='markers',
                marker_color='rgba(0, 0, 0, .8)',
                showlegend=not i,
            ),
        )
    return fig
