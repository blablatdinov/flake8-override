# flake8-override

[![Build Status](https://github.com/blablatdinov/flake8-override/workflows/test/badge.svg?branch=master&event=push)](https://github.com/blablatdinov/flake8-override/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/blablatdinov/flake8-override/branch/master/graph/badge.svg)](https://codecov.io/gh/blablatdinov/flake8-override)
[![Python Version](https://img.shields.io/pypi/pyversions/flake8-override.svg)](https://pypi.org/project/flake8-override/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

`flake8-override` is a Flake8 plugin designed to enforce a coding standard where every method in a class must have the @override decorator. This ensures that all public methods implement their counterparts from an interface, promoting better design practices, easier mocking in unit tests, and simpler extension via decoration.

[Seven Virtues of a Good Object. Part 2](https://www.yegor256.com/2014/11/20/seven-virtues-of-good-object.html#2-he-works-by-contracts)

## Installation

You can install flake8-override via pip:

```bash
pip install flake8-override
```

## Usage

To use flake8-override, simply include it in your Flake8 configuration. You can run Flake8 as usual, and the plugin will check for the presence of the @override decorator on each method.

```bash
flake8 your_code_directory
```

## Example

### Input code

```python
class Dog:

    def sound(self):
        print('bark')
```

### Expected code

```python
from typing import Protocol, override

class Animal(Protocol):

    def sount(self): ...

class Dog(Animal):

    @override
    def sound(self):
        print('bark')
```

## Rationale

The primary motivation for this plugin is to ensure that objects adhere to contracts as specified by interfaces. This has two main benefits:

- Easier Mocking in Unit Tests: Objects that work by contract are easier to mock in unit tests because their behavior is predictable and defined by interfaces.
- Simpler Extension via Decoration: Objects designed with clear contracts are easier to extend and decorate, promoting better software design and maintenance.

## License

[MIT](https://github.com/blablatdinov/flake8-override/blob/master/LICENSE)

## Credits

This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [864a62ecb432655249d071e263ac51f053448659](https://github.com/wemake-services/wemake-python-package/tree/864a62ecb432655249d071e263ac51f053448659). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/864a62ecb432655249d071e263ac51f053448659...master) since then.
