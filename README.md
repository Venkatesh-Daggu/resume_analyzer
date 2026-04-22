# 🚀 AI Resume Analyzer & Career Guidance System

This project is an AI-powered web application that analyzes a user's resume and provides personalized career insights.

It helps users understand which job roles suit them best, what skills they are missing, and what they should learn next — all in a simple and interactive way.

---

## 🌟 Overview

Instead of manually reviewing resumes and guessing career paths, this system automates the process using AI.

After uploading a resume (PDF or DOCX), the application:

• Extracts technical skills using AI  
• Matches your profile with relevant job roles  
• Calculates match percentage for each role  
• Identifies missing skills  
• Recommends courses to improve your profile  
• Provides career guidance using an AI chatbot  

---

## 💼 Features

### 🔍 Smart Skill Extraction  
Uses Google Gemini AI to extract only relevant technical skills from the resume.

### 📊 Job Role Matching  
Compares extracted skills with predefined job roles and gives a match score.

### 📉 Skill Gap Analysis  
Shows:
- ✅ Skills you already have  
- ❌ Skills you are missing  

### 📘 Course Recommendations  
Suggests courses based on missing skills using a CSV dataset.

### 🤖 AI Career Chatbot  
Allows users to ask questions like:
- Which role is best for me?  
- What should I learn next?  

---

## 🛠️ Technologies Used

• Python  
• Streamlit  
• Google Gemini API  
• Pandas  
• PyMuPDF (for PDF parsing)  
• python-docx (for DOCX parsing)  
• dotenv  

---

## 📁 Project Structure

resume_analyzer/

app.py → Frontend (Streamlit UI)  
Backend.py → Core logic (AI processing + matching)  
Courses.csv → Course recommendation dataset  
requirements.txt → Dependencies  
.env → API key (not uploaded to GitHub)  

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
git clone https://github.com/Venkatesh-Daggu/resume_analyzer.git  
cd resume_analyzer  

### 2️⃣ Create virtual environment
python -m venv venv  
venv\Scripts\activate  

### 3️⃣ Install dependencies
pip install -r requirements.txt  

### 4️⃣ Add your API key
Create a `.env` file and add:

GEMINI_API_KEY=your_api_key_here  

### 5️⃣ Run the application
streamlit run app.py  

---

## ⚠️ Important Note

The free version of Gemini API has rate limits.  
If too many requests are made in a short time, you may encounter a **429 quota exceeded error**.

To handle this, retry logic and caching are implemented in the backend.

---

## 🚀 Future Improvements

• Integration with real-time job APIs  
• Resume scoring system  
• ATS (Applicant Tracking System) checker  
• Downloadable analysis report  
• UI/UX enhancements  
