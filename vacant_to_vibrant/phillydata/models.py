from django.db import models
from django.utils.translation import ugettext_lazy as _

from sync.models import DataSource
from .synchronizers import *


class PhillyDataSource(DataSource):
    """
    A DataSource that is specific to Philadelphia.

    """
    NAME_CHOICES = (
        ('citycouncil', 'City Council'),
        ('lilicenses', 'L&I Licenses'),
        ('liviolations', 'L&I Violations'),
        ('landusearea', 'Land Use Areas'),
        ('opa', 'OPA API'),
        ('planningdistrict', 'Planning Districts'),
        ('praavailableproperties', 'PRA Available Properties'),
        ('taxaccount', 'Tax Accounts'),
        ('waterdept', 'Water Department data'),
        ('zoning', 'Zoning'),
    )
    name = models.CharField(_('name'),
        max_length=50,
        choices=NAME_CHOICES,
    )
