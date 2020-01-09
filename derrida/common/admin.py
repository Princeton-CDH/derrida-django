from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class NamedNotableAdmin(admin.ModelAdmin):
    '''Generic model admin for named/notable models.'''
    list_display = ('name', 'has_notes')
    # fields = ('name', 'notes')
    search_fields = ('name', 'notes')


class LocalUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('is_superuser', 'is_active',
                                             'last_login')


admin.site.unregister(User)
admin.site.register(User, LocalUserAdmin)
