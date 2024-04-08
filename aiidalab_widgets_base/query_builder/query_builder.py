from __future__ import annotations

import ipywidgets as ipw

from .guide import QueryBuilderGuide
from .query import QBController, QBModel, QBView
from .results import QBResultsController, QBResultsModel, QBResultsView
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

        self.tabs = ipw.Tab(
            layout={},
            children=[
                self._get_query_view(service),
                self._get_results_view(),
                QueryBuilderGuide(),
            ],
            selected_index=0,
        )

        for i in range(len(self.tabs.children)):
            self.tabs.set_title(i, self._TAB_LABELS[i])

        super().__init__(children=[self.tabs], **kwargs)

        self._set_event_handlers()

    def _switch_to_results(self, _=None) -> None:
        """docstring"""
        self.tabs.selected_index = 1

    def _get_query_view(self, service: AiiDAService) -> QBView:
        """docstring"""
        self.query_model = QBModel(service)
        view = QBView()
        _ = QBController(self.query_model, view)
        return view

    def _get_results_view(self) -> QBResultsView:
        """docstring"""
        self.results_model = QBResultsModel()
        view = QBResultsView()
        _ = QBResultsController(self.results_model, view)
        return view

    def _set_event_handlers(self) -> None:
        """docstring"""
        ipw.dlink(
            (self.query_model, "results"),
            (self.results_model, "results"),
        )
        self.query_model.observe(self._switch_to_results, "results")
