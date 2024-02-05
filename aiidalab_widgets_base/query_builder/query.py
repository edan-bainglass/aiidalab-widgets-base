from __future__ import annotations

import ipywidgets as ipw
import traitlets

from .service import AiiDAService
from .styles import CSS
from .table import TableQueryView, get_table_query_view


def get_query_view():
    """docstring"""
    model = QBModel(service=AiiDAService())
    view = QBView()
    _ = QBController(model, view)
    return view


class QBController:
    """docstring"""

    def __init__(self, model: QBModel, view: QBView) -> None:
        """docstring"""
        self._model = model
        self._view = view
        self._set_event_handlers()
        self._add_table_query()

    def _add_table_query(self, _=None) -> None:
        """docstring"""
        view = get_table_query_view()
        view.observe(self._remove_table_query, "closed")
        self._view.queries_div.children += (view,)

    def _remove_table_query(self, trait: dict) -> None:
        """docstring"""
        view: TableQueryView = trait["owner"]
        self._view.queries_div.children = (
            *filter(
                lambda query_div: query_div != view,
                self._view.queries_div.children,
            ),
        )
        view.unobserve_all()

    def _set_event_handlers(self) -> None:
        """docstring"""
        self._view.add.on_click(self._add_table_query)


class QBModel(traitlets.HasTraits):
    """docstring"""

    def __init__(self, service: AiiDAService) -> None:
        """docstring"""
        self._aiida = service


class QBView(ipw.VBox):
    """docstring"""

    def __init__(self, **kwargs) -> None:
        """docstring"""

        self.queries_div = ipw.VBox()

        self.add = ipw.Button(
            layout={
                **CSS.BUTTON,
                **CSS.CENTERED,
            },
            button_style="",
            icon="plus",
            tooltip="Add table query",
        )

        super().__init__(
            children=[
                self.queries_div,
                ipw.VBox(
                    layout={
                        **CSS.PY5,
                        **CSS.CENTERED,
                    },
                    children=[
                        self.add,
                    ],
                ),
                self._build_controls_div(),
            ],
            **kwargs,
        )

    def _build_controls_div(self) -> ipw.VBox:
        """docstring"""

        self.reset = ipw.Button(
            layout=CSS.BUTTON,
            button_style="danger",
            icon="refresh",
            tooltip="Reset query",
        )

        self.submit = ipw.Button(
            layout=CSS.BUTTON,
            button_style="success",
            icon="check",
            tooltip="Submit query",
        )

        return ipw.VBox(
            layout={},
            children=[
                ipw.HBox(
                    layout=CSS.FLOAT_RIGHT,
                    children=[
                        self.reset,
                        self.submit,
                    ],
                ),
            ],
        )
