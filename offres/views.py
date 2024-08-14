from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Demande, OffreColis, Message
from .forms import CustomUserChangeForm, DemandeForm, MessageForm, OffreColisForm, ReplyMessageForm
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from .models import CustomUser
from django.contrib.auth import authenticate, login


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Rediriger vers la page d'accueil ou une autre page
        else:
            messages.error(request, 'Nom d’utilisateur ou mot de passe incorrect.')

    return render(request, 'connexion/login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Vérifier si les mots de passe correspondent
        if password1 == password2:
            # Vérifier si l'utilisateur avec cet email n'existe pas déjà
            if get_user_model().objects.filter(email=email).exists():
                messages.error(request, 'Cet email est déjà utilisé.')
            else:
                # Créer l'utilisateur
                user = get_user_model().objects.create_user(email=email, username=username, password=password1)
                user.save()
                messages.success(request, 'Compte créé avec succès. Vous pouvez maintenant vous connecter.')
                return redirect('connect')
        else:
            messages.error(request, 'Les mots de passe ne correspondent pas.')

    return render(request, 'connexion/signup.html')

from django.db.models import Q

def accueil(request):
    return render(request, 'dashboard/home.html')

def voir_offres(request):
    query = request.GET.get('q')
    offres_colis = OffreColis.objects.all().order_by('-date_voyage')
    
    
    if query:
        offres_colis = offres_colis.filter(
            Q(ville_depart__icontains=query) | Q(ville_destination__icontains=query)
        )
        
    return render(request, 'dashboard/see_offers.html', {
        'offres_colis': offres_colis,
        
        'query': query
    })


def publish_colis(request):
    if request.method == 'POST':
        form = OffreColisForm(request.POST)
        if form.is_valid():
            offre = form.save(commit=False)
            offre.utilisateur = request.user
            # Récupérer le numéro de contact depuis le formulaire et l'assigner à l'offre
            offre.numero_contact = form.cleaned_data['numero_contact']
            offre.save()
            # Redirection vers la page des offres publiées avec l'offre nouvellement créée
            return redirect('home')
    else:
        form = OffreColisForm()
    return render(request, 'dashboard/publish_offers.html', {'form': form})



def creer_demande(request):
    if request.method == 'POST':
        form = DemandeForm(request.POST)
        if form.is_valid():
            demande = form.save(commit=False)
            demande.utilisateur = request.user
            # Récupérer le numéro de contact depuis le formulaire et l'assigner à la demande
            demande.numero_contact = form.cleaned_data['numero_contact']
            demande.save()
            return redirect('voir_demande')  # Redirige vers la liste des demandes après soumission
    else:
        form = DemandeForm()

    return render(request, 'dashboard/create_demand.html', {'form': form})
def voir_demandes(request):
    demandes = Demande.objects.all().order_by('-created_at')
    return render(request, 'dashboard/see_demand.html', {'demandes': demandes})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('update_success')  # Assurez-vous que 'profile' est une URL valide dans vos URLs
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'dashboard/update_profile.html', {'form': form})


def update_success(request):
    return render(request, 'dashboard/update_success.html')

@login_required
def send_message(request, offre_id):
    offre = get_object_or_404(OffreColis, id=offre_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = offre.utilisateur
            message.offre = offre
            message.save()
            return redirect('home')
    else:
        form = MessageForm()
    return render(request, 'dashboard/send_message.html', {'form': form, 'offre': offre})

def inbox(request):
    messages_received = Message.objects.filter(recipient=request.user)
    return render(request, 'dashboard/inbox.html', {'messages_received': messages_received})


@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    if request.method == 'POST':
        form = ReplyMessageForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.sender = request.user
            reply.recipient = message.sender
            reply.offre = message.offre
            reply.parent = message
            reply.save()
            return redirect('inbox')
    else:
        form = ReplyMessageForm()
    return render(request, 'dashboard/view_message.html', {'message': message, 'form': form})


from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView
from allauth.socialaccount.providers.google.views import OAuth2LoginView
from django.http import HttpResponseRedirect
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.helpers import complete_social_login
from urllib.parse import urlencode
from django.conf import settings


def google_login_redirect(request):
    print("Google login redirect view called")

    adapter = GoogleOAuth2Adapter(request)
    callback_url = adapter.get_callback_url(request, 'google_callback')
    authorize_url = 'https://accounts.google.com/o/oauth2/auth'  # Assurez-vous que cela est correct
    
    client_id = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
    
    scope = 'profile email'
    response_type = 'code'

    params = {
        'client_id': client_id,
        'redirect_uri': callback_url,
        'scope': scope,
        'response_type': response_type,
    }

    url = f"{authorize_url}?{urlencode(params)}"
    print(f"Redirecting to: {url}")
    
    return HttpResponseRedirect(url)



def google_callback(request):
    # Ajouter un message de débogage pour vérifier que la vue est appelée
    print("Google callback called")

    # Ajoutez une vérification de l'utilisateur après la connexion
    if request.user.is_authenticated:
        print("User is authenticated:", request.user.username)
        return redirect('home')
    else:
        print("Pas connnecté")
        return redirect('account_login')