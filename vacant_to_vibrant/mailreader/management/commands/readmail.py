import sys
import traceback

from django.core.management.base import BaseCommand

from ...readers import NotesMailReader
from ...util import get_mail


class Command(BaseCommand):
    help = 'Read mail and perform actions as specified by readers'

    readers = (
        NotesMailReader(),
    )

    def handle(self, *args, **options):
        """
        Read mail and perform actions as specified by readers.
        """
        self.stdout.write('mailreader: Running readmail')

        for mail in get_mail():
            for reader in self.readers:
                try:
                    if reader.should_read(**mail):
                        reader.read(verbose=True, **mail)
                except Exception:
                    self.stdout.write('There was an exception while reading '
                                      'mail with reader %s' % str(reader))
                    self.stdout.write('mail: %s', str(mail))
                    traceback.print_exc(file=sys.stdout)
                    traceback.print_stack(file=sys.stdout)

        self.stdout.write('mailreader: Done running readmail')
