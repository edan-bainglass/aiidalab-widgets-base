from __future__ import annotations

import aiida.plugins.entry_point as ep
from aiida import orm
from aiida.plugins.factories import BaseFactory


class AiiDAService:
    """docstring"""

    _NODES = [
        (entry_point.attr, f"{entry_point.group}_{entry_point.name}")
        for group in filter(
            lambda ep: "aiida." in ep,
            ep.get_entry_point_groups(),
        )
        for entry_point in ep.get_entry_points(group)
        if entry_point.attr
        in (
            "Group",
            "Int",
        )
    ]

    def submit(self, query: list[tuple[orm.Node, dict]]) -> None:
        """docstring"""
        qb = orm.QueryBuilder()
        for node, args in query:
            qb.append(
                node,
                **args,
            )
        results = qb.first(flat=True)
        print(results)

    def get_nodes(self) -> list[str]:
        """docstring"""
        return self._NODES

    def get_fields(self, entry_point: str) -> list[str]:
        """docstring"""
        if entry_point:
            node: orm.Node = self.get_entry_point(entry_point)
            return list(node.fields._dict.keys())
        return []

    def get_entry_point(self, entry_point: str) -> orm.Node:
        """docstring"""
        group, name = entry_point.split("_")
        return BaseFactory(group, name)


NODE_RELATIONSHIPS = [
    "",
    "outgoing",
    "incoming",
    "group",
]

GROUP_RELATIONSHIPS = [
    "",
    "node",
    "user",
]

JOINS = [
    "and",
    "or",
]

OPERATORS = [
    "==",
    "in",
    ">",
    "<",
    "<=",
    ">=",
    "like",
    "ilike",
    "or",
    "and",
    "has_key",
    "of_type",
    "of_length",
    "shorter",
    "longer",
    "contains",
]
