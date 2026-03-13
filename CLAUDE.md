# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

Static website for the SMART'ILIA research lab (University of Mons). Three HTML pages served by nginx via Docker. No build step, no framework, no package manager.

## Stack

- **HTML/CSS/JS** — vanilla, no dependencies
- **Fonts** — Playfair Display (serif, headings) + Source Sans 3 (sans, body) via Google Fonts
- **Nginx** — serves static files from `/usr/share/nginx/html`
- **Docker** — `Dockerfile` builds the nginx image; `docker-compose.yml` for local dev (port 8080)
- **CI/CD** — GitHub Actions (`.github/workflows/docker.yml`) builds and pushes to `ghcr.io/umons-ig/smart-ilia:latest` on every push to `main`
- **Auto-deploy** — Watchtower on the server polls GHCR every 30s and recreates the container on new image

## Local development

Open HTML files directly in browser — no server needed:
```
open index.html
```

Or run with Docker:
```bash
docker compose up
# → http://localhost:8080
```

## Deploy to production

The server (`teamilia`) uses `compose.yml` (not `compose-prod.yml` — they have the same content, `compose.yml` is the one on the server). Any push to `main` triggers a build and auto-deploy via Watchtower.

The server requires a `.env` file (see `.env.example`) with GitHub credentials to pull from the private GHCR registry.

## Design system

Defined in `css/style.css` via CSS custom properties:

- **Primary color**: `--burgundy: #8B1538` (UMONS brand color)
- **Background**: `--ivory: #FDFBF9`
- **Heading font**: `--serif` (Playfair Display)
- **Body font**: `--sans` (Source Sans 3)

All pages share the same `css/style.css` and follow the same nav/footer structure defined in each HTML file (no templating system).
