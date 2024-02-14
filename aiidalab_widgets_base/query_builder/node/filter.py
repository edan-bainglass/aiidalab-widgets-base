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

    def _set_event_handlers(self) -> None:
        """docstring"""
        self._view.remove.on_click(self._close_view)


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

class QueryFilterView(ipw.HBox):
    """docstring"""

    closed = traitlets.Bool(False)

    def __init__(self, **kwargs):
        """docstring"""

        self.add = ipw.Button(
            layout=CSS.BUTTON,
            button_style="",
            icon="plus",
            tooltip="Add filter",
        )

        self.remove = ipw.Button(
            layout=CSS.BUTTON,
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
    def state(self) -> dict:
        """docstring"""
        return {
            "join": self.join.value,
            "(": self.open_.value,
            "field": self.field.value,
            "not": self.not_.value,
            "operator": self.operator.value,
            "argument": self.argument.value,
            ")": self.close_.value,
        }
