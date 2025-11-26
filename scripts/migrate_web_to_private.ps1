# ========================================
# Script: Migrar /web/ al Repositorio Privado
# ========================================
#
# Este script mueve la carpeta /web/ (React Dashboard) y documentación
# relacionada con generación de videos al repositorio privado bestof-pipeline
#
# Uso:
#   .\migrate_web_to_private.ps1 -PrivateRepoPath "C:\ruta\a\bestof-pipeline"
#

param(
    [Parameter(Mandatory=$false)]
    [string]$PrivateRepoPath = "..\bestof-pipeline",

    [Parameter(Mandatory=$false)]
    [switch]$DryRun = $false
)

$ErrorActionPreference = "Stop"

# Colores
$Green = "Green"
$Yellow = "Yellow"
$Red = "Red"
$Cyan = "Cyan"

Write-Host "`n========================================" -ForegroundColor $Cyan
Write-Host "  Migración: /web/ → Repo Privado" -ForegroundColor $Cyan
Write-Host "========================================`n" -ForegroundColor $Cyan

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "web")) {
    Write-Host "❌ Error: No se encuentra la carpeta /web/" -ForegroundColor $Red
    Write-Host "   Ejecuta este script desde la raíz del proyecto" -ForegroundColor $Yellow
    exit 1
}

# Verificar que existe el repo privado
if (-not (Test-Path $PrivateRepoPath)) {
    Write-Host "❌ Error: No se encuentra el repositorio privado en: $PrivateRepoPath" -ForegroundColor $Red
    Write-Host "   Clona el repositorio privado primero:" -ForegroundColor $Yellow
    Write-Host "   git clone https://github.com/iberi22/bestof-pipeline.git $PrivateRepoPath" -ForegroundColor $Yellow
    exit 1
}

Write-Host "📂 Repositorio público:  $(Get-Location)" -ForegroundColor $Green
Write-Host "📂 Repositorio privado:  $(Resolve-Path $PrivateRepoPath)" -ForegroundColor $Green
Write-Host ""

if ($DryRun) {
    Write-Host "🔍 Modo DRY RUN - No se realizarán cambios reales`n" -ForegroundColor $Yellow
}

# ========================================
# Archivos y Carpetas a Migrar
# ========================================

$ItemsToMove = @{
    # Dashboard React
    "web/" = "web/"

    # Documentación sobre videos y voice
    "docs/MULTILINGUAL_README.md" = "docs/MULTILINGUAL_README.md"
    "docs/OPENCUT_ANALYSIS.md" = "docs/OPENCUT_ANALYSIS.md"
    "docs/OPENCUT_INTEGRATION.md" = "docs/OPENCUT_INTEGRATION.md"
    "docs/QUEUE_SYSTEM_GUIDE.md" = "docs/QUEUE_SYSTEM_GUIDE.md"
    "docs/planning/BLOG_VIDEO_ARCHITECTURE.md" = "docs/BLOG_VIDEO_ARCHITECTURE.md"
}

Write-Host "📋 Archivos a migrar:" -ForegroundColor $Cyan
$ItemsToMove.Keys | ForEach-Object {
    if (Test-Path $_) {
        Write-Host "  ✅ $_" -ForegroundColor $Green
    } else {
        Write-Host "  ⚠️  $_ (no existe)" -ForegroundColor $Yellow
    }
}
Write-Host ""

# ========================================
# Confirmación
# ========================================

if (-not $DryRun) {
    Write-Host "⚠️  Esta operación:" -ForegroundColor $Yellow
    Write-Host "   1. Copiará los archivos al repo privado" -ForegroundColor $Yellow
    Write-Host "   2. Los eliminará del repo público" -ForegroundColor $Yellow
    Write-Host "   3. Actualizará el README del repo público`n" -ForegroundColor $Yellow

    $confirm = Read-Host "¿Continuar? (s/n)"
    if ($confirm -ne "s" -and $confirm -ne "S") {
        Write-Host "`n❌ Operación cancelada" -ForegroundColor $Red
        exit 0
    }
}

# ========================================
# Migración
# ========================================

Write-Host "`n🚀 Iniciando migración...`n" -ForegroundColor $Cyan

$successCount = 0
$errorCount = 0

