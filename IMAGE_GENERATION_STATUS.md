# 🎨 Estado de Generación de Imágenes

_Última Actualización: 29 de noviembre de 2025_

## 📋 Estado Actual

**Modo Activo:** SVG Placeholders Profesionales ✅

**Razón:** La API de Gemini Imagen requiere facturación activa. Esperando activación de billing para generar imágenes de máxima calidad.

## 🖼️ Imágenes Actuales (Producción)

**Tipo:** SVG con diseño isométrico 3D profesional
**Cantidad:** 54+ imágenes generadas
**Calidad:** ★★★★☆ (Muy buena)
**Ubicación:** `website/public/images/*/header.png`

**Características del diseño SVG:**
- ✅ Isométrico 3D con cubos flotantes
- ✅ Gradientes modernos por categoría
- ✅ Partículas animadas
- ✅ Badges con emoji de categoría
- ✅ Tipografía profesional (Fira Code)
- ✅ Dark theme con efectos glow

## 🚀 Plan de Migración a Gemini AI

### Paso 1: Activar Billing en Google Cloud

1. **Acceder a Google Cloud Console**
   - URL: https://console.cloud.google.com/billing
   - Iniciar sesión con cuenta de Google

2. **Activar Facturación**
   - Click en "Vincular cuenta de facturación"
   - Agregar método de pago (tarjeta)
   - Google ofrece **$300 USD en créditos gratuitos** para nuevos usuarios

3. **Verificar Créditos**
   - Los primeros $300 son GRATIS
   - Duran 90 días
   - Suficiente para generar miles de imágenes

### Paso 2: Verificar API Key

Tu API key ya está configurada en `.env`:
```bash
GOOGLE_API_KEY=AIzaSy...
GOOGLE_API_KEY_2=AIzaSy...
```

**Verificar acceso:**
```bash
python -c "
from google import genai
import os
client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])
print('✅ API Key válida')
"
```

### Paso 3: Activar Workflows

Una vez que billing esté activo, editar workflows:

**Archivo:** `.github/workflows/investigation_pipeline.yml`

Descomentar líneas 120-130:
```yaml
- name: Generate Images with Gemini API
  env:
    GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
    GOOGLE_API_KEY_2: ${{ secrets.GOOGLE_API_KEY_2 }}
    GOOGLE_API_KEY_3: ${{ secrets.GOOGLE_API_KEY_3 }}
  run: |
    echo "🎨 Generating images with Gemini API..."
    python scripts/generate_blog_images.py --limit 10
  continue-on-error: true
```

**Archivo:** `.github/workflows/rust_blog_automation.yml`

Descomentar líneas 90-98:
```yaml
- name: 5. Generate Images with Gemini API
  env:
    GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
    GOOGLE_API_KEY_2: ${{ secrets.GOOGLE_API_KEY_2 }}
    GOOGLE_API_KEY_3: ${{ secrets.GOOGLE_API_KEY_3 }}
  run: |
    python scripts/generate_blog_images.py --limit 5
  continue-on-error: true
```

### Paso 4: Generar Imágenes Localmente (Opcional)

Para regenerar todas las imágenes con Gemini:

```powershell
# Cargar variables de entorno
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^#=]+)=(.*)') {
        [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), 'Process')
    }
}

# Generar imágenes de alta calidad
python scripts/generate_blog_images.py --regenerate-all

# Sincronizar a carpeta pública
python scripts/sync_blog_images.py
```

## 📊 Comparación de Opciones

| Opción | Calidad | Costo | Disponibilidad |
|--------|---------|-------|----------------|
| **SVG Placeholders** | ★★★★☆ | GRATIS | ✅ Activo ahora |
| **Gemini Imagen 4.0** | ★★★★★ | $300 gratis | 🟡 Requiere billing |
| **Hugging Face** | ★★★☆☆ | GRATIS | ❌ Límite agotado |
| **Replicate FLUX** | ★★★★★ | $0.003/img | 🟡 Requiere token |
| **OpenAI DALL-E 3** | ★★★★★ | $0.04/img | ❌ Key inválida |

## 🎯 Recomendación

**Usar SVG hasta tener:**
1. ✅ Dominio propio configurado
2. ✅ $20 USD invertidos en Google Cloud
3. ✅ Billing activo

**Ventajas de esperar:**
- Blog funcional inmediatamente con SVGs profesionales
- Sin costos hasta tener tráfico real
- Mejor ROI una vez tengas dominio y audiencia

## 🔧 Scripts Disponibles

### Generar Imágenes (Cuando billing esté activo)
```bash
# Generar para posts nuevos
python scripts/generate_blog_images.py

# Regenerar todas las imágenes
python scripts/generate_blog_images.py --regenerate-all

# Limitar cantidad (para pruebas)
python scripts/generate_blog_images.py --limit 5
```

### Generar SVG Placeholders
```bash
# Generar SVG para posts sin imagen
python scripts/generate_placeholder_headers.py

# Regenerar todos los SVGs
python scripts/generate_placeholder_headers.py --force
```

### Pipeline Completo (Local)
```powershell
# Ejecutar pipeline completo con SVGs
.\scripts\run_full_rust_pipeline.ps1
```

## 📚 Documentación Relacionada

- 📖 [docs/IMAGE_GENERATION_GUIDE.md](docs/IMAGE_GENERATION_GUIDE.md) - Guía completa de uso
- 📖 [docs/IMAGE_GENERATION_SUMMARY.md](docs/IMAGE_GENERATION_SUMMARY.md) - Resumen técnico
- 📖 [IMAGE_GENERATION_QUICKSTART.md](IMAGE_GENERATION_QUICKSTART.md) - Quick start

## ✅ Checklist de Activación

- [ ] Activar billing en Google Cloud Console
- [ ] Verificar créditos gratuitos ($300)
- [ ] Descomentar steps en `investigation_pipeline.yml`
- [ ] Descomentar steps en `rust_blog_automation.yml`
- [ ] Probar generación local con `generate_blog_images.py`
- [ ] Ejecutar workflow manualmente para verificar
- [ ] Regenerar todas las imágenes con mejor calidad

---

**Próximos Pasos:**
1. Comprar dominio
2. Invertir $20 en Google Cloud
3. Activar billing
4. Generar imágenes de máxima calidad

**Contacto:** Para dudas sobre activación, revisar [Google Cloud Billing Docs](https://cloud.google.com/billing/docs/how-to/modify-project)
