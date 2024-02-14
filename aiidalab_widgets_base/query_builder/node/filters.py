from __future__ import annotations

import ipywidgets as ipw

from .component import (
    NodeQueryComponentController,
    NodeQueryComponentModel,
    NodeQueryComponentView,
)
from .filter import QueryFilterController, QueryFilterModel, QueryFilterView


class QueryFiltersController(NodeQueryComponentController):
    """docstring"""

    _model: QueryFiltersModel
    _view: QueryFiltersView

    def _init_view(self) -> None:
        """docstring"""
        default_filter = self._get_filter_view()
        default_filter.join.value = None
        default_filter.join.layout.visibility = "hidden"
        default_filter.children += (default_filter.add,)
        default_filter.add.on_click(self._add_filter)
        self._view.filters = [default_filter]

    def _add_filter(self, _=None) -> None:
        """docstring"""
        view = self._get_filter_view()
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

    def _refresh(self, _=None) -> None:
        """docstring"""
        self._init_view()

    def _toggle_validity(self, _=None) -> None:
        """docstring"""
        self._view.is_valid = all(
            filter.is_valid for filter in self._view.filters if filter.argument.value
        )

    def _get_filter_view(self) -> QueryFilterView:
        """docstring"""
        model = QueryFilterModel(self._model.aiida)
        ipw.dlink((self._model, "entry_point"), (model, "entry_point"))
        view = QueryFilterView()
        view.observe(self._toggle_validity, "is_valid")
        _ = QueryFilterController(model, view)
        return view


class QueryFiltersModel(NodeQueryComponentModel):
    """docstring"""


class QueryFiltersView(NodeQueryComponentView):
    """docstring"""

    component_type = "filters"
    expand_button_description = "filter"

    @property
    def filters(self) -> list[QueryFilterView]:
        """docstring"""
        return list(self.content.children)

    @filters.setter
    def filters(self, filters: list[QueryFilterView]) -> None:
        """docstring"""
        self.content.children = filters

    @property
    def state(self) -> list:
        if self.container.layout.display == "none":
            return []
        return [filter.state for filter in self.filters]
