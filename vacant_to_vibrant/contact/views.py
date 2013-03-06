from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

from contact_form.forms import BasicContactForm
from contact_form.views import ContactFormView as _ContactFormView
from fiber.views import FiberPageMixin


class ContactFormView(FiberPageMixin, _ContactFormView):
    form_class = BasicContactForm
    template_name = 'contact_form/form.html'

    def get_fiber_page_url(self):
        return reverse('contact_form:form')


class ContactCompleted(FiberPageMixin, TemplateView):
    template_name = 'contact_form/contact_completed.html'

    def get_fiber_page_url(self):
        return reverse('contact_form:completed')
