from __future__ import annotations


class CSS:
    """`QueryBuilderWidget` styles."""

    HIDDEN = {
        "display": "none",
    }

    CENTERED = {
        "margin": "0 auto",
    }

    M0 = {
        "margin": "0",
    }

    M2 = {
        "margin": "2px",
    }

    MX2 = {
        "margin": "0 2px",
    }

    P2 = {
        "padding": "2px",
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

    H100 = {
        "height": "100%",
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

    SPACE_BETWEEN = {"justify_content": "space-between"}

    BORDERED_BOX = {
        **M2,
        **P5,
        **BORDER1,
    }

    CONTENT_MARGIN = {
        "margin": "2px 3px",
    }

    BUTTON = {
        "width": "33px",
    }

    COMPONENT_BUTTON = {
        "width": "75px",
    }

    NODE_QUERY_SELECTOR = {
        "description_width": "75px",
    }

    TAG_INPUTBOX = {
        "width": "100px",
    }

    OPERATOR_SELECTOR = {
        "width": "15%",
    }

    MULTISELECT = {
        **FLEX1,
        **P2,
        **M0,
        **H100,
    }
