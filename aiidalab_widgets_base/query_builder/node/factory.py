from __future__ import annotations

import typing as t

from .component import NodeQueryComponentView
from .filters import (
    QueryFiltersController,
    QueryFiltersModel,
    QueryFiltersView,
)
from .projections import (
    QueryProjectionsController,
    QueryProjectionsModel,
    QueryProjectionsView,
)

if t.TYPE_CHECKING:
    from .node import NodeQueryModel


class QueryComponentFactory:
    """docstring"""

    model: NodeQueryModel

    @classmethod
    def get_view(cls, component_type: str) -> NodeQueryComponentView:
        """docstring"""

        if cls.model is None:
            raise ValueError("missing model")

        view = None

        if component_type == "filters":
            model = QueryFiltersModel(cls.model)
            view = QueryFiltersView()
            _ = QueryFiltersController(model, view)
        elif component_type == "projections":
            model = QueryProjectionsModel(cls.model)
            view = QueryProjectionsView()
            _ = QueryProjectionsController(model, view)
        else:
            raise ValueError(
                f"type must be 'filters' or 'projections'; got {component_type}"
            )

        return view

    @classmethod
    def set_node_query_model(cls, model: NodeQueryModel) -> None:
        """docstring"""
        cls.model = model
