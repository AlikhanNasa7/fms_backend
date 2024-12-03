from django.contrib import admin
from .models import CustomUser, Farmer, Buyer, Admin
from django.contrib.auth.admin import UserAdmin
from .adminforms import CustomUserChangeForm, CustomUserCreationForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'role','is_staff', 'created_at')
    list_filter = ('is_staff', 'is_active', 'created_at')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'first_name', 'last_name', 'phone_number', 'image', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'updated_at')}),
    )

    readonly_fields = ('created_at', 'updated_at')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'phone_number', 'image' , 'role', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )

    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # If the user is an admin, ensure they have all permissions
        if obj.role == 'Admin':
            admin_profile, created = Admin.objects.get_or_create(user=obj)
            admin_profile.assign_permissions()  # Assign full permissions



@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    pass

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    pass

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    pass

