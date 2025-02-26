from django import forms
from datetime import datetime, date
from .models import User, LoanRequest, News


# region login
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Nom d’utilisateur')
    password = forms.CharField(max_length=150, widget=forms.PasswordInput, label='Mot de passe')


class CreateClientForm(forms.ModelForm) :
    sexe = forms.ChoiceField(required=True, choices=[('male', 'Homme'), ('female', 'Femme')])
    birth_date = forms.DateField(
        required=True,
        label="Date de naissance",
        widget=forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'sexe', 'birth_date', 'email']
        labels = {
            "first_name" : "Prénom", 
            "last_name" : "Nom",
            "email" : "Email"
        }
        
    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        if birth_date > datetime.now().date():
            raise forms.ValidationError("La date de naissance ne peut pas être dans le futur")
        age = (date.today() - birth_date).days // 365
        if age < 18 :
            raise forms.ValidationError("Vous devez être majeur")
        return birth_date


class RequestForm(forms.ModelForm):
    class Meta:
        model = LoanRequest
        fields = ["city", "state", "zip_code", "bank", "bank_state",  "naics", "approval_fy", "term", "no_emp", "new_exist",  "create_job", "retained_job", "franchise_code",  "urban_rural", "low_doc", "disbursement_gross",  "gr_appv", "rev_line_cr"]
        labels = {
            "city": "Ville",
            "state": "État",
            "zip_code": "Code postal",
            "bank": "Nom de la banque",
            "bank_state": "État de la banque",
            "naics": "Code NAICS",
            "approval_fy": "Année d'approbation",
            "term": "Durée (en mois)",
            "no_emp": "Nombre d'employés",
            "new_exist": "Statut (Nouveau ou Existant)",
            "create_job": "Nombre d'emplois créés",
            "retained_job": "Nombre d'emplois conservés",
            "franchise_code": "Code de franchise",
            "urban_rural": "Zone (Urbaine ou Rurale)",
            "low_doc": "Documentation allégée (Oui/Non)",
            "disbursement_gross": "Montant brut du prêt",
            "gr_appv": "Montant approuvé",
            "rev_line_cr": "Ligne de crédit renouvelable (Oui/Non)"
        }


class NewsForm(forms.ModelForm) :
    class Meta:
        model = News
        fields = ["title", "content"]
        labels = {
            "title": "Titre",
            "content": "Contenu"
        }





