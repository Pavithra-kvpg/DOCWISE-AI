# modules/pdf_analyzer.py

import fitz  # PyMuPDF
from transformers import pipeline
import pytesseract
from PIL import Image
import io
import spacy

# Load models once
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=-1)
nlp = spacy.load("en_core_web_sm")

MEDICAL_KEYWORDS = [
    "patient", "diagnosis", "treatment", "prescription", "medical history",
    "symptoms", "blood test", "lab report", "MRI", "CT scan", "disease",
    "doctor", "hospital", "medication", "prognosis", "allergy", "dose"
]

DISEASE_SYMPTOMS = {
    "diabetes": ["thirst", "urination", "fatigue", "blurred vision", "weight loss"],
    "hypertension": ["headache", "dizziness", "blurred vision", "shortness of breath"],
    "asthma": ["wheezing", "shortness of breath", "coughing", "chest tightness"],
    "influenza": ["fever", "cough", "sore throat", "runny nose", "body aches"],
    "pneumonia": ["cough", "fever", "chills", "shortness of breath", "chest pain"],
    "coronary artery disease": ["chest pain", "shortness of breath", "heart attack"],
    "arthritis": ["joint pain", "stiffness", "swelling", "decreased range of motion"],
    "migraine": ["headache", "nausea", "sensitivity to light", "aura"],
    "gastroenteritis": ["diarrhea", "nausea", "vomiting", "abdominal pain", "fever"],
    "urinary tract infection": ["burning urination", "frequent urination", "pelvic pain"]
}

def chunk_text(text, max_chunk_size=900):
    chunks = []
    while len(text) > max_chunk_size:
        split_index = text.rfind(".", 0, max_chunk_size)
        if split_index == -1:
            split_index = max_chunk_size
        chunks.append(text[:split_index + 1])
        text = text[split_index + 1:]
    if text:
        chunks.append(text)
    return chunks

def is_medical(text):
    count = sum(1 for kw in MEDICAL_KEYWORDS if kw.lower() in text.lower())
    return count >= 2

def extract_text_from_pdf(file_bytes):
    doc = fitz.open("pdf", file_bytes)
    text = ""
    for page in doc:
        page_text = page.get_text()
        if page_text.strip():
            text += page_text
        else:
            for img in page.get_images(full=True):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))
                text += pytesseract.image_to_string(image)
    return text

def extract_symptoms(text):
    symptoms = []
    doc = nlp(text.lower())
    
    # Enhanced symptom extraction
    symptom_patterns = [
        "pain", "ache", "sore", "tenderness", "discomfort", "fever", "nausea",
        "vomiting", "dizziness", "fatigue", "weakness", "cough", "headache",
        "rash", "swelling", "bleeding", "bruising", "shortness of breath",
        "wheezing", "chills", "sweating", "palpitations", "numbness", "tingling"
    ]
    
    for sent in doc.sents:
        sent_text = sent.text.lower()
        for symptom in symptom_patterns:
            if symptom in sent_text:
                # Extract context around the symptom
                words = sent_text.split()
                if symptom in words:
                    index = words.index(symptom)
                    start = max(0, index - 2)
                    end = min(len(words), index + 3)
                    context = " ".join(words[start:end])
                    if context not in symptoms:
                        symptoms.append(context)
    
    return list(set(symptoms))[:10]  # Limit to top 10 symptoms

def predict_disease(symptoms, text):
    disease_scores = {}
    text_lower = text.lower()
    
    for disease, disease_syms in DISEASE_SYMPTOMS.items():
        score = 0
        # Score based on symptoms
        for symptom in symptoms:
            for ds in disease_syms:
                if ds in symptom:
                    score += 2
        
        # Score based on disease mentions in text
        if disease in text_lower:
            score += 3
        
        # Score based on keyword mentions
        for ds in disease_syms:
            if ds in text_lower:
                score += 1
        
        if score > 0:
            disease_scores[disease] = score
    
    return sorted(disease_scores.items(), key=lambda x: x[1], reverse=True)[:3]

def suggest_actions(diseases, symptoms):
    actions = []
    
    # Emergency symptoms check
    severe_symptoms = [
        "chest pain", "shortness of breath", "severe bleeding", 
        "loss of consciousness", "difficulty breathing", "severe headache"
    ]
    
    if any(severe in symptom for severe in severe_symptoms for symptom in symptoms):
        actions.append("🚨 SEEK EMERGENCY MEDICAL ATTENTION IMMEDIATELY")
    
    # Disease-specific recommendations
    specialist_mapping = {
        "diabetes": "Schedule appointment with Endocrinologist",
        "hypertension": "Consult Cardiologist for blood pressure management",
        "asthma": "See Pulmonologist for respiratory assessment",
        "influenza": "Rest, hydrate, and monitor symptoms",
        "pneumonia": "Urgent consultation with Pulmonologist required",
        "coronary artery disease": "Immediate Cardiologist consultation recommended",
        "arthritis": "Consult Rheumatologist for joint evaluation",
        "migraine": "See Neurologist for headache management",
        "gastroenteritis": "Consult Gastroenterologist if symptoms persist",
        "urinary tract infection": "See Urologist for proper treatment"
    }
    
    for disease, score in diseases:
        if disease in specialist_mapping:
            actions.append(specialist_mapping[disease])
    
    # General recommendations
    if not actions:
        actions.append("Schedule follow-up with Primary Care Physician")
    
    actions.append("Monitor symptoms and keep health journal")
    actions.append("Follow up with specialist within 1-2 weeks")
    
    return list(set(actions))[:5]

