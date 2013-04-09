from django.contrib import admin

from .models import CityCouncilMember


class CityCouncilMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'district',)
    search_fields = ('name',)

admin.site.register(CityCouncilMember, CityCouncilMemberAdmin)
