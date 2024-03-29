from __future__ import annotations

import ipywidgets as ipw

from aiidalab_widgets_base.query_builder.styles import CSS

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
        default_filter = self._add_filter()
        default_filter.join.value = None
        default_filter.join.layout.visibility = "hidden"
        default_filter.remove.layout.visibility = "hidden"

    def _add_filter(self, _=None) -> QueryFilterView:
        """docstring"""
        view = self._get_filter_view()
        view.observe(self._remove_filter, "closed")
        self._view.filters_container.children += (view,)
        return view

    def _remove_filter(self, trait: dict) -> QueryFilterView:
        """docstring"""
        view: QueryFilterView = trait["owner"]
        self._view.filters = [
            *filter(
                lambda query_div: query_div != view,
                self._view.filters,
            ),
        ]
        view.unobserve_all()
        return view

    def _refresh(self, _=None) -> None:
        """docstring"""
        default_filter = self._view.filters[0]
        self._view.filters = [default_filter]
        default_filter.reset_trigger += 1

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

    def _set_event_handlers(self) -> None:
        super()._set_event_handlers()
        self._view.add.on_click(self._add_filter)


class QueryFiltersModel(NodeQueryComponentModel):
    """docstring"""


class QueryFiltersView(NodeQueryComponentView):
    """docstring"""

    component_type = "filters"
    expand_button_description = "filter"

    def __init__(self, **kwargs) -> None:
        """docstring"""
        super().__init__(**kwargs)

        self.filters_container = ipw.VBox()

        self.add = ipw.Button(
            layout={
                **CSS.BUTTON,
                **CSS.FLOAT_RIGHT,
            },
            button_style="",
            icon="plus",
            tooltip="Add filter",
        )

        self.content.children += (
            self.filters_container,
            self.add,
        )

    @property
    def filters(self) -> list[QueryFilterView]:
        """docstring"""
        return list(self.filters_container.children)

    @filters.setter
    def filters(self, filters: list[QueryFilterView]) -> None:
        """docstring"""
        self.filters_container.children = filters

    @property
    def state(self) -> list:
        if self.container.layout.display == "none":
            return []
        return [filter.state for filter in self.filters]
