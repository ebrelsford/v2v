from django.contrib import admin

from .models import TaxAccount


class TaxAccountAdmin(admin.ModelAdmin):
    list_display = ('brt_number', 'billing_account', 'building_category',
                    'building_description', 'property_address',
                    'amount_delinquent',)
    list_filter = ('building_category', 'building_description',)
    readonly_fields = ('billing_account',)


admin.site.register(TaxAccount, TaxAccountAdmin)
