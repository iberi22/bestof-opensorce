"""
List available Gemini models.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key or api_key == "your_gemini_api_key":
    print("❌ Please set GOOGLE_API_KEY in .env file")
    exit(1)

genai.configure(api_key=api_key)

print("\n📋 Available Gemini Models:\n")
print("="*60)

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ {model.name}")
        print(f"   Display Name: {model.display_name}")
        print(f"   Description: {model.description[:80]}...")
        print()

print("="*60)
