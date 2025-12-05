from typing import Any


def get_config(key: str) -> Any:
    return {}.get(key)


def obs_config() -> dict[str, str]:
    return {
        'connection_filepath': 'service.json',
        'gs_name': 'task5',
        'sheet_name': 'Out',
        'indicator': 'B2',
    }
