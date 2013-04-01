import sys
import traceback

from django.core.management.base import BaseCommand

from ...models import DataSource


class Command(BaseCommand):
    help = 'Synchronize data sources'

    def handle(self, *args, **options):
        self.stdout.write('sync: Running syncdata')

        for data_source_cls in DataSource.__subclasses__():
            for data_source in data_source_cls.objects.all():
                print 'sync: Synchronizing %s' % data_source.get_name_display()
                try:
                    data_source.synchronize()
                except Exception:
                    print 'There was an exception while synchronizing %s' % (
                        data_source,)
                    traceback.print_exc(file=sys.stdout)
                    continue

        self.stdout.write('sync: Done running syncdata')
