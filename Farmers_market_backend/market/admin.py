from django.contrib import admin
from .models import Farm, FarmRank, FarmAnalytics
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import format_html
from .models import Farmer, CustomUser
from .forms import FarmerRejectionForm
from django.shortcuts import render

# Custom filter for `is_active` status of the related `Farmer`
# class FarmAdmin(admin.ModelAdmin):
#     list_display = ('farm_name', 'farm_size', 'farm_location', 'is_active', 'farmer_name')  # Display these fields
#     list_filter = ('is_active',)  # Filter by is_active status in the sidebar
#     search_fields = ('farm_name', 'farm_location')  # Search fields
#
#     def farmer_name(self, obj):
#         # Display the farmer's first name in the admin listing
#         return obj.farmer_id.user.first_name
#
#     farmer_name.short_description = 'Farmer Name'
#
#     # Optional: Sorting by `is_active` so that active farms come first
#     ordering = ('is_active',)
#
#
# # Register the admin class
# admin.site.register(Farm, FarmAdmin)


# @admin.register(Farm)
# class AdminFarm(admin.ModelAdmin):
#     pass


class FarmAdmin(admin.ModelAdmin):
    list_display = ('farm_name', 'farm_size', 'farm_location', 'status', 'action_buttons')
    list_filter = ('status',)  # Filter by status (Pending, Approved, Rejected)
    actions = ['approve_farmer', 'reject_farmer']

    # Display a custom button for approval/rejection
    def action_buttons(self, obj):
        if obj.status == 'Pending':
            approve_button = format_html('<a class="button" href="{}">Approve</a>', f'/admin/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/approve/')
            reject_button = format_html('<a class="button" href="{}">Reject</a>', f'/admin/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/reject/')
            return approve_button + ' ' + reject_button
        return '-'
    action_buttons.short_description = 'Actions'

    def approve_farmer(self, request, queryset):
        for farm in queryset:
            # Approve the farmer and activate their account
            farmer = farm.farmer_id
            farmer.user.is_active = True
            farmer.user.save()
            farm.is_active = True
            farm.status = "Approved"
            farm.save()

            # Send an email notifying the farmer of approval
            send_mail(
                'Your Farm has been approved',
                'Congratulations! Your farm is now approved. You can now access the product listing features.',
                settings.DEFAULT_FROM_EMAIL,
                [farmer.user.email],
                fail_silently=False,
            )
        self.message_user(request, f'{queryset.count()} farmers approved.')
    approve_farmer.short_description = "Approve Farmers"

    def reject_farmer(self, request, queryset):
        # Handle form submission
        for farm in queryset:
            farmer = farm.farmer_id
            farmer.user.is_active = False
            farmer.user.save()

            farm.is_active = False
            farm.status = 'Rejected'
            farm.save()
            send_mail(
                'Your Farm has been rejected',
                f'We are sorry to inform you that your farm has been rejected.',
                settings.DEFAULT_FROM_EMAIL,
                [farmer.user.email],
                fail_silently=False,
            )
        self.message_user(request, f'{queryset.count()} farmers rejected.')
    approve_farmer.short_description = "Reject Farmers"



# Register the admin class
admin.site.register(Farm, FarmAdmin)

# Register the admin model
# admin.site.register(Farmer, FarmerAdmin)



@admin.register(FarmRank)
class AdminFarmRank(admin.ModelAdmin):
    pass


@admin.register(FarmAnalytics)
class AdminFarmAnalytics(admin.ModelAdmin):
    pass