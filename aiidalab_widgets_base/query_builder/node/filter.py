from __future__ import annotations

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
        self._view.field.options = self._model.get_fields()
        field = self._view.field.value
        self._view.operator.options = self._model.get_operators(field)

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

    def _refresh(self, _=None) -> None:
        """docstring"""
        self._init_view()
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
        self._view.field.observe(self._refresh, "value")


class QueryFilterModel(traitlets.HasTraits):
    """docstring"""

    entry_point = traitlets.Unicode("")

    def __init__(self, service: AiiDAService) -> None:
        """docstring"""
        self.aiida = service

    def get_fields(self) -> list[str]:
        """docstring"""
        return self.aiida.get_fields(self.entry_point)

    def get_operators(self, field: str) -> list[str]:
        """docstring"""
        return self.aiida.get_operators(self.entry_point, field)

    def validate(self, filter_args: dict) -> bool:
        """docstring"""
        return self.aiida.validate_filter(self.entry_point, filter_args)


class QueryFilterView(ipw.HBox):
    """docstring"""

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
            layout=CSS.W50,
        )

        self.not_ = ipw.ToggleButton(
            layout={"width": "50px"},
            style=CSS.TIGHT_DESCRIPTION,
            description="not",
            value=False,
        )

        self.operator = ipw.Dropdown(
            layout=CSS.OPERATOR_SELECTOR,
            default="==",
        )

        self.argument = ipw.Text(
            layout=CSS.W50,
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
                self.field,
                self.not_,
                self.operator,
                self.argument,
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
