# Test Niveau 1 Backend (Django REST API)

## I - Objectif

Ce projet a pour but de créer une **API REST** avec Django permettant de gerer de maniere automatique dans un seul script :
- L'inscription (`register`) d’un nouvel utilisateur.
- L’authentification (`login`) et la génération de jeton (`Token Authentication`).
- La création d’une **demande d’application**.
- La confirmation d’une application.

---

## II - Prérequis

Avant de lancer le projet, assurez-vous d’avoir installé sur votre machine :
- **Python 3.11+** (optionnel si Docker est utilisé)
- **Docker** et **Docker Compose**
- **Git**

---

## III - Fonctionnalités principales
| Endpoint                                      | Méthode | Description                                      |
|-----------------------------------------------|---------|--------------------------------------------------|
| `/api/v1.1/auth/register/`                    | POST    | Inscription d’un utilisateur                     |
| `/api/v1.1/auth/login/`                       | POST    | Connexion d’un utilisateur                       |
| `/api/v1.1/job-application-request/`         | POST    | Création d’une demande d’application             |
| `PATCH confirmation` via l’URL retournée     | PATCH   | Confirmation d’une application                   |

## IV - Étapes de lancement

### 4.1 - Cloner le dépôt
```
git clone https://github.com/soniarimamy/test_niveau_1.git
```

### 4.2 - Se déplacer dans le projet
```
cd test_niveau_1
```

### 4.3 - Lancer l’application avec Docker
#### a) créer un fichier .env à la racine du projet et specifier la valeur des variables suivantes:
```
DEBUG=True or False
SECRET_KEY=<YOUR_DJANGO_SECRET_KEY>
POSTGRES_USER=<YOUR_POSTGRES_DB_USER>
POSTGRES_PWD=<YOUR_POSTGRES_DB_PASSWORD>
POSTGRES_HOST=postgresql_db
POSTGRES_INTERNAL_PORT=<YOUR_POSTGRES_DB_INTERNAL_PORT>
POSTGRES_EXTERNAL_PORT=<YOUR_POSTGRES_DB_EXTERNAL_PORT>
POSTGRES_DBNAME=<YOUR_POSTGRES_DB_NAME>
```

#### b) lancer l'application via cette commande:
D'abord, Arrêter les services qui tournent actuellement [Optionnel]
```
docker-compose --env-file .env down -v
```

Lancer le build
```
docker-compose --env-file .env up --build -d
```

## V - Services Docker
Le projet utilise Docker Compose avec trois services principaux :

### 5.1 - Service	Description

| Service        | Description                                              |
|----------------|----------------------------------------------------------|
| postgresql_db  | Base de données PostgreSQL configurée via `.env`         |
| api_app        | Serveur Django exposé sur le port 8000                   |
| run_test1      | Exécute le script de test `run_test1.py` automatiquement |

### 5.2 - Commandes Docker principales

#### 5.2.1 - Builder et lancer l’API
```
docker-compose --env-file .env up --build -d
```

#### 5.2.2 - Launch unit test
```
docker-compose --env-file .env run --rm api_app python manage.py test api_app
```

#### 5.2.3 - Lancer le serveur API manuellement
```
docker-compose --env-file .env run api_app
```

#### 5.2.4 - Exécuter les tests automatisés
##### a) via le script
```
docker-compose --env-file .env run --rm run_test1
```

##### b) via API REST
Créer un compte super utilisateur Django:
```
docker-compose --env-file .env run --rm api_app python manage.py createsuperuser
```

Obtenir un token:
```
curl -X POST http://localhost:8000/api/token/ -H "Content-Type: application/json" \
 -d '{"username": "<django_admin_super_user_name>", "password": "<django_admin_super_user_pwd>"}'
```

Appeler le test via un endpoint
```
curl -X POST http://localhost:8000/api/run_test/ -H "Authorization: Bearer <TOKEN>"
```

## VI - Architecture du projet
```
test_niveau_1/
├── api_app/
│   ├── models.py
│   ├── views.py
│   ├── management/commands/run_test1.py
├── test_niveau_1/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py
```

## VII - Licence
Ce projet est distribué sous la licence MIT.

## VIII - Auteur
- Nom : Rochel Soniarimamy
- Email : rochel.soniarimamy@gmail.com
- GitHub : https://github.com/soniarimamy/
- Docker Hub : rochel05

## IX - Contact
- Email: rochel.soniarimamy@gmail.com
- Téléphone : +261349251646
