from django.contrib import admin

from .models import (DaysAfterAddedMailing, DeliveryRecord)


class DaysAfterAddedMailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_checked', 'days_after_added',)


class DeliveryRecordAdmin(admin.ModelAdmin):
    list_display = ('receiver_object', 'mailing', 'sent', 'recorded',)


admin.site.register(DaysAfterAddedMailing, DaysAfterAddedMailingAdmin)
admin.site.register(DeliveryRecord, DeliveryRecordAdmin)
