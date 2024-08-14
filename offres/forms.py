from django import forms
from .models import OffreColis, Demande



from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'numero', 'photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['numero'].widget.attrs.update({'class': 'form-control'})
        self.fields['photo'].widget.attrs.update({'class': 'form-control'})



class OffreColisForm(forms.ModelForm):
    class Meta:
        model = OffreColis
        fields = ['poids_disponible', 'date_voyage', 'ville_depart', 'ville_destination', 'date_limite_contact', 'numero_contact']
        widgets = {
            'date_voyage': forms.DateInput(attrs={'type': 'date'}),
            'date_limite_contact': forms.DateInput(attrs={'type': 'date'}),
        }

class DemandeForm(forms.ModelForm):
    class Meta:
        model = Demande
        fields = ['message',  'numero_contact']

from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Votre message...'}),
        }
        
        
class ReplyMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']