import os
import re

from djavue.component import VueComponent


class VueComponentList:
    """
    Responsible for storing and loading components.
    """

    def __init__(self):
        self.root = None
        self.engine = None
        self.root_path = ""
        self.components = []

    def _is_loaded(self, location):
        return location in [c.location for c in self.components]

    def load(self, path, by=None):
        """
        Loads a component to the list, if it's already loaded then it does nothing.
        """

        file_name = path.replace(";", "").replace('"', "")
        file_name += ".vue"

        location, file_name = os.path.split(
            str(self.engine.get_template(file_name).origin)
        )

        if self._is_loaded(location):
            return

        self.components.append(VueComponent(location, file_name, self))

    @staticmethod
    def from_file(path, file_name, engine=None):
        """
        Creates a new instance based on the root component location.
        """

        component_list = VueComponentList()
        component_list.root_path = path
        component_list.engine = engine

        root = VueComponent(path, file_name, component_list)
        component_list.root = root

        return component_list
