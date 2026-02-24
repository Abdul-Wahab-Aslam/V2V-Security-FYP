// // import React, { useState, useEffect, useRef } from 'react';
// // import Plot from 'react-plotly.js';
// // import { Shield, ShieldAlert, Activity, Crosshair, Zap } from 'lucide-react';
// // import './App.css';

// // function App() {
// //   const [dataPoints, setDataPoints] = useState([]);
// //   const [current, setCurrent] = useState({ speed: 0, status: "SCANNING...", is_danger: false });
// //   const [logs, setLogs] = useState([]);
// //   const ws = useRef(null);
  
// //   // Sound Effect
// //   const alertSound = new Audio("https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg");

// //   useEffect(() => {
// //     ws.current = new WebSocket("ws://127.0.0.1:8000/ws");
// //     ws.current.onmessage = (event) => {
// //       const data = JSON.parse(event.data);
// //       setCurrent(data);
      
// //       if(data.is_danger) {
// //         alertSound.play().catch(e => console.log("Audio play failed")); // Sound Bajao
// //         addLog(`⚠️ DETECTED: ${data.status} [ID: ${data.id}]`);
// //       }

// //       setDataPoints(prev => {
// //         const newer = [...prev, data];
// //         if (newer.length > 20) newer.shift();
// //         return newer;
// //       });
// //     };
// //     return () => ws.current.close();
// //   }, []);

// //   const addLog = (msg) => {
// //     setLogs(prev => [`[${new Date().toLocaleTimeString()}] ${msg}`, ...prev.slice(0, 5)]);
// //   };

// //   // Button Click Handler
// //   const triggerAttack = async () => {
// //     await fetch("http://127.0.0.1:8000/trigger-attack", { method: "POST" });
// //     addLog("🛑 INITIATING ATTACK SIMULATION...");
// //   };

// //   return (
// //     <div className={`dashboard ${current.is_danger ? 'danger-state' : ''}`}>
      
// //       {/* HEADER */}
// //       <div className="top-bar">
// //         <div className="brand">
// //           {current.is_danger ? <ShieldAlert color="red" /> : <Shield color="#0ff" />}
// //           <h2>V2V <span className="highlight">SENTINEL</span></h2>
// //         </div>
// //         <div className="status-box">
// //           <Activity size={16} /> SYSTEM: {current.is_danger ? "UNDER ATTACK" : "SECURE"}
// //         </div>
// //       </div>

// //       <div className="content-grid">
        
// //         {/* LEFT: RADAR MAP */}
// //         <div className="panel radar-panel">
// //           <div className="panel-header"><Crosshair size={16}/> LIVE RADAR FEED</div>
// //           <Plot
// //             data={[{
// //               r: dataPoints.map(d => Math.sqrt(d.pos_x**2 + d.pos_y**2)),
// //               theta: dataPoints.map(d => Math.atan2(d.pos_y, d.pos_x) * 180 / Math.PI),
// //               mode: 'markers',
// //               type: 'scatterpolar',
// //               marker: { 
// //                 color: dataPoints.map(d => d.is_danger ? '#ff0000' : '#00ffff'), 
// //                 size: 15,
// //                 symbol: dataPoints.map(d => d.is_danger ? 'cross' : 'circle')
// //               }
// //             }]}
// //             layout={{
// //               polar: {
// //                 bgcolor: "rgba(0,0,0,0)",
// //                 radialaxis: { visible: true, range: [0, 8000], showticklabels: false, gridcolor: "#333" },
// //                 angularaxis: { gridcolor: "#333" }
// //               },
// //               paper_bgcolor: "rgba(0,0,0,0)",
// //               font: { color: "#0ff" },
// //               margin: { t: 20, b: 20, l: 20, r: 20 },
// //               showlegend: false
// //             }}
// //             style={{ width: "100%", height: "100%" }}
// //             config={{displayModeBar: false}}
// //           />
// //         </div>

// //         {/* RIGHT: CONTROLS & LOGS */}
// //         <div className="right-col">
          
