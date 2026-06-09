from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'description', 'author__email')
    filter_horizontal = ('participants', 'favorited_by')
