from django.contrib import admin

from feincms.admin import item_editor

from .models import Pathway


class PathwayAdmin(item_editor.ItemEditor):
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
                ('private_owners', 'public_owners', 'specific_public_owners',),
            ],
        }],
        item_editor.FEINCMS_CONTENT_FIELDSET,
    ]

    @classmethod
    def add_extension_options(cls, *f):
        if isinstance(f[-1], dict):     # called with a fieldset
            cls.fieldsets.insert(cls.fieldset_insertion_index, f)
            f[1]['classes'] = list(f[1].get('classes', []))
            f[1]['classes'].append('collapse')
        else:   # assume called with "other" fields
            cls.fieldsets[0][1]['fields'].extend(f)


admin.site.register(Pathway, PathwayAdmin)
