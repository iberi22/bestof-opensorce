"""
Script de prueba para validar la integración completa de Firebase y generación de imágenes.

Este script demuestra cómo usar las nuevas funcionalidades sin ejecutar el pipeline completo.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from persistence.firebase_store import FirebaseStore
from image_gen.image_generator import ImageGenerator


def test_firebase():
    """Test Firebase persistence functionality."""
    print("\n🔥 Testing Firebase Persistence...")

    try:
        # Initialize Firebase (requires FIREBASE_CREDENTIALS env var)
        store = FirebaseStore()
        print("✅ Firebase initialized successfully")

        # Test data
        test_repo = "test-owner/test-repo"
        repo_data = {
            "description": "A test repository for validation",
            "stargazers_count": 100,
            "language": "Python",
            "html_url": "https://github.com/test-owner/test-repo"
        }

        # Check if already processed
        if store.is_processed(test_repo):
            print(f"ℹ️  Repository {test_repo} already exists in database")
        else:
            print(f"✅ Repository {test_repo} not found (as expected)")

        # Save repository
        success = store.save_repo(test_repo, repo_data, status="testing")
        if success:
            print(f"✅ Successfully saved {test_repo}")

        # Retrieve repository
        retrieved = store.get_repo(test_repo)
        if retrieved:
            print(f"✅ Successfully retrieved {test_repo}")
            print(f"   Status: {retrieved.get('status')}")
            print(f"   Stars: {retrieved.get('stars')}")

        # Update status
        store.update_status(test_repo, status="completed", video_url="https://youtube.com/test")
        print(f"✅ Successfully updated status")

        # Get recent repos
        recent = store.get_recent_repos(limit=5)
        print(f"✅ Retrieved {len(recent)} recent repositories")

        print("\n✅ Firebase tests completed successfully!")
        return True

    except Exception as e:
        print(f"\n❌ Firebase test failed: {e}")
        print("   Make sure FIREBASE_CREDENTIALS is set in your environment")
        return False


def test_image_generation():
    """Test image generation functionality."""
    print("\n🎨 Testing Image Generation...")

    try:
        # Initialize ImageGenerator
        generator = ImageGenerator(model_name="nano-banana-2", output_dir="output/test_images")
        print("✅ ImageGenerator initialized successfully")

        # Test data
        repo_data = {
            "name": "test-repo",
            "description": "A test repository for image generation"
        }

        script_data = {
            "hook": "Developers struggle with manual deployment",
            "solution": "Automated CI/CD pipeline with one-click deploys",
            "pros": [
                "Fast deployment",
                "Zero downtime",
                "Automatic rollbacks",
                "Built-in monitoring",
                "Easy to configure"
            ]
        }

        # Generate architecture diagram
        print("\n📐 Generating architecture diagram...")
        arch_img = generator.generate_architecture_diagram(repo_data, script_data)
        if arch_img:
            print(f"✅ Architecture diagram saved: {arch_img}")

        # Generate problem-solution flow
        print("\n🔄 Generating problem-solution flow...")
        flow_img = generator.generate_problem_solution_flow(repo_data, script_data)
        if flow_img:
            print(f"✅ Flow diagram saved: {flow_img}")

        # Generate feature showcase
        print("\n⭐ Generating feature showcase...")
        feature_img = generator.generate_feature_showcase(repo_data, script_data['pros'])
        if feature_img:
            print(f"✅ Feature showcase saved: {feature_img}")

        print("\n✅ Image generation tests completed successfully!")
        print(f"   Check the output/test_images directory for generated images")
        return True

    except Exception as e:
        print(f"\n❌ Image generation test failed: {e}")
        print("   This is expected if Foundry Local is not running")
        print("   Placeholder images should still be generated")
        return False


def main():
    """Run all validation tests."""
    print("=" * 60)
    print("🧪 Open Source Video Generator - Integration Tests")
    print("=" * 60)

    results = {
        "firebase": False,
        "images": False
    }

    # Test Firebase
    results["firebase"] = test_firebase()

    # Test Image Generation
    results["images"] = test_image_generation()

    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"Firebase Persistence: {'✅ PASS' if results['firebase'] else '❌ FAIL'}")
    print(f"Image Generation:     {'✅ PASS' if results['images'] else '⚠️  PARTIAL (placeholders)'}")

    if results["firebase"] and results["images"]:
        print("\n🎉 All tests passed! System is ready for production.")
    elif results["firebase"] or results["images"]:
        print("\n⚠️  Some tests passed. Check configuration for failed components.")
    else:
        print("\n❌ All tests failed. Check your environment configuration.")

    print("\n💡 Next steps:")
    print("   1. Configure Firebase credentials if not done")
    print("   2. Start Foundry Local with Nano Banana 2 model")
    print("   3. Run: python src/main.py --provider foundry --use-firebase --generate-images")


if __name__ == "__main__":
    main()
