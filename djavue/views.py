import os

from django.http import HttpResponse

from djavue.renderer import get_vue_template


class VueTemplate:
    """
    Shortcut for creating a view that returns a Vue file
    """

    def _validate(self):
        """
        Checks if template_name and context exists
        """

        if self.Meta.template_name is None:
            raise Exception("No template given")

        if self.context is None:
            raise Exception(f"{self.Meta.template_name} context is null.")

    def get_context(self, request) -> object:
        """
        Function for defining context that must be overriden by the user
        """

        return None

    def _mount(self, request) -> HttpResponse:
        """
        Validates, loads the template and returns the content in Http
        """

        self.context = self.get_context(request)
        self._validate()

        instance = get_vue_template(
            os.path.split(self.Meta.template_name)[1],
            title=self.Meta.page_title,
        )

        self.content = instance.render(self.context)

        return HttpResponse(self.content)

    @classmethod
    def as_view(cls):
        """
        Returns a function to be used in Django's path() or url()
        """

        instance = cls()
        return lambda request: instance._mount(request)

    class Meta:
        """
        Class that must be overriden by the user with the view's details
        """

        page_title = "Djavue Page"
        root_path = ""
        template_name = None
        context = None