import os

from django.http import HttpResponse

from djavue.renderer import get_vue_template


class VueTemplate:
    def _validate(self):
        if self.Meta.template_name is None:
            raise Exception("No template given")

        if self.context is None:
            raise Exception(f"{self.Meta.template_name} context is null.")

    def get_context(self, request) -> object:
        return None

    def _mount(self, request):
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
        instance = cls()
        return lambda request: instance._mount(request)

    class Meta:
        page_title = "Dejavue Page"
        root_path = ""
        template_name = None
        context = None