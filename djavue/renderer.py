import re
import os

from django.template.backends.django import DjangoTemplates

from djavue.component_list import VueComponentList


class VueRenderer:
    """
    Gets template info and returns the appropriate html
    """

    def __init__(self, title, template_name, version="development", engine=None):
        self.title = title
        self.html = ""
        self.version = version

        if not engine:
            self._load_engine()
        else:
            self.engine = engine

        self.path, self.template_name = os.path.split(
            str(self.engine.get_template(template_name).origin)
        )

        self.component_list = VueComponentList.from_file(
            self.path, self.template_name, engine=self.engine
        )

    # UTILS
    def _load_engine(self):
        """
        Creates the Django Engine instance that we use to get path from file name
        """
        try:
            from django.conf import settings

            obj = settings.TEMPLATES[0].copy()
            obj["NAME"] = "a"
            obj.pop("BACKEND")
            self.engine = DjangoTemplates(params=obj).engine
        except:
            print("Error loading engine. Probably will break.")
            pass

    def _get_cdn(self):
        """
        Chooses which Vue CDN to get based on version
        """

        if self.version == "production":
            return '<script src="https://cdn.jsdelivr.net/npm/vue@2"></script>'
        else:
            return (
                '<script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>'
            )

    def _get_styles(self, context):
        root_css = self.component_list.root.mount(context).style
        components_css = [c.mount().style for c in self.component_list.components]

        return "".join([root_css] + components_css)

    # BUILDER FUNCTIONS
    def _write_header(self, context):
        """
        Writes the head tag to the html
        """

        self.html += f"<html><head><title>{self.title}</title>{self._get_cdn()}<style>{self._get_styles(context)}</style></head>"

    def _write_components(self, context):
        """
        Returns all Vue Components in component form, ready for html
        """

        return ";".join(
            map(lambda c: c.to_component(context), self.component_list.components)
        )

    def _write_body(self):
        """
        Writes the body tag to the html
        """
        root = self.component_list.root.mount(context)

        self.html += f"<body><div id='root'>{root.template}</div><script>{self._write_components(context)}; new Vue({{el:'#root', {root.script} }})</script></body>"

    # RENDERINGS
    def render(self, context={}):
        """
        Creates the html based on the root Vue Component passed
        """

        self._write_header(context)
        self._write_body(context)

        return self.html


def get_vue_template(template_name, title="Dejavue Page") -> VueRenderer:
    """
    Loads a Vue file by it's file name and returns a VueRenderer instance ready for being rendered
    """

    return VueRenderer(title, template_name)
