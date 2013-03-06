from django.db import models
from django.utils.translation import ugettext_lazy as _

from sync.models import DataSource
from .synchronizers import *


class PhillyDataSource(DataSource):
    """
    A DataSource that is specific to Philadelphia.

    """
    NAME_CHOICES = (
        ('praavailableproperties', 'PRA Available Properties'),
        ('opa', 'OPA API'),
        ('liviolations', 'L&I Violations'),
        ('waterdept', 'Water Department data'),
    )
    name = models.CharField(_('name'),
        max_length=50,
        choices=NAME_CHOICES,
    )
