import traceback
from urllib2 import URLError

from django.core.exceptions import MultipleObjectsReturned

import reversion

from lots.load import find_opa_details, load_lots_available
from lots.models import Lot
from sync.synchronizers import Synchronizer
from .availableproperties.models import AvailableProperty
from .availableproperties.reader import AvailablePropertyReader


class OPASynchronizer(Synchronizer):
    """
    A Synchronizer that updates ownership data using the OPA API.

    """
    def sync(self, data_source):
        self.update_owner_data()

    def update_owner_data(self):
        for lot in Lot.objects.filter(owner__isnull=True):
            find_opa_details(lot)


class PRAAvailablePropertiesSynchronizer(Synchronizer):
    """
    Attempts to synchronize the local database with the available properties
    as listed by the Philadelphia Redevelopment Authority.

    As the PRA's data does not include timestamps for available properties,
    we load all available properties every time we synchronize, marking new
    ones (status == 'new and available'), existing ones (status ==
    'available'), and properties no longer in the PRA's data (status == 'no
    longer available').

    Once the above is accomplished, we load lots for available properties that
    are new.

    """
    def sync(self, data_source):
        print 'Synchronizing data for Available Properties'

        # update currently available properties
        try:
            reader = AvailablePropertyReader()
            for feature in reader:
                self.create_or_update(reader, feature)
            print 'Done adding data for current Available Properties'

            # check for AvailableProperty objects that were not seen this time
            no_longer_available = AvailableProperty.objects.filter(
                last_seen__lt=data_source.last_synchronized
            )
            no_longer_available.update(status='no longer available')
            print 'Done updating %d no-longer-available Available Properties' % (
                no_longer_available.count(),
            )
        except URLError:
            print ('Synchronizing Available Properties was interrupted by '
                   'exception')
            traceback.print_stack()
            data_source.healthy = False
            data_source.save()

        # add appropriate lots for newly-added Available Properties
        # TODO or is this its own Synchronizer?
        load_lots_available(added_after=data_source.last_synchronized)

    @reversion.create_revision()
    def create_or_update(self, reader, feature):
        try:
            field_dict = reader.model_defaults(feature)
            model, created = AvailableProperty.objects.get_or_create(
                defaults=field_dict,
                **reader.model_get_kwargs(feature)
            )
            if not created:
                field_dict['status'] = 'available'
                AvailableProperty.objects.filter(pk=model.pk).update(**field_dict)
                model = AvailableProperty.objects.get(pk=model.pk)
        except MultipleObjectsReturned:
            # TODO try to narrow it down?
            print ('Multiple objects found when searching for '
                   'AvailableProperty objects with kwargs:',
                   reader.model_get_kwargs(feature))
        return model


class LIViolationsSynchronizer(Synchronizer):

    def sync(self, data_source):
        print 'hi, i am syncing over here'
        # TODO
        # update database
        # then update lots
        pass
