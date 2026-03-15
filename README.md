# smart-ilia

Site web servi via nginx, déployé automatiquement avec Docker + Watchtower.

## Architecture

- **CI/CD** : GitHub Actions build et push l'image sur GHCR à chaque push sur `main`
- **Watchtower** : surveille le registre toutes les 30 secondes et recrée le conteneur dès qu'une nouvelle image est disponible

## Déploiement sur le serveur

### 1. Créer le `compose.yml` sur le serveur

Copier le contenu de `compose-prod.yml` dans un fichier `compose.yml` sur le serveur via `nano compose.yml`.

### 2. Lancer les services

```bash
sudo docker compose up -d
```

### Mise à jour

Les mises à jour sont automatiques. Watchtower vérifie toutes les 5 minutes si une nouvelle image est disponible sur `ghcr.io` et redémarre le conteneur si c'est le cas.

Pour forcer une mise à jour manuelle :

```bash
sudo docker compose pull && sudo docker compose up -d
```
