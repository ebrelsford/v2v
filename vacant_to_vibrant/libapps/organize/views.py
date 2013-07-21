"""
Generic views for editing participants.

"""

from django.contrib import messages
from django.views.generic.base import ContextMixin
from django.views.generic.edit import DeleteView

from .models import get_organizer_model, get_watcher_model


class EditParticipantMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        hash = self.get_participant_hash()
        context = super(EditParticipantMixin, self).get_context_data(**kwargs)
        context.update({
            'organizers': get_organizer_model().objects.filter(email_hash__istartswith=hash).order_by('added'),
        })
        watcher_model = get_watcher_model()
        if watcher_model:
            context['watchers'] = watcher_model.objects.filter(email_hash__istartswith=hash).order_by('added')
        return context

    def get_participant_hash(self):
        raise NotImplementedError('Implement get_participant_hash() to use '
                                  'EditParticipantMixin.')


class DeleteParticipantView(DeleteView):

    def get_context_data(self, **kwargs):
        context = super(DeleteParticipantView, self).get_context_data(**kwargs)
        context['target'] = self.object.content_object
        context['next_url'] = self.request.GET.get('next_url')
        return context

    def get_success_url(self):
        messages.info(self.request, self._get_success_message())
        return self.request.POST.get(
            'next_url',
            self.object.content_object.get_absolute_url()
        )

    def _get_success_message(self):
        verb = 'working on'
        if isinstance(self.object, get_organizer_model()):
            verb = 'subscribed to'
        elif isinstance(self.object, get_watcher_model()):
            verb = 'watching'
        return 'You are no longer %s %s.' % (verb, self.object.content_object)


class DeleteOrganizerView(DeleteParticipantView):
    model = get_organizer_model()


class DeleteWatcherView(DeleteParticipantView):
    model = get_watcher_model()
