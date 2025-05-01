from django import forms
from django.contrib.auth import get_user_model
from .models import Souscripteur
from authentication.models import CustomUser

CustomUser = get_user_model()   

class SouscripteurForm(forms.ModelForm):
    class Meta:
        model = Souscripteur
        fields = '__all__'
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
            }),
        }

class SouscripteurUpdateForm(forms.ModelForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
        'placeholder': 'Entrez votre nom d\'utilisateur',
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
        'placeholder': 'Entrez votre email',
    }))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
        'placeholder': 'Entrez votre prénom',
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
        'placeholder': 'Entrez votre nom',
    }))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
        'placeholder': 'Entrez votre numéro de téléphone',
    }))
    adresse = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
        'placeholder': 'Entrez votre adresse',
    }))
    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
    }))

    class Meta:
        model = Souscripteur
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'adresse','avatar']

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

class SouscripteurProfileForm(forms.ModelForm):
    class Meta:
        model = Souscripteur
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
            }),
        }