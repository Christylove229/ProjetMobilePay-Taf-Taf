from django.shortcuts import render, redirect

from django.utils.translation import gettext as _

from django.contrib import messages

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from .models import Compte, Transaction, Operation, Notification

from .forms import InscriptionForm, ConnexionForm, EnvoiArgentForm, RetraitForm, FactureForm, PaiementMarchandForm, EpargneForm, MicroCreditForm, ServiceBancaireForm



def inscription(request):

    if request.method == 'POST':

        form = InscriptionForm(request.POST)

        if form.is_valid():

            nom_utilisateur = form.cleaned_data['nom_utilisateur']

            telephone = form.cleaned_data['telephone']

            pin = form.cleaned_data['pin']



            # Créer l'utilisateur Django (le mot de passe = le PIN, pour l'instant)

            user = User.objects.create_user(username=nom_utilisateur, password=pin)



            # Créer le compte associé

            Compte.objects.create(

                utilisateur=user,

                telephone=telephone,

                pin=pin,

                solde=0

            )



            messages.success(request, "Compte créé avec succès ! Vous pouvez vous connecter.")

            return redirect('inscription')

    else:

        form = InscriptionForm()



    return render(request, 'accounts/inscription.html', {'form': form})

def connexion(request):

    if request.method == 'POST':

        form = ConnexionForm(request.POST)

        if form.is_valid():

            telephone = form.cleaned_data['telephone']

            pin = form.cleaned_data['pin']



            try:

                compte = Compte.objects.get(telephone=telephone)

                user = authenticate(request, username=compte.utilisateur.username, password=pin)

                if user is not None:

                    login(request, user)

                    return redirect('tableau_bord')

                else:

                    messages.error(request, _("Numéro de téléphone ou PIN incorrect."))

            except Compte.DoesNotExist:

                messages.error(request, _("Numéro de téléphone ou PIN incorrect."))

    else:

        form = ConnexionForm()



    return render(request, 'accounts/connexion.html', {'form': form})



@login_required

def tableau_bord(request):

    compte = Compte.objects.get(utilisateur=request.user)

    transactions_envoyees = compte.transactions_envoyees.all()

    transactions_recues = compte.transactions_recues.all()

    transactions = (transactions_envoyees | transactions_recues).order_by('-date')[:3]

    return render(request, 'accounts/tableau_bord.html', {

        'compte': compte,

        'transactions': transactions

    })




@login_required
def historique_transactions(request):
    compte = Compte.objects.get(utilisateur=request.user)
    transactions_envoyees = compte.transactions_envoyees.all()
    transactions_recues = compte.transactions_recues.all()
    transactions = (transactions_envoyees | transactions_recues).order_by('-date')
    return render(request, 'accounts/historique.html', {
        'compte': compte,
        'transactions': transactions,
    })

def deconnexion(request):

    logout(request)

    return redirect('connexion')



@login_required

def envoyer_argent(request):

    compte = Compte.objects.get(utilisateur=request.user)



    if request.method == 'POST':

        form = EnvoiArgentForm(request.POST)

        if form.is_valid():

            telephone_dest = form.cleaned_data['telephone_destinataire']

            montant = form.cleaned_data['montant']



            if telephone_dest == compte.telephone:

                messages.error(request, "Vous ne pouvez pas vous envoyer de l'argent à vous-même.")

            elif montant > compte.solde:

                messages.error(request, "Solde insuffisant.")

            else:

                try:

                    destinataire = Compte.objects.get(telephone=telephone_dest)

                    compte.solde -= montant

                    compte.save()

                    destinataire.solde += montant

                    destinataire.save()

                    Transaction.objects.create(

                        expediteur=compte,

                        destinataire=destinataire,

                        montant=montant,

                    )

                    Notification.objects.create(compte=compte, message=_("Vous avez envoyé %(montant)s FCFA à %(dest)s.") % {"montant": montant, "dest": telephone_dest})

                    Notification.objects.create(compte=destinataire, message=_("Vous avez reçu %(montant)s FCFA de %(tel)s.") % {"montant": montant, "tel": compte.telephone})

                    messages.success(request, f"{montant} FCFA envoyés avec succès à {telephone_dest}.")



                    return redirect('tableau_bord')

                except Compte.DoesNotExist:

                    messages.error(request, "Ce numéro de téléphone n'est associé à aucun compte.")

    else:

        form = EnvoiArgentForm()



    return render(request, 'accounts/envoyer_argent.html', {'form': form, 'compte': compte})



