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
        self._init_view()
        self._set_event_handlers()

    def _init_view(self) -> None:
        """docstring"""
        self._update_field_options()

    def _close_view(self, _=None) -> None:
        """docstring"""
        self._view.closed = True
        self._view.close()

    def _update_field_options(self):
        """docstring"""
        self._view.silent = True
        self._view.field.options = self._model.get_fields()
        self._view.silent = False
        if "pk" in self._view.field.options:
            self._view.field.value = "pk"
            self._view.operator.value = "=="
            self._view.argument.value = ""

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

    def _on_field_change(self, change: dict) -> None:
        """docstring"""
        if not self._view.silent:
            self._update_operators(change)
            self._toggle_attr_field(change)
            self._update_state(change)

    def _update_operators(self, _=None, is_attr=False) -> None:
        """docstring"""
        field = self._view.field.value
        self._view.operator.options = self._model.get_operators(field, is_attr)
        self._view.operator.value = "=="
        self._view.argument.value = ""

    def _toggle_attr_field(self, change: dict) -> None:
        """docstring"""
        self._view.attr_field.value = ""
        self._view.attr_field.layout.display = (
            "flex"
            if (field_name := change["new"])
            and self._model.get_field_type(field_name) is dict
            else "none"
        )

    def _toggle_attr_field_rules(self, change: dict) -> None:
        """docstring"""
        has_attr_field = bool(change["new"])
        self._toggle_validation_notice(has_attr_field)
        self._update_operators(is_attr=has_attr_field)
        self._model._needs_validation = not has_attr_field
        self._validate()

    def _toggle_validation_notice(self, has_attr_field_value: str) -> None:
        """docstring"""
        if has_attr_field_value:
            self._view.validation_info.layout.display = "inline-block"
        else:
            self._view.validation_info.layout.display = "none"

    def _refresh(self, _=None) -> None:
        """docstring"""
        self._update_field_options()

    def _refresh_all(self, _=None) -> None:
        """docstring"""
        self._refresh()
        self._view.join.value = "and" if self._view.join.value is not None else None
        self._view.open_.value = False
        self._view.not_.value = False
        self._view.close_.value = False

    def _update_state(self, _=None) -> None:
        """docstring"""
        self._view.state = {
            **self._view.state_of_filter,
            "join": self._view.join_value,
            "(": self._view.open_.value,
            ")": self._view.close_.value,
        }

    def _set_event_handlers(self) -> None:
        """docstring"""
        self._view.remove.on_click(self._close_view)
        self._view.argument.observe(self._validate, "value")
        self._view.field.observe(self._on_field_change, "value")
        self._view.attr_field.observe(self._toggle_attr_field_rules, "value")
        self._view.observe(self._refresh_all, "reset_trigger")
        self._model.observe(self._refresh, "entry_point")

        for attr in (
            "join",
            "open_",
            "attr_field",
            "not_",
            "operator",
            "argument",
            "close_",
        ):
            widget: ipw.ValueWidget = getattr(self._view, attr)
            widget.observe(self._update_state, "value")

        ipw.dlink(
            (self._view.field, "value"),
            (self._view.argument, "disabled"),
            lambda value: value == "",  # argument disabled if no field
        )


class QueryFilterModel(traitlets.HasTraits):
    """docstring"""

    entry_point = traitlets.Unicode("")

    _needs_validation = True

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
        return [""]

    def get_operators(self, field: str, is_attr: bool = False) -> list[str]:
        """docstring"""
        if self.entry_point:
            return self.aiida.get_operators(self.entry_point, field, is_attr)
        return ["==", "in"]

    def validate(self, filter_args: dict) -> bool:
        """docstring"""
        if self._needs_validation:
            return self.aiida.validate_filter(self.entry_point, filter_args)
        return True


class QueryFilterView(ipw.HBox):
    """docstring"""

    reset_trigger = traitlets.Int(0)
    closed = traitlets.Bool(False)
    is_valid = traitlets.Bool(True)
    state = traitlets.Dict({})

    silent = False

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
            value="""
                <i
                    class="fa fa-info"
                    title="No validation for dictionary fields"
                ></i>
            """,
        )

        self.not_ = ipw.ToggleButton(
            layout={"width": "50px"},
            style=CSS.TIGHT_DESCRIPTION,
            description="not",
            value=False,
        )

        self.operator = ipw.Dropdown(
            layout={"width": "10%"},
            options=["==", "in"],
            default="==",
        )

        self.argument = ipw.Text(
            layout=CSS.FLEX1,
            placeholder="value",
            disabled=True,
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
                    layout={"width": "40%"},
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
            "field": self._field,
            "not": self.not_.value,
            "operator": self.operator.value,
            "argument": self.argument.value,
        }

    @property
    def _field(self):
        """docstring"""
        return (
            self.field.value
            if not self.attr_field.value
            else f"{self.field.value}.{self.attr_field.value}"
        )

    @property
    def join_value(self):
        """docstring"""
        return None if self.join.layout.visibility == "hidden" else self.join.value
