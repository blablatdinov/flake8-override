# The MIT License (MIT).
#
# Copyright (c) 2024 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

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
            if not isinstance(elem, ast.FunctionDef):
                continue
            if elem.name == '__init__':
                break
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
