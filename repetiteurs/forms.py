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
        fields = [ 'phone', 'role', 'password', 'avatar', 'first_name', 'last_name',  'adresse', 'biographie', 'competences']
        widgets = {
            'avatar': get_widget(forms.ClearableFileInput, "", "py-4 px-3"),
            'biographie': get_widget(forms.Textarea, "Ex : professeur de mathematiques dans les écoles x, y ...", "rows-4"),
            'competences': forms.CheckboxSelectMultiple(),
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
        fields = ['first_name', 'last_name', 'phone', 'adresse', 'avatar', 'biographie', 'competences']
        widgets = {
            'avatar': get_widget(forms.ClearableFileInput, "", "py-4 px-3"),
            'biographie': get_widget(forms.Textarea, "Entrez une biographie", "rows-4"),
            'competences': get_widget(forms.SelectMultiple, ""),
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

        repetiteur.competences.set(self.cleaned_data.get('competences', repetiteur.competences.all()))
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
        fields = '__all__'
        widgets = {
            'titre': get_widget(forms.TextInput, "Entrez le titre du cours"),
            'description': get_widget(forms.Textarea, "Entrez la description du cours", "rows-4"),
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
            'first_name', 'last_name', 'phone', 'adresse',  # pas dans Repetiteur, mais gérés via user_instance
            'avatar',
            'biographie',
            'competences',
            'cours',
            # 'zone',
            'prix_par_seance',
            'diplome',
            'contrat_ecole',
            'piece_identite',
        ]
        widgets = {
            'avatar': get_widget(forms.ClearableFileInput, "", "py-4 px-3"),
            'biographie': get_widget(forms.Textarea, "Entrez une biographie", "rows-4"),
            'competences': forms.CheckboxSelectMultiple(),
            'cours': forms.CheckboxSelectMultiple(),
            # 'zone': get_widget(forms.TextInput, "Votre zone géographique"),
            'prix_par_seance': get_widget(forms.NumberInput, "Votre tarif par séance"),
            'diplome': get_widget(forms.ClearableFileInput, "", "py-2"),
            'contrat_ecole': get_widget(forms.ClearableFileInput, "", "py-2"),
            'piece_identite': get_widget(forms.ClearableFileInput, "", "py-2"),
        }

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

        if self.user_instance:
            self.fields['first_name'].initial = self.user_instance.first_name
            self.fields['last_name'].initial = self.user_instance.last_name
            self.fields['phone'].initial = self.user_instance.phone
            self.fields['adresse'].initial = self.user_instance.adresse

    def clean(self):
        cleaned_data = super().clean()
        required_fields = [
            'avatar',
            'biographie',
            'competences',
            'cours',
            # 'zone',
            'prix_par_seance',
            'diplome',
            'piece_identite',
        ]
        for field in required_fields:
            value = cleaned_data.get(field)
            if not value or (hasattr(value, 'exists') and not value.exists()):
                self.add_error(field, "Ce champ est obligatoire.")

    def save(self, commit=True, submit_final=False):
        repetiteur = super().save(commit=False)

        # Update les champs du user
        if self.user_instance:
            self.user_instance.first_name = self.cleaned_data['first_name']
            self.user_instance.last_name = self.cleaned_data['last_name']
            self.user_instance.phone = self.cleaned_data['phone']
            self.user_instance.adresse = self.cleaned_data['adresse']
            if commit:
                self.user_instance.save()

        # Update les champs Repetiteur
        repetiteur.avatar = self.cleaned_data.get('avatar', repetiteur.avatar)
        repetiteur.biographie = self.cleaned_data.get('biographie', repetiteur.biographie)
        repetiteur.piece_identite = self.cleaned_data.get('piece_identite', repetiteur.piece_identite)
        repetiteur.diplome = self.cleaned_data.get('diplome', repetiteur.diplome)
        repetiteur.contrat_ecole = self.cleaned_data.get('contrat_ecole', repetiteur.contrat_ecole)
        repetiteur.prix_par_seance = self.cleaned_data.get('prix_par_seance', repetiteur.prix_par_seance)

        if commit:
            repetiteur.save()

        repetiteur.competences.set(self.cleaned_data.get('competences', repetiteur.competences.all()))
        repetiteur.cours.set(self.cleaned_data.get('cours', repetiteur.cours.all()))

        # 👉 Gère ici la soumission finale
        if submit_final and repetiteur.is_profile_complete():
            repetiteur.is_soumis = True
            if commit:
                repetiteur.save()

        return repetiteur
