from typing import Any


def get_config(key: str) -> Any:
    return {'reload_time': 5000}.get(key)


def pdf_config() -> dict[str, int | str]:
    return {
        'main_title': 'Weylan-Yutani Corporation',
        'main_title_size': 20,
        'font': 'DejaVuSansCondensed',
        'pdf_filename': 'task5',
    }


def obs_config() -> dict[str, str]:
    return {
        'connection_filepath': 'service.json',
        'gs_name': 'task5',
        'sheet_name': 'Out',
        'indicator': 'B2',
    }
