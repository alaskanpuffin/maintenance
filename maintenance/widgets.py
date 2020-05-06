from django.forms import widgets
from django.template import loader
from django.utils.safestring import mark_safe


class Select2(widgets.Select):
    template_name = 'widgets/select2.html'
    option_template_name = 'widgets/select2-options.html'
    def __init__(self, form=None, *args, **kwargs):
        self.formObj = form
        super (Select2,self ).__init__(*args,**kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        context['form'] = self.formObj
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)
