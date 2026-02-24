# # ======================================================
# # SECURE V2V BACKEND (FastAPI + Advanced AI Model)
# # ======================================================

# from fastapi import FastAPI, WebSocket
# from fastapi.middleware.cors import CORSMiddleware
# import joblib
# import numpy as np
# import pandas as pd
# import asyncio
# import json
# import random
# import math  # Sin/Cos calculate karne ke liye

# app = FastAPI()

# # 1. ALLOW FRONTEND CONNECTION (CORS)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # React ko allow karein
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # 2. LOAD SAVED MODEL FILES
# print("🔄 Loading AI Brain...")
# try:
#     model = joblib.load("v2v_xgboost_model.pkl")
#     scaler = joblib.load("v2v_scaler.pkl")
#     le = joblib.load("v2v_label_encoder.pkl")
#     print("✅ Model, Scaler & Encoder Loaded Successfully!")
# except Exception as e:
#     print(f"❌ Error Loading Files: {e}")
#     print("Please check that .pkl files are in the same folder.")

# # 3. HELPER FUNCTION: FEATURE ENGINEERING
# # (Ye wahi math hai jo Colab mein Sir ki script ne use kiya tha)
# def calculate_advanced_features(pos_x, pos_y, speed, heading):
#     # Convert heading to Radians
#     heading_rad = np.deg2rad(float(heading))
    
#     # Calculate Sin & Cos
#     heading_sin = np.sin(heading_rad)
#     heading_cos = np.cos(heading_rad)
    
#     # Calculate Position Radius (Distance from center)
#     pos_r = np.sqrt(pos_x**2 + pos_y**2)
    
#     return heading_sin, heading_cos, pos_r

# # 4. SIMULATION LOGIC (Traffic Generator)
# def generate_live_traffic():
#     """Generates random vehicle data (Normal & Attack Mix)"""
    
#     # 20% Chance of Attack
#     is_attack = random.random() < 0.2 
    
#     # Base values
#     pos_x = random.uniform(0, 5000)
#     pos_y = random.uniform(0, 5000)
#     speed = random.uniform(20, 100) # Normal Speed
#     heading = random.uniform(0, 360)
    
#     actual_type_debug = "Normal" # Sirf testing ke liye

#     # --- INJECT ATTACK (Modify Data) ---
#     if is_attack:
#         attack_type = random.choice([1, 2, 4]) # 1=Spoof, 2=Speed, 4=Sybil
        
#         if attack_type == 1: # GPS Spoofing
#             pos_x = 150.0  # Stuck
#             pos_y = 150.0
#             actual_type_debug = "GPS Spoofing (Simulated)"
            
#         elif attack_type == 2: # Speed Hack
#             speed = random.uniform(180, 250) # High Speed
#             actual_type_debug = "Speed Hack (Simulated)"
            
#         elif attack_type == 4: # Sybil
#             pos_x = random.uniform(6000, 10000) # Out of map
#             actual_type_debug = "Sybil Attack (Simulated)"

#     # --- CALCULATE 7 FEATURES FOR AI ---
#     heading_sin, heading_cos, pos_r = calculate_advanced_features(pos_x, pos_y, speed, heading)
    
#     # Ye Dictionary AI ke paas jayegi (Exact 7 Columns)
#     # Order must match Colab Training: 
#     # ['pos_x', 'pos_y', 'speed', 'heading', 'heading_sin', 'heading_cos', 'pos_r']
#     features = {
#         "pos_x": pos_x,
#         "pos_y": pos_y,
#         "speed": speed,
#         "heading": heading,
#         "heading_sin": heading_sin,
#         "heading_cos": heading_cos,
#         "pos_r": pos_r
#     }
    
#     return features, actual_type_debug

# # 5. WEBSOCKET ENDPOINT (Live Stream)
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     print("🔗 React Frontend Connected!")
    
#     try:
#         while True:
#             # A. Generate Data
#             features_dict, debug_label = generate_live_traffic()
            
