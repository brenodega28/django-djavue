import re
import os

from django.template.backends.django import DjangoTemplates

from djavue.component_list import VueComponentList


class VueRenderer:
    def __init__(self, title, template_name, version="development"):
        self.title = title
        self.html = ""
        self.version = version

        self._load_engine()
        self.path, self.template_name = os.path.split(
            str(self.engine.get_template(template_name).origin)
        )

        self.component_list = VueComponentList.from_file(
            self.path, self.template_name, engine=self.engine
        )

    # UTILS
    def _load_engine(self):
        from django.conf import settings

        obj = settings.TEMPLATES[0].copy()
        obj["NAME"] = "a"
        obj.pop("BACKEND")
        self.engine = DjangoTemplates(params=obj).engine

    def _get_cdn(self):
        if self.version == "production":
            return '<script src="https://cdn.jsdelivr.net/npm/vue@2"></script>'
        else:
            return (
                '<script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>'
            )

    # BUILDER FUNCTIONS
    def _write_header(self):
        self.html += f"<html><head><title>{self.title}</title>{self._get_cdn()}</head>"

    def _write_components(self, context):
        return ";".join(
            map(lambda c: c.to_component(context), self.component_list.components)
        )

    def _write_body(self, context):
        root = self.component_list.root.mount(context)
        self.html += f"<body><div id='root'>{root.template}</div><script>{self._write_components(context)}; new Vue({{el:'#root', {root.script} }})</script></body>"

    # RENDERINGS
    def render(self, context={}):
        self._write_header()
        self._write_body(context)

        return self.html

    def dumps(self, file_name, context={}):
        self.render(context)
        with open(file_name, "w+") as f:
            f.write(self.html)


def get_vue_template(template_name, title="Dejavue Page") -> VueRenderer:
    return VueRenderer(title, template_name)
