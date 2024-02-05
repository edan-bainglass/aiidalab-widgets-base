from __future__ import annotations

import ipywidgets as ipw

from .component import (
    TableQueryComponentController,
    TableQueryComponentModel,
    TableQueryComponentView,
)


class QueryProjectionsController(TableQueryComponentController):
    """docstring"""


class QueryProjectionsModel(TableQueryComponentModel):
    """docstring"""


class QueryProjectionsView(TableQueryComponentView):
    """docstring"""

    component_type = "projections"

    def __init__(self, **kwargs) -> None:
        """docstring"""

        super().__init__(**kwargs)

        self.content.children = []

        self.children = [
            ipw.HBox(
                layout={},
                children=[
                    self.expand,
                    self.container,
                ],
            ),
        ]
