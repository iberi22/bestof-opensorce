# 🎬 Dashboard de Producción y Pipeline de Videos

Este documento describe el **Dashboard Web (React)** y el **Pipeline de Generación de Videos** que forman parte del repositorio privado.

---

## 📋 Contenido de esta Carpeta

### 1. 🖥️ `/web/` - Dashboard React de Producción

Dashboard interno para crear contenido multiidioma de manera profesional.

**Stack Tecnológico:**
- React 18 + Vite
- Tailwind CSS
- Lucide Icons

**Funcionalidades:**

#### 🎙️ Voice Studio (Grabación Profesional)
1. **Grabación de Audio**
   - Captura de narración con micrófono
   - Control de grabación (Start/Stop)
   - Visualización de forma de onda
   - Preview del audio grabado

2. **Transcripción Automática**
   - Whisper API para transcribir audio
   - Detección automática de idioma
   - Edición del texto transcrito

3. **Traducción Multiidioma**
   - Traducción a 10 idiomas:
     - 🇺🇸 English
     - 🇪🇸 Español
     - 🇫🇷 Français
     - 🇩🇪 Deutsch
     - 🇮🇹 Italiano
     - 🇵🇹 Português
     - 🇷🇺 Русский
     - 🇨🇳 中文
     - 🇯🇵 日本語
     - 🇸🇦 العربية
   - Selección de idiomas objetivo
   - Edición de traducciones

4. **Síntesis de Voz (TTS)**
   - Generación de audio en cada idioma traducido
   - Preservación del tono y características de voz original
   - Download de archivos de audio por idioma

5. **Gestión de Imágenes**
   - Upload de imágenes para el video:
     - Architecture diagrams
     - Flow diagrams
     - Screenshots
   - Preview de imágenes subidas

6. **Generación de Videos**
   - Generación automática de videos por idioma
   - Integración con OpenCut (editor de video)
   - Timeline de 20 segundos (formato reel)
   - Export en múltiples formatos

#### 📊 Dashboard
- Vista general de posts generados
- Estado de videos por idioma
- Métricas de producción

---

## 🏗️ Arquitectura del Dashboard

```
┌──────────────────────────────────────────────────────────────┐
│                    /web/ (React Dashboard)                   │
│                                                              │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐│
│  │  Voice Studio  │  │   Dashboard    │  │   Blog Posts   ││
│  │                │  │                │  │                ││
│  │  1. Record     │  │  - Stats       │  │  - Published   ││
│  │  2. Transcribe │  │  - Videos      │  │  - Drafts      ││
│  │  3. Translate  │  │  - Languages   │  │  - Scheduled   ││
│  │  4. Synthesize │  │                │  │                ││
│  │  5. Images     │  │                │  │                ││
│  │  6. Generate   │  │                │  │                ││
│  └────────────────┘  └────────────────┘  └────────────────┘│
│                                                              │
└──────────────────────────────────┬───────────────────────────┘
                                   │
                                   ↓
                    ┌──────────────────────────┐
                    │   Flask API (Backend)    │
                    │  /api/multilingual_api   │
                    └──────────────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    ↓                             ↓
          ┌──────────────────┐        ┌──────────────────┐
          │  Video Generator │        │   TTS Engine     │
          │  (moviepy)       │        │  (Coqui/edge)    │
          └──────────────────┘        └──────────────────┘
```

---

## 🚀 Setup y Uso

### Instalación

```bash
cd web/
npm install
```

### Desarrollo

```bash
npm run dev
# Abre http://localhost:5173
```

### Build

```bash
npm run build
# Output en web/dist/
```

---

## 📚 Documentación Relacionada

Estos documentos han sido migrados junto con el dashboard:

### 1. **MULTILINGUAL_README.md**
Documentación completa del sistema de traducción multiidioma:
- Pipeline de voz (Whisper → Translation → TTS)
- Modelos utilizados (MarianMT, Coqui XTTS-v2)
- Generación de reels multiidioma

### 2. **BLOG_VIDEO_ARCHITECTURE.md**
Arquitectura completa del sistema de blog + videos:
- Flujo de generación automática
- Estructura de archivos
- Timeline de videos (20s)
- Integración con GitHub Pages

### 3. **OPENCUT_ANALYSIS.md & OPENCUT_INTEGRATION.md**
Análisis e integración de OpenCut (editor de video):
- Arquitectura de OpenCut (Next.js + FFmpeg.wasm)
- Bridge entre nuestro sistema y OpenCut
- Edición manual opcional de videos

