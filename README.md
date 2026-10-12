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

## Contenu du site

Le site est statique : les pages HTML à la racine utilisent `css/`, `js/`, `images/` et `illustrations/`. Aucun build frontend n’est nécessaire.

La sélection récente de publications est conservée dans `data/recent-publications.json`, avec ses liens ORBI et sa date de vérification. Il s’agit d’une sélection éditoriale, pas d’un flux actualisé automatiquement. Après modification et vérification des données, régénérer les blocs de l’accueil et de la page Publications :

```bash
python3 scripts/render-publications.py
```

Le bloc ajouté au catalogue est actuellement dans le groupe 2026. Pour des publications d’une autre année, adapter le groupe HTML correspondant. Les schémas SVG illustrent les méthodes et les domaines de recherche ; ils ne représentent pas des résultats expérimentaux.
