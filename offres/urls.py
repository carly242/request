from django.urls import path
from .views import *

urlpatterns = [
    path('login/',user_login, name='login' ),
    path('signup/',signup, name='signup' ),
    path('', accueil, name='accueil'),
    path('voir-offres/', voir_offres, name='voir_offres'),
    path('publier-offre-colis/', publish_colis, name='publier_offre_colis'),
    path('demand/',creer_demande, name='demand' ),
    path('voir_demande/', voir_demandes, name='voir_demande' ),
    path('update_profile/', update_profile, name='update_profile'),
    path('update_success/', update_success, name='update_success'),

    
]
