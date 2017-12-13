from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'total',
        'created_at', 'update_at', 'status',
    )
    list_filter = ('status',)
    filter_horizontal = ('items',)
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
