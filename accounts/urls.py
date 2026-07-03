from django.urls import path
from . import views

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('tableau-bord/', views.tableau_bord, name='tableau_bord'),
    path('envoyer/', views.envoyer_argent, name='envoyer_argent'),
    path('retrait/', views.retrait, name='retrait'),
    path('facture/', views.paiement_facture, name='paiement_facture'),
    path('marchand/', views.paiement_marchand, name='paiement_marchand'),
    path('epargne/', views.epargne, name='epargne'),
    path('credit/', views.micro_credit, name='micro_credit'),
    path('marchands/', views.liste_marchands, name='liste_marchands'),
    path('notifications/', views.notifications, name='notifications'),
    path('service-bancaire/', views.service_bancaire, name='service_bancaire'),
    path('historique/', views.historique_transactions, name='historique_transactions'),
]