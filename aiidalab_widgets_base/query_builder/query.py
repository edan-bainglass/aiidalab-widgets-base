from __future__ import annotations

from collections import defaultdict
from copy import deepcopy

import ipywidgets as ipw
import traitlets
from aiida import orm

from .node import NodeQueryController, NodeQueryModel, NodeQueryView
from .service import AiiDAService
from .styles import CSS

PRECEDENCE = {
    "and": 1,
    "or": 0,
}


class QBController:
    """docstring"""

    def __init__(self, model: QBModel, view: QBView) -> None:
        """docstring"""
        self._model = model
        self._view = view
        self._set_event_handlers()
        self._init_view()

    def _init_view(self, _=None) -> None:
        """docstring"""
        self._view.node_queries = []
        node_query = self._add_node_query()
        node_query.remove.layout.display = "none"
        node_query.relationship_container.layout.display = "none"

    def _add_node_query(self, _=None) -> NodeQueryView:
        """docstring"""
        view = self._get_node_query_view()
        view.their_tag.options = ["", *self._model.get_tags()]
        view.observe(self._remove_node_query, "closed")
        view.tag.observe(lambda _: self._update_tags(view), "value")
        self._view.node_queries += (view,)
        return view

    def _update_tags(self, view: NodeQueryView) -> None:
        """docstring"""
        self._update_view_tag(view)
        self._update_other_tags(view)

    def _update_view_tag(self, view: NodeQueryView) -> None:
        """docstring"""
        if self._check_tag_validity(view):
            self._model.set_tag(view.tag_key, view.tag.value)
        else:
            self._model.discard_tag(view.tag_key)

    def _update_other_tags(self, view: NodeQueryView) -> None:
        for node_query in self._view.node_queries:
            if node_query is view:
                continue
            self._update_view_tag(node_query)
            all_tags = self._model.get_tags()
            node_query_tag = node_query.tag.value if node_query.is_valid else ""
            their_tags = [tag for tag in all_tags if tag != node_query_tag]
            node_query.their_tag.options = ["", *their_tags]

    def _check_tag_validity(self, view: NodeQueryView) -> bool:
        """docstring"""
        if self._model.has_tag(view):
            view.tag.add_class("bad-text-input")
            view.has_valid_tag = False
            return False
        view.tag.remove_class("bad-text-input")
        view.has_valid_tag = True
        return True

    def _remove_node_query(self, trait: dict) -> NodeQueryView:
        """docstring"""
        view: NodeQueryView = trait["owner"]
        self._model.discard_tag(view.tag_key)
        self._update_other_tags(view)
        self._view.node_queries = [
            *filter(
                lambda node_query: node_query != view,
                self._view.node_queries,
            ),
        ]
        view.unobserve_all()
        self._toggle_validity()
        return view

    def _submit_query(self, _=None) -> None:
        """docstring"""
        try:
            state = deepcopy(self._view.state)
            self._model.submit(state)
        except Exception:
            self._notify_validity(message="Query failed to submit")

    def _notify_validity(self, _=None, message: str = "") -> None:
        """docstring"""
        if not self._view.is_valid or message:
            style = '"color: red;"'
            message = message or "Please correct invalid input"
            self._view.message.value = f"<span style={style}>{message}</span>"
        else:
            self._view.message.value = ""

    def _toggle_validity(self, _=None) -> None:
        """docstring"""
        self._view.is_valid = all(
            node_query.is_valid
            for node_query in self._view.node_queries
            if node_query.is_valid != None  # noqa: E711
        )

    def _get_node_query_view(self) -> NodeQueryView:
        """docstring"""
        model = NodeQueryModel(self._model.aiida)
        view = NodeQueryView()
        view.observe(self._toggle_validity, "is_valid")
        view.observe(self._update_state, "state")
        _ = NodeQueryController(model, view)
        return view

    def _toggle_code_view(self, _=None) -> None:
        """docstring"""
        self._view.code_view.clear_output()
        if self._view.code_view.layout.display == "none":
            self._display_qb()
            self._view.code_view.layout.display = "block"
        else:
            self._view.code_view.layout.display = "none"

    def _display_qb(self) -> None:
        """docstring"""
        with self._view.code_view:
            state = deepcopy(self._view.state)
            code = self._model.get_query_builder_string(state)
            print(code)

    def _refresh_code_view(self, _=None) -> None:
        """docstring"""
        self._view.code_view.clear_output()
        self._display_qb()

    def _close_code_view(self, _=None) -> None:
        """docstring"""
        self._view.code_view.clear_output()
        if self._view.toggle_code_view.disabled:
            self._view.code_view.layout.display = "none"

    def _refresh(self, _=None) -> None:
        """docstring"""
        self._view.node_queries = self._view.node_queries[:1]
        self._view.node_queries[0].reset_trigger += 1

    def _update_state(self, _=None) -> None:
        """docstring"""
        self._view.state = [
            query.state for query in self._view.node_queries if query.is_valid
        ]
        self._refresh_code_view()

    def _set_event_handlers(self) -> None:
        """docstring"""
        self._view.add.on_click(self._add_node_query)
        self._view.toggle_code_view.on_click(self._toggle_code_view)
        self._view.toggle_code_view.observe(self._close_code_view, "disabled")
        self._view.reset.on_click(self._refresh)
        self._view.submit.on_click(self._submit_query)
        self._view.observe(self._notify_validity, "is_valid")
        ipw.dlink(
            (self._view, "is_valid"),
            (self._view.submit, "disabled"),
            lambda valid: not valid,
        )
        ipw.dlink(
            (self._view.submit, "disabled"),
            (self._view.toggle_code_view, "disabled"),
        )


