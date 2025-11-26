# 📝 Actualización del README - Migración de /web/

## Cambios Realizados

La carpeta `/web/` (Dashboard React) ha sido migrada al **repositorio privado** (bestof-pipeline) junto con la documentación relacionada con generación de videos.

---

## 📋 Archivos Migrados

### Dashboard
- ✅ `/web/` - Dashboard React completo (Voice Studio + Producción)

### Documentación de Videos/Voice
- ✅ `docs/MULTILINGUAL_README.md` - Sistema de traducción multiidioma
- ✅ `docs/OPENCUT_ANALYSIS.md` - Análisis del editor OpenCut
- ✅ `docs/OPENCUT_INTEGRATION.md` - Integración con OpenCut
- ✅ `docs/QUEUE_SYSTEM_GUIDE.md` - Sistema de colas (Redis Queue)
- ✅ `docs/planning/BLOG_VIDEO_ARCHITECTURE.md` - Arquitectura de videos

---

## 🔄 Nueva Estructura de Repositorios

### 🌐 Repositorio PÚBLICO (bestof-opensorce)

**Este repositorio** contiene:
- ✅ `website/` - Blog Astro (GitHub Pages)
- ✅ `investigations/` - Base de datos Markdown
- ✅ `src/scanner/` - Herramientas de scanning
- ✅ `src/persistence/` - Almacenamiento local
- ✅ Documentación pública

**¿Qué NO está aquí?**
- ❌ Dashboard de producción (`/web/`)
- ❌ Pipeline de generación de videos
- ❌ Sistema de TTS y voice cloning
- ❌ API privada de contenido

### 🔐 Repositorio PRIVADO (bestof-pipeline)

**Nuevo repositorio** contiene:
- 🔐 `web/` - Dashboard React (Voice Studio)
- 🔐 `src/blog_generator/` - Generación de posts con IA
- 🔐 `src/video_generator/` - Pipeline de videos
- 🔐 `src/voice_pipeline/` - TTS multiidioma
- 🔐 `api/` - API Flask privada
- 🔐 Documentación de producción

---

## 📖 Sección para Agregar al README.md Principal

Agrega esta sección al README.md del repo público:

```markdown
## 🏗️ Arquitectura de Dos Repositorios

Este proyecto está dividido en dos repositorios para separar código público de herramientas privadas:

### 🌐 Este Repositorio (Público)
**Repositorio:** [bestof-opensorce](https://github.com/iberi22/bestof-opensorce)

Contiene:
- 📚 **Blog Astro** (`website/`) - Sitio estático en GitHub Pages
- 🔍 **Scanner** (`src/scanner/`) - Descubrimiento de repos open source
- 💾 **Investigations** (`investigations/`) - Base de datos Markdown
- 📊 **Dashboard React** (pendiente de deploy público)

### 🔐 Repositorio Privado
**Repositorio:** [bestof-pipeline](https://github.com/iberi22/bestof-pipeline) (privado)

Contiene:
- 🎙️ **Voice Studio** - Dashboard para grabar y traducir narración
- 🤖 **Blog Generator** - Generación de posts con Gemini AI
- 🎬 **Video Pipeline** - Generación automática de reels multiidioma
- 🔊 **TTS System** - Text-to-Speech con voice cloning
- 🔌 **API Flask** - Backend para generación de contenido

### 🔄 Flujo de Trabajo

```
┌─────────────────────────────────────────────────────────┐
│  PÚBLICO: bestof-opensorce                              │
│  - Scanner descubre repos                               │
│  - Crea investigations/*.md                             │
│  - Webhook → Repo Privado                               │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ↓ (webhook)
┌─────────────────────────────────────────────────────────┐
│  PRIVADO: bestof-pipeline                               │
│  - Genera blog post con IA                              │
│  - Crea imágenes y videos                               │
│  - Commit back → Repo Público                           │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────┐
│  DEPLOY: GitHub Pages                                   │
│  - Astro build automático                               │
│  - Blog público en bestof-opensorce.github.io           │
└─────────────────────────────────────────────────────────┘
```

**Documentación:**
- Arquitectura completa: [TWO_REPO_ARCHITECTURE.md](./TWO_REPO_ARCHITECTURE.md)
- Guía de desarrollo: [QUICKSTART_TWO_REPOS.md](./QUICKSTART_TWO_REPOS.md)

---

## 🚫 ¿Dónde está el Dashboard de Producción?

El **Dashboard React** (`/web/`) ha sido movido al **repositorio privado** porque:

1. **Contiene herramientas de producción internas**
   - Voice Studio para grabar narración profesional
   - Sistema de traducción multiidioma
   - Generación de videos con IA

2. **Requiere API keys privadas**
   - Google Gemini API
   - Coqui TTS (voice cloning)
   - Modelos entrenados propietarios

3. **No es necesario para contribuidores públicos**
   - El blog se genera automáticamente
   - Los videos son un proceso interno
   - La comunidad puede contribuir con investigations

**Acceso:** El dashboard está disponible para el equipo core en el repo privado.

```
