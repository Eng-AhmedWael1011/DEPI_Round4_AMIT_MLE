import streamlit as st
import pandas as pd
from db import load_hospital, save_hospital #
from factory import Hospital, Department #
import time


# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="City Hospital Pro", page_icon="🏥", layout="wide")

# --- 2. PREMIUM CSS ---
st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background-color: rgba(59, 130, 246, 0.05);
        border: 1px solid rgba(59, 130, 246, 0.2);
        padding: 15px;
        border-radius: 15px;
    }
    .stButton>button {
        transition: all 0.2s ease;
        border-radius: 8px;
    }
    .stButton>button:hover {
        transform: scale(1.02);
    }
    /* Red button for discharge */
    .discharge-btn {
        color: #ef4444 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATA PERSISTENCE ---
if 'hospital' not in st.session_state:
    st.session_state.hospital = load_hospital() #

hosp = st.session_state.hospital

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🏥 Admin Panel")
    menu = st.radio("Go To", ["📊 Dashboard", "👥 Patient Registry", "🩺 Staff Directory", "📂 Data Export"])
    
    st.divider()
    if st.button("💾 Sync to Database", use_container_width=True, type="primary"):
        save_hospital(hosp) #
        st.toast("Database updated!", icon="💾")

# --- 5. PAGE LOGIC ---

if menu == "📊 Dashboard":
    st.title(f"Welcome to {hosp.hospital_name}") #
    col1, col2, col3 = st.columns(3)
    
    total_p = sum(len(d.patients) for d in hosp.departments) #
    total_s = sum(len(d.staff) for d in hosp.departments) #
    
    col1.metric("Total Patients", total_p)
    col2.metric("Staff Active", total_s)
    col3.metric("Departments", len(hosp.departments)) #

    # Quick Stats Table
    st.subheader("Department Occupancy")
    stats = [{"Dept": d.name, "Patients": len(d.patients), "Staff": len(d.staff)} for d in hosp.departments] #
    st.table(pd.DataFrame(stats))

elif menu == "👥 Patient Registry":
    st.title("Patient Registry")
    
    # Feature 1: Robust Search
    search_query = st.text_input("🔍 Search by Name or ID", placeholder="Search...").lower()

    # Layout for adding/viewing
    tab1, tab2 = st.tabs(["View Records", "New Admission"])

    with tab1:
        for d in hosp.departments:
            # Filter patients based on search
            matches = [p for p in d.patients if search_query in p.name.lower() or search_query in p.id.lower()] #
            
            if matches:
                st.write(f"### {d.name} Department")
                for p in matches:
                    col_info, col_action = st.columns([0.85, 0.15])
                    with col_info:
                        # Using view_info from factory.py
                        st.info(f"**{p.id}** | {p.name} (Age: {p.age}) — *{p.medical_record}*") 
                    
                    with col_action:
                        # Feature 2: Discharge (Delete) Button
                        if st.button("Discharge", key=f"del_{p.id}"):
                            d.patients.remove(p) # Modifying the list in factory.py
                            st.warning(f"Patient {p.name} Discharged.")
                            time.sleep(1)
                            st.rerun()

    with tab2:
        with st.form("add_p"):
            n = st.text_input("Name")
            a = st.number_input("Age", 0, 110)
            r = st.text_input("Medical Record")
            dep_name = st.selectbox("Department", [d.name for d in hosp.departments])
            if st.form_submit_button("Confirm Admission"):
                for d in hosp.departments:
                    if d.name == dep_name:
                        d.add_patient(n, a, r) #
                        st.success("Patient Added")
                        st.rerun()

elif menu == "📂 Data Export":
    st.title("Data Export Center")
    st.write("Generate and download hospital reports for external use.")
    
    # Feature 3: Export to CSV
    all_patients = []
    for d in hosp.departments:
        for p in d.patients:
            all_patients.append({
                "Patient ID": p.id, #
                "Name": p.name,
                "Age": p.age,
                "Diagnosis": p.medical_record,
                "Department": d.name
            })
    
    if all_patients:
        df = pd.DataFrame(all_patients)
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 Download Patient List as CSV",
            data=csv,
            file_name='hospital_patients.csv',
            mime='text/csv',
            use_container_width=True
        )
    else:
        st.info("No patient data available to export.")

elif menu == "🩺 Staff Directory":
    st.title("Medical Staff")
    for d in hosp.departments:
        if d.staff:
            st.subheader(d.name)
            s_data = [{"ID": s.id, "Name": s.name, "Position": s.position} for s in d.staff] #
            st.table(pd.DataFrame(s_data))