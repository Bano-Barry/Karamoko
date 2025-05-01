from django import forms
from django.contrib.auth import get_user_model
from .models import Competence, Cours, Repetiteur

CustomUser = get_user_model()   
     
class RepetiteurForm(forms.ModelForm):
    class Meta:
        model = Repetiteur
        fields = '__all__'
        widgets = {
            'biographie': forms.Textarea(attrs={
                'class': 'form-control px-4 py-3',
                'placeholder': 'Entrez une biographie',
                'rows': 4,
            }),
            'competences': forms.SelectMultiple(attrs={
                'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white px-4 py-3',
            }),
            'formations': forms.SelectMultiple(attrs={
                'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white px-4 py-3',
            }),
        }

class RepetiteurUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
        'placeholder': 'Entrez votre email',
    }))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
        'placeholder': "Entrez votre nom d'utilisateur",
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

    class Meta:
        model = Repetiteur
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'adresse', 'avatar', 'biographie', 'competences', 'formations']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md py-4 px-3 shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
            }),
            'biographie': forms.Textarea(attrs={
                'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
                'placeholder': 'Entrez une biographie',
                'rows': 4,
            }),
            'competences': forms.SelectMultiple(attrs={
                'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
            }),
            'formations': forms.SelectMultiple(attrs={
                'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
                'placeholder': 'Entrez votre numéro de téléphone',
            }),
            'adresse': forms.TextInput(attrs={
                'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
                'placeholder': 'Entrez votre adresse',
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

        if self.user_instance:
            self.fields['email'].initial = self.user_instance.email
            self.fields['username'].initial = self.user_instance.username
            self.fields['first_name'].initial = self.user_instance.first_name
            self.fields['last_name'].initial = self.user_instance.last_name
            self.fields['phone'].initial = self.user_instance.phone
            self.fields['adresse'].initial = self.user_instance.adresse

    def save(self, commit=True):
        repetiteur = super().save(commit=False)

        if self.user_instance:
            self.user_instance.email = self.cleaned_data['email']
            self.user_instance.username = self.cleaned_data['username']
            self.user_instance.first_name = self.cleaned_data['first_name']
            self.user_instance.last_name = self.cleaned_data['last_name']
            self.user_instance.phone = self.cleaned_data['phone']
            self.user_instance.adresse = self.cleaned_data['adresse']
            if commit:
                self.user_instance.save()

        if commit:
            repetiteur.save()
        return repetiteur
    
class CompetenceForm(forms.ModelForm):
    class Meta:
        model = Competence
        fields = '__all__'
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
                'placeholder': 'Entrez le nom de la compétence',
            }),
        }
        
class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = '__all__'
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
                'placeholder': 'Entrez le titre du cours',
            }),
            'niveau': forms.Select(attrs={
                'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
            }),
            'repetiteur': forms.Select(attrs={
                'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
            }),
        }

class RepetiteurProfileForm(forms.ModelForm):
    class Meta:
        model = Repetiteur
        fields = ['avatar', 'biographie', 'competences', 'formations']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md py-4 px-3 shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
            }),
            'biographie': forms.Textarea(attrs={
                'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
                'placeholder': 'Entrez une biographie',
                'rows': 4,
            }),
            'competences': forms.SelectMultiple(attrs={
                'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
            }),
            'formations': forms.SelectMultiple(attrs={
                'class': 'block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
            }),
        }
