# Étape 1: Construction de l'application
FROM node:23-alpine AS builder

# Installer les dépendances nécessaires au build
WORKDIR /app
COPY package*.json ./
COPY postcss.config.mjs ./
COPY tailwind.config.ts ./
COPY components.json ./
RUN npm install 

# Copier tout le code source et construire l'application
COPY . .
RUN npm run build

# Étape 2: Création de l'image finale
FROM node:23-alpine AS runner

# Répertoire de travail
WORKDIR /app

# Copier tout le projet depuis l'étape de construction
COPY --from=builder /app /app  

# Installer uniquement les dépendances de production
RUN npm install --production --frozen-lockfile

# Exposer le port par défaut de Next.js
EXPOSE 3000

# Lancer l'application Next.js
CMD ["npm", "start"]
