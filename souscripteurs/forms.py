from django import forms
from django.contrib.auth import get_user_model
from .models import Souscripteur

CustomUser = get_user_model()


# Utilitaire pour les widgets communs
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


# Formulaire de création de souscripteur
class SouscripteurCreateForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=get_widget(forms.EmailInput, "Entrez votre email"))
    username = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre nom d'utilisateur"))
    first_name = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre prénom"))
    last_name = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre nom"))
    phone = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre numéro de téléphone"))
    adresse = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre adresse"))
    role = forms.ChoiceField(choices=[('parent', 'Parent'), ('repetiteur', 'Répétiteur')],
        widget=get_widget(forms.Select, ""))
    password = forms.CharField(required=True, widget=get_widget(forms.PasswordInput, "Définir un mot de passe"))

    class Meta:
        model = Souscripteur
        fields = ['avatar']  # Champs spécifiques au modèle Souscripteur
        widgets = {
            'avatar': get_widget(forms.ClearableFileInput, "", "py-4 px-3"),
        }

    def save(self, commit=True):
        # Créer un utilisateur lié
        user_data = {
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'username': self.cleaned_data['username'],
            'email': self.cleaned_data['email'],
            'phone': self.cleaned_data['phone'],
            'adresse': self.cleaned_data['adresse'],
            'role': self.cleaned_data['role'],
            'is_active': True,  # Par défaut, le compte est actif
        }
        user = CustomUser(**user_data)
        user.set_password(self.cleaned_data['password'])  # Hacher le mot de passe

        # Créer un souscripteur lié à l'utilisateur
        souscripteur = super().save(commit=False)
        souscripteur.user = user

        if commit:
            user.save()
            souscripteur.save()

        return souscripteur


# Formulaire de mise à jour de souscripteur
class SouscripteurUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=get_widget(forms.EmailInput, "Entrez votre email"))
    username = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre nom d'utilisateur"))
    first_name = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre prénom"))
    last_name = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre nom"))
    phone = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre numéro de téléphone"))
    adresse = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre adresse"))
    avatar = forms.ImageField(required=False, widget=get_widget(forms.ClearableFileInput, ""))

    class Meta:
        model = Souscripteur
        fields = ['avatar']

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

        if self.user_instance:
            self.fields['username'].initial = self.user_instance.username
            self.fields['email'].initial = self.user_instance.email
            self.fields['first_name'].initial = self.user_instance.first_name
            self.fields['last_name'].initial = self.user_instance.last_name
            self.fields['phone'].initial = self.user_instance.phone
            self.fields['adresse'].initial = self.user_instance.adresse

    def save(self, commit=True):
        souscripteur = super().save(commit=False)

        if self.user_instance:
            self.user_instance.username = self.cleaned_data['username']
            self.user_instance.email = self.cleaned_data['email']
            self.user_instance.first_name = self.cleaned_data['first_name']
            self.user_instance.last_name = self.cleaned_data['last_name']
            self.user_instance.phone = self.cleaned_data['phone']
            self.user_instance.adresse = self.cleaned_data['adresse']
            if commit:
                self.user_instance.save()

        if commit:
            souscripteur.save()
        return souscripteur


# Formulaire de profil de souscripteur
class SouscripteurProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=get_widget(forms.EmailInput, "Entrez votre email"))
    username = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre nom d'utilisateur"))
    first_name = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre prénom"))
    last_name = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre nom"))
    phone = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre numéro de téléphone"))
    adresse = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre adresse"))

    class Meta:
        model = Souscripteur
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'adresse', 'avatar']
        widgets = {
            'avatar': get_widget(forms.ClearableFileInput, "", "py-4 px-3"),
        }

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

        if self.user_instance:
            # Pré-remplir les champs liés à l'utilisateur
            self.fields['email'].initial = self.user_instance.email
            self.fields['username'].initial = self.user_instance.username
            self.fields['first_name'].initial = self.user_instance.first_name
            self.fields['last_name'].initial = self.user_instance.last_name
            self.fields['phone'].initial = self.user_instance.phone
            self.fields['adresse'].initial = self.user_instance.adresse

    def save(self, commit=True):
        souscripteur = super().save(commit=False)
        if self.user_instance:
            # Mettre à jour les champs de l'utilisateur lié
            self.user_instance.email = self.cleaned_data['email']
            self.user_instance.username = self.cleaned_data['username']
            self.user_instance.first_name = self.cleaned_data['first_name']
            self.user_instance.last_name = self.cleaned_data['last_name']
            self.user_instance.phone = self.cleaned_data['phone']
            self.user_instance.adresse = self.cleaned_data['adresse']
            if commit:
                self.user_instance.save()

        if commit:
            souscripteur.save()
        return souscripteur