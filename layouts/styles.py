from collections.abc import Mapping


def get_style(style_name: str) -> Mapping[str, str | int] | None:
    return {
        'sidebar': {
            'position': 'fixed',
            'top': 0,
            'left': 0,
            'bottom': 0,
            'width': '14rem',
            'padding': '2rem 1rem',
            'background-color': '#DFE0E1',
            'z-index': 1,
        },
        'content': {
            'margin-left': '18rem',
            'margin-right': '2rem',
            'padding': '2rem 1rem',
        },
    }.get(style_name)
