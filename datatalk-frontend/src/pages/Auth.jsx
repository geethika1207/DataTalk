import { useState } from "react";

const API = "https://datatalk-xq73.onrender.com";

const S = {
  page: { minHeight:"100vh", display:"flex", background:"#0a0f1a" },
  left: {
    flex:1, display:"flex", flexDirection:"column", justifyContent:"center",
    padding:"3rem", background:"linear-gradient(135deg, #0d1424 0%, #111827 50%, #0f1f35 100%)",
    borderRight:"1px solid rgba(255,255,255,0.06)", position:"relative", overflow:"hidden",
  },
  right: { flex:1, display:"flex", alignItems:"center", justifyContent:"center", padding:"2rem" },
  card: {
    width:"100%", maxWidth:420,
    background:"#111827", border:"1px solid rgba(255,255,255,0.08)",
    borderRadius:16, padding:"2.5rem",
  },
  logo: { display:"flex", alignItems:"center", gap:10, marginBottom:"3rem" },
  logoText: { fontSize:22, fontWeight:600, color:"#f0f4ff", letterSpacing:"-0.5px" },
  badge: {
    fontSize:11, fontWeight:500, padding:"3px 8px",
    background:"rgba(99,102,241,0.2)", color:"#818cf8",
    borderRadius:6, letterSpacing:"0.5px",
  },
  hero: { marginBottom:"2rem" },
  heroTitle: { fontSize:36, fontWeight:600, color:"#f0f4ff", lineHeight:1.2, marginBottom:12, letterSpacing:"-0.5px" },
  heroSub: { fontSize:15, color:"#8b9bb4", lineHeight:1.6 },
  featureList: { display:"flex", flexDirection:"column", gap:14, marginTop:"2.5rem" },
  feature: { display:"flex", alignItems:"flex-start", gap:12 },
  featureIcon: {
    width:36, height:36, borderRadius:10, flexShrink:0,
    display:"flex", alignItems:"center", justifyContent:"center",
  },
  featureText: { fontSize:14, color:"#8b9bb4", lineHeight:1.5 },
  featureName: { fontWeight:500, color:"#f0f4ff", fontSize:14, marginBottom:2 },
  glow: {
    position:"absolute", width:400, height:400, borderRadius:"50%",
    background:"radial-gradient(circle, rgba(99,102,241,0.08) 0%, transparent 70%)",
    top:-100, right:-100, pointerEvents:"none",
  },
  glow2: {
    position:"absolute", width:300, height:300, borderRadius:"50%",
    background:"radial-gradient(circle, rgba(20,184,166,0.06) 0%, transparent 70%)",
    bottom:50, left:-50, pointerEvents:"none",
  },
  cardTitle: { fontSize:22, fontWeight:600, color:"#f0f4ff", marginBottom:6 },
  cardSub: { fontSize:14, color:"#8b9bb4", marginBottom:"2rem" },
  label: { fontSize:13, color:"#8b9bb4", display:"block", marginBottom:6, fontWeight:500 },
  formGroup: { marginBottom:"1.25rem" },
  btn: {
    width:"100%", padding:"11px", borderRadius:10, marginTop:8,
    background:"linear-gradient(135deg, #6366f1, #818cf8)",
    color:"#fff", border:"none", fontWeight:600, fontSize:14,
    letterSpacing:"0.2px", transition:"opacity 0.2s, transform 0.1s",
  },
  error: {
    padding:"10px 14px", borderRadius:10, marginBottom:"1.25rem",
    background:"rgba(248,113,113,0.1)", color:"#f87171",
    fontSize:13, border:"1px solid rgba(248,113,113,0.2)",
  },
  success: {
    padding:"10px 14px", borderRadius:10, marginBottom:"1.25rem",
    background:"rgba(52,211,153,0.1)", color:"#34d399",
    fontSize:13, border:"1px solid rgba(52,211,153,0.2)",
  },
  switchText: { textAlign:"center", marginTop:"1.5rem", fontSize:13, color:"#8b9bb4" },
  switchBtn: { background:"none", border:"none", color:"#818cf8", fontWeight:600, fontSize:13, padding:0 },
};