#             # B. Prepare for AI (Dict -> DataFrame -> Scale)
#             input_df = pd.DataFrame([features_dict])
            
#             # Ensure columns are in correct order (Important!)
#             feature_order = ["pos_x", "pos_y", "speed", "heading", "heading_sin", "heading_cos", "pos_r"]
#             input_df = input_df[feature_order]
            
#             # Scale Data
#             input_scaled = scaler.transform(input_df)
            
#             # C. AI Prediction
#             prediction_idx = model.predict(input_scaled)[0]
            
#             # Decode Prediction (0 -> "Normal", 1 -> "Spoofing")
#             ai_result_name = le.inverse_transform([int(prediction_idx)])[0]

#             # D. Send JSON to Frontend
#             response = {
#                 "vehicle_id": random.randint(100, 999),
#                 "pos_x": features_dict['pos_x'],
#                 "pos_y": features_dict['pos_y'],
#                 "speed": features_dict['speed'],
#                 "status": ai_result_name,   # AI ka Faisla
#                 "is_danger": ai_result_name != "Normal" # Red Alert Logic
#             }
            
#             # Terminal mein print karein (Verification ke liye)
#             if response['is_danger']:
#                 print(f"⚠️ DETECTED: {ai_result_name} | Speed: {response['speed']:.1f}")
            
#             await websocket.send_json(response)
            
#             # 0.5 Second Delay (Taake aankh se nazar aaye)
#             await asyncio.sleep(0.5)
            
#     except Exception as e:
#         print(f"❌ Connection Closed: {e}")

# # Run Server: uvicorn main:app --reload

# ======================================================
# SECURE V2V BACKEND (Interactive & Advanced)
# ======================================================

# from fastapi import FastAPI, WebSocket
# from fastapi.middleware.cors import CORSMiddleware
# import joblib
# import numpy as np
# import pandas as pd
# import asyncio
# import json
# import random
# import math

# app = FastAPI()

# # Frontend Connection Allow karein
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Global Variables (Control karne ke liye)
# force_attack_mode = False

# # 1. LOAD MODEL
# print("🔄 Loading AI Brain...")
# try:
#     model = joblib.load("v2v_xgboost_model.pkl")
#     scaler = joblib.load("v2v_scaler.pkl")
#     le = joblib.load("v2v_label_encoder.pkl")
#     print("✅ System Ready!")
# except:
#     print("❌ Model files missing! Make sure .pkl files are in the folder.")

# def calculate_advanced_features(pos_x, pos_y, speed, heading):
#     heading_rad = np.deg2rad(float(heading))
#     return np.sin(heading_rad), np.cos(heading_rad), np.sqrt(pos_x**2 + pos_y**2)

# # 2. API TO TRIGGER ATTACK (Button dabane par ye chalega)
# @app.post("/trigger-attack")
# async def trigger_attack():
#     global force_attack_mode
#     force_attack_mode = True
#     return {"message": "Attack Initiated!"}

# # 3. TRAFFIC GENERATOR
# def generate_live_traffic():
#     global force_attack_mode
    
#     # Agar Button dabaya hai to Attack karo, warna Random (10% chance)
#     is_attack = force_attack_mode or (random.random() < 0.1)
    
#     # Reset flag after one attack frame if it was forced
#     if force_attack_mode:
#         force_attack_mode = False

#     pos_x = random.uniform(0, 5000)
#     pos_y = random.uniform(0, 5000)
#     speed = random.uniform(20, 100)
#     heading = random.uniform(0, 360)
#     actual_type = "Normal"

#     if is_attack:
#         attack_type = random.choice([1, 2, 4])
#         if attack_type == 1: # GPS Spoofing
#             pos_x, pos_y = 150.0, 150.0
#             actual_type = "GPS Spoofing"
#         elif attack_type == 2: # Speed Hack
#             speed = random.uniform(180, 250)
#             actual_type = "Speed Hack"
#         elif attack_type == 4: # Sybil
#             pos_x = random.uniform(6000, 10000)
#             actual_type = "Sybil Attack"