def format_medical_summary(summary_text, symptoms, diseases, actions):
    """Format the analysis results in a clear, professional manner"""
    
    formatted_output = "🏥 MEDICAL REPORT ANALYSIS\n"
    formatted_output += "=" * 50 + "\n\n"
    
    # Executive Summary
    formatted_output += "📋 EXECUTIVE SUMMARY:\n"
    formatted_output += "-" * 20 + "\n"
    formatted_output += f"{summary_text}\n\n"
    
    # Key Findings
    formatted_output += "🔍 KEY FINDINGS:\n"
    formatted_output += "-" * 15 + "\n"
    
    if symptoms:
        formatted_output += "• Detected Symptoms:\n"
        for i, symptom in enumerate(symptoms, 1):
            formatted_output += f"  {i}. {symptom.capitalize()}\n"
    else:
        formatted_output += "• No specific symptoms detected in report\n"
    
    formatted_output += "\n"
    
    # Disease Assessment
    formatted_output += "🩺 DISEASE ASSESSMENT:\n"
    formatted_output += "-" * 20 + "\n"
    if diseases:
        for i, (disease, confidence) in enumerate(diseases, 1):
            confidence_level = "High" if confidence > 5 else "Medium" if confidence > 2 else "Low"
            formatted_output += f"{i}. {disease.title()} (Confidence: {confidence_level})\n"
    else:
        formatted_output += "• No specific disease patterns identified\n"
    
    formatted_output += "\n"
    
    # Recommended Actions
    formatted_output += "✅ RECOMMENDED ACTIONS:\n"
    formatted_output += "-" * 20 + "\n"
    for i, action in enumerate(actions, 1):
        formatted_output += f"{i}. {action}\n"
    
    formatted_output += "\n"
    formatted_output += "=" * 50 + "\n"
    formatted_output += "Note: This AI analysis is for informational purposes only.\n"
    formatted_output += "Please consult healthcare professionals for medical advice.\n"
    
    return formatted_output

# ✅ Unified entry point
def summarize_pdf(file_path):
    """Main function called from App.py (doctor side)"""
    try:
        with open(file_path, "rb") as f:
            file_bytes = f.read()

        # Extract text from PDF
        text = extract_text_from_pdf(file_bytes)
        if not text.strip():
            return "❌ No extractable text found in the PDF document.\nThis may be a scanned document - try using OCR-enabled PDFs."
        
        if not is_medical(text):
            return "⚠️ The uploaded document does not appear to be a medical report.\nPlease upload a valid medical document for analysis."

        # Process text (limit to first 10,000 characters for performance)
        processed_text = text[:10000]
        
        # Extract medical information
        symptoms = extract_symptoms(processed_text)
        predicted_diseases = predict_disease(symptoms, processed_text)
        suggested_actions = suggest_actions(predicted_diseases, symptoms)
        
        # Generate summary using chunks
        chunks = chunk_text(processed_text, max_chunk_size=900)
        
        if not chunks:
            return "❌ Unable to process document content for summarization."

        chunk_summaries = []
        for chunk in chunks[:5]:  # Limit to first 5 chunks
            try:
                summary = summarizer(chunk, max_length=120, min_length=40, do_sample=False)
                chunk_summaries.append(summary[0]["summary_text"])
            except Exception as e:
                chunk_summaries.append(f"Chunk processing error: {str(e)}")

        # Combine and create final summary
        if chunk_summaries:
            combined_text = " ".join(chunk_summaries)
            try:
                final_summary = summarizer(combined_text, max_length=200, min_length=50, do_sample=False)
                summary_text = final_summary[0]["summary_text"]
            except Exception as e:
                summary_text = "Summary generation incomplete due to processing limitations."
        else:
            summary_text = "Unable to generate detailed summary from document content."

        # Format the complete analysis
        formatted_result = format_medical_summary(
            summary_text, 
            symptoms, 
            predicted_diseases, 
            suggested_actions
        )
        
        return formatted_result

    except Exception as e:
        return f"❌ Analysis Error: {str(e)}\nPlease ensure the PDF is not corrupted and try again."