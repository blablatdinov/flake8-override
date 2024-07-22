import ast
from typing import final
from collections.abc import Generator


@final
class ClassVisitor(ast.NodeVisitor):
    """Class visitor for checking that all methods has override decorator."""

    def __init__(self) -> None:
        """Ctor."""
        self.problems: list[int] = []

    def visit_ClassDef(self, node) -> None:
        """Visit by classes."""
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
            yield (line, 0, 'empty', type(self))
