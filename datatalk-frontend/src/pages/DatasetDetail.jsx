import { useState, useEffect, useRef } from "react";
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const API = "http://127.0.0.1:8000";
const COLORS = ["#6366f1","#14b8a6","#fbbf24","#f87171","#818cf8","#34d399"];

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background:"#1a2235", border:"1px solid rgba(255,255,255,0.1)", borderRadius:8, padding:"8px 12px" }}>
      <p style={{ color:"#8b9bb4", fontSize:12, marginBottom:4 }}>{label}</p>
      <p style={{ color:"#f0f4ff", fontWeight:600, fontSize:14 }}>{payload[0]?.value?.toLocaleString()}</p>
    </div>
  );
};

export default function DatasetDetail({ token, datasetId, onBack }) {
  const [dataset, setDataset] = useState(null);
  const [loading, setLoading] = useState(true);
  const [question, setQuestion] = useState("");
  const [asking, setAsking] = useState(false);
  const [error, setError] = useState("");
  const [queries, setQueries] = useState([]);
  const bottomRef = useRef();

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const res = await fetch(`${API}/dataset/${datasetId}`, { headers:{ Authorization:`Bearer ${token}` } });
        const data = await res.json();
        if (!res.ok) { setError("Failed to load dataset."); return; }
        setDataset(data); setQueries(data.queries || []);
      } catch { setError("Network error."); }
      finally { setLoading(false); }
    };
    load();
  }, [datasetId]);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior:"smooth" }); }, [queries]);

  const handleAsk = async () => {
    if (!question.trim()) return;
    setAsking(true); setError("");
    const q = question.trim(); setQuestion("");
    try {
      const res = await fetch(`${API}/datasets/${datasetId}/queries`, {
        method:"POST",
        headers:{ Authorization:`Bearer ${token}`, "Content-Type":"application/json" },
        body:JSON.stringify({ question:q }),
      });
      const data = await res.json();
      if (!res.ok) { setError(data.detail || "Something went wrong."); return; }
      setQueries(prev => [...prev, { id:data.id, question:q, answer:data.answer, charts:data.charts }]);
    } catch { setError("Network error."); }
    finally { setAsking(false); }
  };

  if (loading) return (
    <div style={{ textAlign:"center", padding:"5rem", color:"#8b9bb4" }}>
      <i className="ti ti-loader" style={{ fontSize:28 }} aria-hidden="true" />
      <p style={{ marginTop:12 }}>Loading dataset...</p>
    </div>
  );

  return (
    <div style={{ maxWidth:820, margin:"0 auto" }}>
      <button onClick={onBack} style={{ display:"flex", alignItems:"center", gap:6, marginBottom:"1.5rem", background:"none", border:"none", color:"#8b9bb4", cursor:"pointer", fontSize:14, padding:0, fontFamily:"DM Sans, sans-serif" }}>
        <i className="ti ti-arrow-left" style={{ fontSize:15 }} aria-hidden="true" />Back to history
      </button>

      {dataset && (
        <div style={{ background:"rgba(17,24,39,0.8)", border:"1px solid rgba(255,255,255,0.06)", borderRadius:14, padding:"1rem 1.25rem", marginBottom:"1.5rem", display:"flex", alignItems:"center", gap:14 }}>
          <div style={{ width:44, height:44, borderRadius:12, background:"rgba(99,102,241,0.15)", display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0 }}>
            <i className="ti ti-table" style={{ fontSize:22, color:"#6366f1" }} aria-hidden="true" />
          </div>
          <div style={{ flex:1, minWidth:0 }}>
            <p style={{ fontWeight:600, color:"#f0f4ff", margin:0, fontSize:15 }}>{dataset.title}</p>
            <p style={{ fontSize:13, color:"#8b9bb4", margin:"2px 0 0", overflow:"hidden", textOverflow:"ellipsis", whiteSpace:"nowrap" }}>{dataset.filename}</p>
          </div>
          <div style={{ fontSize:13, color:"#8b9bb4", flexShrink:0 }}>
            <span style={{ padding:"4px 10px", borderRadius:20, background:"rgba(99,102,241,0.12)", color:"#818cf8", fontWeight:500 }}>{queries.length} queries</span>
          </div>
        </div>
      )}

      {error && (
        <div style={{ padding:"12px 16px", borderRadius:10, marginBottom:"1rem", background:"rgba(248,113,113,0.1)", color:"#f87171", fontSize:14, border:"1px solid rgba(248,113,113,0.2)" }}>{error}</div>
      )}

      <div style={{ display:"flex", flexDirection:"column", gap:14, marginBottom:"5rem" }}>
        {queries.length === 0 && (
          <div style={{ textAlign:"center", padding:"4rem 2rem", background:"rgba(17,24,39,0.6)", border:"1px solid rgba(255,255,255,0.06)", borderRadius:16 }}>
            <div style={{ width:56, height:56, borderRadius:14, background:"rgba(99,102,241,0.12)", display:"flex", alignItems:"center", justifyContent:"center", margin:"0 auto 14px" }}>
              <i className="ti ti-message-question" style={{ fontSize:28, color:"#6366f1" }} aria-hidden="true" />
            </div>
            <p style={{ fontWeight:600, color:"#f0f4ff", marginBottom:8 }}>Ask your first question</p>
            <p style={{ color:"#8b9bb4", fontSize:14 }}>Try: "Compare total profit by category" or "Show sales trend over time"</p>
          </div>
        )}

        {queries.map((q) => (
          <div key={q.id}>
            <div style={{ display:"flex", justifyContent:"flex-end", marginBottom:8 }}>
              <div style={{ background:"rgba(99,102,241,0.12)", border:"1px solid rgba(99,102,241,0.2)", borderRadius:12, borderBottomRightRadius:4, padding:"10px 16px", maxWidth:"80%", fontSize:14, color:"#c7d2fe", lineHeight:1.5 }}>
                {q.question}
              </div>
            </div>
            <div style={{ background:"rgba(17,24,39,0.8)", border:"1px solid rgba(255,255,255,0.06)", borderRadius:12, borderTopLeftRadius:4, padding:"1rem 1.25rem" }}>
              <div style={{ display:"flex", gap:10, marginBottom:q.charts ? 16 : 0 }}>
                <div style={{ width:30, height:30, borderRadius:"50%", background:"linear-gradient(135deg,#6366f1,#818cf8)", display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0, marginTop:1 }}>
                  <i className="ti ti-sparkles" style={{ fontSize:14, color:"#fff" }} aria-hidden="true" />
                </div>
                <p style={{ margin:0, fontSize:14, lineHeight:1.7, color:"#d1d9f0" }}>{q.answer}</p>
              </div>
              {q.charts && <ChartView chart={q.charts} />}
            </div>
          </div>
        ))}

        {asking && (
          <div style={{ background:"rgba(17,24,39,0.8)", border:"1px solid rgba(255,255,255,0.06)", borderRadius:12, borderTopLeftRadius:4, padding:"1rem 1.25rem", display:"flex", alignItems:"center", gap:10 }}>
            <div style={{ width:30, height:30, borderRadius:"50%", background:"linear-gradient(135deg,#6366f1,#818cf8)", display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0 }}>
              <i className="ti ti-sparkles" style={{ fontSize:14, color:"#fff" }} aria-hidden="true" />
            </div>
            <div style={{ display:"flex", gap:4, alignItems:"center" }}>
              {[0,1,2].map(i => (
                <div key={i} style={{ width:6, height:6, borderRadius:"50%", background:"#6366f1", animation:`pulse 1.2s ease-in-out ${i*0.2}s infinite` }} />
              ))}
              <style>{`@keyframes pulse { 0%,100%{opacity:0.3;transform:scale(0.8)} 50%{opacity:1;transform:scale(1)} }`}</style>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div style={{
        position:"fixed", bottom:24, left:"50%", transform:"translateX(-50%)",
        width:"min(820px, calc(100vw - 3rem))",
        background:"rgba(17,24,39,0.95)", backdropFilter:"blur(16px)",
        border:"1px solid rgba(99,102,241,0.2)",
        borderRadius:14, padding:"10px 10px 10px 16px",
        display:"flex", gap:8, alignItems:"center",
        boxShadow:"0 8px 32px rgba(0,0,0,0.4)",
      }}>
        <input
          type="text" value={question}
          onChange={e => setQuestion(e.target.value)}
          onKeyDown={e => e.key === "Enter" && !asking && handleAsk()}
          placeholder="Ask a question about your data..."
          style={{ flex:1, border:"none", background:"transparent", outline:"none", fontSize:14, color:"#f0f4ff", fontFamily:"DM Sans, sans-serif" }}
          disabled={asking}
        />
        <button onClick={handleAsk} disabled={asking || !question.trim()} style={{
          background:"linear-gradient(135deg,#6366f1,#818cf8)", color:"#fff",
          border:"none", borderRadius:10, padding:"8px 16px",
          fontWeight:600, fontSize:14, cursor:asking || !question.trim() ? "not-allowed" : "pointer",
          opacity:asking || !question.trim() ? 0.5 : 1,
          display:"flex", alignItems:"center", gap:6, fontFamily:"DM Sans, sans-serif",
          transition:"opacity 0.2s",
        }}>
          <i className="ti ti-send" style={{ fontSize:14 }} aria-hidden="true" />Ask
        </button>
      </div>
    </div>
  );
}

function ChartView({ chart }) {
  if (!chart || !chart.type) return null;
  const chartData = chart.labels.map((label, i) => ({
    name: typeof label === 'object' ? JSON.stringify(label) : String(label),
    value: typeof chart.values[i] === 'number' ? chart.values[i] : Number(chart.values[i])
  }));

  const axisStyle = { fill:"#5a6a82", fontSize:12, fontFamily:"DM Sans, sans-serif" };

  return (
    <div style={{ borderTop:"1px solid rgba(255,255,255,0.06)", paddingTop:16, marginTop:4 }}>
      <p style={{ fontSize:12, color:"#5a6a82", margin:"0 0 14px", display:"flex", alignItems:"center", gap:6, fontWeight:500, textTransform:"capitalize" }}>
        <i className="ti ti-chart-bar" style={{ fontSize:14, color:"#6366f1" }} aria-hidden="true" />
        {chart.type} chart
      </p>
      <ResponsiveContainer width="100%" height={240}>
        {chart.type === "bar" ? (
          <BarChart data={chartData} margin={{ top:4, right:8, left:0, bottom:4 }}>
            <XAxis dataKey="name" tick={axisStyle} axisLine={{ stroke:"rgba(255,255,255,0.08)" }} tickLine={false} />
            <YAxis tick={axisStyle} axisLine={false} tickLine={false} />
            <Tooltip content={<CustomTooltip />} cursor={{ fill:"rgba(99,102,241,0.08)" }} />
            <Bar dataKey="value" fill="#6366f1" radius={[6,6,0,0]} />
          </BarChart>
        ) : chart.type === "line" ? (
          <LineChart data={chartData} margin={{ top:4, right:8, left:0, bottom:4 }}>
            <XAxis dataKey="name" tick={axisStyle} axisLine={{ stroke:"rgba(255,255,255,0.08)" }} tickLine={false} />
            <YAxis tick={axisStyle} axisLine={false} tickLine={false} />
            <Tooltip content={<CustomTooltip />} />
            <Line type="monotone" dataKey="value" stroke="#6366f1" strokeWidth={2.5} dot={{ fill:"#6366f1", r:4, strokeWidth:0 }} activeDot={{ r:6, fill:"#818cf8" }} />
          </LineChart>
        ) : (
          <PieChart>
            <Pie data={chartData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={90} innerRadius={40} paddingAngle={3} label={({ name, percent }) => `${name} ${(percent*100).toFixed(0)}%`} labelLine={{ stroke:"rgba(255,255,255,0.15)" }}>
              {chartData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
          </PieChart>
        )}
      </ResponsiveContainer>
    </div>
  );
}
