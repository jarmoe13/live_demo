import streamlit as st
import pandas as pd
import time

# --- KONFIGURACJA STRONY ---
# Layout "wide" żeby tabela i kolumny dobrze wyglądały w iframe
st.set_page_config(page_title="Kelora WCAG Demo", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS (Ukrywamy branding Streamlita dla embeda) ---
st.markdown("""
    <style>
    /* Ukrycie paska menu i stopki Streamlita */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Własny styl przycisków pod markę Kelora */
    div.stButton > button:first-child {
        background-color: #6366F1; /* Twój główny kolor, zmień na swój */
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        padding: 0.5rem 1rem;
    }
    div.stButton > button:hover {
        background-color: #4F46E5;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- MOCKUPY SILNIKÓW (Tutaj później podepniesz swoje API) ---
def run_axe(url): time.sleep(1.5); return {"score": 85, "errors": 12, "warnings": 24}
def run_wave(url): time.sleep(1.2); return {"errors": 15, "contrast": 8, "alerts": 32}
def run_lighthouse(url): time.sleep(2.0); return {"score": 78, "aria_issues": 5, "nav_issues": 3}

# --- GŁÓWNY INTERFEJS ---
st.markdown("## 🚀 Błyskawiczny Audyt Dostępności (Wersja Demo)")
st.markdown("Sprawdź swoją stronę główną za pomocą 3 silników jednocześnie. **Oszczędź 15 minut manualnego klikania.**")

# Sekcja Inputu
col_input, col_btn = st.columns([3, 1])
with col_input:
    target_url = st.text_input("Wprowadź URL", placeholder="https://twoj-sklep.pl", label_visibility="collapsed")
with col_btn:
    start_scan = st.button("Skanuj teraz (Za darmo)", use_container_width=True)

# --- LOGIKA SKANOWANIA ---
if start_scan:
    if target_url.startswith("http"):
        with st.spinner("Uruchamiam skanery: Axe, WAVE i Lighthouse..."):
            # Pobieranie danych (symulacja)
            axe_data = run_axe(target_url)
            wave_data = run_wave(target_url)
            lh_data = run_lighthouse(target_url)
        
        # --- WYNIKI: 3 KOLUMNY ---
        st.success("Skanowanie zakończone! Zobacz surowe dane poniżej.")
        st.markdown("---")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("### 🪓 Axe Core")
            st.metric(label="Błędy krytyczne", value=axe_data["errors"])
            st.caption("Struktura DOM, ARIA, semantyka.")
        with c2:
            st.markdown("### 🌊 WAVE")
            st.metric(label="Błędy kontrastu", value=wave_data["contrast"])
            st.caption("Kontrast, brakujące etykiety.")
        with c3:
            st.markdown("### 💡 Lighthouse")
            st.metric(label="Wynik Accessibility", value=f"{lh_data['score']}/100")
            st.caption("Ogólna ocena, SEO, nawigacja.")

        # --- TABELA ZBIORCZA (Aha! Moment) ---
        st.markdown("#### 📊 Podsumowanie skanowania")
        df_summary = pd.DataFrame({
            "Silnik": ["Axe Core", "WAVE", "Lighthouse", "De-duplikacja AI (Kelora)"],
            "Wykryte Błędy": [axe_data["errors"], wave_data["errors"] + wave_data["contrast"], lh_data["aria_issues"], "🔒 Zablokowane"],
            "Ostrzeżenia": [axe_data["warnings"], wave_data["alerts"], lh_data["nav_issues"], "🔒 Zablokowane"]
        })
        st.dataframe(df_summary, hide_index=True, use_container_width=True)

        # --- PAYWALL / LEAD MAGNET ---
        st.markdown("---")
        st.markdown("### 🔥 Chcesz pełnego audytu User Journey?")
        st.info("Powyższy test sprawdził tylko **statyczną stronę główną**. Prawdziwe problemy z dostępnością kryją się w rozwijanych menu, pop-upach i koszykach zakupowych.")
        
        st.markdown("""
        **Co zyskujesz w pełnej wersji:**
        * 🤖 **Testowanie całych ścieżek** (Dodaj do koszyka -> Logowanie -> Płatność)
        * ⌨️ **Symulacja klawiatury (Tab)** i czytników ekranu
        * 📄 **Gotowy raport PDF** z rekomendacjami naprawczymi (Fixes) od AI
        """)
        
        st.markdown("#### Zarezerwuj bezpłatne 15-minutowe demo pełnej platformy:")
        
        lead_col1, lead_col2 = st.columns([2, 1])
        with lead_col1:
            email = st.text_input("Służbowy adres e-mail", placeholder="jan@twojaagencja.pl", label_visibility="collapsed")
        with lead_col2:
            if st.button("Zabukuj Demo", type="primary", use_container_width=True):
                if "@" in email:
                    # Tutaj możesz podpiąć webhooka do Make/Zapier/Discorda, żeby wysłał Ci powiadomienie
                    st.success(f"Dzięki! Odezwiemy się na {email} w ciągu 24h.")
                    st.balloons()
                else:
                    st.error("Podaj poprawny e-mail.")
    else:
        st.warning("Pamiętaj o dodaniu http:// lub https:// przed adresem.")
