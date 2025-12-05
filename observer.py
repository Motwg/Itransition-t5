import asyncio
from abc import ABC, abstractmethod
from typing import Self

import gspread
import pandas as pd


class Singleton(type):
    _instances: dict[type, type] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Subscriber(ABC):
    @abstractmethod
    def update(self, data: pd.DataFrame) -> None:
        pass


class DataObserver(metaclass=Singleton):
    is_running: bool
    subscribers: list[Subscriber]
    sheet: gspread.Worksheet | None
    indicator: str

    def __init__(self):
        self.is_running = False
        self.subscribers = []
        self.sheet = None
        self.indicator = ''

    def __repr__(self) -> str:
        return ' '.join([f'{k}:{v}' for k, v in self.__dict__.items()])

    def connect(
        self,
        connection_filepath: str,
        gs_name: str,
        sheet_name: str,
        indicator: str,
    ) -> Self:
        if self.sheet is None:
            connection = gspread.service_account(connection_filepath)
            gs = connection.open(gs_name)
            self.sheet = gs.worksheet(sheet_name)
            self.indicator = indicator
        return self

    async def start(self) -> None:
        if not self.is_running:
            self.is_running = True
            print('Watch work started')
            await self._notify()
            await self._loop()

    def stop(self) -> None:
        self.is_running = False

    def add_subscriber(self, sub: Subscriber) -> None:
        self.subscribers.append(sub)

    async def _loop(self) -> None:
        state = self.sheet.acell(self.indicator)
        while self.is_running:
            await asyncio.sleep(10)
            temp, state = state, self.sheet.acell(self.indicator)
            if state != temp:
                await self._notify()

    async def _notify(self) -> None:
        data = self.sheet.get_all_values()
        headers = data.pop(0)
        mines = pd.DataFrame(data, columns=headers)
        types = {c: pd.to_numeric for c in mines.columns if c != 'Day'}
        for col, f in types.items():
            mines[col] = f(mines[col])
        for s in self.subscribers:
            s.update(mines)
