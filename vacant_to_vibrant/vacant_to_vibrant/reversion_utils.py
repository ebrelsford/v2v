from django.utils.importlib import import_module

from reversion import default_revision_manager


class InitialRevisionManagerMixin(object):

    def _save_initial_revision(self, obj):
        # try to load admin
        try:
            import_module("%s.admin" % obj.__module__.rsplit('.', 1)[0])
        except ImportError:
            pass

        # save revision
        default_revision_manager.save_revision((obj,),
                                               comment='Initial revision')

    def get_or_create(self, **kwargs):
        obj, created = self.get_query_set().get_or_create(**kwargs)
        if created:
            self._save_initial_revision(obj)
        return obj, created
