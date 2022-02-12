from patient.models import Patient
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin   

# Register your models here.


# class UA(UserAdmin):
    
#     list_display = ['user'  ]
#     readonly_fields = []
#     search_fields = []
#     ordering = []
#     list_filter = []
#     fieldsets = ()
#     filter_horizontal=()
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'password1', 'password2' , 'email', 'phone_number' ,  'birthdate' , 'is_patient' ),
#         }),
#     )



admin.site.register(Patient)