foreach ($item in $ItemsToMove.GetEnumerator()) {
    $sourcePath = $item.Key
    $destPath = Join-Path $PrivateRepoPath $item.Value

    if (-not (Test-Path $sourcePath)) {
        Write-Host "⏭️  Saltando $sourcePath (no existe)" -ForegroundColor $Yellow
        continue
    }

    try {
        # Crear directorio de destino si no existe
        $destDir = Split-Path $destPath -Parent
        if (-not (Test-Path $destDir)) {
            if (-not $DryRun) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            Write-Host "📁 Creado directorio: $destDir" -ForegroundColor $Green
        }

        # Copiar archivo/carpeta
        if (-not $DryRun) {
            if (Test-Path $sourcePath -PathType Container) {
                # Es una carpeta
                Copy-Item -Path $sourcePath -Destination $destPath -Recurse -Force
            } else {
                # Es un archivo
                Copy-Item -Path $sourcePath -Destination $destPath -Force
            }
        }

        Write-Host "✅ Copiado: $sourcePath → $destPath" -ForegroundColor $Green
        $successCount++

    } catch {
        Write-Host "❌ Error copiando $sourcePath : $_" -ForegroundColor $Red
        $errorCount++
    }
}

Write-Host ""

# ========================================
# Eliminar del repo público (solo si no es dry-run)
# ========================================

if (-not $DryRun -and $successCount -gt 0) {
    Write-Host "🗑️  Eliminando archivos del repo público...`n" -ForegroundColor $Cyan

    foreach ($item in $ItemsToMove.Keys) {
        if (Test-Path $item) {
            try {
                Remove-Item -Path $item -Recurse -Force
                Write-Host "🗑️  Eliminado: $item" -ForegroundColor $Yellow
            } catch {
                Write-Host "❌ Error eliminando $item : $_" -ForegroundColor $Red
            }
        }
    }
}

# ========================================
# Actualizar .gitignore del repo privado
# ========================================

$gitignorePath = Join-Path $PrivateRepoPath ".gitignore"
$gitignoreContent = @"

# Web Dashboard (React + Vite)
web/node_modules/
web/dist/
web/.env
web/.env.local

"@

if (-not $DryRun) {
    if (Test-Path $gitignorePath) {
        Add-Content -Path $gitignorePath -Value $gitignoreContent
        Write-Host "`n✅ Actualizado .gitignore del repo privado" -ForegroundColor $Green
    }
}

# ========================================
# Resumen
# ========================================

Write-Host "`n========================================" -ForegroundColor $Cyan
Write-Host "  Resumen de Migración" -ForegroundColor $Cyan
Write-Host "========================================`n" -ForegroundColor $Cyan

Write-Host "✅ Archivos copiados exitosamente: $successCount" -ForegroundColor $Green
if ($errorCount -gt 0) {
    Write-Host "❌ Errores: $errorCount" -ForegroundColor $Red
}

if ($DryRun) {
    Write-Host "`n🔍 Esto fue un DRY RUN - No se realizaron cambios" -ForegroundColor $Yellow
    Write-Host "   Ejecuta sin -DryRun para aplicar los cambios" -ForegroundColor $Yellow
} else {
    Write-Host "`n📝 Próximos pasos:" -ForegroundColor $Cyan
    Write-Host "   1. En el repo privado:" -ForegroundColor $Yellow
    Write-Host "      cd $PrivateRepoPath" -ForegroundColor $White
    Write-Host "      git add ." -ForegroundColor $White
    Write-Host "      git commit -m 'feat: add web dashboard and video generation docs'" -ForegroundColor $White
    Write-Host "      git push" -ForegroundColor $White
    Write-Host ""
    Write-Host "   2. En el repo público:" -ForegroundColor $Yellow
    Write-Host "      git add ." -ForegroundColor $White
    Write-Host "      git commit -m 'refactor: move web dashboard to private repo'" -ForegroundColor $White
    Write-Host "      git push" -ForegroundColor $White
    Write-Host ""
    Write-Host "   3. Actualizar README.md del repo público (ver MIGRATION_WEB_README.md)" -ForegroundColor $Yellow
}

Write-Host "`n✅ Migración completada!`n" -ForegroundColor $Green
