from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import Account
# Register your models here.

class AccountAdmin(UserAdmin):
        list_display = ('email', 'first_name', 'date_of_birth', 'last_login', 'is_admin', 'is_staff')
        search_fields = ('email', 'first_name')
        readonly_fields = ('date_joined', 'last_login')

        ordering = ('email',)
        
        list_filter = ()
        fieldsets = ()

        add_fieldsets = (
                (None, {
                'classes': ('wide',),
                'fields': ('email', 'last_name', 'first_name', 'password1', 'password2', 'groups', 'user_permissions'),
                }),
        )

admin.site.register(Account, AccountAdmin)