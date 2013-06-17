from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.views.generic.edit import ModelFormMixin

from django_monitor import model_from_queue
from django_monitor.conf import PENDING_STATUS, APPROVED_STATUS
from django_monitor.models import MonitorEntry
from django_monitor.util import moderate_rel_objects


class MonitorMixin(ModelFormMixin):
    """
    A CreateView that moderates the new object when it is created. Adapted
    form django_monitor.util.save_handler.
    """

    def automoderate(self, object, user):
        """Automatically approve the object if the user has permission."""
        opts = self.object.__class__._meta
        mod_perm = '%s.moderate_%s' % (
            opts.app_label.lower(), opts.object_name.lower()
        )
        if user and user.has_perm(mod_perm):
            return APPROVED_STATUS
        return PENDING_STATUS

    def moderate_object(self, obj, user, status):
        """Moderate the given object"""
        me = MonitorEntry.objects.create(
            status = status,
            content_object = obj,
            timestamp = datetime.now()
        )
        me.moderate(status, user)

    def moderate_parents(self, obj, user, status):
        """Create one monitor_entry per moderated parent"""
        monitored_parents = filter(
            lambda x: model_from_queue(x),
            obj._meta.parents.keys()
        )
        for parent in monitored_parents:
            parent_ct = ContentType.objects.get_for_model(parent)
            parent_pk_field = obj._meta.get_ancestor_link(parent)
            parent_pk = getattr(obj, parent_pk_field.attname)
            try:
                me = MonitorEntry.objects.get(
                    content_type = parent_ct, object_id = parent_pk
                )
            except MonitorEntry.DoesNotExist:
                me = MonitorEntry(
                    content_type = parent_ct, object_id = parent_pk,
                )
            me.moderate(status, user)

    def moderate_related(self, obj, user, status):
        """Moderate related objects"""
        model = model_from_queue(obj.__class__)
        if model:
            for rel_name in model['rel_fields']:
                rel_obj = getattr(obj, rel_name, None)
                if rel_obj:
                    moderate_rel_objects(rel_obj, status, user)

    def get_user(self):
        user = self.request.user
        if not user.is_authenticated():
            return None
        return user

    def form_valid(self, form):
        """
        The following things are done after creating an object in moderated class:
        1. Creates monitor entries for object and its parents.
        2. Auto-approves object, its parents & specified related objects if user
        has ``moderate`` permission. Otherwise, they are put in pending.
        """
        if not self.object:
            self.object = form.save()
        user = self.get_user()
        status = self.automoderate(self.object, user)

        self.moderate_object(self.object, user, status)
        self.moderate_parents(self.object, user, status)
        self.moderate_related(self.object, user, status)

        return super(MonitorMixin, self).form_valid(form)
