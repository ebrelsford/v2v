from django.contrib import admin

from reversion_compare.admin import CompareVersionAdmin

from .models import WaterAccount, WaterParcel


class WaterAccountAdmin(CompareVersionAdmin):
    list_display = ('account_id', 'account_status', 'service_type_label',)
    readonly_fields = ('water_parcel',)


class WaterParcelAdmin(CompareVersionAdmin):
    list_display = ('parcel_id', 'owner1', 'owner2', 'address',
                    'building_type',)


admin.site.register(WaterAccount, WaterAccountAdmin)
admin.site.register(WaterParcel, WaterParcelAdmin)
