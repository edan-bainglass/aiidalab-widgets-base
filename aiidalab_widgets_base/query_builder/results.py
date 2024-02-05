from __future__ import annotations

import ipywidgets as ipw
import traitlets


def get_results_view() -> QBResultsView:
    """docstring"""
    model = QBResultsModel()
    view = QBResultsView()
    _ = QBResultsController(model, view)
    return view


class QBResultsController(ipw.VBox):
    """docstring"""

    def __init__(
        self,
        view: QBResultsView,
        model: QBResultsModel,
    ) -> None:
        """docstring"""
        self._view = view
        self._model = model


class QBResultsModel(traitlets.HasTraits):
    """docstring"""


class QBResultsView(ipw.VBox):
    """docstring"""
