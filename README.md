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

Les liens des 36 publications originales sont conservés dans `data/publication-links.json`. Le même script les applique au catalogue tout en conservant les liens auteurs utilisés par les filtres. Les quatre publications affichées sur l’accueil ont un format compact ; leurs auteurs restent disponibles dans le catalogue complet.

Les sources et les limites de la vérification des projets sont conservées dans `data/project-statuses.json` (revue du 12 octobre 2026). Les statuts affichés dans `projects.html` distinguent la plateforme WALLeSmart opérationnelle de ses phases de financement, les projets en cours, le statut de ROAD-STEP rapporté par CTA Strée et les projets historiques. Les calendriers de TSV et de FEDER-TIC n’ont pas pu être confirmés publiquement ; les anciennes périodes ont été retirées. Lors d’une mise à jour des statuts, adapter ensemble la page, le fichier de suivi et la date de revue.

Les profils et leurs sources sont conservés dans `data/team-members.json`, et les résumés de projets dans `data/project-research.json`. Le statut et la période de chaque projet proviennent de `data/project-statuses.json`. Après modification des données, régénérer les deux pages :

```bash
python3 scripts/render-research-pages.py
```

Les résumés distinguent contributions documentées, objectifs et publications liées au sujet. Les rôles de laboratoire suivent le catalogue existant ; le titre universitaire de Quentin De Coninck et les noms Hani, Chahbar et Jean Bertin Nkamla Penka ont été corrigés à partir de sources primaires. Les spécialités d’Edmond-Prosper Souapiébé et de Claude-Olivier Batungwanayo restent à renseigner par le laboratoire ; elles ne sont pas déduites. Les portraits existants sont conservés, et les profils sans photo utilisent des initiales.

Les quatre pages déclarent une URL canonique sur `https://smartilia.com/` et des métadonnées Open Graph avec `images/smartilia-social-v1.png` (1200 × 627 px). La source éditable se trouve dans `illustrations/smartilia-social.svg`. Le PNG utilise le logo original, Montserrat et Source Sans 3. Lors d’une nouvelle image, changer son nom et les métadonnées pour éviter un ancien aperçu en cache. Aucun build frontend n’est requis : l’image exportée est servie directement.

## Homepage research resources

`data/research-resources.json` maintains a curated research visual and two institutional/partner articles, rendered with `python3 scripts/render-research-resources.py`. The article dates and links to associated projects are visible. French resources are marked FR. The homepage selection remains static and does not claim to be a live news feed.

`images/mpb-unet-figure7.png` is the complete Figure 7 from Chahbar, Merati & Mahmoudi, MPB-UNet, Electronics 14(1), 40, DOI 10.3390/electronics14010040 (published 26 December 2024). The unmodified image is reused under CC BY 4.0, with visible credit, paper and licence links. The original figure URL, dimensions and licence are recorded in the data file. It shows published test examples; it is not evidence of additional clinical validation.

The obsolete CRA-W event link for WALLeSmart was replaced with the current platform article describing Mon Parcellaire.

## Image delivery and documented project outputs

The site uses resized WebP variants for the UMONS logo, pictogram and seven existing portraits. A small PNG favicon is kept for compatibility. MPB-UNet uses lossless WebP previews at 480 and 960 px through `srcset` and `sizes`; the complete original PNG remains linked. No image content was generated, cropped or replaced, and the logo transparency is preserved. Original PNG sources and the LinkedIn share card remain available.

`data/image-optimization.json` records dimensions, encoding settings, source/output hashes and file-size reductions. Conversion uses installed `cwebp` with `-m 6 -resize WIDTH 0`: `-lossless -exact` for logos and the scientific figure, `-q 88 -sharp_yuv -alpha_q 100` for photographs. `dwebp` produces the PNG favicon from the small lossless WebP. New filenames avoid serving previously cached heavy files. The homepage’s unique raster image budget, including the larger scientific preview and favicon, decreases by 93.77%; this is a byte comparison, not a measured page-load speed improvement.

`data/project-research.json` now contains eight sourced outputs/resources across seven projects. Native `details/summary` panels retain the compact project grid. Each output records category, date, description, public links, sources and attribution checks. Lab work, related research and consortium contributions remain distinguished; laboratory/dataset scores are not claimed as operational or clinical validation. Regenerate with `python3 scripts/render-research-pages.py`. Homepage resources remain managed by `python3 scripts/render-research-resources.py`.
