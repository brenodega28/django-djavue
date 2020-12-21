# Djavue

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

## in urls.py -> path('', index, name='index')

# Or

from djavue import VueTemplate

class Index(VueTemplate):
    def get_context(self, request):
        return {"""Context here"""}

    class Meta:
        page_title = "Homepage"
        template_name = "index.vue"

## in urls.py -> path('', Index.as_view(), name='index')
```

## Passing Context

To get context data from django to your vue file you must use the `$(key)` inside the template.

### Example

#### Vue:

```html
<template>
  <h1>My name is {{name}}</h1>
  <h2>My age is $(age)</h2>
</template>
<script>
  export default {
    data: () => ({
      name: "$(name)",
    }),
  };
</script>
```

#### Django:

```python
from djavue.views import VueTemplate

class Index(VueTemplate):
    def get_context(self, request):
        return {'name':'Joe', 'age':20}

    class Meta:
        page_title = "Homepage"
        template_name = "index.vue"
```

#### Result:

```
My name is Joe
```

## Importing

Due to some limitations when adapting Vue to Python, the import statement is different: you only need to pass the file (exactly how you would pass to the get_template). The name of the tag will be the name of the file.

```html
<template>
  <div>
    <component-a></component-a>
    <component-b></component-b>
  </div>
</template>
<script>
  import "component-a";
  import "components/component-b";

  export default {};
</script>
```
