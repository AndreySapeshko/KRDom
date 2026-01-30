FROM node:20-slim AS build

WORKDIR /app

COPY frontend/krdom-webapp/package.json frontend/krdom-webapp/package-lock.json ./
RUN npm install --registry=https://registry.npmjs.org/

COPY frontend/krdom-webapp/ ./
RUN npm run build

# Финальный минимальный слой
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
