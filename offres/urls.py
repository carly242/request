from django.urls import path
from .views import *

urlpatterns = [
    path('connect/',user_login, name='connect' ),
    
    path('signup/',signup, name='signup' ),
    
    path('accueil/', accueil, name='accueil'),
    
    path('', voir_offres, name='home'),
    
    path('publier-offre-colis/', publish_colis, name='publier_offre_colis'),
    
    path('demand/',creer_demande, name='demand' ),
    
    path('voir_demande/', voir_demandes, name='voir_demande' ),
    
    path('update_profile/', update_profile, name='update_profile'),
    
    path('update_success/', update_success, name='update_success'),
    
    path('send_message/<int:offre_id>/', send_message, name='send_message'),
    
    path('inbox/', inbox, name='inbox'),
    
    path('message/<int:message_id>/', view_message, name='view_message'),
    
    path('accounts/google/login/', google_login_redirect, name='google-login-redirect'),
    
    path('accounts/google/login/callback/', google_callback, name='google_callback'),



    
]
