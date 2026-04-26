

🛡️ V2V Sentinel: Agentic XAI for Secure Communication
An advanced AI-driven security framework designed to detect and explain real-time cyber-threats in Vehicular-to-Vehicular (V2V) networks.

📝 Project Objective
The main goal is to scan data packets exchanged between vehicles to detect malicious activities like Speed Hacks, Spoofing, and Sybil attacks in milliseconds. Once a threat is found, the system notifies the security administrator immediately.

🌟 Project Novelty (Why it's unique)
Unlike traditional security systems that only flag an attack, V2V Sentinel offers:

Hybrid Intelligence: Combines a high-performance XGBoost Machine Learning model with the reasoning power of Gemini Agentic AI.

Explainable AI (XAI): Uses the SHAP library to remove the "Black Box" nature of AI. It tells you exactly which technical feature (like speed or position) caused the system to flag a threat.

Agentic Reasoning Engine: Powered by LangGraph and Gemini 1.5 Flash, the system writes a human-readable mitigation plan and generates forensic reports autonomously.

🚀 Key Features & Benefits
Real-time Spatial Monitoring: A live radar dashboard shows the geo-spatial position and security status of vehicles.

Automated Incident Reporting: Upon detecting an attack, the system automatically generates a text-based Forensic Report and saves it to the system logs.

Ultra-Low Latency: Optimized for V2V standards, completing detection and reasoning within 0.02ms to 5ms.

Visual Transparency: Includes a Confusion Matrix and Feature Importance plots in the dashboard as proof of training accuracy.

🛠️ Tech Stack
Backend: Python, FastAPI, WebSockets, LangChain, LangGraph.

AI/ML: XGBoost, Scikit-learn, SHAP, Google Gemini 1.5 Flash API.

Frontend: React.js, Plotly.js, Lucide Icons, CSS3 (Cyberpunk Theme).

📂 Installation & Setup Steps
1. Backend Setup
Navigate to the FYP_Backend folder.

Create a .env file and add your key: GOOGLE_API_KEY=your_key_here.

Install dependencies:

Run the server: uvicorn main:app --reload.

2. Frontend Setup
Navigate to the FYP_Frontend folder.

Install dependencies:

Run the dashboard: npm start.

📊 System Validation
The system performs with 95%+ accuracy on training sets. You can view the live results, such as the Confusion Matrix, at the bottom of the dashboard.

Final Project Status
Simulation Engine: 100% Done

AI Agent Integration: 100% Done

XAI Dashboard: 100% Done

Latency Testing: 100% Done

Note: This project was developed as a Final Year Project (FYP) at Bahria University (BULC).

----------------------------------------------------
# Aero-Sentinel XAI 🛰️
### Secure V2V Communication using Explainable AI

**Aero-Sentinel XAI** ek advanced security framework hai jo Vehicular Networks (V2V) ko spoofing aur sensor manipulation attacks se bachata hai. Is mein humne YOLOv8 ko vision ke liye aur XGBoost ko telemetry data scan karne ke liye use kiya hai.

## ✨ Features
* **Hybrid Detection:** Computer Vision (YOLOv8) aur Machine Learning (XGBoost) ka combo.
* **Explainable AI (XAI):** SHAP terminal ke zariye system batata hai ke usne "Attack" kyun detect kiya.
* **Real-time Dashboard:** Live spatial radar aur altitude tracking.
* **Auto-Response:** Crash detection pe foran "Auto-Brake" signal generate karta hai.

## 🛠️ Tech Stack
* **Frontend:** React.js, Tailwind CSS
* **Backend:** Python (Flask/FastAPI)
* **AI Models:** YOLOv8, XGBoost, Isolation Forest
* **XAI:** SHAP (SHapley Additive exPlanations)

## 🚀 Setup & Installation
1. Clone the repo:
   ```bash
   git clone [https://github.com/Abdul-Wahab-Aslam/V2V-Security-FYP.git](https://github.com/Abdul-Wahab-Aslam/V2V-Security-FYP.git)
