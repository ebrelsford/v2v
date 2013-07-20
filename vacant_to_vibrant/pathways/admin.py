from django.contrib import admin
from django.db import models

from chosen.forms import ChosenSelectMultiple
from feincms.admin import item_editor
from reversion_compare.admin import CompareVersionAdmin

from .models import Pathway


class PathwayAdmin(item_editor.ItemEditor, CompareVersionAdmin):
    list_display = ['name', 'is_active',]
    list_editable = ['is_active',]
    list_filter = ['is_active',]
    raw_id_fields = ['author']
    search_fields = ['name', 'slug',]
    prepopulated_fields = {
        'slug': ('name',),
    }

    fieldset_insertion_index = 1
    fieldsets = [
        [None, {
            'fields': [
                ('is_active', 'author',),
                ('name', 'slug',),
            ],
        }],
        ['Which lots does this pathway apply to?', {
            'fields': [
                ('private_owners', 'public_owners',),
                'specific_public_owners',
                'is_available_property',
                ('has_licenses', 'has_violations',),
            ],
        }],
        item_editor.FEINCMS_CONTENT_FIELDSET,
    ]

    formfield_overrides = {
        models.ManyToManyField: {
            'widget': ChosenSelectMultiple,
        },
    }

    @classmethod
    def add_extension_options(cls, *f):
        if isinstance(f[-1], dict):     # called with a fieldset
            cls.fieldsets.insert(cls.fieldset_insertion_index, f)
            f[1]['classes'] = list(f[1].get('classes', []))
            f[1]['classes'].append('collapse')
        else:   # assume called with "other" fields
            cls.fieldsets[0][1]['fields'].extend(f)


admin.site.register(Pathway, PathwayAdmin)
