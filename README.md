# 🎫 Ticketing System with Notifications & Comments

Ce projet est une application web de gestion de tickets d’assistance technique développée avec **Django**. Il permet aux utilisateurs de créer des tickets, de recevoir des notifications, d’échanger via des commentaires, et de télécharger des fichiers joints.

---

## 🚀 Fonctionnalités

- Création de tickets avec statut, priorité et pièce jointe
- Affectation des tickets à un agent de support
- Notifications automatiques via **Django Signals**
- Système de **commentaires** entre les utilisateurs et les agents
- Téléchargement sécurisé des fichiers joints
- Interface utilisateur simple basée sur **DaisyUI** et **TailwindCSS**

---

## 🛠️ Technologies

- Python 3.9.13
- Django 4.2.20
- SQLite / PostgreSQL
- TailwindCSS + DaisyUI

---

## 🧪 Installation locale

1. **Cloner le projet**
```bash
git clone https://github.com/ton-nom/ticketing-system.git
cd ticketing-system
```

2. **Créer et activer un environnement virtuel**
```bash
python -m venv env
source env/bin/activate  # ou env\Scripts\activate sous Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Appliquer les migrations**
```bash
python manage.py migrate
```

5. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

6. **Démarrer le serveur**
```bash
python manage.py runserver
```