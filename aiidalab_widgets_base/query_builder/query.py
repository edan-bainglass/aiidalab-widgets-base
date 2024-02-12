from __future__ import annotations

import ipywidgets as ipw
import traitlets

from .service import AiiDAService
from .styles import CSS
from .node import NodeQueryView, get_node_query_view


def get_query_view(service: AiiDAService) -> QBView:
    """docstring"""
    model = QBModel(service)
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
        self._add_node_query()

    def _add_node_query(self, _=None) -> None:
        """docstring"""
        view = get_node_query_view(self._model.aiida)
        view.observe(self._remove_node_query, "closed")
        self._view.node_queries += (view,)

    def _remove_node_query(self, trait: dict) -> None:
        """docstring"""
        view: NodeQueryView = trait["owner"]
        self._view.node_queries = [
            *filter(
                lambda node_query: node_query != view,
                self._view.node_queries,
            ),
        ]
        view.unobserve_all()

    def _set_event_handlers(self) -> None:
        """docstring"""
        self._view.add.on_click(self._add_node_query)


class QBModel(traitlets.HasTraits):
    """docstring"""

    def __init__(self, service: AiiDAService) -> None:
        """docstring"""
        self.aiida = service


class QBView(ipw.VBox):
    """docstring"""

    def __init__(self, **kwargs) -> None:
        """docstring"""

        self.node_queries_div = ipw.VBox()

        self.add = ipw.Button(
            layout={
                **CSS.BUTTON,
                **CSS.CENTERED,
            },
            button_style="",
            icon="plus",
            tooltip="Add node query",
        )

        super().__init__(
            children=[
                self.node_queries_div,
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
            button_style="warning",
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

    @property
    def node_queries(self) -> list[NodeQueryView]:
        """docstring"""
        return list(self.node_queries_div.children)

    @node_queries.setter
    def node_queries(self, queries=list[NodeQueryView]) -> None:
        """docstring"""
        self.node_queries_div.children = queries
