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
        self._init_view()
        self._set_event_handlers()

    def _init_view(self) -> None:
        """docstring"""
        self._view.filters = self._get_component_view("filters")
        self._view.projections = self._get_component_view("projections")
        self._view.children += (self._view.filters, self._view.projections)
        self._view.node_selector.options = self._model.aiida.get_nodes()
        self._update_relationship_options()

    def _close_view(self, _=None) -> None:
        """docstring"""
        self._view.closed = True
        self._view.close()

    def _update_relationship_options(self, _=None) -> None:
        """docstring"""
        is_group = self._view.node_selector.label == "Group"
        self._view.relationship.options = (
            GROUP_RELATIONSHIPS if is_group else NODE_RELATIONSHIPS
        )

    def _refresh(self, _=None) -> None:
        """docstring"""
        self._update_relationship_options()

    def _toggle_validity(self, _=None) -> None:
        """docstring"""
        self._view.is_valid = (
            self._view.filters.is_valid and self._view.projections.is_valid
        )

    def _get_component_view(self, type_: str) -> NodeQueryComponentView:
        """docstring"""
        view = None
        if type_ == "filters":
            model = QueryFiltersModel(self._model.aiida)
            ipw.dlink((self._model, "entry_point"), (model, "entry_point"))
            view = QueryFiltersView()
            view.observe(self._toggle_validity, "is_valid")
            _ = QueryFiltersController(model, view)
        elif type_ == "projections":
            model = QueryProjectionsModel(self._model.aiida)
            ipw.dlink((self._model, "entry_point"), (model, "entry_point"))
            view = QueryProjectionsView()
            view.observe(self._toggle_validity, "is_valid")
            _ = QueryProjectionsController(model, view)
        else:
            raise ValueError(
                f"type must be 'filters' or 'projections'; got {type_}",
            )
        return view

    def _set_event_handlers(self) -> None:
        """docstring"""
        self._view.remove.on_click(self._close_view)
        self._view.reset.on_click(self._refresh)
        self._view.node_selector.observe(
            self._update_relationship_options,
            "value",
        )
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

    closed = traitlets.Bool(False)
    is_valid = traitlets.Bool(True)

    def __init__(self, **kwargs):
        """docstring"""

        self.node_selector = ipw.Dropdown(
            layout=CSS.M2,
            style=CSS.NODE_QUERY_SELECTOR,
            description="Node:",
        )

        self.my_tag = ipw.Text(
            layout=CSS.TAG_TEXTBOX,
            style=CSS.TIGHT_DESCRIPTION,
            placeholder="tag",
        )

        self.relationship = ipw.Dropdown(
            layout=CSS.M2,
            style=CSS.NODE_QUERY_SELECTOR,
            description="with:",
        )

        self.their_tag = ipw.Text(
            layout=CSS.TAG_TEXTBOX,
            style=CSS.TIGHT_DESCRIPTION,
            placeholder="other tag",
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

        self.move_up = ipw.Button(
            layout=CSS.BUTTON,
            button_style="",
            icon="arrow-up",
            tooltip="Move up",
        )

        self.move_down = ipw.Button(
            layout=CSS.BUTTON,
            button_style="",
            icon="arrow-down",
            tooltip="Move down",
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
                                ipw.HBox(
                                    children=[
                                        self.node_selector,
                                        self.my_tag,
                                    ],
                                ),
                                ipw.HBox(
                                    children=[
                                        self.relationship,
                                        self.their_tag,
                                    ],
                                ),
                            ],
                        ),
                        ipw.VBox(
                            layout={},
                            children=[
                                ipw.HBox(
                                    layout={},
                                    children=[
                                        self.reset,
                                        self.remove,
                                    ],
                                ),
                                ipw.HBox(
                                    layout={},
                                    children=[
                                        self.move_up,
                                        self.move_down,
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
    def state(self) -> dict:
        """docstring"""
        state = {
            "node": self.node_selector.value,
            "tag": self.my_tag.value,
            "filters": self.filters.state,
            "projections": self.projections.state,
        }
        if self.relationship.value:
            state.update(
                {
                    f"with_{self.relationship.value}": self.their_tag.value,
                }
            )
        return state
