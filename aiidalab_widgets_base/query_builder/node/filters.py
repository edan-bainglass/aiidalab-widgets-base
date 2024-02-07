from __future__ import annotations

from .component import (
    NodeQueryComponentController,
    NodeQueryComponentModel,
    NodeQueryComponentView,
)
from .filter import QueryFilterView, get_filter_view


class QueryFiltersController(NodeQueryComponentController):
    """docstring"""

    _model: QueryFiltersModel
    _view: QueryFiltersView

    def _init_view(self) -> None:
        """docstring"""
        default_filter = get_filter_view(self._model.aiida)
        default_filter.children += (default_filter.add,)
        self._view.filters = [default_filter]

    def _add_filter(self, _=None) -> None:
        """docstring"""
        self._view.filters[-1].join.disabled = False
        view = get_filter_view(self._model.aiida)
        view.children += (view.remove,)
        view.observe(self._remove_filter, "closed")
        self._view.filters = [*self._view.filters, view]

    def _remove_filter(self, trait: dict) -> None:
        """docstring"""
        view: QueryFilterView = trait["owner"]
        self._view.filters = [
            *filter(
                lambda query_div: query_div != view,
                self._view.filters,
            ),
        ]
        view.unobserve_all()
        self._view.filters[-1].join.disabled = True

    def _set_event_handlers(self) -> None:
        """docstring"""
        super()._set_event_handlers()
        self._view.filters[0].add.on_click(self._add_filter)


class QueryFiltersModel(NodeQueryComponentModel):
    """docstring"""


class QueryFiltersView(NodeQueryComponentView):
    """docstring"""

    component_type = "filters"

    @property
    def filters(self) -> list[QueryFilterView]:
        """docstring"""
        return self.content.children

    @filters.setter
    def filters(self, filters: list[QueryFilterView]) -> list[QueryFilterView]:
        """docstring"""
        self.content.children = filters
