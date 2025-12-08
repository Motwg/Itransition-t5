import dash_ag_grid as dag
import pandas as pd


def get_aggrid(
    data: pd.DataFrame,
    ag_id: str,
    height: int,
    first_col_width: int,
    col_width: int,
) -> dag.AgGrid:
    return dag.AgGrid(
        id=ag_id,
        style={'height': height},
        rowData=data.to_dict('records'),
        columnDefs=[
            {
                'field': col,
                'type': 'rightAligned',
                'width': col_width,
                'valueFormatter': {
                    'function': "d3.format('(.2f')(params.value)",
                },
            }
            if i != 0
            else {'field': col, 'width': first_col_width}
            for i, col in enumerate(data.columns)
        ],
    )
