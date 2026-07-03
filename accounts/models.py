from django.db import models
from django.contrib.auth.models import User
class Compte(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=15, unique=True)
    pin = models.CharField(max_length=4)
    solde = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    solde_epargne = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.telephone}"
    
class Transaction(models.Model):
    expediteur = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='transactions_envoyees')
    destinataire = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='transactions_recues')
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.expediteur} -> {self.destinataire} : {self.montant}"
    
class Operation(models.Model):
    TYPE_CHOICES = [
        ('retrait', 'Retrait'),
        ('facture', 'Paiement de facture'),
        ('marchand', 'Paiement marchand QR'),
        ('epargne_depot', 'Dépôt épargne'),
        ('epargne_retrait', 'Retrait épargne'),
        ('credit', 'Micro-crédit accordé'),
        ('depot_banque', 'Dépôt bancaire'),
        ('retrait_banque', 'Virement vers banque'),
    ]
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='operations')
    type_operation = models.CharField(max_length=20, choices=TYPE_CHOICES)
    reference = models.CharField(max_length=100, blank=True)
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_operation} - {self.montant} FCFA - {self.compte}"
    
class Notification(models.Model):
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    lu = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.compte} - {self.message}"