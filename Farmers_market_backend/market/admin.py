from django.contrib import admin
from .models import Farm, FarmRank

@admin.register(Farm)
class AdminFarm(admin.ModelAdmin):
    pass


@admin.register(FarmRank)
class AdminFarmRank(admin.ModelAdmin):
    pass

