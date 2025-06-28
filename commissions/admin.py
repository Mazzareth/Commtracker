from django.contrib import admin
from .models import Commission


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'client_name', 'amount', 'status', 'due_date', 'created_at']
    search_fields = ['title', 'client__nickname', 'client__email', 'client__handle']

    @admin.display(ordering='client__nickname', description='Client')
    def client_name(self, obj):
        return obj.client.nickname
    list_display = ['title', 'client_name', 'amount', 'status', 'due_date', 'created_at']
    list_filter = ['status', 'created_at', 'due_date']
    search_fields = ['title', 'client_name', 'client_email']
    list_editable = ['status']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
