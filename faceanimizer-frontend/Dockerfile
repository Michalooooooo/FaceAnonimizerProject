FROM node:20-bullseye

WORKDIR /src

# Kopiuj pliki lockfile i package.json
COPY package.json package-lock.json ./

# Zainstaluj wszystkie zależności (dev + prod)
RUN npm ci

# Skopiuj resztę kodu
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
