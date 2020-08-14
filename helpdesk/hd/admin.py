from django.contrib import admin

from . import models


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.ClaimModel, UserAdmin)
admin.site.register(models.CommentModel, UserAdmin)
