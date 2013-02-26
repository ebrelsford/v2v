from django.contrib import admin

from reversion_compare.admin import CompareVersionAdmin

from .models import AgencyCode, Alias, Owner


class OwnerAdmin(CompareVersionAdmin):
    list_display = ('name', 'owner_type',)


class AliasAdmin(admin.ModelAdmin):
    list_display = ('name',)


class AgencyCodeAdmin(admin.ModelAdmin):
    list_display = ('code',)

admin.site.register(AgencyCode, AgencyCodeAdmin)
admin.site.register(Alias, AliasAdmin)
admin.site.register(Owner, OwnerAdmin)
