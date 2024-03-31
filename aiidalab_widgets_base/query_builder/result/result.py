import typing as t

import ipywidgets as ipw


class QBResult(ipw.VBox):
    """docstring"""

    def __init__(self, result: t.Any) -> None:
        """docstring"""

        output = ipw.Output()

        super().__init__(
            layout={},
            children=[output],
        )

        with output:
            print(result)
