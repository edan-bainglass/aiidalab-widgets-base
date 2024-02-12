from __future__ import annotations

import typing as t

import ipywidgets as ipw
import traitlets

from ..service import AiiDAService, OPERATORS, JOINS
from ..styles import CSS

if t.TYPE_CHECKING:
    from .filters import QueryFiltersModel


def get_filter_view(filters_model: QueryFiltersModel) -> QueryFilterView:
    """docstring"""
    model = QueryFilterModel(filters_model.aiida)
    view = QueryFilterView()
    ipw.dlink((filters_model, "entry_point"), (model, "entry_point"))
    _ = QueryFilterController(model, view)
    return view


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
        fields = self._model.aiida.get_fields(self._model.entry_point)
        self._view.field.options = fields

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
            options=JOINS,
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
            layout=CSS.WAUTO,
            options=OPERATORS,
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
