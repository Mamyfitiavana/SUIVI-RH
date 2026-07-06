import streamlit as st
import pandas as pd

# 1. Fanamafisana ny Pejy Streamlit (Atao lehibe ny tabilao)
st.set_page_config(layout="wide", page_title="Rafitra Fitantanana - 2026")

st.markdown("""
    <style>
    .reportview-container { background-color: #fafafa; }
    h1 { color: #1E3A8A; font-family: 'Segoe UI', sans-serif; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# 2. MENU PRINCIPAL EO AMIN'NY SIDEBAR (Safidy Pejy)
st.sidebar.title("🎮 Menu lehibe")
pejy_voafidy = st.sidebar.radio(
    "Safidio ny asa tiana hatao:",
    ["📊 SUIVI RH", "⚙️ SUIVI PROD"]
)

# Kalandrie Jolay 2026
anaran_andro = ["Mer", "Jeu", "Ven", "Sam", "Dim", "Lun", "Mar"]
kalandrie_jolay = []
alahady_list = []

for i in range(1, 32):
    index_andro = (i + 1) % 7
    anarana = anaran_andro[index_andro]
    format_daty = f"{anarana} {i:02d}"
    kalandrie_jolay.append(format_daty)
    if anarana == "Dim":
        alahady_list.append(format_daty)

# ------------------------------------------------------------------
# PEJY 1 : SUIVI RH
# ------------------------------------------------------------------
if pejy_voafidy == "📊 SUIVI RH":
    st.title("📊 Rafitra Fitaovana Suivi RH - Jolay 2026")

    # Famoronana tabilao misy mpiasa ohatra iray (Exemple) ao amin'ny Session State
    if "df_rh" not in st.session_state:
        columns = [
            "Matricule", "Nom", "Prénom", "CE / Département", 
            "Date d'embauche", "Type contrat", "Fin contrat", 
            "Solde congé", "NB Jour Absence"
        ]
        for andro in kalandrie_jolay:
            columns.append(andro)
            
        # Mamorona mpiasa ohatra iray (Exemple 1) izay fotsy/vide ny tabilao pointage-ny
        mpiasa_ohatra = {
            "Matricule": "MAT-0001",
            "Nom": "RAKOTO",
            "Prénom": "Jean",
            "CE / Département": "CE 1",
            "Date d'embauche": "2026-01-01",
            "Type contrat": "CDI",
            "Fin contrat": "-",
            "Solde congé": 30,
            "NB Jour Absence": 0
        }
        for andro in kalandrie_jolay:
            mpiasa_ohatra[andro] = None # Atao banga par défaut
            
        st.session_state.df_rh = pd.DataFrame([mpiasa_ohatra], columns=columns)

    # Pop-up hampidirana mpiasa vaovao
    @st.dialog("➕ Ampidiro ny Mpiasa Vaovao")
    def ampiditra_mpiasa_form():
        with st.form(key="form_ajouter", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                matricule = st.text_input("Matricule *")
                nom = st.text_input("Nom *")
                prenom = st.text_input("Prénom *")
                ce = st.selectbox("CE / Département *", ["CE 1", "CE 2", "CE 3", "CE 4"])
            with col2:
                date_embauche = st.date_input("Date d'embauche")
                type_contrat = st.selectbox("Type contrat", ["CDI", "CDD", "Essai", "Stage"])
                fin_contrat = st.text_input("Fin contrat (Raha misy)", value="-")
                solde_conge = st.number_input("Solde congé", min_value=0, value=0)
                
            st.markdown("---")
            submit_button = st.form_submit_button(label="💾 Tehirizo ato amin'ny tabilao", use_container_width=True)

        if submit_button:
            if matricule and nom and prenom:
                new_worker = {
                    "Matricule": matricule,
                    "Nom": nom,
                    "Prénom": prenom,
                    "CE / Département": ce,
                    "Date d'embauche": str(date_embauche),
                    "Type contrat": type_contrat,
                    "Fin contrat": fin_contrat,
                    "Solde congé": solde_conge,
                    "NB Jour Absence": 0
                }
                for andro in kalandrie_jolay:
                    new_worker[andro] = None  
                    
                new_df = pd.DataFrame([new_worker])
                st.session_state.df_rh = pd.concat([st.session_state.df_rh, new_df], ignore_index=True)
                st.rerun()
            else:
                st.error("Misy saha tsy maintsy fenoina (*)")

    # Fitaovana sivana ao amin'ny Sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Sivana RH")
    df = st.session_state.df_rh

    lisitra_ce = ["REHETRA"] + list(df["CE / Département"].unique()) if not df.empty else ["REHETRA"]
    ce_voafidy = st.sidebar.selectbox("Safidio ny CE / Département:", lisitra_ce)
    fikarohana = st.sidebar.text_input("Mikaroka mpiasa (Nom/Matricule):")

    df_filtered = df.copy()
    if not df_filtered.empty:
        if ce_voafidy != "REHETRA":
            df_filtered = df_filtered[df_filtered["CE / Département"] == ce_voafidy]
        if fikarohana:
            df_filtered = df_filtered[
                df_filtered["Nom"].str.contains(fikarohana, case=False) | 
                df_filtered["Matricule"].str.contains(fikarohana, case=False)
            ]

    # Bokotra Ajouter sy Reset (Namboarina ho st.columns(2) mba tsy hisy erreur intsony)
    col_btn, col_clear = st.columns(2)
    with col_btn:
        if st.button("➕ Ajouter un employé", use_container_width=True, type="primary"):
            ampiditra_mpiasa_form()
    with col_clear:
        if st.button("🗑️ Reset Tabilao (Hamafa ny mpiasa rehetra)", use_container_width=True):
            st.session_state.df_rh = pd.DataFrame(columns=st.session_state.df_rh.columns)
            st.rerun()

    st.markdown("---")
    st.subheader(f"📋 Tabilao pointage mpiasa ({len(df_filtered)} hita)")

    if df_filtered.empty:
        st.info("Mbola tsy misy mpiasa ny tabilao. Kitiho ilay bokotra 'Ajouter un employé' eo ambony io mba hampidirana mpiasa vaovao.")
    else:
        config_colona = {}
        for col in kalandrie_jolay:
            if col in alahady_list:
                config_colona[col] = st.column_config.SelectboxColumn(label=f"🔴 {col}", options=["Présent", "Absent", "Repos", "Congé"])
            else:
                config_colona[col] = st.column_config.SelectboxColumn(label=col, options=["Présent", "Absent", "Repos", "Congé"])
                
        config_colona["Type contrat"] = st.column_config.SelectboxColumn(options=["CDI", "CDD", "Essai", "Stage"])
        config_colona["CE / Département"] = st.column_config.SelectboxColumn(options=["CE 1", "CE 2", "CE 3", "CE 4"])

        edited_df = st.data_editor(df_filtered, column_config=config_colona, use_container_width=True, hide_index=True)

        if st.button("💾 Tehirizo ny pointage / fanovana", use_container_width=True):
            st.session_state.df_rh.update(edited_df)
            st.success("Tafatahiry soa aman-tsara ny pointage vaovao!")

# ------------------------------------------------------------------
# PEJY 2 : SUIVI PROD
# ------------------------------------------------------------------
elif pejy_voafidy == "⚙️ SUIVI PROD":
    st.title("⚙️ Rafitra Fitaovana Suivi Production")
    st.write("Eto no hiseho ny tabilao sy ny mombamomba ny famokarana (Production).")
    st.info("💡 Vonona handray ny torimarika momba ny Suivi Prod aho izao. Soraty eto ny tsipiriany rehetra tianao hatao ato!")