### 4. **QUEUE_SYSTEM_GUIDE.md**
Sistema de colas para procesamiento asíncrono:
- Redis Queue (RQ)
- Worker processes
- Job scheduling
- Error handling

---

## 🔗 Integración con el Repositorio Público

El dashboard genera contenido que se publica en el **repositorio público** (bestof-opensorce):

```
Dashboard (/web/) → API (/api/) → Blog Generator → Commit to Public Repo
                                                 ↓
                                    GitHub Pages (website/)
```

**Flujo de Trabajo:**

1. **Producción (Privado):**
   - Grabar narración en el dashboard
   - Transcribir y traducir
   - Generar videos multiidioma
   - Almacenar assets en servidor

2. **Publicación (Público):**
   - API crea blog post en investigations/
   - Webhook dispara generación de página web
   - Deploy automático a GitHub Pages

---

## 🎯 Casos de Uso

### Caso 1: Video Multiidioma desde Cero

```
1. Voice Studio → Grabar narración (español)
2. Transcribe → "Hoy vamos a hablar de un proyecto increíble..."
3. Translate → Seleccionar idiomas (EN, FR, DE)
4. Synthesize → Generar audio en 3 idiomas
5. Upload Images → architecture.png, flow.png, screenshot.png
6. Generate Videos → 3 videos (ES, EN, FR, DE) de 20s cada uno
7. Download → Publicar en redes sociales
```

### Caso 2: Edición Manual con OpenCut

```
1. Generate Video → Video base generado automáticamente
2. Open in OpenCut → Editor web se abre con assets cargados
3. Edit Timeline → Ajustar transiciones, timing, efectos
4. Export → Descargar versión editada
```

### Caso 3: Batch Processing

```
1. Queue System → Encolar 10 videos para generación nocturna
2. Worker → Procesa cada video secuencialmente
3. Notification → Email cuando todos estén listos
```

---

## ⚙️ Configuración

### Variables de Entorno

Crea un archivo `web/.env`:

```env
# API Backend
VITE_API_URL=http://localhost:5000

# Gemini (para transcripción/traducción)
VITE_GOOGLE_API_KEY=your_gemini_api_key

# OpenCut (opcional)
VITE_OPENCUT_URL=http://localhost:3000
```

### Endpoints de la API

El dashboard se conecta a estos endpoints del backend:

```
POST /api/transcribe      - Transcribir audio
POST /api/translate       - Traducir texto
POST /api/synthesize      - Generar voz (TTS)
POST /api/upload-image    - Subir imagen
POST /api/generate-video  - Generar video multiidioma
GET  /api/videos/:id      - Obtener estado del video
```

---

## 🧪 Testing

```bash
# Tests unitarios
npm run test

# Tests de integración con API
npm run test:integration
```

---

## 📦 Estructura del Código

```
web/
├── src/
│   ├── App.jsx                    # Componente principal
│   ├── components/
│   │   ├── VoiceRecorder.jsx     # Voice Studio (500+ líneas)
│   │   └── Dashboard.jsx         # Dashboard principal
│   ├── services/
│   │   └── api.js                # Cliente API
│   └── utils/
│       └── audio.js              # Utilidades de audio
├── public/                        # Assets estáticos
├── package.json
└── vite.config.js
```

---

## 🔐 Seguridad

**Importante:** Este dashboard es **privado** porque:

- Contiene API keys para Gemini, TTS
- Acceso a modelos de IA entrenados (propietario)
- Generación de contenido no debe ser pública
- Datos de producción sensibles

**NO** exponer este dashboard públicamente sin autenticación.

---

## 📝 Notas de Desarrollo

### State Management

El dashboard usa React hooks (useState, useEffect) sin librerías externas de estado global. Para escalabilidad futura, considera:
- Zustand (ligero)
- Jotai (atoms)
- Redux Toolkit (enterprise)

### Performance

- Lazy loading de componentes pesados
- Memoización de traducciones
- Streaming de audio para preview en tiempo real

### Accesibilidad

- Keyboard shortcuts para grabación (Spacebar)
- Labels ARIA para lectores de pantalla
- Contraste de color WCAG AA

---

## 🤝 Contribución

Para contribuir al dashboard:

1. Fork del repo privado
2. Crear branch: `feature/nueva-funcionalidad`
3. Commit cambios
4. Push y crear PR
5. Review por el equipo

---

## 📞 Soporte

Para preguntas o problemas con el dashboard:

- Issues: GitHub Issues (repo privado)
- Email: [tu-email]
- Slack: #video-pipeline

---

**Última Actualización:** 26 de noviembre de 2025
**Versión:** 1.0.0
**Repositorio:** bestof-pipeline (privado)
