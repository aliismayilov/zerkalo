from django.contrib import admin

from eedition.models import Edition, ScreenShot

class EditionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Edition, EditionAdmin)

class ScreenShotAdmin(admin.ModelAdmin):
    pass
admin.site.register(ScreenShot, ScreenShotAdmin)