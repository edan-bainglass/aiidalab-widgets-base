from __future__ import annotations

import ipywidgets as ipw
import traitlets

from aiidalab_widgets_base.query_builder.service import AiiDAService

from ..styles import CSS
from .factory import QueryComponentFactory


def get_table_query_view(aiida_service: AiiDAService) -> TableQueryView:
    """docstring"""
    model = TableQueryModel(aiida_service)
    view = TableQueryView()
    _ = TableQueryController(model, view)
    return view


class TableQueryController:
    """docstring"""

    def __init__(self, model: TableQueryModel, view: TableQueryView) -> None:
        """docstring"""
        self._model = model
        self._view = view
        self._init_view()
        self._set_event_handlers()

    def _init_view(self) -> None:
        """docstring"""
        QueryComponentFactory.set_service(self._model.aiida)
        self.filters_view = QueryComponentFactory.get_view("filters")
        self.projections_view = QueryComponentFactory.get_view("projections")
        self._view.children += (self.filters_view, self.projections_view)

    def _close_view(self, _=None) -> None:
        """docstring"""
        self._view.closed = True
        self._view.close()

    def _set_event_handlers(self) -> None:
        """docstring"""
        self._view.remove.on_click(self._close_view)


class TableQueryModel(traitlets.HasTraits):
    """docstring"""

    def __init__(self, service: AiiDAService) -> None:
        """docstring"""
        self.aiida = service


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
            ],
            **kwargs,
        )
