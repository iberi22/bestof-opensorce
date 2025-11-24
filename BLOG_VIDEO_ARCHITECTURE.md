# 🎬 Arquitectura: Blog + Video Automation

## 📋 Visión General

Sistema automatizado que:
1. **Escanea** repositorios de GitHub
2. **Genera** entradas de blog en Markdown
3. **Publica** en GitHub Pages
4. **Crea** videos de 20 segundos (reels)
5. **Automatiza** todo el proceso

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Workflow (Cloud)                   │
│  1. Escanea repos → 2. Genera blog → 3. Crea PR → 4. Merge  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  GitHub Pages (blog/)                        │
│  - posts/YYYY-MM-DD-repo-name.md                            │
│  - images/repo-name/                                         │
│  - index.html (lista de posts)                              │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              Local Video Generation (Trigger)                │
│  Detecta: git pull → nuevo post → genera video              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Estructura del Proyecto

```
op-to-video/
├── .github/
│   └── workflows/
│       ├── scan-and-blog.yml          # Workflow principal
│       └── generate-video.yml         # Trigger local (opcional)
│
├── blog/                              # GitHub Pages
│   ├── _posts/
│   │   └── YYYY-MM-DD-repo-name.md   # Entradas del blog
│   ├── assets/
│   │   ├── images/
│   │   │   └── repo-name/
│   │   │       ├── architecture.png
│   │   │       ├── screenshot.png
│   │   │       └── flow.png
│   │   └── videos/
│   │       └── repo-name-reel.mp4
│   ├── _layouts/
│   │   └── post.html
│   ├── _config.yml                    # Jekyll config
│   └── index.html
│
├── src/
│   ├── blog_generator/                # NUEVO
│   │   ├── __init__.py
│   │   ├── markdown_writer.py         # Genera posts en MD
│   │   └── blog_manager.py            # Gestiona el blog
│   │
│   ├── video_generator/               # NUEVO (refactor)
│   │   ├── __init__.py
│   │   ├── reel_creator.py            # Crea reels de 20s
│   │   └── screenshot_capturer.py     # Captura web
│   │
│   └── [módulos existentes...]
│
└── scripts/
    ├── watch_blog.py                  # Detecta cambios en blog/
    └── generate_video_from_post.py    # Genera video desde MD
```

---

## 🔄 Flujo de Trabajo

### Fase 1: GitHub Workflow (Cloud)

```yaml
# .github/workflows/scan-and-blog.yml
name: Scan Repos & Generate Blog

on:
  schedule:
    - cron: '0 */6 * * *'  # Cada 6 horas
  workflow_dispatch:

jobs:
  scan-and-blog:
    runs-on: ubuntu-latest
    steps:
      1. Escanear GitHub (Scanner)
      2. Generar análisis con Gemini (ScriptWriter)
      3. Generar imágenes (ImageGenerator)
      4. Crear post en Markdown (BlogGenerator)
      5. Capturar screenshot de la web del repo
      6. Crear rama: blog/YYYY-MM-DD-repo-name
      7. Commit y Push
      8. Crear Pull Request a main
      9. Auto-merge (si pasa checks)
```

### Fase 2: GitHub Pages (Automático)

- Cuando se hace merge a `main`, GitHub Pages se actualiza automáticamente
- El blog está disponible en: `https://username.github.io/op-to-video`

### Fase 3: Generación de Video (Local)

```bash
# Opción A: Manual
python scripts/generate_video_from_post.py blog/_posts/2025-11-23-awesome-repo.md

# Opción B: Automático (watch mode)
python scripts/watch_blog.py
# Detecta: git pull → nuevo archivo en blog/_posts/ → genera video
```

---

## 📝 Formato del Post (Markdown)

```markdown
---
layout: post
title: "Awesome Repo - Solución para X"
date: 2025-11-23
repo: owner/awesome-repo
stars: 1234
language: Python
tags: [automation, devops, ci-cd]
images:
  architecture: /assets/images/awesome-repo/architecture.png
  screenshot: /assets/images/awesome-repo/screenshot.png
  flow: /assets/images/awesome-repo/flow.png
video: /assets/videos/awesome-repo-reel.mp4
---

## 🎯 Problema

[Hook del ScriptWriter]

## 💡 Solución

[Solution del ScriptWriter]

## ✅ Ventajas

- [Pros del ScriptWriter]

## ⚠️ Consideraciones

- [Cons del ScriptWriter]

## 🎬 Veredicto

[Verdict del ScriptWriter]

---

**Narración completa:**

[Narration del ScriptWriter]
```

