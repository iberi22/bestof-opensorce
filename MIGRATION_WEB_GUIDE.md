# ✅ Migración de /web/ al Repositorio Privado - Guía Completa

**Fecha:** 26 de noviembre de 2025
**Acción:** Mover Dashboard React y documentación de videos al repo privado

---

## 📋 Resumen Ejecutivo

El **Dashboard React** (`/web/`) es una herramienta de producción interna para:
- Grabar narración profesional
- Traducir a 10 idiomas
- Generar videos multiidioma
- Gestionar contenido con IA

**No pertenece al repositorio público** porque contiene:
- API keys privadas (Gemini, TTS)
- Herramientas de producción internas
- Código propietario

---

## 🎯 Archivos Preparados

### 1. ✅ Script de Migración Automática

**Archivo:** `scripts/migrate_web_to_private.ps1`

**Qué hace:**
- Copia `/web/` al repo privado
- Copia 5 documentos sobre videos/voice
- Elimina archivos del repo público
- Actualiza .gitignore del repo privado

**Uso:**
```powershell
# Dry run (sin cambios reales)
.\scripts\migrate_web_to_private.ps1 -DryRun

# Ejecutar migración real
.\scripts\migrate_web_to_private.ps1 -PrivateRepoPath "..\bestof-pipeline"
```

### 2. 📚 Documentación para Repo Privado

**Archivo:** `WEB_DASHBOARD_README.md`

**Contenido:**
- Descripción completa del dashboard
- Arquitectura del Voice Studio
- Setup y configuración
- Casos de uso
- Integración con API Flask
- Seguridad y buenas prácticas

**Acción:** Copiar este archivo al repo privado como `README.md` en `/web/`

### 3. 📝 Actualización del README Público

**Archivo:** `MIGRATION_WEB_README.md`

**Contenido:**
- Sección para agregar al README.md principal
- Explicación de la arquitectura de dos repos
- Dónde está el dashboard ahora
- Por qué se movió

**Acción:** Agregar contenido al `README.md` del repo público

---

## 🚀 Pasos para Ejecutar la Migración

### Paso 1: Preparación

```bash
# 1. Asegúrate de tener ambos repos clonados
cd /ruta/a/bestof-opensorce        # Repo público (este)
cd ../bestof-pipeline               # Repo privado

# 2. Verifica que no hay cambios sin commitear
git status

# 3. Haz backup por si acaso
git branch backup-pre-web-migration
```

### Paso 2: Dry Run (Prueba)

```powershell
cd bestof-opensorce
.\scripts\migrate_web_to_private.ps1 -DryRun -PrivateRepoPath "..\bestof-pipeline"
```

**Verifica que la salida muestra:**
- ✅ Archivos que se copiarán
- ✅ Rutas de destino correctas
- ⚠️ Sin errores

### Paso 3: Ejecutar Migración

```powershell
.\scripts\migrate_web_to_private.ps1 -PrivateRepoPath "..\bestof-pipeline"
```

**El script hará:**
1. Copiar `/web/` → `../bestof-pipeline/web/`
2. Copiar docs de videos → `../bestof-pipeline/docs/`
3. Eliminar archivos del repo público
4. Actualizar .gitignore

### Paso 4: Commit en Repo Privado

```bash
cd ../bestof-pipeline

# Copiar README del dashboard
cp ../bestof-opensorce/WEB_DASHBOARD_README.md web/README.md

# Verificar archivos
git status

# Debe mostrar:
# - new file: web/
# - new file: docs/MULTILINGUAL_README.md
# - new file: docs/OPENCUT_ANALYSIS.md
# - new file: docs/OPENCUT_INTEGRATION.md
# - new file: docs/QUEUE_SYSTEM_GUIDE.md
# - new file: docs/BLOG_VIDEO_ARCHITECTURE.md

# Commit y push
git add .
git commit -m "feat: add web dashboard and video generation documentation

- Moved React dashboard from public repo
- Added Voice Studio for multilingual narration
- Included video generation pipeline docs
- Added TTS and OpenCut integration guides"

git push origin main
```

### Paso 5: Commit en Repo Público

```bash
cd ../bestof-opensorce

# Verificar eliminaciones
git status

# Debe mostrar:
# - deleted: web/
# - deleted: docs/MULTILINGUAL_README.md
# - deleted: docs/OPENCUT_ANALYSIS.md
# - deleted: docs/OPENCUT_INTEGRATION.md
# - deleted: docs/QUEUE_SYSTEM_GUIDE.md
# - deleted: docs/planning/BLOG_VIDEO_ARCHITECTURE.md

# Actualizar README.md principal
# (copia contenido de MIGRATION_WEB_README.md)
nano README.md

# Commit y push
git add .
git commit -m "refactor: move web dashboard to private repository

- Moved /web/ (React dashboard) to bestof-pipeline
- Moved video generation documentation
- Dashboard contains production tools (Voice Studio, TTS)
- Requires private API keys (not suitable for public repo)

Public repo now focuses on:
- Blog (Astro website)
- Scanner (GitHub discovery)
- Investigations database

See TWO_REPO_ARCHITECTURE.md for details"

git push origin main
```

