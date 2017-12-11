from django.contrib import admin
from .models import Sendgrid

@admin.register(Sendgrid)
class SendgridAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'template_id', )
