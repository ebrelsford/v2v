from django.views.generic import TemplateView

from contact_form.forms import BasicContactForm
from contact_form.views import ContactFormView as _ContactFormView


class ContactFormView(_ContactFormView):
    form_class = BasicContactForm
    template_name = 'contact_form/form.html'


class ContactCompleted(TemplateView):
    template_name = 'contact_form/contact_completed.html'
