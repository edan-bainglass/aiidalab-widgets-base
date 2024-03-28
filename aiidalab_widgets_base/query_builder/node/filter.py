from __future__ import annotations

import typing as t

import ipywidgets as ipw
import traitlets

from ..service import AiiDAService
from ..styles import CSS


class QueryFilterController:
    """docstring"""

    def __init__(
        self,
        model: QueryFilterModel,
        view: QueryFilterView,
    ) -> None:
        """docstring"""
        self._model = model
        self._view = view
        self._set_event_handlers()
        self._init_view()

    def _init_view(self) -> None:
        """docstring"""
        self._view.field.options = self._model.get_fields()
        if "pk" in self._view.field.options:
            self._view.field.value = "pk"

    def _close_view(self, _=None) -> None:
        """docstring"""
        self._view.closed = True
        self._view.close()

    def _validate(self, _=None) -> None:
        """docstring"""
        if self._view.argument.value:
            state = self._view.state_of_filter
            self._view.is_valid = self._model.validate(state)
            if not self._view.is_valid:
                self._view.argument.add_class("bad-text-input")
            else:
                self._view.argument.remove_class("bad-text-input")
        else:
            self._view.is_valid = True
            self._view.argument.remove_class("bad-text-input")

    def _toggle_attr_field(self, change: dict) -> None:
        """docstring"""
        field_name = change["new"]
        if field_name and self._model.get_field_type(field_name) is dict:
            self._view.attr_field.layout.display = "flex"
        else:
            self._view.attr_field.layout.display = "none"

    def _toggle_validation_notice(self, change: dict) -> None:
        """docstring"""
        if change["new"]:
            self._view.validation_info.layout.display = "inline-block"
        else:
            self._view.validation_info.layout.display = "none"

    def _refresh(self, _=None) -> None:
        """docstring"""
        self._init_view()

    def _update_operators(self, change: dict) -> None:
        """docstring"""
        self._view.operator.options = self._model.get_operators(change["new"])
        self._view.operator.value = "=="
        self._view.argument.value = ""

    def _refresh_all(self, _=None) -> None:
        """docstring"""
        self._refresh()
        self._view.join.value = "and" if self._view.join.value is not None else None
        self._view.open_.value = False
        self._view.not_.value = False
        self._view.close_.value = False

    def _set_event_handlers(self) -> None:
        """docstring"""
        self._view.remove.on_click(self._close_view)
        self._view.argument.observe(self._validate, "value")
        self._view.field.observe(self._update_operators, "value")
        self._view.field.observe(self._toggle_attr_field, "value")
        self._view.attr_field.observe(self._toggle_validation_notice, "value")
        self._view.observe(self._refresh_all, "reset_trigger")
        self._model.observe(self._refresh, "entry_point")


class QueryFilterModel(traitlets.HasTraits):
    """docstring"""

    entry_point = traitlets.Unicode("")

    def __init__(self, service: AiiDAService) -> None:
        """docstring"""
        self.aiida = service

    def get_field_type(self, field_name: str) -> t.Any:
        """docstring"""
        field = self.aiida.get_field(self.entry_point, field_name)
        return field.get_root_type()

    def get_fields(self) -> list[str]:
        """docstring"""
        if self.entry_point:
            return self.aiida.get_fields(self.entry_point)
        else:
            return [""]

    def get_operators(self, field: str) -> list[str]:
        """docstring"""
        if self.entry_point:
            return self.aiida.get_operators(self.entry_point, field)
        else:
            return ["==", "in"]

    def validate(self, filter_args: dict) -> bool:
        """docstring"""
        return self.aiida.validate_filter(self.entry_point, filter_args)


class QueryFilterView(ipw.HBox):
    """docstring"""

    reset_trigger = traitlets.Int(0)
    closed = traitlets.Bool(False)
    is_valid = traitlets.Bool(True)

    def __init__(self, **kwargs):
        """docstring"""

        self.remove = ipw.Button(
            layout={"width": "41px"},
            button_style="danger",
            icon="trash",
            tooltip="Remove filter",
        )

        self.join = ipw.Dropdown(
            layout=CSS.WAUTO,
            options=("and", "or"),
            value="and",
        )

        self.open_ = ipw.ToggleButton(
            layout=CSS.BUTTON,
            description="(",
            value=False,
        )

        self.field = ipw.Dropdown(
            layout=CSS.FLEX1,
            options=[""],
        )

        self.attr_field = ipw.Text(
            layout={**CSS.FLEX1, **CSS.HIDDEN},
            placeholder="attribute",
        )

        self.validation_info = ipw.HTML(
            layout={**CSS.MX5, **CSS.HIDDEN},
            value="<i class='fa fa-info' title='Validation is turned off for attribute fields'></i>",
        )

        self.not_ = ipw.ToggleButton(
            layout={"width": "50px"},
            style=CSS.TIGHT_DESCRIPTION,
            description="not",
            value=False,
        )

        self.operator = ipw.Dropdown(
            layout=CSS.OPERATOR_SELECTOR,
            options=["==", "in"],
            default="==",
        )

        self.argument = ipw.Text(
            layout=CSS.FLEX1,
            placeholder="value",
        )

        self.close_ = ipw.ToggleButton(
            layout=CSS.BUTTON,
            description=")",
            value=False,
        )

        self.form = ipw.HBox(
            layout=CSS.FLEX1,
            children=[
                self.join,
                self.open_,
                ipw.HBox(
                    layout=CSS.W50,
                    children=[
                        self.field,
                        self.attr_field,
                    ],
                ),
                self.not_,
                self.operator,
                ipw.HBox(
                    layout=CSS.W50,
                    children=[
                        self.argument,
                        self.validation_info,
                    ],
                ),
                self.close_,
                self.remove,
            ],
        )

        super().__init__(
            layout={},
            children=[
                self.form,
            ],
            **kwargs,
        )

    @property
    def state_of_filter(self) -> dict:
        """docstring"""
        return {
            "field": self.field.label,
            "not": self.not_.value,
            "operator": self.operator.value,
            "argument": self.argument.value,
        }

    @property
    def state(self) -> dict:
        """docstring"""
        state = self.state_of_filter
        state.update(
            {
                "join": self.join.value,
                "(": self.open_.value,
                ")": self.close_.value,
            }
        )
        return state
