import google.generativeai as genai
import os

print("--- STARTING TEST ---")

# 1. SETUP THE KEY
# This is the key from your screenshot ending in ...LP-Q
my_key = "AIzaSyA_S-PPBkzbJKXmC9wnz7GwtOpvQ__LP-Q"
genai.configure(api_key=my_key)

# 2. TRY TO TALK TO GOOGLE
try:
    print("Attempting to connect to Gemini...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Are you working?")
    
    print("\n✅ SUCCESS! The AI replied:")
    print(response.text)

except Exception as e:
    print("\n❌ ERROR! Something is wrong:")
    print(e)

print("--- END TEST ---")