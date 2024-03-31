import typing as t

import ipywidgets as ipw


class QBResult(ipw.VBox):
    """docstring"""

    def __init__(self, result: t.Any) -> None:
        """docstring"""

        output = ipw.Output()

        super().__init__(
            layout={
                "border": "1px solid #9e9e9e",
                "margin": "2px",
                "padding": "5px",
            },
            children=[output],
        )

        with output:
            print(result)
