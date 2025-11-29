# Run Full Rust Pipeline
# Orchestrates the entire flow from Rust scanning to Blog generation

$ErrorActionPreference = "Stop"

# Load .env if it exists (simple parsing)
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match "^([^#=]+)=(.*)") {
            [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
        }
    }
}

if (-not $env:GITHUB_TOKEN) {
    Write-Error "GITHUB_TOKEN is missing. Please check .env file."
    exit 1
}

$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$OutputDir = "output"
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$RustOutput = "$OutputDir/rust_scan_$Timestamp.json"
$BridgeOutput = "$OutputDir/bridge_scan_$Timestamp.json"
$AiOutput = "$OutputDir/ai_scan_$Timestamp.json"

Write-Host "🚀 Starting Full Rust Pipeline..." -ForegroundColor Green

# 1. Run Rust Scanner
Write-Host "`n1️⃣  Running Rust Scanner..." -ForegroundColor Cyan
python scripts/run_rust_scanner_wrapper.py small $RustOutput
if ($LASTEXITCODE -ne 0) { exit 1 }

# 2. Bridge to AI Format
Write-Host "`n2️⃣  Bridging to AI Format..." -ForegroundColor Cyan
python scripts/bridge_rust_to_ai.py $RustOutput $BridgeOutput
if ($LASTEXITCODE -ne 0) { exit 1 }

# 3. AI Review
Write-Host "`n3️⃣  Running AI Review..." -ForegroundColor Cyan
python scripts/ai_review_from_rust.py $BridgeOutput $AiOutput
if ($LASTEXITCODE -ne 0) { exit 1 }

# 4. Generate Blogs
Write-Host "`n4️⃣  Generating Blogs..." -ForegroundColor Cyan
python scripts/generate_blogs_from_analysis.py $AiOutput
if ($LASTEXITCODE -ne 0) { exit 1 }

# 5. Generate Images with Gemini (with fallback to SVG)
Write-Host "`n5️⃣  Generating Images..." -ForegroundColor Cyan
if ($env:GOOGLE_API_KEY) {
    Write-Host "   Using Gemini Imagen API for high-quality images..." -ForegroundColor Yellow
    python scripts/generate_blog_images.py --limit 5
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   ⚠️  Gemini failed, falling back to SVG placeholders..." -ForegroundColor Yellow
        python scripts/generate_placeholder_headers.py
    }
} else {
    Write-Host "   No API key found, using SVG placeholders..." -ForegroundColor Yellow
    python scripts/generate_placeholder_headers.py
}
if ($LASTEXITCODE -ne 0) { exit 1 }

# 6. Sync Images
Write-Host "`n6️⃣  Syncing Images to Public..." -ForegroundColor Cyan
python scripts/sync_blog_images.py
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host "`n✅ Pipeline Complete!" -ForegroundColor Green