#     heading_sin, heading_cos, pos_r = calculate_advanced_features(pos_x, pos_y, speed, heading)
    
#     features = {
#         "pos_x": pos_x, "pos_y": pos_y, "speed": speed, "heading": heading,
#         "heading_sin": heading_sin, "heading_cos": heading_cos, "pos_r": pos_r
#     }
#     return features, actual_type

# # 4. WEBSOCKET
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     print("🔗 Frontend Connected!")
#     try:
#         while True:
#             features, _ = generate_live_traffic()
            
#             # AI Prediction
#             df = pd.DataFrame([features])
#             scaled = scaler.transform(df[['pos_x', 'pos_y', 'speed', 'heading', 'heading_sin', 'heading_cos', 'pos_r']])
#             pred_idx = model.predict(scaled)[0]
#             status = le.inverse_transform([int(pred_idx)])[0]

#             response = {
#                 "id": random.randint(1000, 9999),
#                 "pos_x": features['pos_x'],
#                 "pos_y": features['pos_y'],
#                 "speed": features['speed'],
#                 "status": status,
#                 "is_danger": status != "Normal"
#             }
            
#             await websocket.send_json(response)
#             await asyncio.sleep(0.8) # Thoda slow kiya taake dekh sakein
            
#     except Exception as e:
#         print(f"❌ Disconnected: {e}")


# # ------------------------------------------
# # ======================================================
# # SECURE V2V BACKEND (Repair Mode / Robust)
# # ======================================================
# from fastapi import FastAPI, WebSocket
# from fastapi.middleware.cors import CORSMiddleware
# import joblib
# import numpy as np
# import pandas as pd
# import asyncio
# import json
# import random
# import traceback # Error track karne ke liye

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # --- 1. SAFE MODEL LOADING ---
# model, scaler, le = None, None, None
# MODEL_READY = False

# print("\n🔄 SYSTEM STARTUP: Loading AI Models...")
# try:
#     model = joblib.load("v2v_xgboost_model.pkl")
#     scaler = joblib.load("v2v_scaler.pkl")
#     le = joblib.load("v2v_label_encoder.pkl")
#     MODEL_READY = True
#     print("✅ SUCCESS: AI Brain Loaded Successfully!")
# except Exception as e:
#     print(f"⚠️ WARNING: Model loading failed. ({e})")
#     print("➡️ Running in SIMULATION MODE (Demo traffic only).")

# # Global Attack Trigger
# force_attack_mode = False

# @app.post("/trigger-attack")
# async def trigger_attack():
#     global force_attack_mode
#     print("🚨 ATTACK COMMAND RECEIVED from Frontend!")
#     force_attack_mode = True
#     return {"status": "Attack Initiated"}

# # --- 2. TRAFFIC GENERATOR ---
# def generate_traffic():
#     global force_attack_mode
    
#     # Logic: Agar button dabaya to attack, warna random safe traffic
#     is_attack = force_attack_mode
#     if force_attack_mode:
#         force_attack_mode = False # Reset trigger

#     # Data creation
#     if is_attack:
#         pos_x, pos_y = 150.0, 150.0
#         speed = random.uniform(180, 250) # High Speed
#         heading = random.uniform(0, 360)
#         status = "Speed Hack"
#         is_danger = True
#     else:
#         pos_x = random.uniform(0, 5000)
#         pos_y = random.uniform(0, 5000)
#         speed = random.uniform(20, 100) # Normal Speed
#         heading = random.uniform(0, 360)
#         status = "Normal"
#         is_danger = False

#     # Agar Model Sahi Hai, to us se confirm karo (Real AI Prediction)
#     if MODEL_READY:
#         try:
#             # Feature Engineering (Wohi jo Colab mein thi)
#             heading_rad = np.deg2rad(float(heading))
#             features = pd.DataFrame([{
#                 "pos_x": pos_x, "pos_y": pos_y, "speed": speed, "heading": heading,
#                 "heading_sin": np.sin(heading_rad), "heading_cos": np.cos(heading_rad),
#                 "pos_r": np.sqrt(pos_x**2 + pos_y**2)
#             }])
            
