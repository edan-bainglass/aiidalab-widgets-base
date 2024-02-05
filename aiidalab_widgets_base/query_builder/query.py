from __future__ import annotations

import ipywidgets as ipw
import traitlets

from .service import AiiDAService


def get_query_view():
    """docstring"""
    model = QBModel(service=AiiDAService())
    view = QBView()
    _ = QBController(model, view)
    return view


class QBController:
    """docstring"""

    def __init__(self, model: QBModel, view: QBView) -> None:
        """docstring"""
        self._model = model
        self._view = view


class QBModel(traitlets.HasTraits):
    """docstring"""

    def __init__(self, service: AiiDAService) -> None:
        """docstring"""
        self._aiida = service


class QBView(ipw.VBox):
    """docstring"""
