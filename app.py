import streamlit as st
import pandas as pd
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Kelora WCAG Demo", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS (Hostinger-like Font 'Inter', No Emojis, Clean UI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global Font Settings */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Button Styling */
    div.stButton > button:first-child {
        background-color: #6366F1;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #4F46E5;
        color: white;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    /* Clean up dataframe borders */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# --- MOCKUP ENGINES (Replace with your actual APIs later) ---
def run_axe(url): time.sleep(1.5); return {"score": 85, "errors": 12, "warnings": 24}
def run_wave(url): time.sleep(1.2); return {"errors": 15, "contrast": 8, "alerts": 32}
def run_lighthouse(url): time.sleep(2.0); return {"score": 78, "aria_issues": 5, "nav_issues": 3}

# --- MAIN INTERFACE ---
st.markdown("## Lightning Fast Accessibility Audit (Demo)")
st.markdown("Check your homepage using 3 engines simultaneously. **Save 15 minutes of manual testing.**")

# Input Section
col_input, col_btn = st.columns([3, 1])
with col_input:
    target_url = st.text_input("Enter URL", placeholder="https://your-store.com", label_visibility="collapsed")
with col_btn:
    start_scan = st.button("Scan Now (Free)", use_container_width=True)

# --- SCAN LOGIC ---
if start_scan:
    if target_url.startswith("http"):
        with st.spinner("Running scanners: Axe, WAVE, and Lighthouse..."):
            # Fetching data (simulation)
            axe_data = run_axe(target_url)
            wave_data = run_wave(target_url)
            lh_data = run_lighthouse(target_url)
        
        # --- RESULTS: 3 COLUMNS ---
        st.success("Scan complete! View the raw data below.")
        st.markdown("---")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("### Axe Core")
            st.metric(label="Critical Errors", value=axe_data["errors"])
            st.caption("DOM structure, ARIA, semantics.")
        with c2:
            st.markdown("### WAVE")
            st.metric(label="Contrast Errors", value=wave_data["contrast"])
            st.caption("Contrast, missing labels.")
        with c3:
            st.markdown("### Lighthouse")
            st.metric(label="Accessibility Score", value=f"{lh_data['score']}/100")
            st.caption("Overall score, SEO, navigation.")

        # --- SUMMARY TABLE ---
        st.markdown("#### Scan Summary")
        df_summary = pd.DataFrame({
            "Engine": ["Axe Core", "WAVE", "Lighthouse", "AI De-duplication (Kelora)"],
            "Detected Errors": [axe_data["errors"], wave_data["errors"] + wave_data["contrast"], lh_data["aria_issues"], "Locked (Premium)"],
            "Warnings": [axe_data["warnings"], wave_data["alerts"], lh_data["nav_issues"], "Locked (Premium)"]
        })
        st.dataframe(df_summary, hide_index=True, use_container_width=True)

        # --- PAYWALL / LEAD MAGNET ---
        st.markdown("---")
        st.markdown("### Want a full User Journey audit?")
        st.info("This test only checked a static homepage. Real accessibility issues hide in dropdowns, pop-ups, and checkout processes.")
        
        st.markdown("""
        **What you get in the full version:**
        * **Full flow testing** (Add to cart -> Login -> Checkout)
        * **Keyboard (Tab)** and screen reader simulation
        * **Ready-to-use PDF report** with AI remediation fixes
        """)
        
        st.markdown("#### Book a free 15-minute demo of the full platform:")
        
        lead_col1, lead_col2 = st.columns([2, 1])
        with lead_col1:
            email = st.text_input("Work email address", placeholder="john@youragency.com", label_visibility="collapsed")
        with lead_col2:
            if st.button("Book Demo", type="primary", use_container_width=True):
                if "@" in email:
                    st.success(f"Thanks! We will contact you at {email} within 24h.")
                else:
                    st.error("Please enter a valid email.")
    else:
        st.warning("Remember to add http:// or https:// before the address.")
