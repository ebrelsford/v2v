"""
Infrastructure for periodically synchronizing data sources. Users of this
framework should define a Synchronizer sublcass for every DataSource subclass.

"""
from django.utils.timezone import now


def find_synchronizer(source_name):
    target_synchronizer = source_name + 'synchronizer'
    for synchronizer in Synchronizer.__subclasses__():
        if synchronizer.__name__.lower() == target_synchronizer.lower():
            return synchronizer
    return None


def do_synchronize(data_source):
    synchronizer_cls = find_synchronizer(data_source.name)
    synchronizer = synchronizer_cls(data_source)
    synchronizer.sync(data_source)

    data_source.last_synchronized = now()
    data_source.save()
    print 'Done synchronizing with %s' % synchronizer.__class__.__name__


class Synchronizer(object):

    def __init__(self, data_source):
        self.data_source = data_source

    def sync(self):
        raise NotImplementedError('Define sync() in all Synchronizers')
