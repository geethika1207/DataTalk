import { useState } from "react";
import Auth from "./pages/Auth";
import Upload from "./pages/Upload";
import History from "./pages/History";
import DatasetDetail from "./pages/DatasetDetail";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || null);
  const [page, setPage] = useState("history");
  const [selectedDatasetId, setSelectedDatasetId] = useState(null);

  const handleLogin = (t) => { localStorage.setItem("token", t); setToken(t); setPage("history"); };
  const handleLogout = () => { localStorage.removeItem("token"); setToken(null); };

  if (!token) return <Auth onLogin={handleLogin} />;

  return (
    <div style={{ minHeight:"100vh", background:"#0a0f1a" }}>
      <Navbar page={page} setPage={(p) => { setSelectedDatasetId(null); setPage(p); }} onLogout={handleLogout} />
      <main style={{ maxWidth:1100, margin:"0 auto", padding:"2rem 1.5rem" }}>
        {page === "history" && <History token={token} onSelectDataset={(id) => { setSelectedDatasetId(id); setPage("detail"); }} />}
        {page === "upload" && <Upload token={token} onUploaded={() => setPage("history")} />}
        {page === "detail" && selectedDatasetId && <DatasetDetail token={token} datasetId={selectedDatasetId} onBack={() => setPage("history")} />}
      </main>
    </div>
  );
}

function Navbar({ page, setPage, onLogout }) {
  const navBtn = (p, icon, label) => (
    <button key={p} onClick={() => setPage(p)} style={{
      display:"flex", alignItems:"center", gap:6, padding:"7px 14px",
      borderRadius:8, border:"none", fontSize:14, fontWeight:500, cursor:"pointer",
      background: page === p ? "rgba(99,102,241,0.15)" : "transparent",
      color: page === p ? "#818cf8" : "#8b9bb4",
      transition:"all 0.15s",
    }}>
      <i className={`ti ${icon}`} style={{ fontSize:15 }} aria-hidden="true" />
      {label}
    </button>
  );

  return (
    <nav style={{
      background:"rgba(17,24,39,0.95)", backdropFilter:"blur(12px)",
      borderBottom:"1px solid rgba(255,255,255,0.06)",
      padding:"0 1.5rem", display:"flex", alignItems:"center",
      justifyContent:"space-between", height:56,
      position:"sticky", top:0, zIndex:100,
    }}>
      <div style={{ display:"flex", alignItems:"center", gap:10 }}>
        <div style={{ width:32, height:32, borderRadius:8, background:"linear-gradient(135deg,#6366f1,#818cf8)", display:"flex", alignItems:"center", justifyContent:"center" }}>
          <i className="ti ti-chart-dots" style={{ fontSize:17, color:"#fff" }} aria-hidden="true" />
        </div>
        <span style={{ fontSize:17, fontWeight:600, color:"#f0f4ff", letterSpacing:"-0.3px" }}>DataTalk</span>
        <span style={{ fontSize:11, fontWeight:500, padding:"2px 7px", background:"rgba(99,102,241,0.2)", color:"#818cf8", borderRadius:5 }}>AI</span>
      </div>
      <div style={{ display:"flex", gap:2, alignItems:"center" }}>
        {navBtn("history", "ti-history", "History")}
        {navBtn("upload", "ti-upload", "Upload")}
        <div style={{ width:1, height:20, background:"rgba(255,255,255,0.08)", margin:"0 6px" }} />
        <button onClick={onLogout} style={{ display:"flex", alignItems:"center", gap:6, padding:"7px 14px", borderRadius:8, border:"none", fontSize:14, color:"#8b9bb4", background:"transparent", cursor:"pointer" }}>
          <i className="ti ti-logout" style={{ fontSize:15 }} aria-hidden="true" />
          Logout
        </button>
      </div>
    </nav>
  );
}
