from django import forms

from notify.helpers import notify_facilitators


class NotifyOnCreationForm(forms.ModelForm):

    should_notify_facilitators = True

    def send_notifications(self, obj, is_creating):
        if is_creating:
            if self.should_notify_facilitators:
                notify_facilitators(obj)

    def save(self, **kwargs):
        is_creating = not self.instance.id

        obj = super(NotifyOnCreationForm, self).save(**kwargs)
        self.send_notifications(obj, is_creating)
        return obj
