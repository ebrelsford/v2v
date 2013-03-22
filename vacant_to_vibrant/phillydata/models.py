from django.db import models
from django.utils.translation import ugettext_lazy as _

from sync.models import DataSource
from .synchronizers import *


class PhillyDataSource(DataSource):
    """
    A DataSource that is specific to Philadelphia.

    """
    NAME_CHOICES = (
        ('liviolations', 'L&I Violations'),
        ('landusearea', 'Land Use Areas'),
        ('opa', 'OPA API'),
        ('praavailableproperties', 'PRA Available Properties'),
        ('waterdept', 'Water Department data'),
    )
    name = models.CharField(_('name'),
        max_length=50,
        choices=NAME_CHOICES,
    )
