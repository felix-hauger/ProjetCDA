# QuickPath – Raccourcisseur d’URL

**QuickPath** est une application de raccourcissement d’URL conçue dans le cadre du passage du titre professionnel **Concepteur Développeur d’Applications (CDA)** – [RNCP 37873](https://www.francecompetences.fr/recherche/rncp/37873/).  
Ce projet couvre une partie des compétences exigées pour les trois blocs d’activités types du référentiel CDA.

---

## 🚀 Fonctionnalités principales

- Raccourcir une URL longue via une API REST (`POST /links`)
- Gérer les collisions de slugs (unicité garantie)
- Redirection automatique (`GET /{slug}`) avec code HTTP 301
- Gestion des erreurs (404 pour slug inconnu, 410 pour lien expiré)
- Ajout optionnel d'une date d’expiration
- Statistiques (clics, date de création, dernière visite)
- Conteneurisation avec Docker

---

## 🧱 Stack technique

- **API** : Python, FastAPI, SQLModel
- **Tests** : Pytest, HTTPX
- **Containers** : Docker, Docker Compose
- **Base de données** : SQLite

---

## 📂 Structure du projet

url-shortener/
├── app/
│ ├── main.py # Point d’entrée FastAPI
│ ├── models.py # Modèles SQLModel
│ ├── schemas.py # Schémas Pydantic
│ ├── crud.py # Opérations BDD
│ ├── database.py # Connexion à la BDD
├── tests/
│ └── test_links.py # Tests Pytest
├── Dockerfile # Image multi-stage
├── docker-compose.yml # Stack : app + db + nginx
├── requirements.txt
└── .github/
  └── workflows/
    └── ci.yml # Workflow CI

---

## ✅ Couverture des compétences CDA

### 1. Développer une application sécurisée
- Environnement configuré via Docker et .env (`1.1`)
- API (`1.2`)
- Composants métier sécurisés (`1.3`)
- Gestion agile avec backlog, sprints, user stories (`1.4`)

### 2. Concevoir et développer une application sécurisée organisée en couches
- Analyse des besoins (`2.5`)
- Architecture REST + modèle MVC simplifié (`2.6`)
- Base PostgreSQL + ORM SQLModel (`2.7`)
- Accès données SQL + simulation NoSQL possible (`2.8`)

### 3. Préparer le déploiement d’une application sécurisée
- Plan de tests (unitaires, redirections, erreurs) (`3.9`)
- Conteneurisation via Docker (`3.10`)
- CI/CD via GitHub Actions (`3.11`)

---

## 🛠 Exécution locale

```bash
cd quickpath
docker-compose up --build
```

## 🧪 Tests et qualité

```bash
pytest -q
```
