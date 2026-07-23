"use client";
import { useState } from "react";

export default function Dashboard() {
  const [token, setToken] = useState<string | null>(null);
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("admin123");
  const [prediction, setPrediction] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    
    try {
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);
      
      const res = await fetch("http://127.0.0.1:8000/api/v1/auth/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
      });
      
      const data = await res.json();
      if (res.ok) {
        setToken(data.access_token);
      } else {
        setError(data.detail || "Login failed");
      }
    } catch (err) {
      setError("Network error connecting to backend API.");
    } finally {
      setLoading(false);
    }
  };

  const fetchPredictions = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/predictions/hyperlocal?lat=23.8103&lng=90.4125&horizon=3", {
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = await res.json();
      if (res.ok) {
        setPrediction(data);
      } else {
        setError("Session expired or unauthorized. Please login again.");
        setToken(null);
      }
    } catch (err) {
      setError("Network error connecting to backend API.");
    } finally {
      setLoading(false);
    }
  };

  if (!token) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white">
        <form onSubmit={handleLogin} className="p-8 bg-gray-800 rounded-lg shadow-lg flex flex-col gap-4">
          <h1 className="text-2xl font-bold mb-4">Dhaka PM2.5 Login</h1>
          {error && <div className="text-red-400 text-sm">{error}</div>}
          <input 
            type="text" value={username} onChange={e => setUsername(e.target.value)}
            className="p-2 bg-gray-700 rounded text-white" placeholder="Username"
          />
          <input 
            type="password" value={password} onChange={e => setPassword(e.target.value)}
            className="p-2 bg-gray-700 rounded text-white" placeholder="Password"
          />
          <button type="submit" disabled={loading} className="p-2 bg-blue-600 rounded font-bold hover:bg-blue-500">
            {loading ? "Authenticating..." : "Login securely via JWT"}
          </button>
        </form>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-8 bg-gray-900 text-white">
      <header className="flex justify-between items-center mb-8 pb-4 border-b border-gray-700">
        <h1 className="text-3xl font-bold">Dhaka STGCN <span className="text-blue-400">Live Inference</span></h1>
        <button onClick={() => setToken(null)} className="px-4 py-2 bg-red-600 rounded text-sm font-bold hover:bg-red-500">Logout</button>
      </header>
      
      {error && <div className="mb-4 p-4 bg-red-900 border border-red-700 rounded text-red-200">{error}</div>}
      
      <div className="flex gap-4 mb-8">
        <button onClick={fetchPredictions} disabled={loading} className="px-6 py-3 bg-blue-600 rounded shadow hover:bg-blue-500 font-bold">
          {loading ? "Fetching PyTorch Tensors..." : "Fetch Real Live Predictions"}
        </button>
      </div>

      {prediction && (
        <div className="p-6 bg-gray-800 rounded-lg border border-gray-700 shadow-xl max-w-2xl">
          <h2 className="text-xl text-gray-400 uppercase tracking-widest mb-2">Intersection ID: {prediction.intersection_id}</h2>
          <div className="text-6xl font-black mb-4 {prediction.current_pm25 > 150 ? 'text-red-500' : 'text-green-500'}">
            {prediction.current_pm25.toFixed(1)} <span className="text-xl text-gray-400 font-normal">µg/m³</span>
          </div>
          <div className="text-gray-400 mb-6">AI Confidence Score: <span className="text-white font-bold">{(prediction.confidence_score * 100).toFixed(0)}%</span> (Model: {prediction.model_version})</div>
          
          <h3 className="font-bold border-b border-gray-700 pb-2 mb-4">Future Horizons</h3>
          <ul className="space-y-3">
            {prediction.predictions.map((p: any, i: number) => (
              <li key={i} className="flex justify-between items-center p-3 bg-gray-700 rounded">
                <span>+{p.hour_offset} Hours</span>
                <span className="font-bold text-xl">{p.predicted_pm25.toFixed(1)} µg/m³</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
