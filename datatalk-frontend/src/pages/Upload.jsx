import { useState, useRef } from "react";

const API = "https://datatalk-5.onrender.com";

export default function Upload({ token, onUploaded }) {
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef();

  const handleFile = (f) => {
    if (!f) return;
    if (!f.name.endsWith(".csv")) { setError("Only CSV files are allowed."); return; }
    setError(""); setFile(f);
    if (!title) setTitle(f.name.replace(".csv", ""));
  };

  const handleDrop = (e) => { e.preventDefault(); setDragging(false); handleFile(e.dataTransfer.files[0]); };

  const handleUpload = async () => {
    if (!file || !title) { setError("Please select a file and enter a title."); return; }
    setLoading(true); setError("");
    try {
      const form = new FormData();
      form.append("file", file); form.append("title", title);
      const res = await fetch(`${API}/datasets/upload`, { method:"POST", headers:{ Authorization:`Bearer ${token}` }, body:form });
      const data = await res.json();
      if (!res.ok) { setError(data.detail || "Upload failed"); return; }
      onUploaded();
    } catch { setError("Network error."); }
    finally { setLoading(false); }
  };

  return (
    <div style={{ maxWidth:580, margin:"0 auto" }}>
      <div style={{ marginBottom:"2rem" }}>
        <h1 style={{ fontSize:26, fontWeight:600, color:"#f0f4ff", marginBottom:6, letterSpacing:"-0.5px" }}>Upload dataset</h1>
        <p style={{ color:"#8b9bb4", fontSize:15 }}>Upload a CSV file to start asking AI-powered questions about your data.</p>
      </div>

      {error && (
        <div style={{ padding:"12px 16px", borderRadius:10, marginBottom:"1.5rem", background:"rgba(248,113,113,0.1)", color:"#f87171", fontSize:14, border:"1px solid rgba(248,113,113,0.2)", display:"flex", alignItems:"center", gap:8 }}>
          <i className="ti ti-alert-circle" style={{ fontSize:16, flexShrink:0 }} aria-hidden="true" />{error}
        </div>
      )}

      <div
        onClick={() => inputRef.current.click()}
        onDragOver={e => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        style={{
          border:`2px dashed ${dragging ? "#6366f1" : "rgba(255,255,255,0.1)"}`,
          borderRadius:16, padding:"3rem 2rem", textAlign:"center", cursor:"pointer",
          background: dragging ? "rgba(99,102,241,0.06)" : "rgba(17,24,39,0.6)",
          transition:"all 0.2s", marginBottom:"1.5rem",
        }}
      >
        <input ref={inputRef} type="file" accept=".csv" style={{ display:"none" }} onChange={e => handleFile(e.target.files[0])} />
        {file ? (
          <div>
            <div style={{ width:56, height:56, borderRadius:14, background:"rgba(52,211,153,0.15)", display:"flex", alignItems:"center", justifyContent:"center", margin:"0 auto 12px" }}>
              <i className="ti ti-file-check" style={{ fontSize:28, color:"#34d399" }} aria-hidden="true" />
            </div>
            <p style={{ fontWeight:600, color:"#f0f4ff", marginBottom:4 }}>{file.name}</p>
            <p style={{ fontSize:13, color:"#8b9bb4" }}>{(file.size / 1024).toFixed(1)} KB — click to change</p>
          </div>
        ) : (
          <div>
            <div style={{ width:56, height:56, borderRadius:14, background:"rgba(99,102,241,0.12)", display:"flex", alignItems:"center", justifyContent:"center", margin:"0 auto 16px" }}>
              <i className="ti ti-upload" style={{ fontSize:28, color:"#6366f1" }} aria-hidden="true" />
            </div>
            <p style={{ fontWeight:600, color:"#f0f4ff", marginBottom:6 }}>Drop your CSV here</p>
            <p style={{ fontSize:13, color:"#8b9bb4", marginBottom:12 }}>or click to browse files</p>
            <span style={{ fontSize:12, padding:"4px 12px", borderRadius:20, border:"1px solid rgba(255,255,255,0.1)", color:"#5a6a82" }}>CSV files only</span>
          </div>
        )}
      </div>

      <div style={{ marginBottom:"1.5rem" }}>
        <label style={{ fontSize:13, color:"#8b9bb4", display:"block", marginBottom:6, fontWeight:500 }}>Dataset title</label>
        <input type="text" value={title} onChange={e => setTitle(e.target.value)} placeholder="e.g. Sales Report Q4 2024" />
      </div>

      <button onClick={handleUpload} disabled={loading} style={{
        width:"100%", padding:"12px", borderRadius:10,
        background:"linear-gradient(135deg, #6366f1, #818cf8)",
        color:"#fff", border:"none", fontWeight:600, fontSize:15,
        cursor:loading ? "not-allowed" : "pointer", opacity:loading ? 0.7 : 1,
        display:"flex", alignItems:"center", justifyContent:"center", gap:8,
      }}>
        <i className="ti ti-upload" style={{ fontSize:16 }} aria-hidden="true" />
        {loading ? "Uploading..." : "Upload dataset"}
      </button>
    </div>
  );
}