---

## 🎥 Generación de Reel (20 segundos)

### Timeline del Video

```
00:00 - 00:03  │ Intro: Logo + Título del repo
00:03 - 00:08  │ Problema: Diagrama flow + texto
00:08 - 00:13  │ Solución: Screenshot web + highlights
00:13 - 00:17  │ Arquitectura: Diagrama + narración
00:17 - 00:20  │ Outro: CTA + link al blog
```

### Componentes del Reel

1. **Imágenes generadas** (ImageGenerator)
   - Diagrama de arquitectura
   - Flujo problema-solución
   - Feature showcase

2. **Screenshot de la web** (Nuevo)
   - Captura de la página del repo
   - Highlights de secciones importantes

3. **Narración** (EdgeTTS)
   - Versión condensada de 20s
   - Voz profesional

4. **Música de fondo** (opcional)
   - Música libre de derechos

---

## 🤖 Componentes a Implementar

### 1. Blog Generator (`src/blog_generator/`)

```python
class MarkdownWriter:
    def create_post(self, repo_data, script_data, images):
        """Genera un post en Markdown con frontmatter YAML"""

class BlogManager:
    def create_branch(self, post_name):
        """Crea rama blog/YYYY-MM-DD-repo-name"""

    def commit_and_push(self, files):
        """Commit y push de archivos"""

    def create_pull_request(self):
        """Crea PR a main"""
```

### 2. Reel Creator (`src/video_generator/`)

```python
class ReelCreator:
    def create_20s_reel(self, post_md, images, screenshot):
        """Crea reel de 20 segundos"""

    def _create_timeline(self):
        """Define timeline de 20s"""

    def _add_transitions(self):
        """Agrega transiciones suaves"""
```

### 3. Screenshot Capturer

```python
class ScreenshotCapturer:
    def capture_repo_page(self, repo_url):
        """Captura screenshot de la página del repo"""

    def capture_highlights(self, sections):
        """Captura secciones específicas"""
```

### 4. Blog Watcher (`scripts/watch_blog.py`)

```python
class BlogWatcher:
    def watch(self):
        """Monitorea cambios en blog/_posts/"""

    def on_new_post(self, post_path):
        """Trigger: genera video cuando hay nuevo post"""
```

---

## 🚀 Implementación por Fases

### Fase 1: Blog Generator (Prioridad Alta)
- ✅ Crear estructura de blog/
- ✅ Implementar MarkdownWriter
- ✅ Implementar BlogManager
- ✅ Crear GitHub Workflow

### Fase 2: Screenshot & Reel (Prioridad Alta)
- ✅ Implementar ScreenshotCapturer
- ✅ Implementar ReelCreator (20s)
- ✅ Integrar con imágenes existentes

### Fase 3: Automatización Local (Prioridad Media)
- ✅ Implementar BlogWatcher
- ✅ Script generate_video_from_post.py
- ✅ Documentación de uso

### Fase 4: GitHub Pages (Prioridad Media)
- ✅ Configurar Jekyll
- ✅ Crear layouts personalizados
- ✅ Agregar estilos CSS

---

## 💡 Ventajas de esta Arquitectura

1. **Blog como Base de Datos**
   - Historial completo en Markdown
   - Versionado con Git
   - Búsqueda fácil

2. **Separación de Responsabilidades**
   - Workflow: Genera contenido
   - Local: Genera videos
   - GitHub Pages: Publica

3. **Escalabilidad**
   - Fácil agregar más fuentes (no solo GitHub)
   - Fácil cambiar formato de video
   - Fácil agregar más plataformas

4. **Costo Cero**
   - GitHub Actions (gratis)
   - GitHub Pages (gratis)
   - Generación local (sin costos de cloud)

---

## 🎯 Próximos Pasos Inmediatos

1. **Crear estructura de blog/**
2. **Implementar MarkdownWriter**
3. **Crear GitHub Workflow básico**
4. **Implementar ReelCreator (20s)**
5. **Probar flujo completo**

---

**¿Quieres que empiece a implementar alguna fase específica?**
