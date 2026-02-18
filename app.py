import os
import json
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- CONFIGURATION ---
# Your API Key
os.environ["GEMINI_API_KEY"] = "Google API Key"

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Use the specific version that works for you
model = genai.GenerativeModel('gemini-2.5-flash') 

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- THE AI BRAIN ---
def analyze_label_with_ai(image_path):
    prompt = """
    You are a strict Food Safety Auditor (FSSAI/FDA standards). Analyze this product label image.
    Return ONLY a raw JSON object. Do not use Markdown.
    
    Section 1: Basic Compliance (Presence Check)
    - "Expiry Date" (Look for Exp, Use By, Best Before)
    - "MRP / Price" (Look for MRP, Rs, Price)
    - "Net Weight" (Look for g, kg, ml, L, Net Qty)
    - "License No." (Look for FSSAI, Lic No)

    Section 2: Ingredient Standards Audit (Deep Check)
    Analyze the text of the ingredient list:
    1. "Allergen Declaration": Are allergens (Milk, Soy, Nuts, Wheat) clearly mentioned or bolded? If not, flag as "Allergens not highlighted".
    2. "Additive Format": Do additives have class titles (e.g., 'Preservative (INS 211)')? If just numbers are used, flag as "Improper Additive Labeling".
    3. "Veg/Non-Veg": Look for the Green Dot (Veg) or Brown Triangle (Non-Veg). If missing, flag as "Veg Symbol Missing".
    
    Section 3: Nutritional Health Check
    - "High Sugar": If Added Sugar > 25g (Flag as "High Sugar")
    - "High Sodium": If Sodium > 600mg (Flag as "High Sodium")

    Output Format:
    {
        "score": 85,
        "found": ["MRP", "Net Weight", "Ingredients"],
        "missing": ["Expiry Date"],
        "ingredient_issues": ["Allergens not highlighted", "Veg Symbol Missing"],
        "health_warnings": ["High Sugar detected (32g)"],
        "raw_text": "Extracted summary..."
    }
    """
    
    try:
        sample_file = genai.upload_file(path=image_path, display_name="Label Image")
        response = model.generate_content([sample_file, prompt])
        
        json_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(json_text)
        
    except Exception as e:
        print("GOOGLE AI ERROR:", e)
        return {
            "error": str(e), 
            "score": 0, 
            "found": [], 
            "missing": ["Error analyzing image"], 
            "ingredient_issues": [],
            "health_warnings": []
        }

# --- ROUTES ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files: return jsonify({'error': 'No file'})
    file = request.files['file']
    if file.filename == '': return jsonify({'error': 'No file'})

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        result = analyze_label_with_ai(filepath)
        os.remove(filepath)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