class QBModel(traitlets.HasTraits):
    """docstring"""

    _tags = {}
    results = traitlets.List([])

    def __init__(self, service: AiiDAService) -> None:
        """docstring"""
        self.aiida = service

    def get_query_builder_string(self, node_queries: list[dict]) -> str:
        """docstring"""
        query, _ = self._build_query(node_queries)
        code = "QueryBuilder()"
        for item in query:
            args: dict
            node, args = item
            code += ".append(\n"
            code += f"    {node.__name__},\n"
            for key, value in args.items():
                if not value:
                    continue
                if key == "filters":
                    filters: orm.fields.QbFieldFilters = value
                    code += f"    filters={filters.as_dict()},\n"
                elif key == "project":
                    projections: list[orm.QbField] = value
                    keys = [proj.backend_key for proj in projections]
                    code += f"    project={keys},\n"
                elif isinstance(value, str):
                    code += f"    {key}='{value}',\n"
                else:
                    code += f"    {key}={value},\n"
            code += ")"
        return code

    def submit(self, node_queries: list[dict]) -> None:
        """docstring"""
        query, projections = self._build_query(node_queries)
        results = [projections, self.aiida.get_results(query)]
        self.results = results

    def has_tag(self, view: NodeQueryView) -> bool:
        """docstring"""
        return any(
            tag == view.tag.value and key != view.tag_key
            for key, tag in self._tags.items()
        )

    def set_tag(self, key: str, tag: str) -> None:
        """docstring"""
        if tag:
            self._tags[key] = tag
        else:
            self.discard_tag(key)

    def discard_tag(self, key: str) -> None:
        """docstring"""
        if key in self._tags:
            del self._tags[key]

    def get_tags(self) -> list[str]:
        """docstring"""
        return list(self._tags.values())

    def _build_query(self, node_queries: list[dict]) -> tuple[list, dict]:
        """docstring"""
        query: list[tuple[orm.Node, dict]] = []
        projections: dict[str, list] = defaultdict(lambda: [])
        for node_query in node_queries:
            entry_point = node_query.pop("node")
            node = self.aiida.get_entry_point(entry_point)
            node_type = node.entry_point.attr
            args = self._process_query_args(node, node_query)
            if "project" in args:
                projections[node_type].extend(
                    [
                        p.key
                        for p in args["project"]
                        if p.key not in projections[node_type]
                    ]
                )
            query.append((node, args))
        return query, projections or {node_type: ["node"]}

    def _process_query_args(self, node: orm.Node, query: dict) -> dict:
        """docstring"""
        filters = query.pop("filters")
        projections = query.pop("projections")
        if filters:
            query.update(
                {
                    "filters": self._process_filters(node, filters),
                },
            )
        if projections:
            query.update(
                {
                    "project": self._process_projections(node, projections),
                }
            )
        return query

    def _process_filters(
        self,
        node: orm.Node,
        filters: list[dict],
    ) -> orm.QbFieldFilters:
        """docstring"""

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
        key: str
        key, not_, op, value = filter.values()
        if "." in key:
            field, attribute = key.split(".", maxsplit=1)
            field = node.fields[field][attribute]
        else:
            field = node.fields[key]
        operator = f"!{op}" if not_ else op
        if "in" in operator:
            value = f"[{value}]"
        value = self.aiida.cast_filter_value(value)
        return orm.QbFieldFilters([(field, operator, value)])

    def _process_projections(
        self,
        node: orm.Node,
        projections: list[str],
    ) -> list[orm.QbField]:
        """docstring"""
        processed = []
        for projection in projections:
            if "." in projection:
                field, attribute = projection.split(".", maxsplit=1)
                processed.append(node.fields[field][attribute])
            else:
                processed.append(node.fields[projection])
        return processed


class QBView(ipw.VBox):
    """docstring"""

    is_valid = traitlets.Bool()
    state = traitlets.List([])

    def __init__(self, **kwargs) -> None:
        """docstring"""

        self.node_queries_container = ipw.VBox()

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
                self.node_queries_container,
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
                self.code_view,
            ],
            **kwargs,
        )

    def _build_controls_div(self) -> ipw.VBox:
        """docstring"""

        self.toggle_code_view = ipw.Button(
            layout=CSS.WFIT,
            button_style="primary",
            icon="code",
            tooltip="Show code",
            disabled=True,
        )

        self.code_view = ipw.Output(
            layout={
                "margin": "5px 2px 2px 2px",
                "padding": "5px",
                "border": "1px solid #D3D3D3",
                "display": "none",
            }
        )

        self.message = ipw.HTML(layout=CSS.MX5)

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
            disabled=True,
        )

        return ipw.VBox(
            layout={},
            children=[
                ipw.HBox(
                    layout=CSS.SPACE_BETWEEN,
                    children=[
                        ipw.HBox(
                            layout={},
                            children=[
                                self.toggle_code_view,
                                self.message,
                            ],
                        ),
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
        return list(self.node_queries_container.children)

    @node_queries.setter
    def node_queries(self, queries=list[NodeQueryView]) -> None:
        """docstring"""
        self.node_queries_container.children = queries
