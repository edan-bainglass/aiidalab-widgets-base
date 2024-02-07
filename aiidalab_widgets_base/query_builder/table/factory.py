from __future__ import annotations

from ..service import AiiDAService
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


class QueryComponentFactory:
    """docstring"""

    aiida: AiiDAService

    @classmethod
    def get_view(cls, component_type: str) -> TableQueryComponentView:
        """docstring"""

        if cls.aiida is None:
            raise ValueError("missing service")

        view = None

        if component_type == "filters":
            model = QueryFiltersModel(cls.aiida)
            view = QueryFiltersView()
            _ = QueryFiltersController(model, view)
        elif component_type == "projections":
            model = QueryProjectionsModel(cls.aiida)
            view = QueryProjectionsView()
            _ = QueryProjectionsController(model, view)
        else:
            raise ValueError(
                f"type must be 'filters' or 'projections'; got {component_type}"
            )

        return view

    @classmethod
    def set_service(cls, service: AiiDAService) -> None:
        """docstring"""
        cls.aiida = service
