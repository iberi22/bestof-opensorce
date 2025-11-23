# 📋 Reglas de Desarrollo: Open Source Video Generator

_Última Actualización: 23 de noviembre de 2025_

## 🔄 Contexto del Proyecto

### Visión General
- **Objetivo:** Sistema automatizado para detectar repositorios Open Source de alta calidad, generar guiones con IA, grabar tours visuales y producir videos narrados.
- **Filosofía:** "Serverless" first (GitHub Actions) pero con soporte local robusto (Foundry Local).
- **Stack Principal:** Python 3.11+, Playwright, MoviePy, Google Gemini / Foundry Local.

### Arquitectura del Sistema
El proyecto sigue una arquitectura modular estricta:
1.  **Scanner (`src/scanner`):** Ojos del sistema. Filtra repositorios usando criterios de calidad (CI, Licencia, Actividad).
2.  **Agents (`src/agents`):** Cerebro. Genera guiones y análisis usando LLMs (Gemini/Foundry).
3.  **Engine (`src/engine`):** Manos.
    *   `visuals.py`: Controla el navegador (Playwright) para grabar.
    *   `renderer.py`: Edita video y audio (MoviePy, EdgeTTS).
4.  **Uploader (`src/uploader`):** Voz. Publica el contenido final.

## 🧱 Estándares de Código

### Python
- **Estilo:** Adherencia estricta a **PEP 8**.
- **Tipado:** Uso obligatorio de **Type Hints** en firmas de funciones y métodos.
- **Docstrings:** Formato Google Style para todas las clases y funciones públicas.
- **Imports:** Organizados: Estándar -> Terceros -> Locales.

```python
# Ejemplo de firma correcta
def generate_script(self, repo_data: Dict[str, Any]) -> Optional[Dict[str, str]]:
    """Genera un guion de video basado en datos del repositorio."""
    ...
```

### Manejo de Errores y Logging
- **No usar `print`:** Usar siempre el módulo `logging`.
- **Excepciones:** Capturar excepciones específicas, nunca `except Exception:` vacío sin re-raise o log.
- **Fail-fast:** Si falta una configuración crítica (ej. API Key), fallar inmediatamente al inicio.

## 🤖 Reglas de IA (LLMs)

### Hibridez Obligatoria
Todo componente de IA debe soportar dos modos:
1.  **Cloud (Gemini):** Para ejecución en CI/CD (GitHub Actions). Requiere `GOOGLE_API_KEY`.
2.  **Local (Foundry):** Para desarrollo local sin costos. Requiere `foundry-local-sdk`.

### Ingeniería de Prompts
- Los prompts deben solicitar salidas estructuradas (JSON) para facilitar el parsing.
- Incluir instrucciones de "Persona" (ej. "Actúa como un Ingeniero DevOps Senior").

## 🧪 Testing y Calidad

### Criterios de Validación de Repositorios
El Scanner debe ser implacable. Solo procesar si:
- [x] Tiene Licencia Open Source válida.
- [x] Tiene CI/CD pasando (GitHub Actions success).
- [x] README sustancial (>500 chars).
- [x] No es un proyecto "toy" (alpha, test, demo).

### Pruebas
- **Unitarias:** Usar `pytest`.
- **Mocking:** NUNCA llamar a APIs reales (GitHub, YouTube, Gemini) en los tests automáticos. Usar mocks.

## 🚀 DevOps y CI/CD

### GitHub Actions
- **Idempotencia:** Los workflows deben poder correr múltiples veces sin efectos adversos (ej. no subir el mismo video dos veces).
- **Headless:** Todo código de UI (Playwright) debe soportar ejecución `--headless`.
- **Secretos:** Las credenciales se leen EXCLUSIVAMENTE de variables de entorno.

### Docker
- El contenedor debe incluir todas las dependencias de sistema (FFmpeg, Browsers) para garantizar que la generación de video funcione idéntica en local y en la nube.

## 🔒 Seguridad
- **.gitignore:** Verificar siempre que `output/`, `.env` y `__pycache__` estén ignorados.
- **Sanitización:** Limpiar nombres de archivos generados para evitar inyecciones de comandos o errores de sistema de archivos.