@login_required

def retrait(request):

    compte = Compte.objects.get(utilisateur=request.user)



    if request.method == 'POST':

        form = RetraitForm(request.POST)

        if form.is_valid():

            montant = form.cleaned_data['montant']



            if montant > compte.solde:

                messages.error(request, "Solde insuffisant.")

            else:

                compte.solde -= montant

                compte.save()

                Operation.objects.create(

                    compte=compte,

                    type_operation='retrait',

                    montant=montant

                )

                messages.success(request, f"Retrait de {montant} FCFA effectué avec succès.")

                return redirect('tableau_bord')

    else:

        form = RetraitForm()



    return render(request, 'accounts/retrait.html', {'form': form, 'compte': compte})





@login_required

def paiement_facture(request):

    compte = Compte.objects.get(utilisateur=request.user)



    if request.method == 'POST':

        form = FactureForm(request.POST)

        if form.is_valid():

            fournisseur = form.cleaned_data['fournisseur']

            numero_reference = form.cleaned_data['numero_reference']

            montant = form.cleaned_data['montant']



            if montant > compte.solde:

                messages.error(request, "Solde insuffisant.")

            else:

                compte.solde -= montant

                compte.save()

                Operation.objects.create(

                    compte=compte,

                    type_operation='facture',

                    reference=f"{fournisseur} - {numero_reference}",

                    montant=montant

                )

                messages.success(request, f"Facture {fournisseur} payée avec succès ({montant} FCFA).")

                return redirect('tableau_bord')

    else:

        form = FactureForm()



    return render(request, 'accounts/paiement_facture.html', {'form': form, 'compte': compte})



@login_required

def paiement_marchand(request):

    compte = Compte.objects.get(utilisateur=request.user)



    if request.method == 'POST':

        form = PaiementMarchandForm(request.POST)

        if form.is_valid():

            code_marchand = form.cleaned_data['code_marchand']

            montant = form.cleaned_data['montant']



            if montant > compte.solde:

                messages.error(request, "Solde insuffisant.")

            else:

                compte.solde -= montant

                compte.save()

                Operation.objects.create(

                    compte=compte,

                    type_operation='marchand',

                    reference=code_marchand,

                    montant=montant

                )

                messages.success(request, f"Paiement de {montant} FCFA effectué chez {code_marchand}.")

                return redirect('tableau_bord')

    else:

        code_pre_rempli = request.GET.get('code', '')

        form = PaiementMarchandForm(initial={'code_marchand': code_pre_rempli})



    return render(request, 'accounts/paiement_marchand.html', {'form': form, 'compte': compte})





@login_required

def epargne(request):

    compte = Compte.objects.get(utilisateur=request.user)



    if request.method == 'POST':

        form = EpargneForm(request.POST)

        if form.is_valid():

            action = form.cleaned_data['action']

            montant = form.cleaned_data['montant']



            if action == 'depot':

                if montant > compte.solde:

                    messages.error(request, "Solde principal insuffisant.")

                else:

                    compte.solde -= montant

                    compte.solde_epargne += montant

                    compte.save()

                    Operation.objects.create(compte=compte, type_operation='epargne_depot', montant=montant)

                    messages.success(request, f"{montant} FCFA déposés dans votre épargne.")

                    return redirect('tableau_bord')

            else:

                if montant > compte.solde_epargne:

                    messages.error(request, "Solde épargne insuffisant.")

                else:

                    compte.solde_epargne -= montant

                    compte.solde += montant

                    compte.save()

                    Operation.objects.create(compte=compte, type_operation='epargne_retrait', montant=montant)

                    messages.success(request, f"{montant} FCFA retirés de votre épargne.")

                    return redirect('tableau_bord')

    else:

        form = EpargneForm()



    return render(request, 'accounts/epargne.html', {'form': form, 'compte': compte})





