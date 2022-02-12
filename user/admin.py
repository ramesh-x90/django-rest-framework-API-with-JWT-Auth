from user.models import AdminAccount , SuperuserAccount , StaffAccount
from django.contrib import admin 
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model


User= get_user_model()

class UserAdmin(BaseUserAdmin):
    
    list_display = ['username' , 'email', 'created_date' , 'last_login' ,'is_superuser', 'is_admin' , 'is_staff' ]
    readonly_fields = [ 'created_date' , 'last_login']
    search_fields = ['email' , 'username' , 'phone_number','birthdate']
    ordering = ['email']
    list_filter = []
    fieldsets = ()
    filter_horizontal=()
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2' , 'email', 'phone_number' ,  'birthdate' ),
        }),
    )

admin.site.register(User, UserAdmin)
admin.site.register(AdminAccount, UserAdmin)
admin.site.register(SuperuserAccount, UserAdmin)
admin.site.register(StaffAccount, UserAdmin)

