import typing as t

import ipywidgets as ipw


class QBResult(ipw.VBox):
    """docstring"""

    projections: dict[str, list] = {}

    def __init__(self, result: list[t.Any]) -> None:
        """docstring"""

        output = ipw.Output()

        super().__init__(
            layout={
                "border": "1px solid #9e9e9e",
                "margin": "2px",
                "padding": "5px",
            },
            children=[output],
        )

        with output:
            if isinstance(result, str):
                print(result.strip())
            else:
                for i, node in enumerate(self.projections):
                    new_line = '\n' if i > 0 else ''
                    print(f"{new_line}{node}\n{'=' * len(node)}")
                    for projection in self.projections[node]:
                        value = result.pop(0)
                        print(f"{projection}: {value}")
