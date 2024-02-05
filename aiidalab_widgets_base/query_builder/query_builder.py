from __future__ import annotations

import ipywidgets as ipw

from .query import get_query_view
from .results import get_results_view
from .guide import QueryBuilderGuide


class QueryBuilderWidget(ipw.VBox):
    """docstring"""

    _TAB_LABELS = (
        "Query",
        "Results",
        "Guide",
    )

    def __init__(self, **kwargs):
        """docstring"""

        tabs = ipw.Tab(
            layout={},
            children=[
                get_query_view(),
                get_results_view(),
                QueryBuilderGuide(),
            ],
            selected_index=0,
        )

        for i in range(len(tabs.children)):
            tabs.set_title(i, self._TAB_LABELS[i])

        super().__init__(children=[tabs], **kwargs)
