from __future__ import annotations

import ipywidgets as ipw

from .guide import QueryBuilderGuide
from .query import QBController, QBModel, QBView
from .results import get_results_view
from .service import AiiDAService


class QueryBuilderWidget(ipw.VBox):
    """docstring"""

    _TAB_LABELS = (
        "Query",
        "Results",
        "Guide",
    )

    def __init__(self, **kwargs):
        """docstring"""

        service = AiiDAService()

        tabs = ipw.Tab(
            layout={},
            children=[
                self._get_query_view(service),
                get_results_view(),
                QueryBuilderGuide(),
            ],
            selected_index=0,
        )

        for i in range(len(tabs.children)):
            tabs.set_title(i, self._TAB_LABELS[i])

        super().__init__(children=[tabs], **kwargs)

    def _get_query_view(self, service: AiiDAService) -> QBView:
        """docstring"""
        model = QBModel(service)
        view = QBView()
        _ = QBController(model, view)
        return view
