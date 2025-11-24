# 🚀 Guía de Inicio Rápido

## Configuración Inicial

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
# GitHub
GITHUB_TOKEN=ghp_your_github_token_here

# Google Gemini (opcional, si usas Gemini)
GOOGLE_API_KEY=your_gemini_api_key_here

# Firebase (opcional, para persistencia)
FIREBASE_CREDENTIALS=/path/to/firebase-credentials.json
# O en base64 para CI/CD:
# FIREBASE_CREDENTIALS=base64_encoded_credentials_here

# YouTube (opcional, para upload)
YOUTUBE_CLIENT_SECRET=your_client_secret_here
YOUTUBE_REFRESH_TOKEN=your_refresh_token_here
```

### 3. Obtener Credenciales

#### GitHub Token
1. Ve a https://github.com/settings/tokens
2. Genera un nuevo token con permisos `public_repo`
3. Copia el token a `.env`

#### Firebase Credentials (Opcional)
1. Ve a https://console.firebase.google.com/
2. Crea un nuevo proyecto
3. Ve a Project Settings → Service Accounts
4. Genera una nueva clave privada (JSON)
5. Guarda el archivo y actualiza `FIREBASE_CREDENTIALS` en `.env`

#### Foundry Local (Opcional)
```bash
# Instalar Foundry Local
pip install foundry-local-sdk

# Verificar instalación
python -c "from foundry_local import FoundryLocalManager; print('OK')"
```

---

## Uso Básico

### Opción 1: Solo con Gemini (Cloud)
```bash
python src/main.py \
  --provider gemini \
  --model gemini-1.5-flash \
  --mode once
```

### Opción 2: Con Foundry Local (100% Local)
```bash
python src/main.py \
  --provider foundry \
  --model phi-3.5-mini \
  --mode once
```

### Opción 3: Con Firebase (Evitar Duplicados)
```bash
python src/main.py \
  --provider foundry \
  --model phi-3.5-mini \
  --use-firebase \
  --mode once
```

### Opción 4: Con Generación de Imágenes
```bash
python src/main.py \
  --provider foundry \
  --model phi-3.5-mini \
  --generate-images \
  --mode once
```

### Opción 5: Full Stack (Todo Habilitado)
```bash
python src/main.py \
  --provider foundry \
  --model phi-3.5-mini \
  --use-firebase \
  --generate-images \
  --headless \
  --mode once
```

---

## Validación

### Verificar Instalación
```bash
# Verificar que todos los módulos se importan correctamente
python -c "
from src.scanner.github_scanner import GitHubScanner
from src.agents.scriptwriter import ScriptWriter
from src.persistence.firebase_store import FirebaseStore
from src.image_gen.image_generator import ImageGenerator
print('✅ Todos los módulos importados correctamente')
"
```

### Ejecutar Tests
```bash
# Tests básicos
pytest tests/test_scanner.py -v

# Tests de persistencia (requiere Firebase configurado)
pytest tests/test_persistence.py -v

# Todos los tests
pytest tests/ -v
```

### Validar Integración
```bash
# Script de validación completo
python validate_integration.py
```

---

## Troubleshooting

### Error: "GITHUB_TOKEN is missing"
**Solución:** Asegúrate de que `.env` existe y contiene `GITHUB_TOKEN`

### Error: "Firebase credentials required"
**Solución:**
- Opción 1: No uses `--use-firebase`
- Opción 2: Configura `FIREBASE_CREDENTIALS` en `.env`

### Error: "foundry-local-sdk is required"
**Solución:**
```bash
pip install foundry-local-sdk
```

### Error: "Failed to initialize ImageGenerator"
**Solución:**
- Opción 1: No uses `--generate-images`
- Opción 2: Asegúrate de que Foundry Local está corriendo
- Nota: El sistema generará placeholders automáticamente si falla

### Error: "Playwright browser not found"
**Solución:**
```bash
playwright install chromium
```

---

## Ejemplos de Uso

### Desarrollo Local (Sin Costos)
```bash
# Usa Foundry Local + Placeholders de imágenes
python src/main.py \
  --provider foundry \
  --model phi-3.5-mini \
  --mode once
```

### Producción (Con Firebase)
```bash
# Usa Gemini + Firebase + Imágenes reales
python src/main.py \
  --provider gemini \
  --use-firebase \
  --generate-images \
  --headless \
  --mode daemon
```

### Testing (Headless)
```bash
# Para CI/CD
python src/main.py \
  --provider foundry \
  --model phi-3.5-mini \
  --headless \
  --mode once
```

---

## Estructura de Output

Después de ejecutar, encontrarás:

```
output/
├── {repo-name}_raw.mp4          # Video grabado del repo
├── {repo-name}.mp3              # Narración generada
├── {repo-name}_final.mp4        # Video final con audio
└── images/                      # (si --generate-images)
    ├── {repo-name}_architecture.png
    ├── {repo-name}_flow.png
    └── {repo-name}_features.png
```

---

## Modo Daemon

Para ejecutar continuamente (cada hora):

```bash
python src/main.py \
  --provider foundry \
  --model phi-3.5-mini \
  --use-firebase \
  --generate-images \
  --headless \
  --mode daemon
```

**Nota:** En modo daemon, el sistema:
1. Escanea GitHub cada hora
2. Procesa solo repositorios nuevos (si Firebase está habilitado)
3. Genera y sube videos automáticamente
4. Registra todo en logs

---

## Monitoreo

### Ver Logs en Tiempo Real
```bash
python src/main.py --mode daemon 2>&1 | tee -a logs/app.log
```

### Verificar Estado en Firebase
```python
from src.persistence.firebase_store import FirebaseStore

store = FirebaseStore()
recent = store.get_recent_repos(limit=10)

for repo in recent:
    print(f"{repo['repo_name']}: {repo['status']}")
```

---

## Próximos Pasos

1. ✅ Ejecuta `python validate_integration.py`
2. ✅ Prueba con un repo de prueba
3. ✅ Configura Firebase (opcional)
4. ✅ Configura YouTube OAuth (opcional)
5. ✅ Ejecuta en modo daemon

---

**¿Necesitas ayuda?** Revisa:
- `SESSION_SUMMARY.md` - Resumen de la última sesión
- `IMPLEMENTATION_SUMMARY.md` - Detalles técnicos
- `TASK.md` - Estado de tareas
- `PLANNING.md` - Arquitectura del proyecto
