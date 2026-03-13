# smart-ilia

Site web servi via nginx, déployé automatiquement avec Docker + Watchtower.

## Architecture

- **CI/CD** : GitHub Actions build et push l'image sur GHCR à chaque push sur `main`
- **Watchtower** : surveille le registre et recrée le conteneur dès qu'une nouvelle image est disponible

## Déploiement sur le serveur

### 1. Se connecter au registre privé

Générer un token GitHub avec la permission `read:packages` puis :

```bash
echo "TON_TOKEN" | docker login ghcr.io -u ton-user --password-stdin
```

### 2. Lancer les services

```bash
docker compose -f compose-prod.yml up -d
```

### Mise à jour

Les mises à jour sont automatiques. Watchtower vérifie toutes les 5 minutes si une nouvelle image est disponible sur `ghcr.io` et redémarre le conteneur si c'est le cas.

Pour forcer une mise à jour manuelle :

```bash
docker compose -f compose-prod.yml pull && docker compose -f compose-prod.yml up -d
```