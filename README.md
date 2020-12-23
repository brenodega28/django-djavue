# Djavue

![Build](https://travis-ci.com/brenodega28/django-djavue.svg?branch=main&status=passed)
[![codecov](https://codecov.io/gh/brenodega28/django-djavue/branch/main/graph/badge.svg?token=UYLA6IFYOL)](https://codecov.io/gh/brenodega28/django-djavue)\
Djavue is a Django app that allows the usage of Vue files as Django Templates.

## Installation

1. Install django-djavue from pip

```
pip install django-djavue
```

2. Add djavue to your INSTALLED APPS

```python
INSTALLED_APPS = [
  ...,
  'djavue',
  ...
]
```

## Quickstart

1. Create a .vue file inside your templates folder.

2. Write a view that loads the template

```python
from djavue import get_vue_template

def index(request):
    template = get_vue_template('index.vue', title="Homepage")

    return template.render({"""context here"""})
```

## Links:

[Tutorial](https://github.com/brenodega28/django-djavue/wiki/0.-Tutorial)
[Pypi](https://pypi.org/project/django-djavue/)
[Github](https://github.com/brenodega28/django-djavue)