#             # Predict
#             scaled_input = scaler.transform(features)
#             pred_idx = model.predict(scaled_input)[0]
#             ai_status = le.inverse_transform([int(pred_idx)])[0]
            
#             # Agar AI ne kaha Danger hai, to Danger maano
#             if ai_status != "Normal":
#                 status = ai_status
#                 is_danger = True
                
#         except Exception as e:
#             print(f"⚠️ AI Prediction Error: {e}")

#     return {
#         "id": random.randint(1000, 9999),
#         "pos_x": pos_x, "pos_y": pos_y, "speed": speed,
#         "status": status, "is_danger": is_danger
#     }

# # --- 3. WEBSOCKET CONNECTION ---
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     print("🔗 CLIENT CONNECTED: Dashboard is live!")
    
#     try:
#         while True:
#             data = generate_traffic()
            
#             # Terminal mein sirf Attack print karo (spam kam karne ke liye)
#             if data['is_danger']:
#                 print(f"🔥 ATTACK SENT: {data['status']} | Speed: {data['speed']:.0f}")

#             await websocket.send_json(data)
#             await asyncio.sleep(0.5) # Speed control
            
#     except Exception as e:
#         print("❌ CLIENT DISCONNECTED")



# ===========================
# ======================================================
# # SECURE V2V BACKEND (With Explainable AI - SHAP)
# # ======================================================
# from fastapi import FastAPI, WebSocket
# from fastapi.middleware.cors import CORSMiddleware
# import joblib
# import numpy as np
# import pandas as pd
# import asyncio
# import json
# import random
# import shap  # <--- New Library for Explanation

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
# )

# # --- 1. LOAD MODEL & SHAP EXPLAINER ---
# model, scaler, le, explainer = None, None, None, None
# MODEL_READY = False
# FEATURE_NAMES = ['pos_x', 'pos_y', 'speed', 'heading', 'heading_sin', 'heading_cos', 'pos_r']

# print("\n🔄 SYSTEM STARTUP: Loading AI Brain & Explainer...")
# try:
#     model = joblib.load("v2v_xgboost_model.pkl")
#     scaler = joblib.load("v2v_scaler.pkl")
#     le = joblib.load("v2v_label_encoder.pkl")
    
#     # Initialize SHAP Explainer (Ye batayega 'Kyun?')
#     explainer = shap.TreeExplainer(model)
#     MODEL_READY = True
#     print("✅ SUCCESS: AI Brain & Reasoning Engine Loaded!")
# except Exception as e:
#     print(f"⚠️ WARNING: {e}")
#     print("➡️ Running in SIMULATION MODE.")

# force_attack_mode = False

# @app.post("/trigger-attack")
# async def trigger_attack():
#     global force_attack_mode
#     force_attack_mode = True
#     return {"status": "Attack Initiated"}

# def generate_traffic():
#     global force_attack_mode
#     is_attack = force_attack_mode
#     if force_attack_mode: force_attack_mode = False

#     # Data Logic
#     if is_attack:
#         pos_x, pos_y = 150.0, 150.0
#         speed = random.uniform(180, 250)
#         heading = random.uniform(0, 360)
#         status = "Speed Hack"
#         is_danger = True
#     else:
#         pos_x = random.uniform(0, 5000)
#         pos_y = random.uniform(0, 5000)
#         speed = random.uniform(20, 100)
#         heading = random.uniform(0, 360)
#         status = "Normal"
#         is_danger = False

#     reason = "Normal Traffic Pattern"  # Default Reason

