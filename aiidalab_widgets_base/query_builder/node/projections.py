from __future__ import annotations

import ipywidgets as ipw

from ..styles import CSS
from .component import (
    NodeQueryComponentController,
    NodeQueryComponentModel,
    NodeQueryComponentView,
)


class QueryProjectionsController(NodeQueryComponentController):
    """docstring"""

    _model: QueryProjectionsModel
    _view: QueryProjectionsView

    def _select(self, all=False) -> None:
        """docstring"""
        selected = getattr(self._view.selector, "options" if all else "value")
        options = self._view.selected.options
        self._view.selected.options = [*sorted({*options} | {*selected})]

    def _deselect(self, all=False) -> None:
        """docstring"""
        selected = getattr(self._view.selected, "options" if all else "value")
        options = self._view.selected.options
        self._view.selected.options = [*sorted({*options} - {*selected})]

    def _set_event_handlers(self) -> None:
        """docstring"""
        super()._set_event_handlers()
        self._view.select.on_click(lambda _: self._select())
        self._view.select_all.on_click(lambda _: self._select(all=True))
        self._view.deselect.on_click(lambda _: self._deselect())
        self._view.deselect_all.on_click(lambda _: self._deselect(all=True))


class QueryProjectionsModel(NodeQueryComponentModel):
    """docstring"""


class QueryProjectionsView(NodeQueryComponentView):
    """docstring"""

    component_type = "projections"

    def __init__(self, **kwargs) -> None:
        """docstring"""

        super().__init__(**kwargs)

        self.selector = ipw.SelectMultiple(
            layout=CSS.MULTISELECT,
        )

        self.selected = ipw.SelectMultiple(
            layout=CSS.MULTISELECT,
        )

        self.select = ipw.Button(
            layout=CSS.WAUTO,
            icon="angle-right",
            tooltip="Select",
        )

        self.select_all = ipw.Button(
            layout=CSS.WAUTO,
            icon="angle-double-right",
            tooltip="Select all",
        )

        self.deselect = ipw.Button(
            layout=CSS.WAUTO,
            icon="angle-left",
            tooltip="Deselect",
        )

        self.deselect_all = ipw.Button(
            layout=CSS.WAUTO,
            icon="angle-double-left",
            tooltip="Deselect all",
        )

        self.controls = ipw.VBox(
            layout=CSS.MX2,
            children=[
                self.select,
                self.select_all,
                self.deselect,
                self.deselect_all,
            ],
            **kwargs,
        )

        self.content.children = [
            ipw.HBox(
                layout={},
                children=[
                    self.selector,
                    self.controls,
                    self.selected,
                ],
            ),
        ]
