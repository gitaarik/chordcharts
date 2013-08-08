from django.core import urlresolvers
from django.contrib import admin

from models import Chart, Section, Measure, Chord, ChordType, Note, Key


class ChordInline(admin.TabularInline):
    model = Chord
    extra = 0


class MeasureAdmin(admin.ModelAdmin):
    inlines = (ChordInline,)


class MeasureInline(admin.TabularInline):
    model = Measure
    extra = 0


class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'chart', 'key', 'position',
        'key_distance_from_chart')
    inlines = (MeasureInline,)


class SectionInline(admin.StackedInline):

    model = Section
    extra = 0
    readonly_fields = ('change',)

    def change(self, instance):

        if instance.id:
            # Replace "myapp" with the name of the app containing
            # your Certificate model:
            change_chord_item_url = urlresolvers.reverse(
                'admin:chordcharts_section_change', args=(instance.id,)
            )

            return '<a class="changelink" href="{}">Change</a>'.format(
                change_chord_item_url)

        else:
            return 'Save the chart first before editing the section.'

    change.allow_tags = True


class ChartAdmin(admin.ModelAdmin):
    list_display = ('song', 'key')
    inlines = (SectionInline,)


class ChordTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'chord_output', 'order')


class NoteInline(admin.TabularInline):
    model = Note
    extra = 0


class KeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'tone', 'tonality', 'distance_from_c',
        'order')
    prepopulated_fields = {'slug': ('name',)}
    inlines = (NoteInline,)


admin.site.register(Chart, ChartAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(ChordType, ChordTypeAdmin)
admin.site.register(Key, KeyAdmin)
