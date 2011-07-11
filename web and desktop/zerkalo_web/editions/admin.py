from django.contrib import admin

from editions.models import Edition, Chapter

class ChapterInline(admin.TabularInline):
    model = Chapter

class EditionAdmin(admin.ModelAdmin):
    list_filter = ['date']
    inlines = [ ChapterInline ]

admin.site.register(Edition, EditionAdmin)