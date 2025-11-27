"""
Rust Scanner Bridge - Integrates Rust-based GitHub scanner with Python workflow
"""
import subprocess
import json
import os
import logging
from pathlib import Path
from typing import Optional, Dict

logger = logging.getLogger(__name__)


class RustScanner:
    """Bridge to Rust-based GitHub scanner for faster performance"""

    def __init__(self, token: str):
        self.token = token
        self.rust_binary = self._find_rust_binary()

    def _find_rust_binary(self) -> Optional[Path]:
        """Find the Rust scanner binary"""
        possible_paths = [
            Path(__file__).parent.parent.parent / "rust-scanner" / "target" / "release" / "github-scanner-rust",
            Path(__file__).parent.parent.parent / "rust-scanner" / "target" / "release" / "github-scanner-rust.exe",
        ]

        for path in possible_paths:
            if path.exists():
                logger.info(f"✅ Found Rust scanner at: {path}")
                return path

        logger.warning("⚠️  Rust scanner binary not found. Use 'cargo build --release' to build it.")
        return None

    def is_available(self) -> bool:
        """Check if Rust scanner is available"""
        return self.rust_binary is not None and self.rust_binary.exists()

    def scan_and_find_repo(self) -> Optional[Dict]:
        """
        Use Rust scanner to find a valid repository
        Returns repository data or None
        """
        if not self.is_available():
            logger.warning("Rust scanner not available, falling back to Python scanner")
            return None

        try:
            logger.info("🦀 Running Rust scanner for faster performance...")

            env = os.environ.copy()
            env['GITHUB_TOKEN'] = self.token
            env['RUST_LOG'] = 'info'

            # Run Rust binary
            result = subprocess.run(
                [str(self.rust_binary)],
                capture_output=True,
                text=True,
                env=env,
                timeout=60  # 1 minute timeout
            )

            if result.returncode != 0:
                logger.error(f"Rust scanner failed with code {result.returncode}")
                logger.error(f"stderr: {result.stderr}")
                return None

            # Parse output
            output = result.stdout
            logger.info(f"Rust scanner output:\n{output}")

            # Extract JSON between markers
            if "__REPO_JSON__" in output and "__END_JSON__" in output:
                json_start = output.index("__REPO_JSON__") + len("__REPO_JSON__\n")
                json_end = output.index("__END_JSON__")
                json_str = output[json_start:json_end].strip()

                repo_data = json.loads(json_str)
                logger.info(f"✅ Rust scanner found repository: {repo_data.get('full_name')}")
                return repo_data
            else:
                logger.warning("No repository JSON found in Rust scanner output")
                return None

        except subprocess.TimeoutExpired:
            logger.error("Rust scanner timed out after 60 seconds")
            return None
        except Exception as e:
            logger.error(f"Error running Rust scanner: {e}")
            return None


def get_scanner(token: str, prefer_rust: bool = True):
    """
    Get the best available scanner (Rust or Python fallback)

    Args:
        token: GitHub API token
        prefer_rust: If True, try Rust scanner first

    Returns:
        Scanner instance (RustScanner or GitHubScanner)
    """
    if prefer_rust:
        rust_scanner = RustScanner(token)
        if rust_scanner.is_available():
            logger.info("🦀 Using Rust scanner (faster)")
            return rust_scanner

    # Fallback to Python scanner
    from scanner.github_scanner import GitHubScanner
    logger.info("🐍 Using Python scanner (fallback)")
    return GitHubScanner(token)
