from django.contrib import admin
from .models import Client, Character, Tag, Commission, ClientNote, CommissionNote

class ClientNoteInline(admin.StackedInline):
    model = ClientNote
    extra = 0

class CommissionNoteInline(admin.StackedInline):
    model = CommissionNote
    extra = 0

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    inlines = [ClientNoteInline]
    list_display = ('nickname', 'handle', 'email', 'created_at')

@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    inlines = [CommissionNoteInline]
    list_display = ['title', 'client_name', 'amount', 'status', 'due_date', 'created_at']
    list_filter = ['status', 'created_at', 'due_date']
    search_fields = ['title', 'client__nickname', 'client__email', 'client__handle']
    list_editable = ['status']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']

    @admin.display(ordering='client__nickname', description='Client')
    def client_name(self, obj):
        return obj.client.nickname

admin.site.register(Character)
admin.site.register(Tag)