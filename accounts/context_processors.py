from .models import Compte

def notifications_non_lues(request):
    if request.user.is_authenticated:
        try:
            compte = Compte.objects.get(utilisateur=request.user)
            nb = compte.notifications.filter(lu=False).count()
            return {'nb_notifications_non_lues': nb}
        except Compte.DoesNotExist:
            return {'nb_notifications_non_lues': 0}
    return {'nb_notifications_non_lues': 0}
