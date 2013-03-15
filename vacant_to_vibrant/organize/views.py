"""
Abstraction of 596 Acres' organize.views.
"""

#
# TODO allow participant on any type using contenttypes
# TODO remove all references to Lot and bbl
#

import json

from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from django.views.generic.edit import DeleteView

from recaptcha_works.decorators import fix_recaptcha_remote_ip

from lots.models import Lot
from .forms import OrganizerForm, WatcherForm
from .models import Organizer, Watcher


def details(request, bbl=None):
    organizers = Organizer.objects.filter(lot__bbl=bbl)

    details = []
    for organizer in organizers:
        details.append({
            'name': organizer.name,
            'phone': organizer.phone,
            'email': organizer.email,
            'url': organizer.url,
            'type': organizer.type.name,
            'lots': [organizer.lot.bbl],
        })
    return HttpResponse(json.dumps(details), mimetype='application/json')


def details_tab(request, bbl=None):
    lot = get_object_or_404(Lot, bbl=bbl)

    return render_to_response('organize/tab.html', {
        'organizers': lot.organizer_set.all()
    }, context_instance=RequestContext(request))


@fix_recaptcha_remote_ip
def add_organizer(request, bbl=None):
    lot = get_object_or_404(Lot, bbl=bbl)
    if request.method == 'POST':
        form = OrganizerForm(request.POST, user=request.user)
        if form.is_valid():
            organizer = form.save()
            return redirect('organize_organizer_add_success', bbl=bbl,
                            email_hash=organizer.email_hash[:10])
    else:
        form = OrganizerForm(initial={
            'lot': lot,
        }, user=request.user)

    template = 'organize/add_organizer.html'

    return render_to_response(template, {
        'form': form,
        'lot': lot,
    }, context_instance=RequestContext(request))


@fix_recaptcha_remote_ip
def add_watcher(request, bbl=None):
    lot = get_object_or_404(Lot, bbl=bbl)
    if request.method == 'POST':
        form = WatcherForm(request.POST, user=request.user)
        if form.is_valid():
            watcher = form.save()
            return redirect('organize_watcher_add_success', bbl=bbl,
                            email_hash=watcher.email_hash[:10])
    else:
        form = WatcherForm(initial={
            'lot': lot,
        }, user=request.user)

    template = 'organize/add_watcher.html'

    return render_to_response(template, {
        'form': form,
        'lot': lot,
    }, context_instance=RequestContext(request))


class AddParticipantSuccessView(TemplateView):
    model = None

    def get_context_data(self, **kwargs):
        lot = get_object_or_404(Lot, bbl=kwargs['bbl'])

        context = super(AddParticipantSuccessView, self).get_context_data(**kwargs)
        context['lot'] = lot
        try:
            context['object'] = self.model.objects.filter(email_hash__istartswith=kwargs['email_hash'])[0]
        except Exception:
            raise Http404
        return context


@fix_recaptcha_remote_ip
def edit_organizer(request, bbl=None, id=None):
    lot = get_object_or_404(Lot, bbl=bbl)
    organizer = get_object_or_404(Organizer, id=id)

    if request.method == 'POST':
        form = OrganizerForm(request.POST, instance=organizer)
        if form.is_valid():
            organizer = form.save()
            return redirect('lots.views.details', bbl=bbl)
    else:
        form = OrganizerForm(instance=organizer)

    return render_to_response('organize/edit_organizer.html', {
        'form': form,
        'lot': lot,
    }, context_instance=RequestContext(request))


class EditParticipantMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        hash = self.get_participant_hash()
        context = super(EditParticipantMixin, self).get_context_data(**kwargs)
        context.update({
            'organizers': Organizer.objects.filter(email_hash__istartswith=hash).order_by('added'),
            'watchers': Watcher.objects.filter(email_hash__istartswith=hash).order_by('added'),
        })
        return context

    def get_participant_hash(self):
        raise NotImplementedError('Implement get_participant_hash() to use '
                                  'EditParticipantMixin.')


class DeleteParticipantView(DeleteView):

    def get_context_data(self, **kwargs):
        context = super(DeleteParticipantView, self).get_context_data(**kwargs)
        context['target'] = self.object.target
        context['next_url'] = self.request.GET.get('next_url')
        return context

    def get_success_url(self):
        messages.info(self.request, self._get_success_message())
        return self.request.POST.get('next_url', self.object.target.get_absolute_url())

    def _get_success_message(self):
        verb = 'working on'
        if isinstance(self.object, Organizer):
            verb = 'organizing'
        elif isinstance(self.object, Watcher):
            verb = 'watching'
        return 'You are no longer %s %s.' % (verb, self.object.target)


class DeleteOrganizerView(DeleteParticipantView):
    model = Organizer


class DeleteWatcherView(DeleteParticipantView):
    model = Watcher
