import ast

import pytest

from flake8_override.plugin import Plugin


@pytest.fixture
def plugin_run():
    """Fixture for easy run plugin."""
    def _plugin_run(code: str) -> list[tuple[int, int, str]]:  # noqa: WPS430
        """Plugin run result."""
        plugin = Plugin(ast.parse(code))
        res = []
        for viol in plugin.run():
            res.append((
                viol[0],
                viol[1],
                viol[2],
            ))
        return res
    return _plugin_run


@pytest.mark.parametrize('variation', [
    'override',
    'typing.override',
    't.override',
])
def test_valid(plugin_run, variation):
    """Test valid case."""
    got = plugin_run('\n'.join([
        'class Animal(object):',
        '',
        '    @{0}'.format(variation),
        '    def move(self, to_x: int, to_y: int):',
        '        # Some logic for change coordinates',
        '        pass',
        '',
        '    @{0}'.format(variation),
        '    def sound(self):',
        '        print("Abstract animal sound")',
        '',
    ]))

    assert not got


def test_with_attribute(plugin_run):
    got = plugin_run('\n'.join([
        'class Animal(object):',
        '',
        '    x: int',
        '    y = 0',
        '',
        '    @override',
        '    def move(self, to_x: int, to_y: int):',
        '        # Some logic for change coordinates',
        '        pass',
        '',
        '    @override',
        '    def sound(self):',
        '        print("Abstract animal sound")',
        '',
    ]))

    assert not got


@pytest.mark.parametrize('deco', ['staticmethod', 'classmethod'])
def test_runtime_decorators(deco, plugin_run):
    got = plugin_run('\n'.join([
        'class Animal(object):',
        '',
        '    @{0}'.format(deco),
        '    def secondary_ctor(cls):',
        '        return cls()',
        '',
        '    @override',
        '    def move(self, to_x: int, to_y: int):',
        '        # Some logic for change coordinates',
        '        pass',
        '',
        '    @override',
        '    def sound(self):',
        '        print("Abstract animal sound")',
        '',
    ]))

    assert not got


def test_init(plugin_run):
    got = plugin_run('\n'.join([
        'class Animal(object):',
        '',
        '    def __init__(self, x, y):',
        '        self.x = x',
        '        self.y = y',
        '',
        '    def move(self, to_x: int, to_y: int):',
        '        # Some logic for change coordinates',
        '        pass',
        '',
        '    def sound(self):',
        '        print("Abstract animal sound")',
        '',
    ]))

    assert not got


def test_wrong(plugin_run):
    got = plugin_run('\n'.join([
        'class Animal(object):',
        '',
        '    def move(self, to_x: int, to_y: int):',
        '        # Some logic for change coordinates',
        '        pass',
        '',
        '    def sound(self):',
        '        print("Abstract animal sound")',
        '',
    ]))

    assert got == [
        (3, 4, 'OVRD: method must contain `typing.override` decorator'),
        (7, 4, 'OVRD: method must contain `typing.override` decorator')
    ]



def test_wrong_other_deco(plugin_run):
    got = plugin_run('\n'.join([
        'class Animal(object):',
        '',
        '    @cache',
        '    def move(self, to_x: int, to_y: int):',
        '        # Some logic for change coordinates',
        '        pass',
        '',
        '    @cache',
        '    def sound(self):',
        '        print("Abstract animal sound")',
        '',
    ]))

    assert got == [
        (4, 4, 'OVRD: method must contain `typing.override` decorator'),
        (9, 4, 'OVRD: method must contain `typing.override` decorator')
    ]
