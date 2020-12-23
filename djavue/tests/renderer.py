import unittest

from djavue.renderer import VueRenderer
from djavue.tests.component import TestingEngine


class VueRendererTestCase(unittest.TestCase):
    def setUp(self):
        self.title = "New Title"
        self.renderer = VueRenderer(self.title, "component.vue", engine=TestingEngine())

    def test_write_header(self):
        self.renderer._write_header()

        self.assertEqual(
            self.renderer.html,
            f"<html><head><title>{self.title}</title>{self.renderer._get_cdn()}</head>",
        )

    def test_write_component(self):
        context = {"name": "test_name"}
        components = self.renderer._write_components(context).split(";")

        self.assertEqual(len(components), 2)
        self.assertEqual(
            components[0],
            self.renderer.component_list.components[0].to_component(context),
        )
        self.assertEqual(
            components[1],
            self.renderer.component_list.components[1].to_component(context),
        )
