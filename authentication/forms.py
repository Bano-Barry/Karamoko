from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser

def get_widget(input_type, placeholder, additional_classes=""):
    base_classes = (
        "block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm "
        "focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 "
        "dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"
    )
    return input_type(attrs={
        'class': f"{base_classes} {additional_classes}",
        'placeholder': placeholder,
    })

class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(
        label="Téléphone",
        widget=get_widget(forms.TextInput, "Entrez votre numéro de téléphone")
    )
    first_name = forms.CharField(
        label="Prénom",
        widget=get_widget(forms.TextInput, "Entrez votre prénom")
    )
    last_name = forms.CharField(
        label="Nom de famille",
        widget=get_widget(forms.TextInput, "Entrez votre nom de famille")
    )
    role = forms.ChoiceField(
        label="Rôle",
        choices=CustomUser.ROLE_CHOICES,
        widget=get_widget(forms.Select, "")
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=get_widget(forms.PasswordInput, "Entrez votre mot de passe")
    )
    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=get_widget(forms.PasswordInput, "Confirmez votre mot de passe")
    )
    cgu_acceptees = forms.BooleanField(
        required=True, 
        label="J'accepte les Conditions Générales d'Utilisation", 
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox h-4 w-4 text-blue-600 focus:ring-blue-500'})
    )
    class Meta:
        model = CustomUser
        fields = ['phone', 'first_name', 'last_name', 'role', 'password1', 'password2', 'cgu_acceptees']

class CustomLoginForm(forms.Form):
    phone = forms.CharField(
        label="Numéro de téléphone",
        widget=get_widget(forms.TextInput, "Entrez votre numéro de téléphone")
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=get_widget(forms.PasswordInput, "Entrez votre mot de passe")
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # On récupère et enlève request des kwargs
        super().__init__(*args, **kwargs)
    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')
        password = cleaned_data.get('password')
        if phone and password:
            self.user = authenticate(phone=phone, password=password)
            if self.user is None:
                raise forms.ValidationError("Numéro de téléphone ou mot de passe incorrect.")
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)