// //           {/* SPEEDOMETER & STATUS */}
// //           <div className="panel stats-panel">
// //             <div className="speed-circle" style={{borderColor: current.is_danger ? 'red' : '#0ff'}}>
// //               <h1>{current.speed.toFixed(0)}</h1>
// //               <small>KM/H</small>
// //             </div>
// //             <div className="vehicle-info">
// //               <h3>ID: {current.id || "---"}</h3>
// //               <p style={{color: current.is_danger ? 'red' : '#0ff'}}>
// //                 TYPE: {current.status}
// //               </p>
// //             </div>
// //           </div>

// //           {/* ATTACK BUTTON (Unique Feature) */}
// //           <button className="attack-btn" onClick={triggerAttack}>
// //             <Zap size={20} /> SIMULATE CYBER ATTACK
// //           </button>

// //           {/* LOGS */}
// //           <div className="panel logs-panel">
// //             <div className="panel-header">_SECURITY_LOGS</div>
// //             {logs.map((log, i) => (
// //               <div key={i} className="log-line">{log}</div>
// //             ))}
// //           </div>

// //         </div>
// //       </div>
// //     </div>
// //   );
// // }

// // export default App;
// import React, { useState, useEffect, useRef } from 'react';
// import Plot from 'react-plotly.js';
// import { Shield, ShieldAlert, Activity, Crosshair, Zap, BarChart3 } from 'lucide-react';
// import './App.css';

// function App() {
//   const [dataPoints, setDataPoints] = useState([]); // Stores history for graphs
//   const [current, setCurrent] = useState({ speed: 0, status: "SCANNING...", is_danger: false });
//   const [logs, setLogs] = useState([]);
//   const ws = useRef(null);
//   const alertSound = useRef(new Audio("https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg"));

//   useEffect(() => {
//     ws.current = new WebSocket("ws://127.0.0.1:8000/ws");

//     ws.current.onmessage = (event) => {
//       const data = JSON.parse(event.data);
//       setCurrent(data);

//       // Play Sound on Attack
//       if(data.is_danger) {
//         alertSound.current.play().catch(e => console.log("Audio play failed"));
//         addLog(`⚠️ THREAT: ${data.status} DETECTED!`);
//       }

//       // Maintain History (Last 50 points for Graph)
//       setDataPoints(prev => {
//         const newer = [...prev, { ...data, time: new Date().toLocaleTimeString() }];
//         if (newer.length > 50) newer.shift();
//         return newer;
//       });
//     };
//     return () => ws.current.close();
//   }, []);

//   const addLog = (msg) => {
//     setLogs(prev => [`> ${msg}`, ...prev.slice(0, 4)]);
//   };

//   const triggerAttack = async () => {
//     await fetch("http://127.0.0.1:8000/trigger-attack", { method: "POST" });
//     addLog("🛑 INJECTING MALICIOUS TRAFFIC...");
//   };

//   return (
//     <div className={`dashboard ${current.is_danger ? 'danger-state' : ''}`}>
      
//       {/* --- HEADER --- */}
//       <div className="top-bar">
//         <div className="brand">
//           {current.is_danger ? <ShieldAlert color="red" size={28}/> : <Shield color="#0ff" size={28}/>}
//           <h2>CYBER<span className="highlight">SENTINEL</span></h2>
//         </div>
//         <div className={`status-badge ${current.is_danger ? 'blink-red' : ''}`}>
//            STATUS: {current.is_danger ? "CRITICAL ALERT" : "SYSTEM SECURE"}
//         </div>
//       </div>

