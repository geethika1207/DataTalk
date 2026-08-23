import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# --- CONFIGURATION ---
# Point this to your Render URL!
API_URL = "https://datatalk-1-qlhh.onrender.com" 

st.set_page_config(page_title="DataTalk AI", layout="wide")

# --- SESSION STATE INITIALIZATION ---
if "token" not in st.session_state:
    st.session_state.token = None
if "dataset_id" not in st.session_state:
    st.session_state.dataset_id = None
if "latest_question" not in st.session_state:
    st.session_state.latest_question = None
if "latest_response" not in st.session_state:
    st.session_state.latest_response = None

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
                # ADDED SPINNER HERE
                with st.spinner("Connecting to server (may take a minute to wake up)..."):
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
                # ADDED SPINNER HERE
                with st.spinner("Registering user & waking up backend..."):
                    res = requests.post(f"{API_URL}/user", json={"email": reg_email, "password": reg_pass})
                    if res.status_code == 201:
                        st.success("Registered! Please login.")
                    else:
                        st.error("Email already registered.")                    
    # Logged In
    else:
        st.success("✅ Logged in")
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()
            
        st.divider()
        st.subheader("📁 Upload Dataset")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        title = st.text_input("Dataset Title", value="My Dataset")
        
        if uploaded_file and st.button("Upload to Backend"):
            with st.spinner("Processing metadata..."):
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                data = {"title": title}
                
                res = requests.post(f"{API_URL}/datasets/upload", headers=headers, files=files, data=data)
                
                if res.status_code == 201:
                    st.session_state.dataset_id = res.json()["dataset_id"]
                    st.success(f"Dataset active! (ID: {st.session_state.dataset_id})")
                else:
                    st.error("Upload failed.")

# --- MAIN CHAT INTERFACE ---
st.header("Ask your Data Anything 💡")

if not st.session_state.token:
    st.info("👈 Please login from the sidebar to start analyzing data.")
elif not st.session_state.dataset_id:
    st.info("👈 Please upload a CSV dataset from the sidebar.")
else:
    # 1. Chat Input
    question = st.chat_input("E.g., Show me the top 10 cities by total sales...")
    
    if question:
        st.session_state.latest_question = question
        with st.spinner("Analyzing data..."):
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            payload = {"question": question}
            res = requests.post(f"{API_URL}/dataset/{st.session_state.dataset_id}/queries", headers=headers, json=payload)
            
            if res.status_code == 201:
                st.session_state.latest_response = res.json()
            else:
                st.error("Error generating insight.")
    
    # 2. Render Latest Result (No History)
    if st.session_state.latest_question and st.session_state.latest_response:
        st.chat_message("user").write(st.session_state.latest_question)
        
        with st.chat_message("assistant"):
            data = st.session_state.latest_response
            
            # Print the AI's explanation
            st.write(data.get("answer", ""))
            
            charts = data.get("charts")
            if charts and charts.get("data"):
                df = pd.DataFrame(charts["data"])
                config = charts.get("config", {})
                chart_type = config.get("type")
                x_col = config.get("x_axis")
                y_col = config.get("y_axis")
                
                if chart_type and x_col and y_col:
                    # Smart Rendering: Use Horizontal Bar Chart if too many categories
                    if chart_type == "bar":
                        if len(df) > 10:
                            # Horizontal bar chart prevents crowded labels!
                            fig = px.bar(df, x=y_col, y=x_col, orientation='h', title=f"{y_col} by {x_col}")
                            fig.update_layout(yaxis={'categoryorder':'total ascending'})
                        else:
                            fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
                        st.plotly_chart(fig, use_container_width=True)
                        
                    elif chart_type == "line":
                        fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} Trend")
                        st.plotly_chart(fig, use_container_width=True)
                        
                    elif chart_type == "pie":
                        fig = px.pie(df, names=x_col, values=y_col, title=f"{y_col} Distribution")
                        st.plotly_chart(fig, use_container_width=True)
                        
                elif chart_type is None:
                    # Render Scalar Totals nicely side-by-side
                    st.divider()
                    cols = st.columns(len(df.columns))
                    for col_obj, col_name in zip(cols, df.columns):
                        val = df.iloc[0][col_name]
                        # Format if numeric
                        if isinstance(val, (int, float)):
                            val = f"{val:,.2f}"
                        col_obj.metric(label=col_name.replace("_", " ").title(), value=val)