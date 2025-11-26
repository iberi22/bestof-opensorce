# ========================================
# SCRIPT DE VERIFICACIÓN
# ========================================
# Verifica que la migración entre repos se completó exitosamente

param(
    [string]$PublicRepo = "E:\scripts-python\op-to-video",
    [string]$PrivateRepo = "E:\scripts-python\bestof-pipeline"
)

$ErrorActionPreference = "Continue"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "VERIFICACIÓN DE MIGRACIÓN" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ========================================
# 1. Verificar que repos existen
# ========================================
Write-Host "[1/5] Verificando que ambos repos existen..." -ForegroundColor Cyan

$PublicExists = Test-Path $PublicRepo
$PrivateExists = Test-Path $PrivateRepo

if ($PublicExists) {
    Write-Host "  ✓ Repo público encontrado: $PublicRepo" -ForegroundColor Green
} else {
    Write-Host "  ✗ Repo público NO encontrado: $PublicRepo" -ForegroundColor Red
    exit 1
}

if ($PrivateExists) {
    Write-Host "  ✓ Repo privado encontrado: $PrivateRepo" -ForegroundColor Green
} else {
    Write-Host "  ✗ Repo privado NO encontrado: $PrivateRepo" -ForegroundColor Red
    exit 1
}

# ========================================
# 2. Verificar archivos en repo PRIVADO
# ========================================
Write-Host ""
Write-Host "[2/5] Verificando archivos en repo privado..." -ForegroundColor Cyan

$PrivateExpected = @(
    "src\blog_generator\blog_manager.py",
    "src\image_gen\image_generator.py",
    "src\scanner\github_scanner.py",
    "src\persistence\local_store.py",
    "scripts\manage_investigations.py",
    "api\multilingual_api.py",
    "requirements.txt",
    "README.md",
    ".env.example",
    ".github\workflows\generate_content.yml"
)

$PrivateMissing = @()
foreach ($file in $PrivateExpected) {
    $path = Join-Path $PrivateRepo $file
    if (Test-Path $path) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file" -ForegroundColor Red
        $PrivateMissing += $file
    }
}

if ($PrivateMissing.Count -gt 0) {
    Write-Host ""
    Write-Host "  ⚠ ADVERTENCIA: Faltan $($PrivateMissing.Count) archivos en repo privado" -ForegroundColor Yellow
} else {
    Write-Host "  ✓ Todos los archivos esenciales presentes" -ForegroundColor Green
}

# ========================================
# 3. Verificar archivos ELIMINADOS de público
# ========================================
Write-Host ""
Write-Host "[3/5] Verificando que archivos privados fueron eliminados del público..." -ForegroundColor Cyan

$ShouldBeDeleted = @(
    "TTS",
    "Trainer",
    "src\blog_generator",
    "src\image_gen",
    "scripts\manage_investigations.py",
    "api\multilingual_api.py",
    "Dockerfile",
    "docker-compose.yml"
)

$StillPresent = @()
foreach ($file in $ShouldBeDeleted) {
    $path = Join-Path $PublicRepo $file
    if (Test-Path $path) {
        Write-Host "  ✗ TODAVÍA EXISTE: $file" -ForegroundColor Red
        $StillPresent += $file
    } else {
        Write-Host "  ✓ Eliminado: $file" -ForegroundColor Green
    }
}

if ($StillPresent.Count -gt 0) {
    Write-Host ""
    Write-Host "  ⚠ ADVERTENCIA: $($StillPresent.Count) archivos privados aún en repo público" -ForegroundColor Yellow
} else {
    Write-Host "  ✓ Todos los archivos privados eliminados correctamente" -ForegroundColor Green
}

# ========================================
# 4. Verificar archivos PÚBLICOS intactos
# ========================================
Write-Host ""
Write-Host "[4/5] Verificando que archivos públicos permanecen intactos..." -ForegroundColor Cyan

$PublicExpected = @(
    "investigations",
    "website\src\pages\index.astro",
    "website\package.json",
    "web\src\App.jsx",
    "web\package.json",
    "src\scanner\github_scanner.py",
    "src\persistence\local_store.py",
    "scripts\run_scanner.py",
    "README.md",
    "requirements.txt"
)

$PublicMissing = @()
foreach ($file in $PublicExpected) {
    $path = Join-Path $PublicRepo $file
    if (Test-Path $path) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ FALTA: $file" -ForegroundColor Red
        $PublicMissing += $file
    }
}

