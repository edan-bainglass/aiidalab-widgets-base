from __future__ import annotations

import typing as t

import ipywidgets as ipw
import traitlets

from ..styles import CSS

if t.TYPE_CHECKING:
    from .node import NodeQueryModel


class NodeQueryComponentController:
    """docstring"""

    def __init__(
        self,
        model: NodeQueryComponentModel,
        view: NodeQueryComponentView,
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


class NodeQueryComponentModel(traitlets.HasTraits):
    """docstring"""

    entry_point = traitlets.Unicode("")

    def __init__(self, model: NodeQueryModel) -> None:
        """docstring"""
        ipw.dlink((model, "entry_point"), (self, "entry_point"))
        self.aiida = model.aiida


class NodeQueryComponentView(ipw.VBox):
    """docstring"""

    component_type = ""
    expand_button_description = ""

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
            layout=CSS.COMPONENT_BUTTON,
            button_style="",
            icon="plus",
            description=self.expand_button_description,
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
