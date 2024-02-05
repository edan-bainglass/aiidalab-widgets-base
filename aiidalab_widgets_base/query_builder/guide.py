from __future__ import annotations

import ipywidgets as ipw


class QueryBuilderGuide(ipw.VBox):
    """docstring"""

    def __init__(self, **kwargs) -> None:
        """docstring"""

        super().__init__(
            children=[
                ipw.Label("Coming Soon"),
            ],
            **kwargs,
        )
