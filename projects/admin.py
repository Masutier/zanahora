from django.contrib import admin
from .models import Project, Video


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'email', 'phoneNum', 'modelo')


class VideoAdmin(admin.ModelAdmin):
    list_display = ('title')


admin.site.register(Project)
admin.site.register(Video)

