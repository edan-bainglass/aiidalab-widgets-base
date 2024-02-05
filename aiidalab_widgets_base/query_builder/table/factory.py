from __future__ import annotations

from .component import TableQueryComponentView
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


def get_query_component_view(component_type: str) -> TableQueryComponentView:
    """docstring"""

    view = None

    if component_type == "filters":
        model = QueryFiltersModel()
        view = QueryFiltersView()
        _ = QueryFiltersController(model, view)
    elif component_type == "projections":
        model = QueryProjectionsModel()
        view = QueryProjectionsView()
        _ = QueryProjectionsController(model, view)
    else:
        raise ValueError(
            f"type must be 'filters' or 'projections'; got {component_type}"
        )

    return view
