# 🚀 Guía de Configuración de GitHub Pages

## ✅ Archivos Creados/Actualizados

He realizado las siguientes correcciones para habilitar GitHub Pages:

### 1. ✅ Creado `blog/Gemfile`
Archivo de dependencias de Ruby para Jekyll.

### 2. ✅ Creado `.github/workflows/deploy-blog.yml`
Workflow para auto-deploy del blog a GitHub Pages cuando se hace merge a main.

### 3. ✅ Actualizado `blog/_config.yml`
```yaml
url: "https://iberi22.github.io"
baseurl: "/plantilla-ingenieria-contexto"
```

---

## 📋 Pasos para Completar la Configuración

### Paso 1: Habilitar GitHub Pages en el Repositorio

1. Ir a: https://github.com/iberi22/plantilla-ingenieria-contexto/settings/pages

2. En **"Build and deployment"**, configurar:
   - **Source:** GitHub Actions
   - No seleccionar branch (se usa Actions)

3. Guardar cambios

### Paso 2: Commit y Push de los Cambios

```bash
# Verificar archivos modificados
git status

# Agregar archivos
git add blog/Gemfile \
        blog/_config.yml \
        .github/workflows/deploy-blog.yml \
        GITHUB_PAGES_ANALYSIS.md \
        GITHUB_PAGES_SETUP.md

# Commit
git commit -m "Configure GitHub Pages for blog

✅ Changes:
- Created blog/Gemfile with Jekyll dependencies
- Created deploy-blog.yml workflow for auto-deployment
- Updated _config.yml with correct URL and baseurl
- Added comprehensive analysis and setup documentation

🚀 Blog will be available at:
   https://iberi22.github.io/plantilla-ingenieria-contexto/

Next steps:
1. Enable GitHub Pages in repo settings (Source: GitHub Actions)
2. Push to trigger first deployment
3. Verify blog is accessible"

# Push
git push origin main
```

### Paso 3: Verificar el Deploy

1. Ir a: https://github.com/iberi22/plantilla-ingenieria-contexto/actions

2. Buscar el workflow **"Deploy Blog to GitHub Pages"**

3. Esperar a que complete (1-2 minutos)

4. Visitar el blog:
   ```
   https://iberi22.github.io/plantilla-ingenieria-contexto/
   ```

---

## 🔍 Verificación

### Comando para Verificar GitHub Pages API
```bash
gh api repos/iberi22/plantilla-ingenieria-contexto/pages
```

### Testing Local (Opcional)
```bash
cd blog
bundle install
bundle exec jekyll serve

# Visitar: http://localhost:4000/plantilla-ingenieria-contexto/
```

---

## 🎯 Resultado Esperado

Después de completar estos pasos:

✅ Blog accesible en: `https://iberi22.github.io/plantilla-ingenieria-contexto/`  
✅ Auto-deploy cuando se hace merge a main  
✅ Workflow `scan-and-blog.yml` crea posts automáticamente  
✅ Posts visibles en el blog después de merge de PR  

---

## 🔄 Flujo Completo Final

```
1. GitHub Actions Timer (Diario 3 AM UTC)
   ↓
2. Scan Workflow ejecuta
   ↓
3. Encuentra repo de calidad
   ↓
4. Gemini genera análisis
   ↓
5. Genera imágenes (diagramas)
   ↓
6. Crea post Markdown
   ↓
7. Crea Pull Request automático
   ↓
8. [REVISIÓN MANUAL]
   ↓
9. Merge PR a main
   ↓
10. Deploy Workflow se activa automáticamente
   ↓
11. Jekyll construye el sitio
   ↓
12. Deploy a GitHub Pages
   ↓
13. ✅ Blog actualizado y público
```

---

## 🐛 Troubleshooting

### Si el workflow falla:

**Check 1: Permisos**
```bash
# En Settings → Actions → General
# Workflow permissions: "Read and write permissions"
```

**Check 2: GitHub Pages habilitado**
```bash
# En Settings → Pages
# Source debe estar en "GitHub Actions"
```

**Check 3: Logs del workflow**
```bash
gh run list --workflow=deploy-blog.yml
gh run view <run-id> --log
```

### Si el blog no se ve bien:

**Check URLs en _config.yml:**
```yaml
url: "https://iberi22.github.io"
baseurl: "/plantilla-ingenieria-contexto"
```

**Rebuild forzado:**
```bash
gh workflow run deploy-blog.yml
```

---

## 📊 Estado Actual vs Deseado

### Antes
```
❌ GitHub Pages: No configurado
❌ Deploy: Manual
❌ Blog: No publicado
❌ URL: Placeholder
```

### Después (al completar pasos)
```
✅ GitHub Pages: Configurado con Actions
✅ Deploy: Automático en cada merge
✅ Blog: Público y actualizado
✅ URL: https://iberi22.github.io/plantilla-ingenieria-contexto/
```

---

## ⏱️ Tiempo Estimado

- **Habilitar GitHub Pages:** 2 minutos
- **Commit y push:** 2 minutos
- **Primer deploy:** 2-3 minutos
- **Verificación:** 1 minuto

**Total:** ~7-8 minutos

---

## 🎉 Siguientes Pasos

Una vez el blog esté publicado:

1. ✅ Verificar que los posts existentes se muestran correctamente
2. ✅ Ejecutar `scan-and-blog.yml` manualmente para generar nuevo post
3. ✅ Revisar y hacer merge del PR generado
4. ✅ Verificar que el nuevo post aparece en el blog
5. ✅ Documentar URL del blog en README principal

---

## 📝 Notas Importantes

### Limpieza Recomendada

Existe un workflow duplicado que deberías eliminar:

```bash
git rm .github/workflows/scan_and_blog.yml
git commit -m "Remove duplicate workflow (using scan-and-blog.yml)"
git push
```

### Ajuste de Frecuencia

El workflow `hourly_scan.yml` ejecuta cada hora. Considera cambiar a cada 6 horas:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Cada 6 horas
```

---

**Estado:** ✅ Preparado para deploy  
**Acción requerida:** Habilitar GitHub Pages en settings y push cambios  
**Tiempo:** ~8 minutos  
**Resultado:** Blog completamente funcional y auto-actualizado