#     if MODEL_READY:
#         try:
#             # Prepare Data
#             heading_rad = np.deg2rad(float(heading))
#             features = pd.DataFrame([{
#                 "pos_x": pos_x, "pos_y": pos_y, "speed": speed, "heading": heading,
#                 "heading_sin": np.sin(heading_rad), "heading_cos": np.cos(heading_rad),
#                 "pos_r": np.sqrt(pos_x**2 + pos_y**2)
#             }], columns=FEATURE_NAMES)
            
#             # Predict
#             scaled_input = scaler.transform(features)
#             pred_idx = model.predict(scaled_input)[0]
#             ai_status = le.inverse_transform([int(pred_idx)])[0]

#             if ai_status != "Normal":
#                 status = ai_status
#                 is_danger = True
                
#                 # --- SHAP EXPLANATION LOGIC (Magic Happens Here) ---
#                 shap_values = explainer.shap_values(scaled_input)
#                 # Sabse bada factor dhundo (jisne decision change kiya)
#                 max_impact_idx = np.argmax(np.abs(shap_values[0])) 
#                 top_feature = FEATURE_NAMES[max_impact_idx]
                
#                 # Human Readable Reason
#                 if top_feature == "speed": reason = "CRITICAL: Abnormal High Speed Detected"
#                 elif top_feature in ["pos_x", "pos_y", "pos_r"]: reason = "CRITICAL: Location Spoofing / Jump Detected"
#                 elif "heading" in top_feature: reason = "WARNING: Erratic Steering / Heading"
#                 else: reason = f"Anomaly in {top_feature}"

#         except Exception as e:
#             print(f"Error: {e}")

#     return {
#         "id": random.randint(1000, 9999),
#         "pos_x": pos_x, "pos_y": pos_y, "speed": speed,
#         "status": status, "is_danger": is_danger,
#         "reason": reason  # <--- Ye naya data hai Frontend ke liye
#     }

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = generate_traffic()
#             await websocket.send_json(data)
#             await asyncio.sleep(0.5)
#     except:
#         print("❌ Client Disconnected")

#         # Pehle aapka route sirf database mein save karta tha.


#         # Ab wo Agent ko call karega:

#         @app.post("/process-packet")
# async def process(packet: dict):
#     # Agent ko packet bhejein
#     result = await my_agent_graph.invoke({"packet": packet})
#     # Agent ka faisla wapis bhejein
#     return {"decision": result["action"]}

# -----------------------------------------------------------------

#  simulation chale, to agent faisla le.
# from agents_logic import agent_app # Hamari nayi file

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             # 1. Data generate ya receive karein
#             raw_data = generate_traffic() 
            
#             # 2. AGENTIC AI ko kaam par lagayein
#             inputs = {"packet_data": raw_data}
#             result = agent_app.invoke(inputs)
            
#             # 3. Data update karein agent ke faisle ke mutabiq
#             raw_data["status"] = result["decision"]
#             raw_data["reason"] = result["reasoning"] # Ye aapke UI mein jayega
            
#             await websocket.send_json(raw_data)
#             await asyncio.sleep(0.5)
#     except:
#         print("Client Disconnected")


#         # ----------------------------------
#         from agents_logic import agent_executor

# @app.post("/analyze-v2v")
# async def analyze(data: dict):
#     # Agent ko trigger karein
#     result = agent_executor.invoke({"packet_data": data})
    
#     return {
#         "status": result["decision"],
#         "reason": result["explanation"],
#         "prediction": result["prediction"]
#     }


# ======================================================
# SECURE V2V BACKEND (With Agentic AI & SHAP)
# ======================================================
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
import pandas as pd
import asyncio
import json
import random
import shap
from agents_logic import agent_executor  # Import your Agentic Logic

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"],
)

# --- 1. LOAD MODEL & SHAP EXPLAINER ---
model, scaler, le, explainer = None, None, None, None
MODEL_READY = False
FEATURE_NAMES = ['pos_x', 'pos_y', 'speed', 'heading', 'heading_sin', 'heading_cos', 'pos_r']

