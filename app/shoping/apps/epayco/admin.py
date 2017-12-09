from django.contrib import admin

from .models import EpayCo

@admin.register(EpayCo)
class EpayCoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'client_id', 'p_key', 'test',)
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
