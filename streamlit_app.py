import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# --- CONFIGURATION ---
API_URL = "https://datatalk-1-qlhh.onrender.com" 

st.set_page_config(page_title="DataTalk AI", layout="wide")

# --- SESSION STATE INITIALIZATION ---
if "token" not in st.session_state:
    st.session_state.token = None
if "dataset_id" not in st.session_state:
    st.session_state.dataset_id = None
# Swapped single-question states for a persistent messages list
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR: AUTHENTICATION & UPLOADS ---
with st.sidebar:
    st.title("📊 DataTalk AI")
    
    # Not Logged In
    if not st.session_state.token:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            log_email = st.text_input("Email", key="log_email")
            log_pass = st.text_input("Password", type="password", key="log_pass")
            if st.button("Login"):
                # Professional UX copy
                with st.spinner("Authenticating securely... This may take a moment."):
                    res = requests.post(f"{API_URL}/login", data={"username": log_email, "password": log_pass})
                    if res.status_code == 201 or res.status_code == 200:
                        st.session_state.token = res.json()["access_token"]
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
                    
        with tab2:
            reg_email = st.text_input("Email", key="reg_email")
            reg_pass = st.text_input("Password", type="password", key="reg_pass")
            if st.button("Register"):
                # Professional UX copy
                with st.spinner("Setting up your account workspace..."):
                    res = requests.post(f"{API_URL}/user", json={"email": reg_email, "password": reg_pass})
                    if res.status_code == 201:
                        st.success("Registration successful! Please log in.")
                    else:
                        st.error("Email already registered.")
                        
    # Logged In
    else:
        st.success("✅ Logged in")
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()
            
        st.divider()
        st.subheader("📁 Dataset Management")
        
        # Lock uploader after one dataset is active
        if st.session_state.dataset_id:
            st.success("Your dataset is linked and ready for analysis.")
            st.info("To analyze a different dataset, please log out and start a new session.")
        else:
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
            title = st.text_input("Dataset Title", value="My Dataset")
            
            if uploaded_file and st.button("Upload & Analyze"):
                with st.spinner("Parsing dataset structure..."):
                    headers = {"Authorization": f"Bearer {st.session_state.token}"}
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                    data = {"title": title}
                    
                    res = requests.post(f"{API_URL}/datasets/upload", headers=headers, files=files, data=data)
                    
                    if res.status_code == 201:
                        st.session_state.dataset_id = res.json()["dataset_id"]
                        st.rerun()
                    else:
                        st.error("Upload failed. Please check your file.")

# --- MAIN CHAT INTERFACE ---
st.header("Ask your Data Anything 💡")

if not st.session_state.token:
    st.info("👈 Please log in from the sidebar to begin.")
elif not st.session_state.dataset_id:
    st.info("👈 Please upload a CSV dataset from the sidebar to start analyzing.")
else:
    # 1. Render Chat History (Allows scrolling and comparing)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        elif msg["role"] == "assistant":
            with st.chat_message("assistant"):
                data = msg["content"]
                st.write(data.get("answer", ""))
                
                charts = data.get("charts")
                if charts and charts.get("data"):
                    df = pd.DataFrame(charts["data"])
                    config = charts.get("config", {})
                    chart_type = config.get("type")
                    x_col = config.get("x_axis")
                    y_col = config.get("y_axis")
                    
                    if chart_type and x_col and y_col:
                        if chart_type == "bar":
                            if len(df) > 10:
                                fig = px.bar(df, x=y_col, y=x_col, orientation='h', title=f"{y_col} by {x_col}")
                                fig.update_layout(yaxis={'categoryorder':'total ascending'})
                                # Show numbers directly on horizontal bars
                                fig.update_traces(texttemplate='%{x:,.0f}', textposition='outside')
                            else:
                                fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
                                # Show numbers directly on vertical bars
                                fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
                            st.plotly_chart(fig, use_container_width=True)
                            
                        elif chart_type == "line":
                            fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} Trend")
                            st.plotly_chart(fig, use_container_width=True)
                            
                        elif chart_type == "pie":
                            fig = px.pie(df, names=x_col, values=y_col, title=f"{y_col} Distribution")
                            st.plotly_chart(fig, use_container_width=True)
                            
                    elif chart_type is None:
                        st.divider()
                        cols = st.columns(len(df.columns))
                        for col_obj, col_name in zip(cols, df.columns):
                            val = df.iloc[0][col_name]
                            if isinstance(val, (int, float)):
                                val = f"{val:,.2f}"
                            col_obj.metric(label=col_name.replace("_", " ").title(), value=val)

    # 2. Chat Input Zone
    question = st.chat_input("E.g., Show me the top 10 cities by total sales...")
    
    if question:
        # Append user question to history and instantly render it
        st.session_state.messages.append({"role": "user", "content": question})
        st.rerun()

    # 3. Trigger API Call (Runs only if the last message was from the user)
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.spinner("Generating insights..."):
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            payload = {"question": st.session_state.messages[-1]["content"]}
            res = requests.post(f"{API_URL}/dataset/{st.session_state.dataset_id}/queries", headers=headers, json=payload)
            
            if res.status_code == 201:
                st.session_state.messages.append({"role": "assistant", "content": res.json()})
                st.rerun()
            else:
                st.error("An error occurred while generating insights. Please try again.")