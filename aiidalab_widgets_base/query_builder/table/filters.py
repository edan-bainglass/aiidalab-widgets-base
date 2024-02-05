from __future__ import annotations

import ipywidgets as ipw

from .component import (
    TableQueryComponentController,
    TableQueryComponentModel,
    TableQueryComponentView,
)


class QueryFiltersController(TableQueryComponentController):
    """docstring"""

    def _set_event_handlers(self) -> None:
        """docstring"""
        super()._set_event_handlers()


class QueryFiltersModel(TableQueryComponentModel):
    """docstring"""


class QueryFiltersView(TableQueryComponentView):
    """docstring"""

    component_type = "filters"

    def __init__(self, **kwargs) -> None:
        """docstring"""

        super().__init__(**kwargs)

        self.children = [
            ipw.HBox(
                layout={},
                children=[
                    self.expand,
                    self.container,
                ],
            ),
        ]
