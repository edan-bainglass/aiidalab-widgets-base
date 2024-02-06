from __future__ import annotations

import ipywidgets as ipw
import traitlets

from ..styles import CSS


def get_filter_view():
    """docstring"""
    model = QueryFilterModel()
    view = QueryFilterView()
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
        self._set_event_handlers()

    def _close_view(self, _=None) -> None:
        """docstring"""
        self._view.closed = True
        self._view.close()

    def _set_event_handlers(self) -> None:
        """docstring"""
        self._view.remove.on_click(self._close_view)


class QueryFilterModel(traitlets.HasTraits):
    """docstring"""


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

        self.attribute = ipw.Dropdown(
            layout=CSS.W50,
        )

        self.operator = ipw.Dropdown(
            layout=CSS.WAUTO,
            options=OPERATORS,
        )

        self.argument = ipw.Text(
            layout=CSS.W50,
        )

        self.join = ipw.Dropdown(
            layout=CSS.WAUTO,
            options=JOINS,
            value="",
            disabled=True,
        )

        self.form = ipw.HBox(
            layout=CSS.FLEX1,
            children=[
                self.attribute,
                self.operator,
                self.argument,
                self.join,
            ],
        )

        super().__init__(
            layout={},
            children=[
                self.form,
            ],
            **kwargs,
        )


JOINS = [
    "",
    "and",
    "or",
    "(or)",
]

OPERATORS = [
    "",
    "==",
    "in",
    ">",
    "<",
    "<=",
    ">=",
    "like",
    "ilike",
    "or",
    "and",
    "has_key",
    "of_type",
    "of_length",
    "shorter",
    "longer",
    "contains",
]
