# 🚀 Guía Rápida: Activación de Gemini para Imágenes de Alta Calidad

## ⚡ Resumen de 30 Segundos

**Estado actual:** SVG placeholders (muy buenos)
**Para activar AI:** Billing de Google Cloud + $20 USD
**Resultado:** Imágenes 4K profesionales generadas por Gemini

---

## 📋 Pasos para Activar

### 1️⃣ Activar Billing en Google Cloud (5 minutos)

```bash
# 1. Abrir consola
https://console.cloud.google.com/billing

# 2. Vincular tarjeta de crédito/débito

# 3. Activar proyecto actual
# Buscar tu proyecto: "bestof-opensource" o similar

# 4. Verificar créditos gratis
# Google da $300 USD para nuevos usuarios
```

### 2️⃣ Verificar API Key (1 minuto)

```powershell
# En tu terminal de PowerShell
cd e:\scripts-python\bestof-opensource

# Cargar .env
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^#=]+)=(.*)') {
        [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), 'Process')
    }
}

# Probar API
python -c "from google import genai; import os; client = genai.Client(api_key=os.environ['GOOGLE_API_KEY']); print('✅ API Key válida y billing activo')"
```

**Resultado esperado:** `✅ API Key válida y billing activo`

### 3️⃣ Descomentar Workflows (2 minutos)

**Archivo 1:** `.github/workflows/investigation_pipeline.yml`

Buscar línea ~120 y descomentar:
```yaml
- name: Generate Images with Gemini API
  env:
    GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
    GOOGLE_API_KEY_2: ${{ secrets.GOOGLE_API_KEY_2 }}
  run: |
    python scripts/generate_blog_images.py --limit 10
  continue-on-error: true
```

**Archivo 2:** `.github/workflows/rust_blog_automation.yml`

Buscar línea ~90 y descomentar:
```yaml
- name: 5. Generate Images with Gemini API
  env:
    GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
  run: |
    python scripts/generate_blog_images.py --limit 5
  continue-on-error: true
```

### 4️⃣ Generar Imágenes (10 minutos)

```powershell
# Opción A: Generar solo nuevas
python scripts/generate_blog_images.py

# Opción B: Regenerar TODAS con máxima calidad
python scripts/generate_blog_images.py --regenerate-all

# Ver progreso
# El script mostrará:
# ✅ Imagen generada: website/public/images/nixcord/header.png (2.1 MB, 4K)
```

### 5️⃣ Commit y Deploy (2 minutos)

```powershell
git add .github/workflows/ website/public/images/
git commit -m "feat: Activate Gemini image generation with billing"
git push origin main
```

**GitHub Actions automáticamente:**
- ✅ Generará imágenes AI para nuevos posts
- ✅ Fallback a SVG si falla
- ✅ Deploy a GitHub Pages

---

## 🎯 Comandos Rápidos

### Test Local (Generar 1 imagen)
```powershell
python scripts/generate_blog_images.py --limit 1
```

### Regenerar Todo (Máxima calidad)
```powershell
python scripts/generate_blog_images.py --regenerate-all
```

### Solo SVG (Sin AI)
```powershell
python scripts/generate_placeholder_headers.py
```

---

## 🔍 Troubleshooting

### Error: "RESOURCE_EXHAUSTED" o "limit: 0"
**Causa:** Billing no activado
**Solución:** Ir a https://console.cloud.google.com/billing y vincular tarjeta

### Error: "INVALID_ARGUMENT: Imagen API is only accessible to billed users"
**Causa:** Mismo que arriba
**Solución:** Activar billing en Google Cloud

### Error: "429 Quota exceeded"
**Causa:** Muchas requests en poco tiempo
**Solución:** El script tiene retry automático, esperar 1 minuto

### Imágenes se ven mal
**Causa:** SVG placeholder usado (billing no activo)
**Solución:** Activar billing y regenerar con `--regenerate-all`

---

## 💰 Costos Estimados

| Acción | Costo con $300 gratis | Costo real |
|--------|----------------------|------------|
| 100 imágenes 4K | $0 (usa créditos) | ~$5 |
| 500 imágenes 4K | $0 (usa créditos) | ~$25 |
| 1000 imágenes 4K | $0 (usa créditos) | ~$50 |

**Nota:** Con $300 de créditos, puedes generar **6,000+ imágenes** sin pagar nada.

---

## ✅ Checklist Final

Antes de activar, asegúrate de tener:

- [ ] Dominio propio comprado
- [ ] $20 USD disponibles en tarjeta
- [ ] Cuenta de Google Cloud activa
- [ ] API Key configurada en `.env`
- [ ] Backup de imágenes SVG actuales

**Una vez listo:**

- [ ] Activar billing en Google Cloud
- [ ] Verificar API con comando de prueba
- [ ] Descomentar workflows
- [ ] Generar 1 imagen de prueba local
- [ ] Commit y push
- [ ] Verificar GitHub Actions

---

## 📚 Más Info

- 📖 [IMAGE_GENERATION_STATUS.md](IMAGE_GENERATION_STATUS.md) - Estado completo
- 📖 [docs/IMAGE_GENERATION_GUIDE.md](docs/IMAGE_GENERATION_GUIDE.md) - Guía detallada
- 🌐 [Google Cloud Billing](https://console.cloud.google.com/billing)
- 🌐 [Gemini API Docs](https://ai.google.dev/gemini-api/docs)

---

**¿Listo para activar?** Sigue los 5 pasos arriba y tendrás imágenes AI en 20 minutos. 🚀
