from django import forms
from django.contrib.auth import get_user_model
from .models import Competence, Cours, Repetiteur

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


# Formulaire de création de répétiteur
class RepetiteurCreateForm(forms.ModelForm):
    first_name = forms.CharField(
        # required=True, 
        label="Prénom", 
        widget=get_widget(forms.TextInput, "Entrez votre prénom")
    )
    last_name = forms.CharField(
        # required=True, 
        label="Nom", 
        widget=get_widget(forms.TextInput, "Entrez votre nom")
    )
    phone = forms.CharField(
        required=True, 
        label="Numéro de téléphone", 
        widget=get_widget(forms.TextInput, "Entrez votre numéro de téléphone")
    )
    adresse = forms.CharField(
        # required=True, 
        label="Adresse", 
        widget=get_widget(forms.TextInput, "Entrez votre adresse")
    )
    role = forms.ChoiceField(
        required=True,
        choices=[('parent', 'Parent'), ('repetiteur', 'Répétiteur')],
        label="Rôle", 
        widget=get_widget(forms.Select, "")
    )
    password = forms.CharField(
        required=True, 
        label="Mot de passe", 
        widget=get_widget(forms.PasswordInput, "Définir un mot de passe")
    )

    class Meta:
        model = Repetiteur
        fields = [ 'phone', 'role', 'password', 'avatar', 'first_name', 'last_name',  'adresse', 'biographie', ]
        widgets = {
            'avatar': get_widget(forms.ClearableFileInput, "", "py-4 px-3"),
            'biographie': get_widget(forms.Textarea, "Ex : professeur de mathematiques dans les écoles x, y ...", "rows-4"),
            # 'competences': forms.CheckboxSelectMultiple(),
        }

    def save(self, commit=True):
        user_data = {
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'phone': self.cleaned_data['phone'],
            'adresse': self.cleaned_data['adresse'],
            'role': self.cleaned_data['role']
        }
        user = CustomUser(**user_data)
        user.set_password(self.cleaned_data['password'])  # Hacher le mot de passe

        repetiteur = super().save(commit=False)
        repetiteur.user = user
        if commit:
            user.save()
            repetiteur.save()
            self.save_m2m()  # Enregistrer les relations ManyToMany
        return repetiteur


# Formulaire de mise à jour de répétiteur
class RepetiteurUpdateForm(forms.ModelForm):
    # email = forms.EmailField(required=True, widget=get_widget(forms.EmailInput, "Entrez votre email"))
    # username = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre nom d'utilisateur"))
    first_name = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre prénom"))
    last_name = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre nom"))
    phone = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre numéro de téléphone"))
    adresse = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre adresse"))

    class Meta:
        model = Repetiteur
        fields = ['first_name', 'last_name', 'phone', 'adresse', 'avatar', 'biographie']
        widgets = {
            'avatar': get_widget(forms.ClearableFileInput, "", "py-4 px-3"),
            'biographie': get_widget(forms.Textarea, "Entrez une biographie", "rows-4"),
        }

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

        if self.user_instance:
            # self.fields['email'].initial = self.user_instance.email
            # self.fields['username'].initial = self.user_instance.username
            self.fields['first_name'].initial = self.user_instance.first_name
            self.fields['last_name'].initial = self.user_instance.last_name
            self.fields['phone'].initial = self.user_instance.phone
            self.fields['adresse'].initial = self.user_instance.adresse

    def save(self, commit=True):
        repetiteur = super().save(commit=False)
        if self.user_instance:
            # self.user_instance.email = self.cleaned_data['email']
            # self.user_instance.username = self.cleaned_data['username']
            self.user_instance.first_name = self.cleaned_data['first_name']
            self.user_instance.last_name = self.cleaned_data['last_name']
            self.user_instance.phone = self.cleaned_data['phone']
            self.user_instance.adresse = self.cleaned_data['adresse']
            if commit:
                self.user_instance.save()

        if commit:
            repetiteur.save()
        return repetiteur