### Paso 6: Actualizar Documentación

En el **repo público**, actualiza estos archivos:

1. **README.md** - Agregar sección sobre arquitectura de dos repos
2. **docs/INDEX.md** - Remover referencias a docs eliminados
3. **TASK.md** - Marcar migración de /web/ como completada

En el **repo privado**, crea:

1. **README.md** principal (si no existe)
2. **web/README.md** - Usar WEB_DASHBOARD_README.md

---

## ✅ Verificación

### Repo Privado (bestof-pipeline)

```bash
cd bestof-pipeline

# Debe existir:
ls web/                          # Dashboard React
ls docs/MULTILINGUAL_README.md   # Docs de voice
ls docs/BLOG_VIDEO_ARCHITECTURE.md

# Instalar y probar
cd web/
npm install
npm run dev  # Debe abrir en http://localhost:5173
```

### Repo Público (bestof-opensorce)

```bash
cd bestof-opensorce

# NO debe existir:
ls web/              # Error: directory not found ✅
ls docs/MULTILINGUAL_README.md  # Error: file not found ✅

# Debe existir:
ls website/          # Blog Astro ✅
ls src/scanner/      # Scanner ✅
ls investigations/   # Database ✅
```

---

## 📊 Resumen de Archivos Migrados

### Carpetas
- ✅ `/web/` (completa) → Dashboard React + dependencies

### Documentos sobre Videos/Voice
- ✅ `docs/MULTILINGUAL_README.md` (5KB)
- ✅ `docs/OPENCUT_ANALYSIS.md` (8KB)
- ✅ `docs/OPENCUT_INTEGRATION.md` (12KB)
- ✅ `docs/QUEUE_SYSTEM_GUIDE.md` (6KB)
- ✅ `docs/planning/BLOG_VIDEO_ARCHITECTURE.md` (15KB)

**Total:** ~1 carpeta + 5 documentos + 46KB

---

## 🎯 Beneficios de la Migración

### Para el Repo Público
- ✅ Más claro y enfocado (blog + scanner)
- ✅ Sin confusión sobre qué es público/privado
- ✅ Contribuidores no ven herramientas internas
- ✅ Sin API keys accidentales en commits

### Para el Repo Privado
- ✅ Herramientas de producción en un solo lugar
- ✅ Dashboard junto con API backend
- ✅ Documentación de video pipeline centralizada
- ✅ Seguridad: API keys solo en repo privado

### Para el Equipo
- ✅ Separación clara de responsabilidades
- ✅ Deploy independiente de dashboard vs blog
- ✅ Menos riesgo de exponer código privado
- ✅ Mejor organización del proyecto

---

## 🔄 Flujo Después de la Migración

```
┌─────────────────────────────────────────────────────┐
│  PÚBLICO: bestof-opensorce (GitHub)                 │
│  - Scanner corre cada 4 horas                       │
│  - Crea/actualiza investigations/*.md               │
│  - Webhook dispara evento al repo privado           │
└─────────────────────────┬───────────────────────────┘
                          │
                          ↓ (webhook)
┌─────────────────────────────────────────────────────┐
│  PRIVADO: bestof-pipeline (Local/Cloud)             │
│  - Recibe evento de nuevo investigation             │
│  - Dashboard: Grabar narración (opcional)           │
│  - API: Generar blog post con Gemini                │
│  - API: Crear imágenes con IA                       │
│  - (Opcional) Generar video multiidioma             │
│  - Commit blog post → repo público                  │
└─────────────────────────┬───────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────┐
│  DEPLOY: GitHub Pages                               │
│  - Astro detecta cambios en website/                │
│  - Build automático                                 │
│  - Deploy a bestof-opensorce.github.io              │
└─────────────────────────────────────────────────────┘
```

---

## 📝 Notas Finales

- Los archivos `WEB_DASHBOARD_README.md` y `MIGRATION_WEB_README.md` son **temporales**
- Después de la migración, pueden eliminarse del repo público
- El script `migrate_web_to_private.ps1` puede quedar como referencia

---

## 🤝 Preguntas Frecuentes

**P: ¿Por qué mover el dashboard si ya estaba funcionando aquí?**
R: El dashboard contiene herramientas de producción y API keys privadas que no deben ser públicas.

**P: ¿Cómo contribuyo si el dashboard está en repo privado?**
R: Contribuciones públicas se enfocan en el scanner, investigations y blog. El dashboard es solo para el equipo core.

**P: ¿El blog dejará de funcionar?**
R: No. El blog (website/) se queda en el repo público. Solo se mueve la herramienta de producción interna.

**P: ¿Necesito acceso al repo privado?**
R: Solo si trabajas en la generación de contenido (videos, TTS, IA). Para contribuir al blog o scanner, el repo público es suficiente.

---

**¿Listo para ejecutar?** Sigue los pasos desde "Paso 1: Preparación" 🚀
