from collections.abc import Callable

import pandas as pd
from outliers import smirnov_grubbs as grubbs
from scipy.stats import zscore


def available_detectors() -> dict[str, Callable[[pd.Series, float], pd.Series]]:
    return {
        'IQR': detect_iqr,
        'Zscore': detect_zscore,
        'Distance': detect_distance,
        'Grubb': detect_grubbs,
    }


def detect_iqr(column: pd.Series, iqr_threshold: float) -> pd.Series:
    iqr = (q3 := column.quantile(0.75)) - (q1 := column.quantile(0.25))
    outliers = column[
        ((column < (q1 - iqr_threshold * iqr)) | (column > (q3 + iqr_threshold * iqr)))
    ]
    return outliers


def detect_zscore(column: pd.Series, zscore_threshold: float) -> pd.Series:
    z = zscore(column)
    return column[(z < -zscore_threshold) | (z > zscore_threshold)]


def detect_grubbs(column: pd.Series, grubbs_alpha: float) -> pd.Series:
    ind = pd.Series(grubbs.two_sided_test_indices(column, alpha=grubbs_alpha))
    return column.iloc[~ind]


def detect_distance(column: pd.Series, dist_perc: float) -> pd.Series:
    x = 1 + (dist_perc / 100)
    avg = column.rolling(5, closed='both').mean().bfill()
    return column[((column > (avg * x)) | (column < (avg / x)))]
