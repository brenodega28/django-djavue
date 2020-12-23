import unittest

from djavue.component import VueComponent
from djavue.component_list import VueComponentList


class TestVueFile:
    def __init__(self, path):
        self.origin = "djavue/tests/src/" + path


class TestingEngine:
    def get_template(self, path):
        return TestVueFile(path)


class VueComponentListTestCase(unittest.TestCase):
    def setUp(self):
        self.test_file_path = "djavue/tests/src/"
        self.test_file_name = "component.vue"
        self.component_list = VueComponentList()
        self.component_list.engine = TestingEngine()

    def test_load(self):
        self.component_list.load("component")

        self.assertEqual(len(self.component_list.components), 2)

    def test_load_duplicate(self):
        self.component_list.load("component")
        self.component_list.load("imported")

        self.assertEqual(len(self.component_list.components), 2)

    def test_from_file(self):
        component_list = VueComponentList.from_file(
            self.test_file_path, self.test_file_name, engine=TestingEngine()
        )
        names = [c.name for c in component_list.components]

        self.assertEqual(component_list.root.name, "component")
        self.assertEqual(len(names), 2)
        self.assertIn("imported", names)
        self.assertIn("component-a", names)


class VueComponentTestCase(unittest.TestCase):
    def setUp(self):
        self.test_file_path = "djavue/tests/src/"
        self.test_file_name = "component.vue"
        self.component_list = VueComponentList.from_file(
            self.test_file_path, self.test_file_name, engine=TestingEngine()
        )
        self.component = self.component_list.root

    def test_initialization(self):
        with open(self.test_file_path + self.test_file_name, "r") as f:
            content = f.read()

        self.assertEqual(self.component.name, "component")
        self.assertEqual(self.component.location, self.test_file_path)
        self.assertEqual(self.component.file_name, self.test_file_name)
        self.assertEqual(self.component._raw, content)

    def test_import(self):
        names = [c.name for c in self.component_list.components]

        self.assertEqual(len(names), 2)
        self.assertIn("imported", names)
        self.assertIn("component-a", names)

    def test_mount(self):
        component = self.component.mount({"name": "test"})

        self.assertEqual(component.template, "<h1>{{name}}</h1>")
        self.assertEqual(component.script, 'data: () => ({        name: "test"    })')
        self.assertEqual(self.component.style, "h1{  color: 'red'}")

    def test_to_component(self):
        self.assertEqual(
            self.component.to_component({"name": "test"}),
            """Vue.component('component',{ template:'<h1>{{name}}</h1>', data: () => ({        name: "test"    }) })""",
        )
