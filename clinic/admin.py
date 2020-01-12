from django.contrib import admin
from .models import Clinic, Doctor, UserProfile, Comment


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'surname',
        'email'
    )
    prepopulated_fields = {'slug': ('name', )}
    search_fields = ('name',)
    list_filter = ('name', 'created')


@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'address',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'created', 'active')
    list_filter = ('created',)
    search_fields = ('name', 'body')
    actions = ['approve_comments']

    def approve_comments(self, queryset):
        queryset.update(active=True)




