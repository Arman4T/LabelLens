import google.generativeai as genai
import os

# Your API Key
os.environ["GEMINI_API_KEY"] = "AIzaSyA_S-PPBkzbJKXmC9wnz7GwtOpvQ__LP-Q"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

print("--- SEARCHING FOR AVAILABLE MODELS ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ FOUND: {m.name}")
except Exception as e:
    print(f"❌ ERROR: {e}")
print("--------------------------------------")