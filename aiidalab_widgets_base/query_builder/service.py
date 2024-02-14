from __future__ import annotations

import datetime
import typing as t

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
            qb.append(node, **args)
        results = qb.first(flat=True)
        print(results)

    def get_nodes(self) -> list[tuple[str, str]]:
        """docstring"""
        return self._NODES

    def get_fields(self, entry_point: str) -> list[str]:
        """docstring"""
        if not entry_point:
            return []
        node = self.get_entry_point(entry_point)
        return list(node.fields._dict.keys())

    def get_operators(self, entry_point: str, field_name: str) -> list[str]:
        """docstring"""
        if not entry_point or not field_name:
            return []
        node = self.get_entry_point(entry_point)
        field = node.fields[field_name]
        if field.qb_field == "attributes.value":
            if isinstance(node, orm.Str):
                return _LITERAL_OPERATORS
            if issubclass(node, orm.NumericType):
                return _NUMERICAL_OPERATORS
            if isinstance(node, orm.List):
                return _ITERABLE_OPERATORS
            if isinstance(node, orm.Dict):
                return _DICTIONARY_OPERATORS
        dtype = _extract_field_type(field.dtype)
        if dtype is str:
            return _LITERAL_OPERATORS
        if dtype in (int, float, datetime.date, datetime.datetime):
            return _NUMERICAL_OPERATORS
        if dtype in (list, tuple):
            return _ITERABLE_OPERATORS
        if dtype is dict:
            return _DICTIONARY_OPERATORS
        return _GENERAL_OPERATORS

    def get_entry_point(self, entry_point: str) -> orm.Node:
        """docstring"""
        group, name = entry_point.split("_")
        return BaseFactory(group, name)


def _extract_field_type(dtype: t.Any) -> t.Any:
    """docstring"""
    if origin := t.get_origin(dtype):
        return t.get_args(dtype)[0] if origin is t.Union else origin
    if dtype is datetime.datetime:
        return datetime.datetime  # VERIFY
    return dtype


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

_GENERAL_OPERATORS = [
    "==",
    "in",
]

_NUMERICAL_OPERATORS = [
    *_GENERAL_OPERATORS,
    ">",
    "<",
    "<=",
    ">=",
]

_LITERAL_OPERATORS = [
    *_GENERAL_OPERATORS,
    "like",
    "ilike",
]

_ITERABLE_OPERATORS = [
    *_GENERAL_OPERATORS,
    "of_length",
    "shorter",
    "longer",
    "contains",
]

_DICTIONARY_OPERATORS = [
    *_GENERAL_OPERATORS,
    "has_key",
    "of_type",
]
