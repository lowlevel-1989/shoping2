from django.contrib import admin
from django.utils.html import format_html
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'preview')
    ordering = ('price',)
