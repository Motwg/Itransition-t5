import pandas as pd

from singleton import Singleton


def count_indicators(data: pd.DataFrame) -> pd.DataFrame:
    desc = data.loc[:, data.columns != 'Day'].describe().transpose()
    desc['source'] = desc.index
    cols = list(desc.columns)
    return desc[cols[-1:] + cols[:-1]]


class DB(metaclass=Singleton):
    mines: pd.DataFrame
    indicators: pd.DataFrame

    def __init__(self) -> None:
        self.mines = pd.DataFrame()
        self.indicators = pd.DataFrame()

    def update(self, mines: pd.DataFrame | None = None) -> None:
        self.mines = mines if mines is not None else self.mines
        self.indicators = count_indicators(mines)

    def __getitem__(self, key: str) -> pd.DataFrame:
        return getattr(self, key)

    def __setitem__(self, key: str, value: pd.DataFrame) -> None:
        setattr(self, key, value)
