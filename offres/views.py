from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Demande, OffreColis
from .forms import CustomUserChangeForm, DemandeForm, OffreColisForm
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
            return redirect('accueil')  # Rediriger vers la page d'accueil ou une autre page
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
                return redirect('login')
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
            return redirect('voir_offres')
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
