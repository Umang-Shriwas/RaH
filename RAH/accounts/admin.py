from django.contrib import admin

# Register your models here.
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser,MultiToken


class CustomUserAdmin(BaseUserAdmin):
    
    model = CustomUser
    list_display = ["email" , "first_name","last_name", "phone_number", "address","profile_image","is_active" ] 
    search_fields = ["email", "first_name", "last_name", "phone_number",]
   
    fieldsets = (
        ('User Details', {'fields': ('email','password')}),
        ('Personal Details', {'fields': ('first_name', 'last_name', 'phone_number','address','profile_image',)}),
        ('Permission Info', {
            'classes': ('wide',),
            'fields': ('is_staff', 'is_active', 'is_superuser','groups', 'user_permissions')}
        )
    )
    
    add_fieldsets = (
        ('Personal Info', {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'profile_image', 'phone_number', 'password1', 'password2')}
        ),
    )
    ordering = ('email',)
    filter_horizontal = ['groups', 'user_permissions']


admin.site.unregister(Group)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(MultiToken)

