from django.contrib import admin
from .models import CustomUser, OffreColis, Demande, Message
from django.contrib.auth.admin import UserAdmin

# Personnalisation de l'affichage de CustomUser dans l'admin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'numero', 'photo')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('numero', 'photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('numero', 'photo')}),
    )

# Enregistrement des modèles dans l'admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OffreColis)
admin.site.register(Demande)
admin.site.register(Message)
