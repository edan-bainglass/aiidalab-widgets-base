from __future__ import annotations

import ipywidgets as ipw
import traitlets

from ..service import AiiDAService
from ..styles import CSS


class TableQueryComponentController:
    """docstring"""

    def __init__(
        self,
        model: TableQueryComponentModel,
        view: TableQueryComponentView,
    ) -> None:
        """docstring"""
        self._model = model
        self._view = view
        self._init_view()
        self._set_event_handlers()

    def _init_view(self) -> None:
        """docstring"""

    def _show_view(self, _=None) -> None:
        """docstring"""
        self._view.container.layout.display = "flex"
        self._view.expand.layout.display = "none"

    def _hide_view(self, _=None) -> None:
        """docstring"""
        self._view.container.layout.display = "none"
        self._view.expand.layout.display = "inline-block"

    def _set_event_handlers(self) -> None:
        """docstring"""
        self._view.expand.on_click(self._show_view)
        self._view.collapse.on_click(self._hide_view)


class TableQueryComponentModel(traitlets.HasTraits):
    """docstring"""

    def __init__(self, service: AiiDAService) -> None:
        """docstring"""
        self.aiida = service


class TableQueryComponentView(ipw.VBox):
    """docstring"""

    component_type = ""

    def __init__(self, **kwargs) -> None:
        """docstring"""

        self.reset = ipw.Button(
            layout=CSS.BUTTON,
            button_style="warning",
            icon="refresh",
            tooltip=f"Reset {self.component_type}",
        )

        self.collapse = ipw.Button(
            layout=CSS.BUTTON,
            button_style="danger",
            icon="times",
            tooltip=f"Remove {self.component_type}",
        )

        self.expand = ipw.Button(
            layout=CSS.BUTTON,
            button_style="",
            icon="plus",
            description=self.component_type,
            tooltip=f"Add {self.component_type}",
        )

        self.content = ipw.VBox(
            layout={
                **CSS.FLEX1,
                **CSS.CONTENT_MARGIN,
            },
        )

        self.container = ipw.HBox(
            layout={
                **CSS.BORDERED_BOX,
                **CSS.W100,
                **CSS.HIDDEN,
            },
            children=[
                self.content,
                ipw.HBox(
                    layout=CSS.FLOAT_RIGHT,
                    children=[
                        self.reset,
                        self.collapse,
                    ],
                ),
            ],
        )

        super().__init__(
            children=[
                ipw.HBox(
                    children=[
                        self.expand,
                        self.container,
                    ],
                ),
            ],
            **kwargs,
        )
