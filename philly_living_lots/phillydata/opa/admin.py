from django.contrib import admin

from reversion_compare.admin import CompareVersionAdmin

from .models import BillingAccount, AccountOwner


class BillingAccountAdmin(CompareVersionAdmin):
    list_display = ('property_address', 'mailing_name', 'mailing_address',)
    list_filter = ('improvement_description',)
    search_fields = ('property_address', 'mailing_name', 'mailing_address',)


class AccountOwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner',)

admin.site.register(BillingAccount, BillingAccountAdmin)
admin.site.register(AccountOwner, AccountOwnerAdmin)
