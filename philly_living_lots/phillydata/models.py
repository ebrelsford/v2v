from django.db import models
from django.utils.translation import ugettext_lazy as _

from sync.models import DataSource
from .synchronizers import *

# TODO move other apps (violations, opa, ...) into phillydata?

class PhillyDataSource(DataSource):

    NAME_CHOICES = (
        ('praavailableproperties', 'PRA Available Properties'),
        ('opa', 'OPA API'),
        ('liviolations', 'L&I Violations'),
    )
    name = models.CharField(_('name'),
        max_length=50,
        choices=NAME_CHOICES,
    )
