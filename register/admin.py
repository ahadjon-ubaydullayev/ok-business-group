from django.contrib import admin
from .models import *


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'filled_date']


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'first_name', 'tel_number']
