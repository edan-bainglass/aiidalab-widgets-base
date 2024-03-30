from __future__ import annotations

import typing as t

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

    def _init_view(self) -> None:
        """docstring"""
        self._update_options()

    def _update_options(self) -> None:
        """docstring"""
        self._view.selector.options = self._model.get_fields()

    def _select(self, all=False) -> None:
        """docstring"""
        selected = getattr(self._view.selector, "options" if all else "value")
        if not all and self._view.attr_field.value:
            selected = (f"{selected[0]}.{self._view.attr_field.value}",)
        options = self._view.selected.options
        self._view.selected.options = [*sorted({*options} | {*selected})]

    def _deselect(self, all=False) -> None:
        """docstring"""
        selected = getattr(self._view.selected, "options" if all else "value")
        options = self._view.selected.options
        self._view.selected.options = [*sorted({*options} - {*selected})]

    def _toggle_attr_field(self, change: dict) -> None:
        """docstring"""
        self._view.attr_field.value = ""
        self._view.attr_field.layout.display = (
            "flex"
            if len(field_names := change["new"]) == 1
            and self._model.get_field_type(field_names[0]) is dict
            else "none"
        )

    def _refresh(self, _=None) -> None:
        """docstring"""
        self._deselect(all=True)
        self._update_options()

    def _set_event_handlers(self) -> None:
        """docstring"""
        super()._set_event_handlers()
        self._view.select.on_click(lambda _: self._select())
        self._view.select_all.on_click(lambda _: self._select(all=True))
        self._view.deselect.on_click(lambda _: self._deselect())
        self._view.deselect_all.on_click(lambda _: self._deselect(all=True))
        self._view.selector.observe(self._toggle_attr_field, "value")


class QueryProjectionsModel(NodeQueryComponentModel):
    """docstring"""

    def get_field_type(self, field_name: str) -> t.Any:
        """docstring"""
        field = self.aiida.get_field(self.entry_point, field_name)
        return field.get_root_type()

    def get_fields(self) -> list[str]:
        """docstring"""
        return self.aiida.get_fields(self.entry_point)


class QueryProjectionsView(NodeQueryComponentView):
    """docstring"""

    component_type = "projection"
    expand_button_description = "project"

    def __init__(self, **kwargs) -> None:
        """docstring"""

        super().__init__(**kwargs)

        self.selector = ipw.SelectMultiple(
            layout=CSS.MULTISELECT,
        )

        self.selected = ipw.SelectMultiple(
            layout=CSS.MULTISELECT,
        )

        self.attr_field = ipw.Text(
            layout={**CSS.FLEX1, **CSS.HIDDEN},
            description="Attribute:",
        )

        self.select = ipw.Button(
            layout=CSS.BUTTON,
            icon="angle-right",
            tooltip="Select",
        )

        self.select_all = ipw.Button(
            layout=CSS.BUTTON,
            icon="angle-double-right",
            tooltip="Select all",
        )

        self.deselect = ipw.Button(
            layout=CSS.BUTTON,
            icon="angle-left",
            tooltip="Deselect",
        )

        self.deselect_all = ipw.Button(
            layout=CSS.BUTTON,
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
            ipw.HBox(
                layout={},
                children=[
                    self.attr_field,
                ],
            ),
        ]

    @property
    def state(self) -> list:
        if self.container.layout.display != "none":
            return list(self.selected.options)
        return []
