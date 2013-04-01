from django.contrib import admin

from reversion_compare.admin import CompareVersionAdmin

from .models import TaxAccount


class TaxAccountAdmin(CompareVersionAdmin):
    list_display = ('brt_number', 'billing_account', 'building_category',
                    'building_description', 'property_address',
                    'amount_delinquent',)
    list_filter = ('building_category', 'building_description',)
    readonly_fields = ('billing_account',)


admin.site.register(TaxAccount, TaxAccountAdmin)
