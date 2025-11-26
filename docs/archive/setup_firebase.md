# 🔥 Guía de Configuración de Firebase

## Paso 1: Crear Proyecto en Firebase

1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Haz clic en "Agregar proyecto" (Add project)
3. Nombre del proyecto: `op-to-video` (o el que prefieras)
4. Desactiva Google Analytics (no es necesario)
5. Haz clic en "Crear proyecto"

## Paso 2: Habilitar Firestore

1. En el menú lateral, ve a **Build** → **Firestore Database**
2. Haz clic en "Crear base de datos" (Create database)
3. Selecciona **Modo de producción** (Production mode)
4. Selecciona una ubicación cercana (ej: `us-central1`)
5. Haz clic en "Habilitar"

## Paso 3: Generar Credenciales de Servicio

1. Ve a **Configuración del proyecto** (⚙️ → Project Settings)
2. Ve a la pestaña **Cuentas de servicio** (Service accounts)
3. Haz clic en **Generar nueva clave privada** (Generate new private key)
4. Confirma haciendo clic en **Generar clave** (Generate key)
5. Se descargará un archivo JSON (ej: `op-to-video-firebase-adminsdk-xxxxx.json`)

## Paso 4: Configurar en el Proyecto

### Opción A: Usar archivo JSON directamente

1. Mueve el archivo JSON descargado a una ubicación segura:
   ```bash
   # Ejemplo en Windows
   mkdir C:\credentials
   move Downloads\op-to-video-firebase-adminsdk-xxxxx.json C:\credentials\
   ```

2. Crea un archivo `.env` en la raíz del proyecto:
   ```bash
   # En PowerShell
   Copy-Item .env.example .env
   ```

3. Edita `.env` y agrega:
   ```
   FIREBASE_CREDENTIALS=C:\credentials\op-to-video-firebase-adminsdk-xxxxx.json
   ```

### Opción B: Usar base64 (para CI/CD)

1. Convierte el archivo JSON a base64:
   ```powershell
   # En PowerShell
   $json = Get-Content "C:\credentials\op-to-video-firebase-adminsdk-xxxxx.json" -Raw
   $bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
   $base64 = [Convert]::ToBase64String($bytes)
   $base64 | Set-Clipboard
   # El base64 está ahora en tu clipboard
   ```

2. Edita `.env` y agrega:
   ```
   FIREBASE_CREDENTIALS=<pega_el_base64_aquí>
   ```

## Paso 5: Verificar Configuración

Ejecuta el script de validación:

```bash
python validate_integration.py
```

Deberías ver:
```
✅ Firebase initialized successfully
✅ Firebase tests completed successfully!
```

## Paso 6: Configurar Reglas de Seguridad (Opcional)

En Firestore, ve a **Reglas** (Rules) y usa estas reglas básicas:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow read/write from server-side only (service account)
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```

Esto asegura que solo tu aplicación (con las credenciales de servicio) puede acceder a la base de datos.

## Troubleshooting

### Error: "Firebase credentials required"
- Verifica que el archivo `.env` existe
- Verifica que `FIREBASE_CREDENTIALS` está configurado correctamente
- Verifica que la ruta al archivo JSON es correcta

### Error: "Permission denied"
- Verifica que las reglas de Firestore permiten escritura desde service accounts
- Verifica que el service account tiene los permisos correctos

### Error: "Project not found"
- Verifica que el `project_id` en el JSON coincide con tu proyecto en Firebase Console

## Estructura de Datos en Firestore

El sistema creará una colección llamada `processed_repos` con documentos como:

```json
{
  "repo_name": "owner/repo",
  "description": "Repository description",
  "stars": 100,
  "language": "Python",
  "status": "completed",
  "created_at": "2025-11-23T20:00:00Z",
  "updated_at": "2025-11-23T20:30:00Z",
  "url": "https://github.com/owner/repo",
  "video_url": "https://youtube.com/watch?v=xxxxx"
}
```

## Próximos Pasos

Una vez configurado Firebase:

1. Ejecuta una prueba:
   ```bash
   python src/main.py --provider gemini --use-firebase --mode once
   ```

2. Verifica en Firebase Console que se creó la colección `processed_repos`

3. Ejecuta de nuevo y verifica que no procesa el mismo repo dos veces

---

**¿Necesitas ayuda?** Revisa los logs o ejecuta `python validate_integration.py`