//       <div className="middle-section">
//         {/* --- LEFT: LIVE RADAR --- */}
//         <div className="panel radar-box">
//           <div className="panel-header"><Crosshair size={16}/> GEO-SPATIAL TRACKING</div>
//           <Plot
//             data={[{
//               r: dataPoints.map(d => Math.sqrt(d.pos_x**2 + d.pos_y**2)),
//               theta: dataPoints.map(d => Math.atan2(d.pos_y, d.pos_x) * 180 / Math.PI),
//               mode: 'markers',
//               type: 'scatterpolar',
//               marker: { 
//                 color: dataPoints.map(d => d.is_danger ? '#ff0000' : '#00ffff'), 
//                 size: dataPoints.map(d => d.is_danger ? 18 : 8),
//                 symbol: dataPoints.map(d => d.is_danger ? 'cross' : 'circle')
//               }
//             }]}
//             layout={{
//               polar: {
//                 bgcolor: "rgba(0,0,0,0)",
//                 radialaxis: { visible: true, range: [0, 8000], showticklabels: false, gridcolor: "#333" },
//                 angularaxis: { gridcolor: "#333" }
//               },
//               paper_bgcolor: "rgba(0,0,0,0)",
//               margin: { t: 20, b: 20, l: 20, r: 20 },
//               showlegend: false
//             }}
//             style={{ width: "100%", height: "100%" }}
//             config={{displayModeBar: false}}
//           />
//         </div>

//         {/* --- RIGHT: CONTROL CENTER --- */}
//         <div className="right-col">
//           <div className="panel stats-box">
//             <div className="speed-gauge" style={{borderColor: current.is_danger ? 'red' : '#0ff'}}>
//               <h1>{current.speed.toFixed(0)}</h1>
//               <small>KM/H</small>
//             </div>
//             <div className="info-text">
//               <h3>VEHICLE ID: {current.id || "---"}</h3>
//               <p style={{color: current.is_danger ? 'red' : '#0ff'}}>TYPE: {current.status}</p>
//             </div>
//           </div>

//           <button className="attack-btn" onClick={triggerAttack}>
//             <Zap size={20} /> SIMULATE ATTACK
//           </button>

//           <div className="panel logs-box">
//             <div className="panel-header">_TERMINAL_LOGS</div>
//             {logs.map((log, i) => <div key={i} className="log-line">{log}</div>)}
//           </div>
//         </div>
//       </div>

//       {/* --- BOTTOM: LIVE ANALYTICS GRAPH --- */}
//       <div className="panel bottom-graph">
//         <div className="panel-header"><BarChart3 size={16}/> LIVE SPEED & THREAT ANALYTICS</div>
//         <Plot
//           data={[
//             {
//               x: dataPoints.map((_, i) => i),
//               y: dataPoints.map(d => d.speed),
//               type: 'scatter',
//               mode: 'lines+markers',
//               marker: { color: '#00ffff' },
//               line: { color: '#00ffff', width: 2 },
//               name: 'Speed',
//               fill: 'tozeroy'
//             }
//           ]}
//           layout={{
//             autosize: true,
//             paper_bgcolor: "rgba(0,0,0,0)",
//             plot_bgcolor: "rgba(0,0,0,0)",
//             xaxis: { showgrid: false, zeroline: false, showticklabels: false },
//             yaxis: { gridcolor: '#333', title: 'Speed (km/h)', titlefont: {color: '#666'} },
//             font: { color: "#0ff" },
//             margin: { t: 10, b: 30, l: 40, r: 10 },
//             showlegend: false
//           }}
//           style={{ width: "100%", height: "160px" }}
//           config={{displayModeBar: false}}
//         />
//       </div>
//     </div>
//   );
// }

// export default App;
// -----------------------------------------------------------------------


// import React, { useState, useEffect, useRef } from 'react';
// import Plot from 'react-plotly.js';
// import { Shield, ShieldAlert, Activity, Crosshair, Zap, BrainCircuit } from 'lucide-react'; 
// import './App.css';

// function App() {
//   const [dataPoints, setDataPoints] = useState([]);
//   const [current, setCurrent] = useState({ 
//     speed: 0, 
//     status: "SCANNING...", 
//     is_danger: false, 
//     reason: "Analyzing Patterns..." // Default text
//   });
//   const [logs, setLogs] = useState([]);
//   const ws = useRef(null);
  
//   // Sound Effect
//   const alertSound = useRef(new Audio("https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg"));

//   useEffect(() => {
//     ws.current = new WebSocket("ws://127.0.0.1:8000/ws");
    
//     ws.current.onmessage = (event) => {
//       const data = JSON.parse(event.data);
//       setCurrent(data);

