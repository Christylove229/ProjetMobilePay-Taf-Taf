from django.contrib import admin
from .models import Compte

@admin.register(Compte)
class CompteAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'telephone', 'solde', 'date_creation')
    search_fields = ('telephone', 'utilisateur__username')