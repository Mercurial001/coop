from django.contrib import admin
from .models import CashIn
from .models import CashOut
from .models import Profile
from .models import DailyRecord
from .models import MissionVision


class MissionVisionAdmin(admin.ModelAdmin):
    list_display = ('title',)


class CashOutAdmin(admin.ModelAdmin):
    list_display = ('name', 'cash_out')


class CashInAdmin(admin.ModelAdmin):
    list_display = ('name', 'cash_in')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_name',)


class DailyRecordAdmin(admin.ModelAdmin):
    list_display = ('date',)


admin.site.register(CashIn, CashInAdmin)
admin.site.register(CashOut, CashOutAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(DailyRecord, DailyRecordAdmin)
admin.site.register(MissionVision, MissionVisionAdmin)
