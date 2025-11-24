# 🚀 Sprint: Video Editor & YouTube Automation Integration

## 📋 Context

Proyecto: **Open Source Video Generator** - Sistema automatizado de generación de videos multilingües para GitHub repos.

**Estado Actual:** 85% completado
- ✅ Voice Translation Studio (React + Flask API)
- ✅ Reel Creator con duraciones dinámicas
- ✅ Blog design moderno
- ✅ 10+ idiomas con voice cloning

**Repositorio:** https://github.com/iberi22/Video-Generator

---

## 🎯 Objetivos del Sprint

Implementar 2 fases críticas sin ejecutar tests (tests en local):

### 1. **Fase 6: OpenCut Video Editor Integration** (Prioridad ALTA)
### 2. **Fase 7: YouTube MCP Automation** (Prioridad CRÍTICA)

---

## ✂️ FASE 6: OpenCut Integration (3-4 días)

### Objetivo
Integrar [OpenCut](https://github.com/OpenCut-app/OpenCut) para permitir edición manual opcional de videos auto-generados.

### Tareas Research (8h)

**OC-01: Analizar Repositorio OpenCut (2h)**
- Clonar: `git clone https://github.com/OpenCut-app/OpenCut`
- Revisar arquitectura, componentes principales
- Identificar dependencias y stack tecnológico
- Documentar en `docs/OPENCUT_ANALYSIS.md`

**OC-02: Identificar Componentes Reutilizables (3h)**
- Timeline editor
- Video preview component
- Export/render functionality
- Audio sync features
- Listar en documento con pros/contras

**OC-03: Evaluar Estrategia de Integración (1h)**
- **Opción A:** Fork completo como submódulo
- **Opción B:** Extraer componentes específicos
- **Opción C:** Integración mediante API/IPC
- Documentar decisión con justificación técnica

**OC-04: Documentar Arquitectura (2h)**
- Crear diagrama de integración
- Flujo de datos: ReelCreator → OpenCut → Export
- Interfaces necesarias

### Tareas Implementación (14h)

**OC-05: Diseñar Interfaz de Integración (3h)**
- Crear `src/video_editor/opencut_bridge.py`
- Definir API/métodos de comunicación
- Especificación de formato de intercambio

**OC-06: Implementar Puente ReelCreator ↔ OpenCut (4h)**
- Método: `export_for_editing(video_path, metadata)`
- Método: `import_edited_video(project_path)`
- Manejo de assets (audio, images, subtitles)

**OC-07: UI - Botón "Edit Video" (2h)**
- Agregar en `web/src/components/VoiceRecorder.jsx`
- Después de generar video: mostrar opción "Edit"
- Lanzar OpenCut con proyecto pre-cargado

**OC-08: Implementar Flujo Completo (4h)**
```
Auto-Generate → [Edit Optional] → Final Export
```
- Estado en frontend: `editing`, `exporting`
- Callback cuando edición completa
- Re-upload de video editado

### Entregables Fase 6
- ✅ `docs/OPENCUT_ANALYSIS.md` - Análisis completo
- ✅ `docs/OPENCUT_INTEGRATION.md` - Decisión y diseño
- ✅ `src/video_editor/opencut_bridge.py` - Puente funcional
- ✅ UI actualizada con botón "Edit Video"
- ✅ Flujo end-to-end implementado
- ⚠️ **NO ejecutar tests** (se harán en local)

---

## 📤 FASE 7: YouTube MCP Automation (2-3 días)

### Objetivo
Implementar publicación automatizada a YouTube evaluando MCP protocol vs integración directa.

### Tareas Research (8h)

**YT-01: Analizar youtube-mcp-server (2h)**
- Clonar: `git clone https://github.com/ZubeidHendricks/youtube-mcp-server`
- Revisar endpoints y capacidades
- Documentar en `docs/YOUTUBE_MCP_ANALYSIS.md`

**YT-02: Estudiar Model Context Protocol (3h)**
- Revisar especificación MCP
- Entender arquitectura cliente-servidor
- Identificar beneficios vs overhead
- Ejemplos de uso

**YT-03: Evaluar Estrategias (2h - CRÍTICO)**
- **Opción A:** Usar MCP protocol completo
  - Pros: Estándar, reutilizable, robusto
  - Contras: Complejidad, deps adicionales
- **Opción B:** Extraer solo lógica YouTube API
  - Pros: Más simple, menos deps
  - Contras: Menos estándar, mantenimiento
- **Documentar decisión técnica con justificación**

**YT-04: Documentar OAuth Flow (1h)**
- Proceso de autenticación YouTube
- Refresh tokens y manejo de expiración
- Variables de entorno necesarias

### Tareas Implementación (14h)

**YT-05: Implementar Cliente (4h)**
- **Si MCP:** Crear `src/uploader/mcp_youtube_client.py`
- **Si directo:** Crear `src/uploader/youtube_api_client.py`
- Métodos: `authenticate()`, `upload()`, `set_metadata()`

**YT-06: Upload Automático desde ReelCreator (3h)**
- Integrar en `src/video_generator/reel_creator.py`
- Método: `upload_to_youtube(video_path, metadata)`
- Callback para estado de upload

**YT-07: Metadata Automation (2h)**
- Auto-generar título desde repo name
- Descripción con link a blog post
- Tags automáticos basados en tech stack
- Thumbnail desde frame del video

**YT-08: Retry Logic y Error Handling (2h)**
- Reintentos con exponential backoff
- Manejo de rate limits YouTube API
- Logging detallado de errores
- Notificaciones de fallo

**YT-09: Scheduling Óptimo (3h)**
- Sistema de cola para publicación
- Publicar en horarios de mayor engagement
- Configuración por zona horaria
- Batch processing de múltiples videos

### Entregables Fase 7
- ✅ `docs/YOUTUBE_MCP_ANALYSIS.md` - Análisis MCP
- ✅ `docs/YOUTUBE_INTEGRATION_DECISION.md` - Decisión técnica
- ✅ Cliente YouTube (MCP o directo) funcional
- ✅ Upload automático integrado
- ✅ Metadata automation
- ✅ Sistema de retry y scheduling
- ⚠️ **NO ejecutar tests** (se harán en local)

---

## 📦 Estructura de Archivos a Crear/Modificar

```
docs/
├── OPENCUT_ANALYSIS.md         (NUEVO)
├── OPENCUT_INTEGRATION.md      (NUEVO)
├── YOUTUBE_MCP_ANALYSIS.md     (NUEVO)
└── YOUTUBE_INTEGRATION_DECISION.md (NUEVO)

src/
├── video_editor/
│   ├── __init__.py             (NUEVO)
│   └── opencut_bridge.py       (NUEVO)
└── uploader/
    ├── mcp_youtube_client.py   (NUEVO - Opción A)
    └── youtube_api_client.py   (NUEVO - Opción B)

web/src/components/
└── VoiceRecorder.jsx           (MODIFICAR - agregar botón Edit)

api/
└── multilingual_api.py         (MODIFICAR - agregar endpoints upload)
```

---

## 🎯 Criterios de Éxito

### Fase 6 - OpenCut
- [ ] Decisión técnica documentada (Fork/Extracción/API)
- [ ] Puente funcional entre ReelCreator y OpenCut
- [ ] UI permite lanzar editor desde video generado
- [ ] Flujo completo: Generate → Edit → Export funciona
- [ ] Código limpio con docstrings

### Fase 7 - YouTube
- [ ] Decisión MCP vs Directo documentada con justificación
- [ ] Upload automático funciona con video real
- [ ] Metadata se genera correctamente
- [ ] Sistema de retry implementado
- [ ] Scheduling opcional configurado

---

## ⚠️ Restricciones Importantes

1. **NO EJECUTAR TESTS** - Los tests se ejecutarán en local después
2. **NO HACER COMMITS** - Solo generar código y documentación
3. **Código Production-Ready** - Limpio, documentado, type hints
4. **Documentación Completa** - Decisiones técnicas justificadas
5. **Error Handling** - Try-catch comprehensivo
6. **Logging** - Log detallado en cada operación crítica

---

## 📝 Formato de Entrega

Para cada fase, proporcionar:

1. **Documentos de Análisis** (Markdown)
2. **Decisión Técnica** con pros/contras
3. **Código Implementado** (Python/JavaScript)
4. **Diagrama de Arquitectura** (Mermaid o texto)
5. **Resumen Ejecutivo** de cambios

---

## 🔗 Referencias

- Repo actual: https://github.com/iberi22/Video-Generator
- OpenCut: https://github.com/OpenCut-app/OpenCut
- YouTube MCP: https://github.com/ZubeidHendricks/youtube-mcp-server
- MCP Spec: https://modelcontextprotocol.io/
- YouTube API: https://developers.google.com/youtube/v3

---

## 💡 Notas para Jules

- Enfócate en decisiones técnicas bien fundamentadas
- Prioriza código limpio y mantenible sobre "quick wins"
- Si encuentras bloqueadores, documenta alternativas
- El objetivo es 100% automatización con edición opcional
- Tests y deployment son responsabilidad del equipo local

**Estimación Total:** 5-7 días de desarrollo
**Prioridad:** CRÍTICA para Fase 7, ALTA para Fase 6

¡Adelante! 🚀
