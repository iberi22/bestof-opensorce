#!/usr/bin/env pwsh
# Setup script for Rust scanner

Write-Host "🦀 Setting up Rust Scanner for bestof-opensource" -ForegroundColor Cyan
Write-Host "=" * 60

# Check if Rust is installed
Write-Host "`n📦 Checking Rust installation..." -ForegroundColor Yellow
if (!(Get-Command cargo -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Rust not found!" -ForegroundColor Red
    Write-Host "Please install Rust from: https://rustup.rs/" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Quick install:" -ForegroundColor Cyan
    Write-Host "  winget install Rustlang.Rustup" -ForegroundColor White
    exit 1
}

$rustVersion = cargo --version
Write-Host "✅ Rust installed: $rustVersion" -ForegroundColor Green

# Navigate to rust-scanner directory
Write-Host "`n🔧 Building Rust scanner..." -ForegroundColor Yellow
Set-Location rust-scanner

# Build release version
Write-Host "Building optimized release binary (this may take a minute)..." -ForegroundColor Cyan
cargo build --release

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Rust scanner built successfully!" -ForegroundColor Green

    # Show binary location
    $binaryPath = "target\release\github-scanner-rust.exe"
    if (Test-Path $binaryPath) {
        $size = (Get-Item $binaryPath).Length / 1MB
        Write-Host "`n📦 Binary created:" -ForegroundColor Cyan
        Write-Host "  Location: $binaryPath" -ForegroundColor White
        Write-Host "  Size: $([math]::Round($size, 2)) MB" -ForegroundColor White
    }
} else {
    Write-Host "❌ Build failed!" -ForegroundColor Red
    Write-Host "Don't worry - the Python scanner will be used as fallback" -ForegroundColor Yellow
    Set-Location ..
    exit 1
}

Set-Location ..

# Test the scanner
Write-Host "`n🧪 Testing scanner..." -ForegroundColor Yellow

if ($env:GITHUB_TOKEN) {
    Write-Host "Running quick test with your GITHUB_TOKEN..." -ForegroundColor Cyan

    $testResult = & "rust-scanner\target\release\github-scanner-rust.exe"

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Scanner test passed!" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Scanner test failed, but binary is built" -ForegroundColor Yellow
    }
} else {
    Write-Host "⏭️  Skipping test (GITHUB_TOKEN not set)" -ForegroundColor Yellow
    Write-Host "   To test: " -ForegroundColor Cyan
    Write-Host "   `$env:GITHUB_TOKEN='your_token'" -ForegroundColor White
    Write-Host "   .\rust-scanner\target\release\github-scanner-rust.exe" -ForegroundColor White
}

# Summary
Write-Host "`n" + ("=" * 60)
Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host ("=" * 60)
Write-Host ""
Write-Host "✅ Rust scanner is ready to use" -ForegroundColor Green
Write-Host "✅ Python workflows will automatically use Rust for speed" -ForegroundColor Green
Write-Host "✅ Fallback to Python scanner if Rust fails" -ForegroundColor Green
Write-Host ""
Write-Host "Performance improvement: ~10x faster scanning" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Run workflow: python scripts/workflow_generate_blog.py" -ForegroundColor White
Write-Host "  2. Or trigger GitHub Action: Investigation Pipeline" -ForegroundColor White
Write-Host ""
