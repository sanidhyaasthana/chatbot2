from fastapi import FastAPI, Request, HTTPException, Depends
import spacy
import os

# Load spaCy NLP model
nlp = spacy.load("en_core_web_md")

app = FastAPI()

# API Key for Security
API_KEY = "your_secure_api_key"

# Middleware for API Key Authentication
async def verify_api_key(request: Request):
    key = request.headers.get("X-API-Key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return key

@app.get("/")
def home():
    return {"message": "Welcome to the Medical Chatbot API!"}

@app.post("/analyze")
async def analyze_text(data: dict, key: str = Depends(verify_api_key)):
    """
    Takes user input and processes it with NLP to provide medical insights.
    """
    user_input = data.get("text", "")
    if not user_input:
        raise HTTPException(status_code=400, detail="Text is required")

    doc = nlp(user_input)
    
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
    tokens = [token.text for token in doc]

    response = {
        "input": user_input,
        "tokens": tokens,
        "entities": entities,
        "response": generate_medical_advice(doc.text)
    }

    return response

def generate_medical_advice(text: str):
    """
    Simple function to generate predefined responses based on detected medical conditions.
    """
    if "headache" in text.lower():
        return "Try staying hydrated and resting. If it persists, consult a doctor."
    elif "fever" in text.lower():
        return "Drink plenty of fluids and monitor your temperature. Seek medical help if it worsens."
    elif "diabetes" in text.lower():
        return "Maintain a balanced diet and regularly check your blood sugar levels."
    return "Your input has been analyzed. For more details, consult a medical professional."

