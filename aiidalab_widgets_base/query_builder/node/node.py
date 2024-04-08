from __future__ import annotations

import ipywidgets as ipw
import traitlets

from ..service import GROUP_RELATIONSHIPS, NODE_RELATIONSHIPS, AiiDAService
from ..styles import CSS
from .component import NodeQueryComponentView
from .filters import QueryFiltersController, QueryFiltersModel, QueryFiltersView
from .projections import (
    QueryProjectionsController,
    QueryProjectionsModel,
    QueryProjectionsView,
)


class NodeQueryController:
    """docstring"""

    def __init__(self, model: NodeQueryModel, view: NodeQueryView) -> None:
        """docstring"""
        self._model = model
        self._view = view
        self._set_event_handlers()
        self._init_view()

    def _init_view(self) -> None:
        """docstring"""
        self._view.filters = self._get_component_view("filters")
        self._view.projections = self._get_component_view("projections")
        self._view.children += (self._view.filters, self._view.projections)
        self._view.node_selector.options = [("", ""), *self._model.aiida.get_nodes()]
        self._update_relationship_options()

    def _close_view(self, _=None) -> None:
        """docstring"""
        self._view.closed = True
        self._view.close()

    def _on_value_change(self, _=None) -> None:
        """docstring"""
        self._toggle_validity()
        self._update_relationship_options()

    def _update_relationship_options(self, _=None) -> None:
        """docstring"""
        is_group = self._view.node_selector.label == "Group"
        relationships = GROUP_RELATIONSHIPS if is_group else NODE_RELATIONSHIPS
        self._view.relationship.options = ["", *relationships]

    def _refresh(self, _=None) -> None:
        """docstring"""
        self._view.node_selector.value = ""
        self._view.tag.value = ""
        self._view.their_tag.value = ""
        self._view.relationship.value = ""
        self._view.filters.collapse.click()
        self._view.projections.collapse.click()

    def _has_valid_node(self) -> bool:
        """docstring"""
        if not self._view.node_selector.value:
            self._view.node_selector.add_class("bad-dropdown-input")
            return False
        self._view.node_selector.remove_class("bad-dropdown-input")
        return True

    def _has_filters(self) -> bool:
        """docstring"""
        return len(self._view.filters.state) > 0

    def _has_valid_filters(self) -> bool:
        """docstring"""
        has_valid_filters = bool(self._view.filters.is_valid)
        return has_valid_filters if self._has_filters() else True

    def _has_projections(self) -> bool:
        """docstring"""
        return len(self._view.projections.state) > 0

    def _has_valid_projections(self) -> bool:
        """docstring"""
        has_valid_projections = bool(self._view.projections.is_valid)
        return has_valid_projections if self._has_projections() else True

    def _toggle_validity(self, _=None) -> None:
        """docstring"""
        self._view.is_valid = (
            self._has_valid_node()
            and self._view.has_valid_tag
            and self._has_valid_filters()
            and self._has_valid_projections()
        )

    def _update_state(self, _=None) -> None:
        """docstring"""
        state = {
            "node": self._view.node_selector.value,
            "tag": self._view.tag.value,
            "filters": self._view.filters.state,
            "projections": self._view.projections.state,
        }
        if self._view.relationship.value:
            state.update(
                {
                    f"with_{self._view.relationship.value}": self._view.their_tag.value,
                }
            )
        self._view.state = state

    def _get_component_view(self, type_: str) -> NodeQueryComponentView:
        """docstring"""
        view = None
        if type_ == "filters":
            model = QueryFiltersModel(self._model.aiida)
            ipw.dlink((self._model, "entry_point"), (model, "entry_point"))
            view = QueryFiltersView()
            _ = QueryFiltersController(model, view)
        elif type_ == "projections":
            model = QueryProjectionsModel(self._model.aiida)
            ipw.dlink((self._model, "entry_point"), (model, "entry_point"))
            view = QueryProjectionsView()
            _ = QueryProjectionsController(model, view)
        else:
            raise ValueError(
                f"type must be 'filters' or 'projections'; got {type_}",
            )
        view.observe(self._toggle_validity, "is_valid")
        view.observe(self._update_state, "state")
        return view

    def _set_event_handlers(self) -> None:
        """docstring"""
        self._view.remove.on_click(self._close_view)
        self._view.reset.on_click(self._refresh)
        self._view.node_selector.observe(self._on_value_change, "value")
        self._view.observe(self._refresh, "reset_trigger")
        self._view.observe(self._toggle_validity, "has_valid_tag")

        for item in self._view.__dict__.values():
            if isinstance(item, ipw.ValueWidget):
                item.observe(self._update_state, "value")

        ipw.dlink(
            (self._view.node_selector, "value"),
            (self._model, "entry_point"),
        )


class NodeQueryModel(traitlets.HasTraits):
    """docstring"""

    entry_point = traitlets.Unicode("")

    def __init__(self, service: AiiDAService) -> None:
        """docstring"""
        self.aiida = service


class NodeQueryView(ipw.VBox):
    """docstring"""

    reset_trigger = traitlets.Int(0)
    closed = traitlets.Bool(False)
    is_valid = traitlets.Bool()
    has_valid_tag = traitlets.Bool(True)
    state = traitlets.Dict({})

    def __init__(self, **kwargs):
        """docstring"""

        self.node_selector = ipw.Dropdown(
            layout=CSS.M2,
            style=CSS.NODE_QUERY_SELECTOR,
            description="Node:",
            options=[("", "")],
        )

        self.tag = ipw.Text(
            layout=CSS.TAG_INPUTBOX,
            style=CSS.TIGHT_DESCRIPTION,
            placeholder="tag",
        )

        self.relationship = ipw.Dropdown(
            layout=CSS.M2,
            style=CSS.NODE_QUERY_SELECTOR,
            description="with:",
            options=[""],
        )

        self.their_tag = ipw.Dropdown(
            layout=CSS.TAG_INPUTBOX,
            style=CSS.TIGHT_DESCRIPTION,
            options=[""],
        )

        self.their_tag_info = ipw.HTML(
            layout=CSS.MX5,
            value="<i class='fa fa-info' title='Choose other tag'></i>",
        )

        self.reset = ipw.Button(
            layout=CSS.BUTTON,
            button_style="warning",
            icon="refresh",
            tooltip="Reset node query",
        )

        self.remove = ipw.Button(
            layout=CSS.BUTTON,
            button_style="danger",
            icon="times",
            tooltip="Remove query",
        )

        self.node_selection_container = ipw.HBox(
            children=[
                self.node_selector,
                self.tag,
            ],
        )

        self.relationship_container = ipw.HBox(
            children=[
                self.relationship,
                self.their_tag,
                self.their_tag_info,
            ],
        )

        self.filters: QueryFiltersView
        self.projections: QueryProjectionsView

        super().__init__(
            layout=CSS.BORDERED_BOX,
            children=[
                ipw.HBox(
                    layout={},
                    children=[
                        ipw.VBox(
                            layout=CSS.FLEX1,
                            children=[
                                self.node_selection_container,
                                self.relationship_container,
                            ],
                        ),
                        ipw.VBox(
                            layout={},
                            children=[
                                ipw.VBox(
                                    layout={},
                                    children=[
                                        self.remove,
                                        self.reset,
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
            **kwargs,
        )

    @property
    def tag_key(self) -> str:
        return str(id(self))
