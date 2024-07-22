import ast
from typing import final
from collections.abc import Generator


@final
class ClassVisitor(ast.NodeVisitor):
    """Class visitor for checking that all methods has override decorator."""

    def __init__(self) -> None:
        """Ctor."""
        self.problems: list[tuple[int, int]] = []

    def visit_ClassDef(self, node) -> None:
        """Visit by classes."""
        available_decorators = {'override', 'typing.override', 't.override'}
        for elem in node.body:
            if not isinstance(elem, ast.FunctionDef):
                continue
            for deco in elem.decorator_list:
                if isinstance(deco, ast.Attribute) and deco.attr in available_decorators:
                    break
                elif isinstance(deco, ast.Name) and deco.id in available_decorators:
                    break
            else:
                self.problems.append((elem.lineno, elem.col_offset))
        self.generic_visit(node)


@final
class Plugin:
    """Flake8 plugin."""

    def __init__(self, tree) -> None:
        """Ctor."""
        self._tree = tree

    def run(self) -> Generator[tuple[int, int, str, type], None, None]:
        """Entry."""
        visitor = ClassVisitor()
        visitor.visit(self._tree)
        for line in visitor.problems:  # noqa: WPS526
            yield (line[0], line[1], 'OVRD: method must contain `typing.override` decorator', type(self))