const features = [
  { icon:"ti-upload", color:"rgba(99,102,241,0.2)", iconColor:"#818cf8", name:"Upload any CSV", desc:"Drag and drop your dataset and we handle the rest" },
  { icon:"ti-brain", color:"rgba(20,184,166,0.15)", iconColor:"#14b8a6", name:"Ask in plain English", desc:"No SQL needed — just type your question naturally" },
  { icon:"ti-chart-bar", color:"rgba(251,191,36,0.15)", iconColor:"#fbbf24", name:"Instant visual charts", desc:"Bar, line, and pie charts generated automatically" },
];

export default function Auth({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState("");

  const handleSubmit = async () => {
    setError(""); setSuccess("");
    if (!email || !password) { setError("Please fill in all fields."); return; }
    setLoading(true);
    try {
      if (isLogin) {
        const form = new URLSearchParams();
        form.append("username", email);
        form.append("password", password);
        const res = await fetch(`${API}/login`, { method:"POST", body:form });
        const data = await res.json();
        if (!res.ok) { setError(data.detail || "Login failed"); return; }
        onLogin(data.access_token);
      } else {
        const res = await fetch(`${API}/user`, {
          method:"POST",
          headers:{ "Content-Type":"application/json" },
          body:JSON.stringify({ email, password }),
        });
        const data = await res.json();
        if (!res.ok) { setError(data.detail || "Registration failed"); return; }
        setSuccess("Account created! Please sign in.");
        setIsLogin(true);
      }
    } catch { setError("Network error. Is your backend running?"); }
    finally { setLoading(false); }
  };

  return (
    <div style={S.page}>
      <div style={S.left}>
        <div style={S.glow} />
        <div style={S.glow2} />
        <div style={S.logo}>
          <div style={{ width:38, height:38, borderRadius:10, background:"linear-gradient(135deg,#6366f1,#818cf8)", display:"flex", alignItems:"center", justifyContent:"center" }}>
            <i className="ti ti-chart-dots" style={{ fontSize:20, color:"#fff" }} aria-hidden="true" />
          </div>
          <span style={S.logoText}>DataTalk</span>
          <span style={S.badge}>AI</span>
        </div>
        <div style={S.hero}>
          <h1 style={S.heroTitle}>Turn your CSV<br />into insights<br /><span style={{ color:"#818cf8" }}>in seconds</span></h1>
          <p style={S.heroSub}>Ask questions about your data in plain English. Get answers, charts, and analysis instantly — no coding required.</p>
        </div>
        <div style={S.featureList}>
          {features.map(f => (
            <div key={f.name} style={S.feature}>
              <div style={{ ...S.featureIcon, background:f.color }}>
                <i className={`ti ${f.icon}`} style={{ fontSize:18, color:f.iconColor }} aria-hidden="true" />
              </div>
              <div>
                <p style={S.featureName}>{f.name}</p>
                <p style={S.featureText}>{f.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div style={S.right}>
        <div style={S.card}>
          <h2 style={S.cardTitle}>{isLogin ? "Welcome back" : "Create account"}</h2>
          <p style={S.cardSub}>{isLogin ? "Sign in to your DataTalk account" : "Start analyzing your data with AI"}</p>

          {error && <div style={S.error}><i className="ti ti-alert-circle" style={{ marginRight:6 }} />{error}</div>}
          {success && <div style={S.success}><i className="ti ti-check" style={{ marginRight:6 }} />{success}</div>}

          <div style={S.formGroup}>
            <label style={S.label}>Email address</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="you@example.com" onKeyDown={e => e.key === "Enter" && handleSubmit()} />
          </div>
          <div style={S.formGroup}>
            <label style={S.label}>Password</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="••••••••" onKeyDown={e => e.key === "Enter" && handleSubmit()} />
          </div>
          <button onClick={handleSubmit} disabled={loading} style={{ ...S.btn, opacity:loading?0.7:1 }}>
            {loading ? "Please wait..." : (isLogin ? "Sign in" : "Create account")}
          </button>

          <p style={S.switchText}>
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <button onClick={() => { setIsLogin(!isLogin); setError(""); setSuccess(""); }} style={S.switchBtn}>
              {isLogin ? "Sign up" : "Sign in"}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}