if ($PublicMissing.Count -gt 0) {
    Write-Host ""
    Write-Host "  ⚠ ERROR: Faltan $($PublicMissing.Count) archivos públicos esenciales!" -ForegroundColor Red
} else {
    Write-Host "  ✓ Todos los archivos públicos intactos" -ForegroundColor Green
}

# ========================================
# 5. Verificar Git remotes
# ========================================
Write-Host ""
Write-Host "[5/5] Verificando Git remotes..." -ForegroundColor Cyan

Push-Location $PublicRepo
$PublicRemote = git remote get-url origin 2>$null
if ($PublicRemote -like "*bestof-opensorce*") {
    Write-Host "  ✓ Repo público: $PublicRemote" -ForegroundColor Green
} else {
    Write-Host "  ✗ Remote público incorrecto: $PublicRemote" -ForegroundColor Red
}
Pop-Location

Push-Location $PrivateRepo
$PrivateRemote = git remote get-url origin 2>$null
if ($PrivateRemote -like "*bestof-pipeline*") {
    Write-Host "  ✓ Repo privado: $PrivateRemote" -ForegroundColor Green
} else {
    Write-Host "  ✗ Remote privado incorrecto: $PrivateRemote" -ForegroundColor Red
}
Pop-Location

# ========================================
# Resumen final
# ========================================
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "RESUMEN DE VERIFICACIÓN" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$TotalIssues = $PrivateMissing.Count + $StillPresent.Count + $PublicMissing.Count

if ($TotalIssues -eq 0) {
    Write-Host "✅ MIGRACIÓN EXITOSA" -ForegroundColor Green
    Write-Host ""
    Write-Host "Todos los archivos están en el lugar correcto:" -ForegroundColor Green
    Write-Host "  - Código privado → bestof-pipeline (private repo)" -ForegroundColor White
    Write-Host "  - Blog/Investigations → bestof-opensorce (public repo)" -ForegroundColor White
    Write-Host ""
    Write-Host "Repos remotos configurados:" -ForegroundColor Green
    Write-Host "  PUBLIC:  $PublicRemote" -ForegroundColor White
    Write-Host "  PRIVATE: $PrivateRemote" -ForegroundColor White
} else {
    Write-Host "⚠ PROBLEMAS ENCONTRADOS: $TotalIssues" -ForegroundColor Yellow
    Write-Host ""
    if ($PrivateMissing.Count -gt 0) {
        Write-Host "  - $($PrivateMissing.Count) archivos faltan en repo privado" -ForegroundColor Red
    }
    if ($StillPresent.Count -gt 0) {
        Write-Host "  - $($StillPresent.Count) archivos privados aún en repo público" -ForegroundColor Red
    }
    if ($PublicMissing.Count -gt 0) {
        Write-Host "  - $($PublicMissing.Count) archivos públicos perdidos" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Revisa los errores arriba y corrígelos manualmente." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

# ========================================
# Stats finales
# ========================================
Write-Host ""
Write-Host "📊 ESTADÍSTICAS" -ForegroundColor Cyan
Write-Host ""

Push-Location $PublicRepo
$PublicFiles = (Get-ChildItem -Recurse -File | Where-Object { $_.FullName -notmatch 'node_modules|\.git|__pycache__|\.vscode' }).Count
$PublicSize = (Get-ChildItem -Recurse -File | Where-Object { $_.FullName -notmatch 'node_modules|\.git|__pycache__' } | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host "Repo PÚBLICO:" -ForegroundColor Green
Write-Host "  Archivos: $PublicFiles" -ForegroundColor White
Write-Host "  Tamaño: $([math]::Round($PublicSize, 2)) MB (sin node_modules)" -ForegroundColor White
Pop-Location

Push-Location $PrivateRepo
$PrivateFiles = (Get-ChildItem -Recurse -File | Where-Object { $_.FullName -notmatch 'node_modules|\.git|__pycache__|\.vscode' }).Count
$PrivateSize = (Get-ChildItem -Recurse -File | Where-Object { $_.FullName -notmatch 'node_modules|\.git|__pycache__' } | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host ""
Write-Host "Repo PRIVADO:" -ForegroundColor Yellow
Write-Host "  Archivos: $PrivateFiles" -ForegroundColor White
Write-Host "  Tamaño: $([math]::Round($PrivateSize, 2)) MB (sin node_modules)" -ForegroundColor White
Pop-Location

Write-Host ""
