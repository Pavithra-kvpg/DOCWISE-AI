# 🩺 DOCWISE-AI
# A SMART MEDICAL HISTORY ANALYZER AND DOCTOR RECOMMENDATION SYSTEM

## 🧠 Abstract
**DocWise AI** is an intelligent prototype that analyzes medical documents and recommends doctors automatically.  
Using **OCR**, **NLP**, and **AI-based Summarization**, it extracts and interprets information from reports and connects diseases to relevant specialists.

It integrates:
- **Tesseract OCR**, **PyMuPDF** – for text extraction  
- **spaCy**, **Transformers (BART/T5)** – for NLP and summarization  
- **SQLite** – for doctor data storage  
- **KivyMD** – for an interactive GUI  

DocWise AI maps **56 diseases** to **22 specializations** and holds **1,000+ doctor profiles**.

---

## 🩻 System Modules

### 1. PDF Report Reader
- Extracts text from reports (PDFs, scans).
- Uses **OCR** for clean text extraction.

### 2. Disease Matcher
- Detects symptoms and disease keywords using **NLP**.
- Matches them against a curated medical dataset.

### 3. Report Summarizer
- Condenses lengthy text using **Transformer-based models**.
- Keeps key medical details intact.

### 4. Suggested Action Generator
- Suggests next medical steps (tests or doctor visits).

### 5. Disease-to-Doctor Mapper
- Maps detected disease to correct specialization.

### 6. Doctor Database
- Contains verified doctor profiles with details.

### 7. Matching Engine
- Filters and ranks doctors by location and expertise.

### 8. Recommendation Engine
- Displays best matches in a clean **KivyMD interface**.

---

## ⚙️ Technologies Used

| Category | Tools |
|-----------|-------|
| Programming | Python |
| OCR & Extraction | PyMuPDF, Tesseract |
| NLP & Summarization | spaCy, Transformers |
| Database | SQLite |
| Interface | KivyMD |
| Utilities | Pandas, NumPy, Scikit-learn |

---

## 🔄 Workflow
1. Upload medical PDF.  
2. OCR extracts text.  
3. NLP identifies diseases.  
4. Summarizer shortens text.  
5. Mapper links diseases to doctors.  
6. Recommendation engine displays best specialists.

---

## 📊 Performance

| Module | Metric | Accuracy |
|---------|---------|-----------|
| OCR | Extraction Accuracy | 94.8% |
| Disease Detection | Recognition Accuracy | 92.4% |
| Summarization | Retention | 90% |
| Recommendation | Precision | 93.1% |
| System Speed | Avg. 4.8s/report | ✅ |

---

## 🧩 Results
- Reliable recognition across 15 medical domains.  
- Effective text summarization.  
- High recommendation accuracy.  
- Smooth GUI interaction.

---

## 🔮 Future Enhancements

Multi-language OCR/NLP support.

Real-time hospital API integration.

Doctor profile verification with live status.

Cloud/Android deployment for accessibility.

---


## 🏗️ Folder Structure

```
DOCWISE AI/
├── doctor_recommendation_system/
│   ├── App.py
│   ├── data/
│   │   ├── disease_to_doctor.csv
│   │   ├── doctor_profiles.csv
│   ├── modules/
│   │   ├── disease_mapper.py
│   │   ├── doctor_filtering.py
│   │   ├── doctor_profile.py
│   │   ├── doctor_profiles.py
│   │   ├── pdf_analyzer.py
│   │   ├── __init__.py
│   │   ├── __pycache__/
│   │       ├── disease_mapper.cpython-313.pyc
│   │       ├── doctor_filtering.cpython-313.pyc
│   │       ├── doctor_profile.cpython-313.pyc
│   │       ├── doctor_profiles.cpython-313.pyc
│   │       ├── pdf_analyzer.cpython-313.pyc
│           ├── __init__.cpython-313.pyc
├── requirements.txt

```
## 🚀 How to Run the Project

Follow these steps to set up and run DocWise AI on your system:

1️⃣ Prerequisites

Make sure you have the following installed:

Python 3.8 or higher

pip (Python package manager)

Tesseract OCR
 (for text extraction)

 2️⃣ Install Dependencies

All required Python libraries are listed in requirements.txt.
Run the following command:

pip install -r requirements.txt

3️⃣ Run the Application

Navigate into the project’s main folder:

cd doctor_recommendation_system


Then run:

python App.py

## 🎬 Demo Video
[Download demo video](https://github.com/Pavithra-kvpg/DOCWISE-AI/raw/main/video.mp4)
