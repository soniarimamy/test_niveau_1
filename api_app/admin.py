from django.contrib import admin
from .models import Test1Result


@admin.register(Test1Result)
class Test1ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'status', 'logs', 'created_at')
    search_fields = ('email', 'status', 'logs', 'created_at')
