# Build l'image docker
docker build -t flask_api .

# Lancer le container
docker run -p 5000:5000 flask_api