# Utilise une image de base avec Python
FROM python:3.8-slim

# Installer les dépendances de l'application
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application dans le conteneur
COPY . /app/

# Exposer le port sur lequel Flask écoutera
EXPOSE 5000

# Définir la commande par défaut pour démarrer l'application Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