print("\n🔄 SYSTEM STARTUP: Loading AI Brain & Agentic Engine...")
try:
    model = joblib.load("v2v_xgboost_model.pkl")
    scaler = joblib.load("v2v_scaler.pkl")
    le = joblib.load("v2v_label_encoder.pkl")
    
    # Initialize SHAP Explainer for ML transparency
    explainer = shap.TreeExplainer(model)
    MODEL_READY = True
    print("✅ SUCCESS: XGBoost, SHAP & Agentic Engine Loaded!")
except Exception as e:
    print(f"⚠️ WARNING: {e}")
    print("➡️ Running in SIMULATION MODE.")

force_attack_mode = False

@app.post("/trigger-attack")
async def trigger_attack():
    global force_attack_mode
    force_attack_mode = True
    return {"status": "Attack Initiated"}

def generate_traffic():
    global force_attack_mode
    is_attack = force_attack_mode
    if force_attack_mode: force_attack_mode = False

    if is_attack:
        pos_x, pos_y = 150.0, 150.0
        speed = random.uniform(180, 250)
        heading = random.uniform(0, 360)
        status = "Speed Hack"
        is_danger = True
    else:
        pos_x = random.uniform(0, 5000)
        pos_y = random.uniform(0, 5000)
        speed = random.uniform(20, 100)
        heading = random.uniform(0, 360)
        status = "Normal"
        is_danger = False

    reason = "System monitoring traffic..."

    if MODEL_READY:
        try:
            # Prepare Data for Model
            heading_rad = np.deg2rad(float(heading))
            features = pd.DataFrame([{
                "pos_x": pos_x, "pos_y": pos_y, "speed": speed, "heading": heading,
                "heading_sin": np.sin(heading_rad), "heading_cos": np.cos(heading_rad),
                "pos_r": np.sqrt(pos_x**2 + pos_y**2)
            }], columns=FEATURE_NAMES)
            
            # Predict
            scaled_input = scaler.transform(features)
            pred_idx = model.predict(scaled_input)[0]
            ai_status = le.inverse_transform([int(pred_idx)])[0]

            if ai_status != "Normal":
                status = ai_status
                is_danger = True
                
                # SHAP Explanation (Internal ML Reason)
                shap_values = explainer.shap_values(scaled_input)
                max_impact_idx = np.argmax(np.abs(shap_values[0])) 
                top_feature = FEATURE_NAMES[max_impact_idx]
                reason = f"ML Alert: High impact on {top_feature}"

        except Exception as e:
            print(f"ML Processing Error: {e}")

    return {
        "id": random.randint(1000, 9999),
        "pos_x": pos_x, "pos_y": pos_y, "speed": speed,
        "status": status, "is_danger": is_danger,
        "ml_reason": reason 
    }

# --- 2. MAIN WEBSOCKET WITH AGENTIC AI ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Step A: Generate or Get Raw Traffic Data
            raw_data = generate_traffic() 
            
            # Step B: Trigger AGENTIC AI (LangGraph + Gemini)
            # Hum ML ka result bhi bhej rahe hain taake Gemini behtar explain kare
            try:
                agent_input = {
                    "packet_data": raw_data,
                    "ml_analysis": raw_data["ml_reason"]
                }
                result = agent_executor.invoke(agent_input)
                
                # Step C: Update Data with Agent's Human-like Reasoning
                raw_data["reason"] = result.get("explanation", "AI is analyzing...")
                raw_data["agent_decision"] = result.get("decision", "Monitoring")
            except Exception as e:
                print(f"Agentic Error: {e}")
                raw_data["reason"] = "Agent connection error"

            # Send back to Frontend (React)
            await websocket.send_json(raw_data)
            await asyncio.sleep(0.5)
            
    except Exception as e:
        print(f"❌ Client Disconnected: {e}")

# HTTP Endpoint for manual analysis
@app.post("/analyze-v2v")
async def analyze(data: dict):
    result = agent_executor.invoke({"packet_data": data})
    return {
        "status": result["decision"],
        "reason": result["explanation"],
        "prediction": result.get("prediction", 0)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)