//       if(data.is_danger) {
//         alertSound.current.play().catch(e => console.log("Audio play failed"));
//         addLog(`⚠️ ${data.status}: ${data.reason}`);
//       }

//       // Graph Data Update
//       setDataPoints(prev => {
//         const newer = [...prev, { ...data, time: new Date().toLocaleTimeString() }];
//         if (newer.length > 50) newer.shift();
//         return newer;
//       });
//     };
//     return () => ws.current.close();
//   }, []);

//   const addLog = (msg) => setLogs(prev => [`> ${msg}`, ...prev.slice(0, 4)]);
  
//   const triggerAttack = async () => {
//     await fetch("http://127.0.0.1:8000/trigger-attack", { method: "POST" });
//     addLog("🛑 INJECTING MALICIOUS DATA PACKETS...");
//   };

//   return (
//     <div className={`dashboard ${current.is_danger ? 'danger-state' : ''}`}>
      
//       {/* HEADER */}
//       <div className="top-bar">
//         <div className="brand">
//           {current.is_danger ? <ShieldAlert color="red" size={28}/> : <Shield color="#0ff" size={28}/>}
//           <h2>CYBER<span className="highlight">SENTINEL</span> XAI</h2>
//         </div>
//         <div className={`status-badge ${current.is_danger ? 'blink-red' : ''}`}>
//            {current.is_danger ? "THREAT DETECTED" : "SYSTEM SECURE"}
//         </div>
//       </div>

//       <div className="middle-section">
//         {/* RADAR MAP */}
//         <div className="panel radar-box">
//           <div className="panel-header"><Crosshair size={16}/> GEO-SPATIAL TRACKING</div>
//           <Plot
//             data={[{
//               r: dataPoints.map(d => Math.sqrt(d.pos_x**2 + d.pos_y**2)),
//               theta: dataPoints.map(d => Math.atan2(d.pos_y, d.pos_x) * 180 / Math.PI),
//               mode: 'markers',
//               type: 'scatterpolar',
//               marker: { 
//                 color: dataPoints.map(d => d.is_danger ? '#ff0000' : '#00ffff'), 
//                 size: dataPoints.map(d => d.is_danger ? 18 : 8),
//                 symbol: dataPoints.map(d => d.is_danger ? 'cross' : 'circle')
//               }
//             }]}
//             layout={{
//               polar: {
//                 bgcolor: "rgba(0,0,0,0)",
//                 radialaxis: { visible: true, range: [0, 8000], showticklabels: false, gridcolor: "#333" },
//                 angularaxis: { gridcolor: "#333" }
//               },
//               paper_bgcolor: "rgba(0,0,0,0)",
//               margin: { t: 20, b: 20, l: 20, r: 20 },
//               showlegend: false
//             }}
//             style={{ width: "100%", height: "100%" }}
//             config={{displayModeBar: false}}
//           />
//         </div>

//         {/* RIGHT SIDE CONTROLS */}
//         <div className="right-col">
//           <div className="panel stats-box">
//             <div className="speed-gauge" style={{borderColor: current.is_danger ? 'red' : '#0ff'}}>
//               <h1>{current.speed.toFixed(0)}</h1><small>KM/H</small>
//             </div>
//             <div className="info-text">
//               <h3>ID: {current.id || "---"}</h3>
//               <p style={{color: current.is_danger ? 'red' : '#0ff'}}>{current.status}</p>
//             </div>
//           </div>

//           {/* --- NEW: AI REASONING BOX --- */}
//           <div className="panel reason-box" style={{borderLeft: current.is_danger ? "4px solid red" : "4px solid #0ff"}}>
//             <div className="panel-header"><BrainCircuit size={16}/> AI REASONING ENGINE</div>
//             <div className="reason-text">
//               {current.is_danger ? 
//                 <span style={{color: '#ff4444', fontWeight: 'bold'}}>{current.reason}</span> : 
//                 <span style={{color: '#00ff00'}}>Analysis: Behavior within normal parameters.</span>
//               }
//             </div>
//           </div>

//           <button className="attack-btn" onClick={triggerAttack}>
//             <Zap size={20} /> SIMULATE ATTACK
//           </button>