@login_required

def micro_credit(request):

    compte = Compte.objects.get(utilisateur=request.user)



    if request.method == 'POST':

        form = MicroCreditForm(request.POST)

        if form.is_valid():

            montant = form.cleaned_data['montant']

            compte.solde += montant

            compte.save()

            Operation.objects.create(

                compte=compte,

                type_operation='credit',

                reference="Micro-crédit accordé",

                montant=montant

            )

            messages.success(request, f"Micro-crédit de {montant} FCFA accordé et crédité sur votre compte.")

            return redirect('tableau_bord')

    else:

        form = MicroCreditForm()



    return render(request, 'accounts/micro_credit.html', {'form': form, 'compte': compte})



@login_required

def liste_marchands(request):

    marchands = [

        {'nom': 'Restaurant KFC', 'code': 'MARCHAND001'},

        {'nom': 'Station Total Dakar', 'code': 'MARCHAND002'},

        {'nom': 'Auchan', 'code': 'MARCHAND003'},

        {'nom': 'Numero Uno', 'code': 'MARCHAND004'},

        {'nom': 'Boutique Electronique', 'code': 'MARCHAND005'},

        {'nom': 'Hopital Militaire', 'code': 'MARCHAND006'},

    ]

    return render(request, 'accounts/liste_marchands.html', {'marchands': marchands})



@login_required

def notifications(request):

    compte = Compte.objects.get(utilisateur=request.user)

    compte.notifications.filter(lu=False).update(lu=True)

    mes_notifications = compte.notifications.all().order_by('-date')[:20]

    return render(request, 'accounts/notifications.html', {'notifications': mes_notifications, 'compte': compte})





@login_required

def service_bancaire(request):

    compte = Compte.objects.get(utilisateur=request.user)



    if request.method == 'POST':

        form = ServiceBancaireForm(request.POST)

        if form.is_valid():

            action = form.cleaned_data['action']

            banque = form.cleaned_data['banque']

            numero_compte = form.cleaned_data['numero_compte']

            montant = form.cleaned_data['montant']



            if action == 'depot_banque':

                compte.solde += montant

                compte.save()

                Operation.objects.create(

                    compte=compte,

                    type_operation='depot_banque',

                    reference=f"{banque} - {numero_compte}",

                    montant=montant

                )

                Notification.objects.create(compte=compte, message=_("Depot de %(montant)s FCFA depuis %(banque)s recu.") % {"montant": montant, "banque": banque})

                messages.success(request, f"Depot de {montant} FCFA depuis {banque} effectue avec succes.")

                return redirect('tableau_bord')

            else:

                if montant > compte.solde:

                    messages.error(request, "Solde insuffisant.")

                else:

                    compte.solde -= montant

                    compte.save()

                    Operation.objects.create(

                        compte=compte,

                        type_operation='retrait_banque',

                        reference=f"{banque} - {numero_compte}",

                        montant=montant

                    )

                    Notification.objects.create(compte=compte, message=_("Virement de %(montant)s FCFA vers %(banque)s effectue.") % {"montant": montant, "banque": banque})

                    messages.success(request, f"Virement de {montant} FCFA vers {banque} effectue avec succes.")

                    return redirect('tableau_bord')

    else:

        form = ServiceBancaireForm()



    return render(request, 'accounts/service_bancaire.html', {'form': form, 'compte': compte})

