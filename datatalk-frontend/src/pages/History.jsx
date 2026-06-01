import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

export default function History({ token, onSelectDataset }) {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [deleting, setDeleting] = useState(null);

  const fetchDatasets = async (q = "") => {
    setLoading(true); setError("");
    try {
      const res = await fetch(`${API}/history?search=${encodeURIComponent(q)}&limit=20`, { headers:{ Authorization:`Bearer ${token}` } });
      if (res.status === 404) { setDatasets([]); return; }
      if (!res.ok) { setError("Failed to load datasets."); return; }
      setDatasets(await res.json());
    } catch { setError("Network error."); }
    finally { setLoading(false); }
  };

  useEffect(() => { fetchDatasets(); }, []);

  const handleSearch = (e) => { setSearch(e.target.value); fetchDatasets(e.target.value); };

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm("Delete this dataset and all its queries?")) return;
    setDeleting(id);
    try {
      await fetch(`${API}/dataset/${id}`, { method:"DELETE", headers:{ Authorization:`Bearer ${token}` } });
      setDatasets(prev => prev.filter(d => d.id !== id));
    } catch { setError("Delete failed."); }
    finally { setDeleting(null); }
  };

  const categoryColors = ["rgba(99,102,241,0.15)", "rgba(20,184,166,0.15)", "rgba(251,191,36,0.15)", "rgba(248,113,113,0.15)"];
  const iconColors = ["#818cf8", "#14b8a6", "#fbbf24", "#f87171"];

  return (
    <div>
      <div style={{ display:"flex", alignItems:"center", justifyContent:"space-between", marginBottom:"2rem", flexWrap:"wrap", gap:12 }}>
        <div>
          <h1 style={{ fontSize:26, fontWeight:600, color:"#f0f4ff", marginBottom:4, letterSpacing:"-0.5px" }}>Your datasets</h1>
          <p style={{ color:"#8b9bb4", fontSize:15 }}>
            {datasets.length > 0 ? `${datasets.length} dataset${datasets.length !== 1 ? "s" : ""} · click to analyze` : "Upload a CSV to get started"}
          </p>
        </div>
        <div style={{ position:"relative" }}>
          <i className="ti ti-search" style={{ position:"absolute", left:12, top:"50%", transform:"translateY(-50%)", fontSize:15, color:"#5a6a82", pointerEvents:"none" }} aria-hidden="true" />
          <input type="text" value={search} onChange={handleSearch} placeholder="Search datasets..." style={{ paddingLeft:36, width:220, background:"rgba(17,24,39,0.8)" }} />
        </div>
      </div>

      {error && (
        <div style={{ padding:"12px 16px", borderRadius:10, marginBottom:"1rem", background:"rgba(248,113,113,0.1)", color:"#f87171", fontSize:14, border:"1px solid rgba(248,113,113,0.2)" }}>{error}</div>
      )}

      {loading ? (
        <div style={{ textAlign:"center", padding:"5rem", color:"#8b9bb4" }}>
          <i className="ti ti-loader" style={{ fontSize:28 }} aria-hidden="true" />
          <p style={{ marginTop:12 }}>Loading your datasets...</p>
        </div>
      ) : datasets.length === 0 ? (
        <div style={{ textAlign:"center", padding:"5rem 2rem", background:"rgba(17,24,39,0.6)", border:"1px solid rgba(255,255,255,0.06)", borderRadius:16 }}>
          <div style={{ width:64, height:64, borderRadius:16, background:"rgba(99,102,241,0.12)", display:"flex", alignItems:"center", justifyContent:"center", margin:"0 auto 16px" }}>
            <i className="ti ti-database-off" style={{ fontSize:32, color:"#6366f1" }} aria-hidden="true" />
          </div>
          <p style={{ fontWeight:600, color:"#f0f4ff", marginBottom:8, fontSize:16 }}>No datasets yet</p>
          <p style={{ color:"#8b9bb4", fontSize:14 }}>Upload a CSV file to start analyzing your data with AI</p>
        </div>
      ) : (
        <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fill, minmax(320px, 1fr))", gap:14 }}>
          {datasets.map((ds, i) => (
            <div key={ds.id} onClick={() => onSelectDataset(ds.id)} style={{
              background:"rgba(17,24,39,0.8)", border:"1px solid rgba(255,255,255,0.06)",
              borderRadius:14, padding:"1.25rem", cursor:"pointer", transition:"all 0.2s",
              position:"relative", overflow:"hidden",
            }}
              onMouseEnter={e => { e.currentTarget.style.borderColor = "rgba(99,102,241,0.3)"; e.currentTarget.style.background = "rgba(26,34,53,0.9)"; }}
              onMouseLeave={e => { e.currentTarget.style.borderColor = "rgba(255,255,255,0.06)"; e.currentTarget.style.background = "rgba(17,24,39,0.8)"; }}
            >
              <div style={{ display:"flex", alignItems:"flex-start", justifyContent:"space-between", marginBottom:12 }}>
                <div style={{ width:42, height:42, borderRadius:12, background:categoryColors[i % 4], display:"flex", alignItems:"center", justifyContent:"center" }}>
                  <i className="ti ti-table" style={{ fontSize:20, color:iconColors[i % 4] }} aria-hidden="true" />
                </div>
                <button onClick={e => handleDelete(ds.id, e)} disabled={deleting === ds.id} style={{
                  background:"transparent", border:"none", borderRadius:8, padding:"6px",
                  cursor:"pointer", color:"#5a6a82", display:"flex", alignItems:"center", transition:"all 0.15s",
                }}
                  onMouseEnter={e => { e.currentTarget.style.color = "#f87171"; e.currentTarget.style.background = "rgba(248,113,113,0.1)"; }}
                  onMouseLeave={e => { e.currentTarget.style.color = "#5a6a82"; e.currentTarget.style.background = "transparent"; }}
                  aria-label="Delete">
                  <i className="ti ti-trash" style={{ fontSize:15 }} aria-hidden="true" />
                </button>
              </div>
              <p style={{ fontWeight:600, color:"#f0f4ff", fontSize:15, marginBottom:4, overflow:"hidden", textOverflow:"ellipsis", whiteSpace:"nowrap" }}>{ds.title}</p>
              <p style={{ fontSize:13, color:"#8b9bb4", marginBottom:14, overflow:"hidden", textOverflow:"ellipsis", whiteSpace:"nowrap" }}>{ds.filename}</p>
              <div style={{ display:"flex", alignItems:"center", justifyContent:"space-between" }}>
                <span style={{ fontSize:12, padding:"4px 10px", borderRadius:20, background:ds.queries.length > 0 ? "rgba(52,211,153,0.12)" : "rgba(255,255,255,0.05)", color:ds.queries.length > 0 ? "#34d399" : "#5a6a82", fontWeight:500 }}>
                  {ds.queries.length} {ds.queries.length === 1 ? "query" : "queries"}
                </span>
                <i className="ti ti-arrow-right" style={{ fontSize:15, color:"#5a6a82" }} aria-hidden="true" />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
