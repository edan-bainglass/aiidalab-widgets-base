from __future__ import annotations

import ipywidgets as ipw
import traitlets

from .result import QBResult


class QBResultsController(ipw.VBox):
    """docstring"""

    _ResultClass = QBResult

    def __init__(
        self,
        model: QBResultsModel,
        view: QBResultsView,
        result_class=QBResult,
    ) -> None:
        """docstring"""
        self._model = model
        self._view = view
        self._ResultClass = result_class
        self._set_event_handlers()

    def _display_results(self, change: dict) -> None:
        """docstring"""
        if change["new"]:
            projections, results = change["new"]
            self._ResultClass.projections = projections
            self._view.children = (
                [self._ResultClass(result) for result in results]
                if results
                else [self._ResultClass("No results")]
            )

    def _set_event_handlers(self) -> None:
        """docstring"""
        self._model.observe(self._display_results, "results")


class QBResultsModel(traitlets.HasTraits):
    """docstring"""

    results = traitlets.List([])


class QBResultsView(ipw.VBox):
    """docstring"""
