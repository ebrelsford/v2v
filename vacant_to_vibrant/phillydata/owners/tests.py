from django.test import TestCase

from lots.models import Lot
from .models import Owner


class ModelTest(TestCase):

    def test_add_alias(self):
        owner = Owner(name='Test Owner', owner_type='public')
        owner.save()

        owner.add_alias('Alias Name')
        self.assertEquals(owner.aliases.count(), 1)

    def test_make_alias(self):
        owner = Owner(name='Test Owner', owner_type='public')
        owner.save()

        alias_owner = Owner(name='Alias of Test Owner', owner_type='public')
        alias_owner.save()

        owner.make_alias(alias_owner)
        self.assertEquals(owner.aliases.count(), 1)

    def test_make_alias_with_other_aliases(self):
        """
        Test making an alias out of an owner that already has aliases of its
        own.
        """
        owner = Owner(name='Test Owner', owner_type='public')
        owner.save()

        alias_owner = Owner(name='Alias of Test Owner', owner_type='public')
        alias_owner.save()

        alias_owner.add_alias('Alias 1 of Alias of Test Owner')
        alias_owner.add_alias('Alias 2 of Alias of Test Owner')

        self.assertEquals(owner.aliases.count(), 0)

        owner.make_alias(alias_owner)
        self.assertEquals(owner.aliases.count(), 3)

    def test_make_alias_with_related(self):
        """
        Test making an alias out of an owner that has relations on it.
        """
        owner = Owner(name='Test Owner', owner_type='public')
        owner.save()

        alias_owner = Owner(name='Alias of Test Owner', owner_type='public')
        alias_owner.save()

        lot = Lot(owner=alias_owner)
        lot.save()

        self.assertEquals(owner.lot_set.count(), 0)

        owner.make_alias(alias_owner)
        self.assertEquals(owner.lot_set.count(), 1)
