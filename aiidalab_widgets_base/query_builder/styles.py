from __future__ import annotations


class CSS:
    """`QueryBuilderWidget` styles."""

    HIDDEN = {
        "display": "none",
    }

    CENTERED = {
        "margin": "0 auto",
    }

    M2 = {
        "margin": "2px",
    }

    P5 = {
        "padding": "5px",
    }

    PY5 = {
        "padding": "5px 0",
    }

    W100 = {
        "width": "100%",
    }

    W50 = {
        "width": "50%",
    }

    WAUTO = {
        "width": "auto",
    }

    WFIT = {
        "width": "fit-content",
    }

    FLEX1 = {
        "flex": "1",
    }

    FLOAT_RIGHT = {
        "margin": "2px 2px 2px auto",
    }

    TIGHT_DESCRIPTION = {
        "description_width": "initial",
    }

    BORDER1 = {
        "border": "1px solid lightgray",
    }

    BORDERED_BOX = {
        **M2,
        **P5,
        **BORDER1,
    }

    CONTENT_MARGIN = {
        "margin": "2px 3px",
    }

    BUTTON = {
        **WFIT,
    }
