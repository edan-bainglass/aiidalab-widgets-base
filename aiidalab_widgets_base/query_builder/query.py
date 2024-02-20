from __future__ import annotations

import ipywidgets as ipw
import traitlets
from aiida import orm

from .node import NodeQueryController, NodeQueryModel, NodeQueryView
from .service import AiiDAService
from .styles import CSS


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
        view = self._get_node_query_view()
        view.observe(self._remove_node_query, "closed")
        view.move_up.on_click(lambda _: self._move_query_up(view))
        view.move_down.on_click(lambda _: self._move_query_down(view))
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

    def _move_query_up(self, node_query_view: NodeQueryView) -> None:
        """docstring"""
        views = self._view.node_queries
        index = views.index(node_query_view)
        prev_index = index - 1
        views[prev_index], views[index] = views[index], views[index - 1]
        self._view.node_queries = views

    def _move_query_down(self, node_query_view: NodeQueryView) -> None:
        """docstring"""
        views = self._view.node_queries
        index = views.index(node_query_view)
        next_index = (index + 1) % len(views)
        views[next_index], views[index] = views[index], views[next_index]
        self._view.node_queries = views

    def _submit_query(self, _=None) -> None:
        """docstring"""
        node_queries = [node.state for node in self._view.node_queries]
        self._model.submit(node_queries)

    def _notify_validity(self, _=None) -> None:
        """docstring"""
        if not self._view.is_valid:
            style = '"color: red;"'
            message = "Please correct invalid input"
            self._view.message.value = f"<span style={style}>{message}</span>"
            self._view.submit.disabled = True
        else:
            self._view.message.value = ""
            self._view.submit.disabled = False

    def _toggle_validity(self, _=None) -> None:
        """docstring"""
        self._view.is_valid = all(
            node_query.is_valid for node_query in self._view.node_queries
        )

    def _get_node_query_view(self) -> NodeQueryView:
        """docstring"""
        model = NodeQueryModel(self._model.aiida)
        view = NodeQueryView()
        view.observe(self._toggle_validity, "is_valid")
        _ = NodeQueryController(model, view)
        return view

    def _set_event_handlers(self) -> None:
        """docstring"""
        self._view.add.on_click(self._add_node_query)
        self._view.submit.on_click(self._submit_query)
        self._view.observe(self._notify_validity, "is_valid")


class QBModel(traitlets.HasTraits):
    """docstring"""

    def __init__(self, service: AiiDAService) -> None:
        """docstring"""
        self.aiida = service

    def submit(self, node_queries: list[dict]) -> None:
        """docstring"""
        query = []
        for node_query in node_queries:
            node = self.aiida.get_entry_point(node_query.pop("node"))
            args = self._process_query_args(node, node_query)
            query.append((node, args))
        self.aiida.submit(query)

    def _process_query_args(self, node: orm.Node, query: dict) -> dict:
        """docstring"""
        filters = query.pop("filters")
        projections = query.pop("projections")
        return {
            "filters": self._process_filters(node, filters),
            "project": self._process_projections(node, projections),
            **query,
        }

    def _process_filters(
        self,
        node: orm.Node,
        filters: list[dict],
    ) -> orm.QbFieldFilters:
        """docstring"""

        PRECEDENCE = {
            "and": 1,
            "or": 0,
        }

        filter_stack: list[orm.QbFieldFilters] = []
        operator_stack: list[str] = []
        opened_parentheses_count = 0

        for filter_args in filters:
            join = filter_args.pop("join")
            open_ = filter_args.pop("(")
            close_ = filter_args.pop(")")
            filter = self._process_filter(node, filter_args)

            if join:
                while operator_stack:
                    op = operator_stack[-1]
                    if op == "(" or PRECEDENCE[op] <= PRECEDENCE[join]:
                        break
                    operator_stack.pop()
                    right = filter_stack.pop()
                    left = filter_stack.pop()
                    filter_stack.append(left & right)
                operator_stack.append(join)

            if open_:
                opened_parentheses_count += 1
                operator_stack.append("(")

            filter_stack.append(filter)

            if close_:
                opened_parentheses_count -= 1
                if opened_parentheses_count < 0:
                    raise ValueError("found ) without preceding (")

                while operator_stack:
                    op = operator_stack.pop()
                    if op == "(":
                        break
                    right = filter_stack.pop()
                    left = filter_stack.pop()
                    if op == "and":
                        filter_stack.append(left & right)
                    elif op == "or":
                        filter_stack.append(left | right)
                    else:
                        raise ValueError("invalid operator")

        while operator_stack:
            op = operator_stack.pop()
            right = filter_stack.pop()
            left = filter_stack.pop()
            if op == "and":
                filter_stack.append(left & right)
            elif op == "or":
                filter_stack.append(left | right)
            else:
                raise ValueError("invalid operator")

        return filter_stack.pop()

    def _process_filter(
        self,
        node: orm.Node,
        filter: dict,
    ) -> orm.QbFieldFilters:
        """docstring"""
        field, not_, op, value = filter.values()
        qb_field = node.fields[field]
        operator = f"!{op}" if not_ else op
        if "in" in operator:
            value = f"[{value}]"
        value = self.aiida.cast_filter_value(value)
        return orm.QbFieldFilters([(qb_field, operator, value)])

    def _process_projections(self, node: orm.Node, projections: dict):
        """docstring"""
        return [node.fields[projection] for projection in projections]


class QBView(ipw.VBox):
    """docstring"""

    is_valid = traitlets.Bool(True)

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

        self.message = ipw.HTML()

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
                    layout=CSS.SPACE_BETWEEN,
                    children=[
                        self.message,
                        ipw.HBox(
                            layout={},
                            children=[
                                self.reset,
                                self.submit,
                            ],
                        ),
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
