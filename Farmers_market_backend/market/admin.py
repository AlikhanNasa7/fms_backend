from django.contrib import admin
from .models import Farm, FarmRank, FarmAnalytics

@admin.register(Farm)
class AdminFarm(admin.ModelAdmin):
    pass


@admin.register(FarmRank)
class AdminFarmRank(admin.ModelAdmin):
    pass


@admin.register(FarmAnalytics)
class AdminFarmAnalytics(admin.ModelAdmin):
    pass