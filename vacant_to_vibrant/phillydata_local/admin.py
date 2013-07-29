from django.core.urlresolvers import reverse
from django.contrib import admin

from phillydata.owners.admin import OwnerAdmin
from phillydata.owners.models import Owner


class OverrideOwnerAdmin(OwnerAdmin):
    fields = ('name', 'owner_type', 'agency_codes', 'aliases', 'view_lots',)
    list_display = ('name', 'owner_type', 'aliases_summary', 'view_lots',)
    readonly_fields = ('aliases', 'view_lots',)

    def view_lots(self, obj):
        try:
            return '<a href="%s?owner=%d">view lots</a>' % (
                reverse('admin:lots_lot_changelist'),
                obj.pk
            )
        except Exception:
            return ''
    view_lots.allow_tags = True


admin.site.unregister(Owner)
admin.site.register(Owner, OverrideOwnerAdmin)
