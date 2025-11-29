"""
Script de prueba simple para verificar que Gemini funciona correctamente.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agents.scriptwriter import ScriptWriter

def test_gemini():
    """Test Gemini API connection."""
    print("\n🤖 Testing Gemini API...")

    # Load environment variables
    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("❌ GOOGLE_API_KEY not found in .env file")
        print("   Please edit .env and add your Gemini API key")
        return False

    if api_key == "your_gemini_api_key":
        print("❌ GOOGLE_API_KEY is still the default value")
        print("   Please edit .env and add your actual Gemini API key")
        return False

    print(f"✅ API Key found: {api_key[:10]}...")

    try:
        # Initialize ScriptWriter with Gemini
        writer = ScriptWriter(api_key=api_key, provider="gemini", model_name="gemini-2.5-flash")
        print("✅ ScriptWriter initialized successfully")

        # Test data
        test_repo = {
            "name": "test-repo",
            "description": "A simple test repository to verify Gemini integration",
            "readme": "This is a test project that demonstrates how to use AI for code generation."
        }

        print("\n📝 Generating test script...")
        print("   (This may take a few seconds...)")

        script = writer.generate_script(test_repo)

        if script:
            print("\n✅ Script generated successfully!")
            print("\n" + "="*60)
            print("📋 Generated Script Preview:")
            print("="*60)
            print(f"Hook: {script.get('hook', 'N/A')[:100]}...")
            print(f"Solution: {script.get('solution', 'N/A')[:100]}...")
            print(f"Verdict: {script.get('verdict', 'N/A')[:100]}...")
            print("="*60)

            return True
        else:
            print("❌ Failed to generate script")
            return False

    except Exception as e:
        print(f"\n❌ Gemini test failed: {e}")
        return False


def main():
    print("="*60)
    print("🧪 Gemini API Test")
    print("="*60)

    success = test_gemini()

    print("\n" + "="*60)
    if success:
        print("✅ Gemini is working correctly!")
        print("\n💡 Next steps:")
        print("   1. Configure Firebase (see setup_firebase.md)")
        print("   2. Run: python src/main.py --provider gemini --mode once")
    else:
        print("❌ Gemini test failed")
        print("\n💡 Troubleshooting:")
        print("   1. Check that .env file exists")
        print("   2. Verify GOOGLE_API_KEY is set correctly")
        print("   3. Get API key from: https://makersuite.google.com/app/apikey")
    print("="*60)


if __name__ == "__main__":
    main()