# Formulaire de compétence
class CompetenceForm(forms.ModelForm):
    class Meta:
        model = Competence
        fields = '__all__'
        widgets = {
            'nom': get_widget(forms.TextInput, "Entrez le nom de la compétence"),
        }


# Formulaire de cours
class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['titre', 'niveaux', 'description']
        labels = {
            'titre': "Titre du cours",
            'description': "Description du cours",
            'niveaux': "Niveaux d'enseignement",
        }
        widgets = {
            'titre': get_widget(forms.TextInput, "Entrez le titre du cours"),
            'description': get_widget(forms.Textarea, "Entrez la description du cours", "rows-4"),
            'niveaux': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-control px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
        }


# Formulaire de profil de répétiteur
class RepetiteurProfileForm(forms.ModelForm):
    # Champs du modèle CustomUser à afficher ici
    first_name = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre prénom"))
    last_name = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre nom"))
    phone = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre numéro de téléphone"))
    adresse = forms.CharField(required=True, widget=get_widget(forms.TextInput, "Entrez votre adresse"))

    class Meta:
        model = Repetiteur
        fields = [
            'first_name',
            'last_name',
            'phone',
            'adresse',
            'avatar',
            'biographie',
            # 'competences',
            'cours',
            'experience',  
            'prix_par_seance',
            'disponibilite_matin',
            'disponibilite_apres_midi',
            'disponibilite_soir',
            'disponibilite_weekend',
            'diplome',
            'contrat_ecole',
            'piece_identite',
        ]
        labels = {
            'avatar': "Avatar",
            'biographie': "Biographie",
            # 'competences': "Compétences",
            'cours': "Cours enseignés",
            'prix_par_seance': "Prix par séance (en GNF)",
            'disponibilite_matin': "Disponible le matin",
            'disponibilite_apres_midi': "Disponible l'après-midi",
            'disponibilite_soir': "Disponible le soir",
            'disponibilite_weekend': "Disponible le weekend",
            'diplome': "Diplôme",
            'contrat_ecole': "Contrat école ou document justificatif",
            'piece_identite': "Pièce d'identité",
            'experience': "Années d'expérience",
        }
        widgets = {
            'avatar': get_widget(forms.ClearableFileInput, "", "py-4 px-3"),
            'biographie': get_widget(forms.Textarea, "Entrez une biographie", "rows-4"),
            'cours': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-control px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'prix_par_seance': get_widget(forms.NumberInput, "Votre tarif par séance"),
            'disponibilite_matin': get_widget(forms.CheckboxInput, "Disponible le matin", "form-check-input"),
            'disponibilite_apres_midi': get_widget(forms.CheckboxInput, "Disponible l'après-midi", "form-check-input"),
            'disponibilite_soir': get_widget(forms.CheckboxInput, "Disponible le soir", "form-check-input"),
            'disponibilite_weekend': get_widget(forms.CheckboxInput, "Disponible le weekend", "form-check-input"),
            'diplome': get_widget(forms.ClearableFileInput, "", "py-2"),
            'contrat_ecole': get_widget(forms.ClearableFileInput, "", "py-2"),
            'piece_identite': get_widget(forms.ClearableFileInput, "", "py-2"),
            'experience': get_widget(forms.NumberInput, "Entrez vos années d'expérience"),
        }

    def clean(self):
        cleaned_data = super().clean()
        required_fields = [
            'avatar',
            'biographie',
            # 'competences',
            'cours',
            'contrat_ecole',
            'prix_par_seance',
            'diplome',
            'piece_identite',
            'experience',
        ]
        for field in required_fields:
            value = cleaned_data.get(field)
            if not value or (hasattr(value, 'exists') and not value.exists()):
                self.add_error(field, "Ce champ est obligatoire.")
        
        return cleaned_data