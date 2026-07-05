# AGENTS.md — Instructions concises pour les agents AI

Objectif
- Fournir aux agents AI les informations minimales et actionnables
  pour démarrer rapidement avec ce dépôt Django.

Quick start
- Activer l'environnement virtuel fourni (Windows):
  - PowerShell: `env\\Scripts\\Activate.ps1`
  - CMD: `env\\Scripts\\activate.bat`
- Lancer les migrations et le serveur:
  - `python manage.py migrate`
  - `python manage.py runserver`
- Lancer les tests:
  - `python manage.py test`

Points d'entrée importants
- `manage.py` — commande d'administration et démarrage du projet: [manage.py](manage.py#L1)
- Réglages principaux: [mobilepay/settings.py](mobilepay/settings.py#L1-L60) (Django 6.0.6, SQLite)
- Application principale: le module `accounts/` contient les vues, modèles,
  templates et static (voir [accounts/](accounts/)).

Conventions et remarques spécifiques
- Base de données: fichier `db.sqlite3` à la racine — attention aux opérations destructrices.
- Localisation: le projet utilise `LOCALE_PATHS` → dossier `locale/` (fr/en/es/pt).
- Templates et statiques vivent sous `accounts/templates/accounts` et
  `accounts/static/` (voir `STATICFILES_DIRS` dans settings).
- URL racine et configuration se trouvent dans `mobilepay/urls.py`.

Conseils pour les agents
- Préférez activer l'environnement `env/` inclus plutôt que d'installer
  dépendances globales si l'environnement fonctionne localement.
- Vérifiez les migrations dans `accounts/migrations/` avant d'en générer de nouvelles.
- Ne modifiez pas `SECRET_KEY` ni ne publiez de secrets.

Liens utiles
- Code: [manage.py](manage.py#L1), [mobilepay/settings.py](mobilepay/settings.py#L1-L60), [accounts/](accounts/)

Personnalisation suggérée (prochaines étapes)
- Ajouter un fichier `.github/copilot-instructions.md` ou enrichir AGENTS.md
  avec des commandes de build/CI si le dépôt en a besoin.
- Créer des skills automatisés pour: exécuter tests unitaires, vérifier migrations,
  et exécuter une vérification rapide de sécurité/secret.

Si vous voulez, je peux maintenant créer `.github/copilot-instructions.md` avec
consignes d'usage spécifiques pour les PRs et la CI.
