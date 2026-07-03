from django import forms
from django.contrib.auth.models import User
from .models import Compte
from django.utils.translation import gettext_lazy as _

class InscriptionForm(forms.Form):
    nom_utilisateur = forms.CharField(label=_("Nom d'utilisateur"), max_length=150)
    telephone = forms.CharField(label=_("Numéro de téléphone"), max_length=15)
    pin = forms.CharField(label=_("Code PIN (4 chiffres)"), max_length=4, widget=forms.PasswordInput)
    pin_confirmation = forms.CharField(label=_("Confirmez le PIN"), max_length=4, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data.get("pin")
        pin_confirmation = cleaned_data.get("pin_confirmation")

        if pin and not pin.isdigit():
            raise forms.ValidationError(_("Le PIN doit contenir uniquement des chiffres."))
        if pin and len(pin) != 4:
            raise forms.ValidationError(_("Le PIN doit contenir exactement 4 chiffres."))
        if pin != pin_confirmation:
            raise forms.ValidationError(_("Les deux PIN ne correspondent pas."))

        if Compte.objects.filter(telephone=cleaned_data.get("telephone")).exists():
            raise forms.ValidationError(_("Ce numéro de téléphone est déjà utilisé."))
        if User.objects.filter(username=cleaned_data.get("nom_utilisateur")).exists():
            raise forms.ValidationError(_("Ce nom d'utilisateur est déjà pris."))

        return cleaned_data


class ConnexionForm(forms.Form):
    telephone = forms.CharField(label=_("Numéro de téléphone"), max_length=15)
    pin = forms.CharField(label=_("Code PIN"), max_length=4, widget=forms.PasswordInput)
class EnvoiArgentForm(forms.Form):
    telephone_destinataire = forms.CharField(label=_("Numéro du destinataire"), max_length=15)
    montant = forms.DecimalField(label=_("Montant à envoyer"), max_digits=12, decimal_places=2, min_value=1)

class RetraitForm(forms.Form):
    montant = forms.DecimalField(label=_("Montant à retirer"), max_digits=12, decimal_places=2, min_value=1)

class FactureForm(forms.Form):
    FOURNISSEUR_CHOICES = [
        ('SONATEL', 'SONATEL'),
        ('SENELEC', 'SENELEC'),
        ('SENEAU', 'SENEAU'),
        ('WOLOFAL', 'WOLOFAL'),
        ('CANAL+', 'CANAL+'),
        ('RAPIDO', 'RAPIDO'),
    ]
    fournisseur = forms.ChoiceField(label=_("Choisir la facture"), choices=FOURNISSEUR_CHOICES)
    numero_reference = forms.CharField(label=_("Numéro de facture / référence"), max_length=50)
    montant = forms.DecimalField(label=_("Montant à payer"), max_digits=12, decimal_places=2, min_value=1)

class PaiementMarchandForm(forms.Form):
    code_marchand = forms.CharField(label=_("Code marchand (QR)"), max_length=50)
    montant = forms.DecimalField(label=_("Montant à payer"), max_digits=12, decimal_places=2, min_value=1)


class EpargneForm(forms.Form):
    ACTION_CHOICES = [
        ('depot', _('Déposer dans mon épargne')),
        ('retrait', _('Retirer de mon épargne')),
    ]
    action = forms.ChoiceField(label=_("Action"), choices=ACTION_CHOICES)
    montant = forms.DecimalField(label=_("Montant"), max_digits=12, decimal_places=2, min_value=1)


class MicroCreditForm(forms.Form):
    montant = forms.DecimalField(label=_("Montant du crédit demandé"), max_digits=12, decimal_places=2, min_value=1000, max_value=50000)

class ServiceBancaireForm(forms.Form):
    ACTION_CHOICES = [
        ('depot_banque', _('Deposer depuis ma banque vers TAF-TAF')),
        ('retrait_banque', _('Transferer vers ma banque')),
    ]
    BANQUE_CHOICES = [
        ('CBAO', 'CBAO'),
        ('SGBS', 'Societe Generale Senegal'),
        ('ECOBANK', 'Ecobank'),
        ('BICIS', 'BICIS'),
        ('UBA', 'UBA'),
    ]
    action = forms.ChoiceField(label=_("Type d'operation"), choices=ACTION_CHOICES)
    banque = forms.ChoiceField(label=_("Banque"), choices=BANQUE_CHOICES)
    numero_compte = forms.CharField(label=_("Numero de compte bancaire"), max_length=30)
    montant = forms.DecimalField(label=_("Montant"), max_digits=12, decimal_places=2, min_value=1)
