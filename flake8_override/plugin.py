# SPDX-FileCopyrightText: Copyright (c) 2024-2026 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
# SPDX-License-Identifier: MIT

# flake8: noqa: WPS232

import ast
from collections.abc import Generator
from typing import final


@final
class ClassVisitor(ast.NodeVisitor):
    """Class visitor for checking that all methods has override decorator."""

    def __init__(self) -> None:
        """Ctor."""
        self.problems: list[tuple[int, int]] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802, WPS231, C901
        """Visit by classes."""
        available_decorators = {'override', 'typing.override', 't.override'}
        for base in node.bases:
            if isinstance(base, ast.Subscript):
                if isinstance(base.value, ast.Name) and base.value.id == 'Protocol':
                    self.generic_visit(node)
                    return
            if isinstance(base, ast.Subscript):
                if isinstance(base.value, ast.Name) and base.value.id != 'Protocol':
                    continue
            if isinstance(base, ast.Name) and base.id != 'Protocol':
                continue
            if isinstance(base, ast.Name) and base.id == 'Protocol':
                self.generic_visit(node)
                return
            if isinstance(base, ast.Attribute) and base.attr == 'Protocol':
                self.generic_visit(node)
                return
        for elem in node.body:
            if not isinstance(elem, ast.FunctionDef) and not isinstance(elem, ast.AsyncFunctionDef):
                continue
            if elem.name == '__init__':
                continue
            if elem.name.startswith('_'):
                break
            is_class_or_static_method = False
            for deco in elem.decorator_list:
                if is_class_or_static_method:
                    break
                if isinstance(deco, ast.Attribute):
                    if deco.attr in available_decorators:
                        break
                elif isinstance(deco, ast.Name):
                    if deco.id in available_decorators:
                        break
                    elif deco.id in {'classmethod', 'staticmethod'}:
                        is_class_or_static_method = True
            else:
                if not is_class_or_static_method:
                    self.problems.append((elem.lineno, elem.col_offset))
        self.generic_visit(node)


@final
class Plugin:
    """Flake8 plugin."""

    def __init__(self, tree: ast.AST) -> None:
        """Ctor."""
        self._tree = tree

    def run(self) -> Generator[tuple[int, int, str, type], None, None]:
        """Entry."""
        visitor = ClassVisitor()
        visitor.visit(self._tree)
        for line in visitor.problems:  # noqa: WPS526
            yield (line[0], line[1], 'OVR100 method must contain `typing.override` decorator', type(self))
