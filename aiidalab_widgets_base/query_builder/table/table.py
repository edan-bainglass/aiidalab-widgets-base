from __future__ import annotations

import ipywidgets as ipw
import traitlets

from ..styles import CSS
from .factory import get_query_component_view


def get_table_query_view() -> TableQueryView:
    """docstring"""
    model = TableQueryModel()
    view = TableQueryView()
    _ = TableQueryController(model, view)
    return view


class TableQueryController:
    """docstring"""

    def __init__(self, model: TableQueryModel, view: TableQueryView) -> None:
        """docstring"""
        self._model = model
        self._view = view
        self._set_event_handlers()

    def _close_view(self, _=None) -> None:
        """docstring"""
        self._view.closed = True
        self._view.close()

    def _set_event_handlers(self) -> None:
        """docstring"""
        self._view.remove.on_click(self._close_view)


class TableQueryModel(traitlets.HasTraits):
    """docstring"""


class TableQueryView(ipw.VBox):
    """docstring"""

    closed = traitlets.Bool(False)

    def __init__(self, **kwargs):
        """docstring"""

        self.table_selector = ipw.Dropdown(
            layout=CSS.M2,
            style=CSS.TIGHT_DESCRIPTION,
            description="Table:",
        )

        self.reset = ipw.Button(
            layout=CSS.BUTTON,
            button_style="warning",
            icon="refresh",
            tooltip="Reset table query",
        )

        self.remove = ipw.Button(
            layout=CSS.BUTTON,
            button_style="danger",
            icon="times",
            tooltip="Remove query",
        )

        self.filters_view = get_query_component_view("filters")
        self.projections_view = get_query_component_view("projections")

        super().__init__(
            layout=CSS.BORDERED_BOX,
            children=[
                ipw.HBox(
                    layout={},
                    children=[
                        self.table_selector,
                        ipw.HBox(
                            layout=CSS.FLOAT_RIGHT,
                            children=[
                                self.reset,
                                self.remove,
                            ],
                        ),
                    ],
                ),
                self.filters_view,
                self.projections_view,
            ],
            **kwargs,
        )
