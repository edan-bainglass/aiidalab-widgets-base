from __future__ import annotations

import ipywidgets as ipw
import traitlets


def get_table_query_view() -> TableQueryView:
    """docstring"""
    model = TableQueryModel()
    view = TableQueryView()
    _ = TableQueryController(model, view)
    return view


class TableQueryController:
    """docstring"""

    def __init__(self, model: TableQueryModel, view: TableQueryView) -> None:
        """docstring"""
        self._model = model
        self._view = view

class TableQueryModel(traitlets.HasTraits):
    """docstring"""


class TableQueryView(ipw.VBox):
    """docstring"""

