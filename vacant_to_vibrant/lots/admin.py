from django import forms
from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from reversion_compare.admin import CompareVersionAdmin

from phillydata.parcels.models import Parcel
from .models import Lot, Use


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
            lot.centroid = lot.parcel.geometry.centroid
            lot.polygon = lot.parcel.geometry
            lot.save()
        except Exception:
            raise

        return lot

    class Meta:
        model = Lot


class LotAdmin(OSMGeoAdmin, CompareVersionAdmin):
    exclude = ('available_property', 'parcel',)
    form = LotAdminForm
    list_display = ('address_line1', 'city', 'owner', 'known_use',
                    'billing_account',)
    list_filter = ('known_use',)
    readonly_fields = ('added', 'available_property_link', 'billing_account',
                       'land_use_area', 'owner', 'parcel_link', 'tax_account',
                       'violations', 'water_parcel', 'zoning_district',)
    search_fields = ('address_line1',)

    fieldsets = (
        (None, {
            'fields': ('name', 'address_line1', 'address_line2', 'city',
                       'state_province', 'postal_code', 'known_use', 'added',),
        }),
        ('Other data', {
            'classes': ('collapse',),
            'fields': ('owner', 'billing_account', 'tax_account',
                       'parcel_pk', 'parcel_link', 'land_use_area', 'violations',
                       'available_property_link', 'water_parcel',
                       'zoning_district'),
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

    def parcel_link(self, obj):
        change_url = reverse(
            'admin:parcels_parcel_change',
            args=(obj.parcel.pk,)
        )
        return mark_safe('<a href="%s">%s</a>' % (change_url, str(obj.parcel)))
    parcel_link.short_description = 'parcel'


class UseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',),}


admin.site.register(Lot, LotAdmin)
admin.site.register(Use, UseAdmin)
