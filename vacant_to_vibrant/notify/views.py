from django.views.generic.edit import ModelFormMixin

from notify.helpers import notify_facilitators


class NotifyFacilitatorsMixin(ModelFormMixin):
    """A ModelFormMixin that notifies facilitators on saving."""
    should_notify_facilitators = True

    def get_should_notify_facilitators(self, obj):
        return self.should_notify_facilitators

    def send_notifications(self, obj):
        if self.get_should_notify_facilitators(obj):
            notify_facilitators(obj)

    def form_valid(self, form):
        if not self.object:
            self.object = form.save()
        self.send_notifications(self.object)
        return super(NotifyFacilitatorsMixin, self).form_valid(form)
