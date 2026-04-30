from django.contrib import admin
from .models import KibaliUser, Permit


@admin.register(KibaliUser)
class KibaliUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email']


@admin.register(Permit)
class PermitAdmin(admin.ModelAdmin):
    list_display = ['permit_number', 'jina', 'aina', 'created_by', 'tarehe_kutolewa', 'tarehe_mwisho']
    list_filter = ['aina', 'tarehe_kutolewa', 'created_at']
    search_fields = ['permit_number', 'jina', 'pahala']
    readonly_fields = ['permit_number', 'created_at', 'updated_at']
