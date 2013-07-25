from django import forms
from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe

from reversion_compare.admin import CompareVersionAdmin

from phillydata.parcels.models import Parcel
from .admin_views import AddToGroupView
from .models import Lot, LotGroup, Use


class LotAdminForm(forms.ModelForm):

    parcel_pk = forms.IntegerField(
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(LotAdminForm, self).__init__(*args, **kwargs)

        # Set parcel_pk if Lot has parcel
        try:
            self.fields['parcel_pk'].initial = self.instance.parcel.pk
        except Exception:
            pass

    def save(self, *args, **kwargs):
        lot = super(LotAdminForm, self).save(*args, **kwargs)

        # Give lot the parcel with parcel_pk
        try:
            parcel_pk = self.cleaned_data['parcel_pk']
            lot.parcel = Parcel.objects.get(pk=parcel_pk)

            polygon_tied_to_parcel = self.cleaned_data['polygon_tied_to_parcel']
            if polygon_tied_to_parcel:
                lot.centroid = lot.parcel.geometry.centroid
                lot.polygon = lot.parcel.geometry
        except Exception:
            # It's okay to have lots without parcels sometimes (eg, with
            # LotGroup instances).
            pass

        lot.save()
        return lot

    class Meta:
        model = Lot


class LotAdmin(OSMGeoAdmin, CompareVersionAdmin):
    actions = ('add_to_group',)
    exclude = ('available_property', 'parcel',)
    form = LotAdminForm
    list_display = ('address_line1', 'city', 'name', 'owner_link', 'known_use',
                    'billing_account',)
    list_filter = ('known_use',)
    readonly_fields = ('added', 'available_property_link', 'billing_account',
                       'city_council_district', 'land_use_area', 'owner_link',
                       'parcel_link', 'tax_account', 'violations',
                       'water_parcel', 'zoning_district',)
    search_fields = ('address_line1', 'name',)

    fieldsets = (
        (None, {
            'fields': ('name', 'address_line1', 'address_line2', 'city',
                       'state_province', 'postal_code', 'group', 'added',),
        }),
        ('Known use', {
            'fields': ('known_use', 'known_use_certainty',
                       'known_use_locked',),
        }),
        ('Stewards', {
            'fields': ('steward_inclusion_opt_in',),
        }),
        ('Other data', {
            'classes': ('collapse',),
            'fields': ('owner_link', 'billing_account', 'tax_account',
                       'parcel_pk', 'parcel_link', 'land_use_area',
                       'violations', 'available_property_link', 'water_parcel',
                       'city_council_district', 'zoning_district',
                       'polygon_area', 'polygon_width',
                       'polygon_tied_to_parcel',),
        }),
        ('Geography', {
            'classes': ('collapse',),
            'fields': ('centroid', 'polygon',),
        }),
    )

    def available_property_link(self, obj):
        change_url = reverse(
            'admin:availableproperties_availableproperty_change',
            args=(obj.available_property.pk,)
        )
        return mark_safe('<a href="%s">%s</a>' % (change_url,
                                                  str(obj.available_property)))
    available_property_link.short_description = 'public available property record'

    def owner_link(self, obj):
        try:
            return '<a href="%s">%s</a>' % (
                reverse('admin:owners_owner_change', args=(obj.owner.pk,)),
                obj.owner.name,
            )
        except Exception:
            return ''
    owner_link.allow_tags = True
    owner_link.short_description = 'Owner'

    def parcel_link(self, obj):
        change_url = reverse(
            'admin:parcels_parcel_change',
            args=(obj.parcel.pk,)
        )
        return mark_safe('<a href="%s">%s</a>' % (change_url, str(obj.parcel)))
    parcel_link.short_description = 'parcel'

    def add_to_group(self, request, queryset):
        ids = queryset.values_list('pk', flat=True)
        ids = [str(id) for id in ids]
        return HttpResponseRedirect(reverse('admin:lots_lot_add_to_group') +
                                    '?ids=%s' % (','.join(ids)))

    def get_urls(self):
        opts = self.model._meta
        app_label, object_name = (opts.app_label, opts.object_name.lower())
        prefix = "%s_%s" % (app_label, object_name)

        urls = super(LotAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^add-to-group/', AddToGroupView.as_view(),
                name='%s_add_to_group' % prefix),
        )
        return my_urls + urls


class LotInlineAdmin(admin.TabularInline):
    model = Lot

    extra = 0
    fields = ('address_line1', 'name',)
    readonly_fields = ('address_line1', 'name',)
    template = 'admin/lots/lot/edit_inline/tabular.html'


class LotGroupAdmin(LotAdmin):
    inlines = (LotInlineAdmin,)


class UseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',),}


admin.site.register(Lot, LotAdmin)
admin.site.register(LotGroup, LotGroupAdmin)
admin.site.register(Use, UseAdmin)
