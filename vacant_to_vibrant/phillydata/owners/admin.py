from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from reversion_compare.admin import CompareVersionAdmin

from .admin_views import MakeAliasesView
from .models import AgencyCode, Alias, Owner


class OwnerAdmin(CompareVersionAdmin):
    actions = ('make_aliases',)
    list_display = ('name', 'owner_type', 'agency_codes_summary',
                    'aliases_summary',)
    list_filter = ('owner_type', 'agency_codes',)
    search_fields = ('name',)

    def agency_codes_summary(self, obj):
        return ', '.join(obj.agency_codes.all().values_list('code', flat=True))
    agency_codes_summary.short_description = 'Agency Codes'

    def aliases_summary(self, obj):
        return ', '.join(obj.aliases.all().values_list('name', flat=True))
    aliases_summary.short_description = 'AKA'

    def make_aliases(self, request, queryset):
        ids = queryset.values_list('pk', flat=True)
        ids = [str(id) for id in ids]
        return HttpResponseRedirect(reverse('admin:owners_owner_make_aliases') +
                                    '?ids=%s' % (','.join(ids)))

    def get_urls(self):
        opts = self.model._meta
        app_label, object_name = (opts.app_label, opts.object_name.lower())
        prefix = "%s_%s" % (app_label, object_name)

        urls = super(OwnerAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^make-aliases/', MakeAliasesView.as_view(),
                name='%s_make_aliases' % prefix),
        )
        return my_urls + urls


class AliasAdmin(admin.ModelAdmin):
    list_display = ('name',)


class AgencyCodeAdmin(admin.ModelAdmin):
    list_display = ('code',)


admin.site.register(AgencyCode, AgencyCodeAdmin)
admin.site.register(Alias, AliasAdmin)
admin.site.register(Owner, OwnerAdmin)
