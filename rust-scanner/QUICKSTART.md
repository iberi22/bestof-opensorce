# Quick Setup Guide - Rust Scanner

## 1. Install Rust (if not installed)

```powershell
# Option 1: Using winget
winget install Rustlang.Rustup

# Option 2: Download from https://rustup.rs/
```

## 2. Build the Scanner

```powershell
# Automated setup (recommended)
.\rust-scanner\setup.ps1

# Manual build
cd rust-scanner
cargo build --release
cd ..
```

## 3. Test It

```powershell
# Set your GitHub token
$env:GITHUB_TOKEN = "your_github_token_here"

# Run the workflow
python scripts/workflow_generate_blog.py
```

## 4. Verify Performance

Check the logs for:
- 🦀 = Rust scanner used (~3 seconds)
- 🐍 = Python fallback (~30 seconds)

## Performance Comparison

| Scanner | Time | Improvement |
|---------|------|-------------|
| Python  | ~30s | Baseline    |
| Rust    | ~3s  | **10x faster** |

## Troubleshooting

### Build fails?
- Don't worry! The system automatically falls back to Python
- Check `docs/RUST_MIGRATION_GUIDE.md` for detailed troubleshooting

### Want to skip Rust?
```powershell
# The workflow will use Python automatically if Rust binary is missing
```

## What Gets Installed

- ✅ Rust compiler and cargo (package manager)
- ✅ Optimized binary at `rust-scanner/target/release/github-scanner-rust.exe`
- ✅ Automatic integration with Python workflows
- ✅ Smart fallback system

## Next Steps

1. Run `.\rust-scanner\setup.ps1` to build
2. Test with `python scripts/workflow_generate_blog.py`
3. Enjoy 10x faster scanning! 🚀

For detailed documentation, see `rust-scanner/README.md` and `docs/RUST_MIGRATION_GUIDE.md`.
