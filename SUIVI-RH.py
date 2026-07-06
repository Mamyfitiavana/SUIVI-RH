import streamlit as st
import pandas as pd

# 1. Fanamafisana ny Pejy Streamlit ho an'ny tabilao lehibe
st.set_page_config(layout="wide", page_title="Suivi RH - Jolay 2026")

st.title("📊 Rafitra Fitaovana Suivi RH - Jolay 2026")

# Lisitry ny Alahady amin'ny volana Jolay 2026 (05, 12, 19, 26)
alahady_list = ["05/07", "12/07", "19/07", "26/07"]

# 2. Famoronana tabilao banga ao amin'ny Session State
if "df_rh" not in st.session_state:
    columns = [
        "Matricule", "Nom", "Prénom", "CE / Département", 
        "Date d'embauche", "Type contrat", "Fin contrat", 
        "Solde congé", "NB Jour Absence"
    ]
    # Manampy ny andro 01 hatramin'ny 31 Jolay
    for andro in range(1, 32):
        columns.append(f"{andro:02d}/07")
        
    st.session_state.df_rh = pd.DataFrame(columns=columns)

# 3. PEJY KELY MISOKATRA (Modal Pop-up) REHEFA TSINDRINA ILAY BOUTON
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
            # ATAO VIDE TANTERAKA (fotsy) NY ANDRO REHETRA 01-31
            for andro in range(1, 32):
                new_worker[f"{andro:02d}/07"] = None  # None no mahatonga azy ho banga eo amin'ny tabilao
                
            new_df = pd.DataFrame([new_worker])
            st.session_state.df_rh = pd.concat([st.session_state.df_rh, new_df], ignore_index=True)
            st.rerun()
        else:
            st.error("Misy saha tsy maintsy fenoina (*)")

# 4. FITAOVANA SIVANA SY FIKAROHANA (Ao amin'ny Sidebar)
st.sidebar.header("🔍 Sivana sy Fikarohana")
df = st.session_state.df_rh

lisitra_ce = ["REHETRA"] + list(df["CE / Département"].unique()) if not df.empty else ["REHETRA"]
ce_voafidy = st.sidebar.selectbox("Safidio ny CE / Département:", lisitra_ce)
fikarohana = st.sidebar.text_input("Mikaroka mpiasa (Nom/Matricule):")

# Fampiharana ny sivana
df_filtered = df.copy()
if not df_filtered.empty:
    if ce_voafidy != "REHETRA":
        df_filtered = df_filtered[df_filtered["CE / Département"] == ce_voafidy]
    if fikarohana:
        df_filtered = df_filtered[
            df_filtered["Nom"].str.contains(fikarohana, case=False) | 
            df_filtered["Matricule"].str.contains(fikarohana, case=False)
        ]

# 5. BOUTON "AJOUTER" SY FAMPISEHOANA NY TABILAO LEHIBE
col_btn, col_clear = st.columns([1, 4])
with col_btn:
    if st.button("➕ Ajouter un employé", use_container_width=True, type="primary"):
        ampiditra_mpiasa_form()
with col_clear:
    # Bokotra hamafana ny fitadidiana taloha raha mbola misy "Présent" niletra teo
    if st.button("🗑️ Fafao ny data taloha (Atao vide ny tabilao)"):
        st.session_state.df_rh = pd.DataFrame(columns=st.session_state.df_rh.columns)
        st.rerun()

st.markdown("---")
st.subheader(f"📋 Tabilao pointage mpiasa ({len(df_filtered)} tafiditra)")

if df_filtered.empty:
    st.info("Mbola tsy misy mpiasa ny tabilao. Kitiho ilay bokotra 'Ajouter un employé' eo ambony io mba hampidirana ny voalohany.")
else:
    # 6. HEADERS CONFIGURATION: Mandamina ny safidy sy ny loko ho an'ny Alahady
    andro_columns = [f"{andro:02d}/07" for andro in range(1, 32)]
    config_colona = {}
    
    for col in andro_columns:
        if col in alahady_list:
            # Raha Alahady dia asiana famantarana 🔴 sady asiana soratra hoe (Dimanche)
            config_colona[col] = st.column_config.SelectboxColumn(
                label=f"🔴 {col} (Dim)",
                options=["Présent", "Absent", "Repos", "Congé"],
                help="Andro Alahady"
            )
        else:
            config_colona[col] = st.column_config.SelectboxColumn(
                options=["Présent", "Absent", "Repos", "Congé"]
            )
            
    config_colona["Type contrat"] = st.column_config.SelectboxColumn(options=["CDI", "CDD", "Essai", "Stage"])
    config_colona["CE / Département"] = st.column_config.SelectboxColumn(options=["CE 1", "CE 2", "CE 3", "CE 4"])

    # Fampisehoana ilay tabilao azo ovaina mivantana
    edited_df = st.data_editor(
        df_filtered,
        column_config=config_colona,
        use_container_width=True,
        hide_index=True
    )

    # Bokotra hitahirizana ny fanovana
    if st.button("💾 Tehirizo ny pointage / fanovana"):
        st.session_state.df_rh.update(edited_df)
        st.success("Tafatahiry soa aman-tsara ny pointage vaovao!")