//           <div className="panel logs-box">
//             <div className="panel-header">_TERMINAL_LOGS</div>
//             {logs.map((log, i) => <div key={i} className="log-line">{log}</div>)}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default App;


// -------------------------------------------------

import React, { useState, useEffect, useRef } from 'react';
import Plot from 'react-plotly.js';
import { Shield, ShieldAlert, Activity, Crosshair, Zap, BrainCircuit } from 'lucide-react'; 
import './App.css';

function App() {
  const [dataPoints, setDataPoints] = useState([]);
  const [current, setCurrent] = useState({ speed: 0, status: "SCANNING", is_danger: false, reason: "Initializing AI..." });
  const [logs, setLogs] = useState([]);
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket("ws://127.0.0.1:8000/ws");
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setCurrent(data);
      if(data.is_danger) addLog(`⚠️ ${data.status}: ${data.reason}`);
      setDataPoints(prev => {
        const newer = [...prev, { ...data, time: new Date().toLocaleTimeString() }];
        return newer.length > 50 ? newer.slice(1) : newer;
      });
    };
    return () => ws.current.close();
  }, []);

  const addLog = (msg) => setLogs(prev => [`> ${msg}`, ...prev.slice(0, 4)]);
  const triggerAttack = () => fetch("http://127.0.0.1:8000/trigger-attack", { method: "POST" });

  return (
    <div className={`dashboard ${current.is_danger ? 'danger-state' : ''}`}>
      <div className="top-bar">
        <div className="brand">
          {current.is_danger ? <ShieldAlert color="red" size={28}/> : <Shield color="#0ff" size={28}/>}
          <h2>CYBER<span className="highlight">SENTINEL</span> XAI</h2>
        </div>
        <div className={`status-badge ${current.is_danger ? 'blink-red' : ''}`}>
           {current.is_danger ? "THREAT DETECTED" : "SYSTEM SECURE"}
        </div>
      </div>

      <div className="middle-section">
        <div className="panel radar-box">
          <div className="panel-header"><Crosshair size={16}/> GEO-SPATIAL TRACKING</div>
          <Plot data={[{ r: dataPoints.map(d => Math.sqrt(d.pos_x**2 + d.pos_y**2)), theta: dataPoints.map(d => Math.atan2(d.pos_y, d.pos_x) * 180 / Math.PI), mode: 'markers', type: 'scatterpolar', marker: { color: dataPoints.map(d => d.is_danger ? '#ff0000' : '#00ffff'), size: 10 }}]} layout={{ polar: { bgcolor: "rgba(0,0,0,0)", radialaxis: { range: [0, 8000] } }, paper_bgcolor: "rgba(0,0,0,0)", showlegend: false }} style={{ width: "100%", height: "100%" }} />
        </div>

        <div className="right-col">
          <div className="panel stats-box">
            <div className="speed-gauge" style={{borderColor: current.is_danger ? 'red' : '#0ff'}}>
              <h1>{current.speed.toFixed(0)}</h1><small>KM/H</small>
            </div>
            <div className="info-text">
              <h3>ID: {current.id || "---"}</h3>
              <p style={{color: current.is_danger ? 'red' : '#0ff'}}>{current.status}</p>
            </div>
          </div>

          <div className="panel reason-box" style={{borderLeft: current.is_danger ? "4px solid red" : "4px solid #0ff"}}>
            <div className="panel-header"><BrainCircuit size={16}/> AI REASONING ENGINE</div>
            <div className="reason-text" style={{color: current.is_danger ? '#ff4444' : '#00ff00', fontSize: '14px', padding: '10px'}}>
              {current.reason}
            </div>
          </div>

          <button className="attack-btn" onClick={triggerAttack}><Zap size={20} /> SIMULATE ATTACK</button>
          
          <div className="panel logs-box">
            <div className="panel-header">_TERMINAL_LOGS</div>
            {logs.map((log, i) => <div key={i} className="log-line">{log}</div>)}
          </div>
        </div>
      </div>
    </div>
  );
}
export default App;