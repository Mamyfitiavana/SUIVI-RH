import streamlit as st
import pandas as pd

# 1. Fanamafisana ny Pejy Streamlit ho an'ny tabilao lehibe
st.set_page_config(layout="wide", page_title="Suivi RH - Jolay 2026")

st.title("📊 Rafitra Fitaovana Suivi RH - Jolay 2026")

# 2. Famoronana tabilao banga ao amin'ny Session State (Tsy fafana rehefa mi-actualise)
if "df_rh" not in st.session_state:
    # Mamorona ny lohatenin'ny tsanganana rehetra (Colonnes)
    columns = [
        "Matricule", "Nom", "Prénom", "CE / Département", 
        "Date d'embauche", "Type contrat", "Fin contrat", 
        "Solde congé", "NB Jour Absence"
    ]
    # Manampy ny andro 01 hatramin'ny 31 Jolay
    for andro in range(1, 32):
        columns.append(f"{andro:02d}/07")
        
    # Atomboka amin'ny tabilao tsy misy mpiasa mihitsy (banga)
    st.session_state.df_rh = pd.DataFrame(columns=columns)

# 3. FITAOVANA AMPIDIRANA MPIASA VAOVAO (Formulaire Ajouter)
st.sidebar.header("➕ Ampidiro ny Mpiasa Vaovao")
with st.sidebar.form(key="form_ajouter_mpiasa", clear_on_submit=True):
    matricule = st.text_input("Matricule *")
    nom = st.text_input("Nom *")
    prenom = st.text_input("Prénom *")
    ce = st.selectbox("CE / Département *", ["CE 1", "CE 2", "CE 3", "CE 4"])
    date_embauche = st.date_input("Date d'embauche")
    type_contrat = st.selectbox("Type contrat", ["CDI", "CDD", "Essai", "Stage"])
    fin_contrat = st.text_input("Fin contrat (Raha misy)", value="-")
    solde_conge = st.number_input("Solde congé", min_value=0, max_value=100, value=0)
    nb_absence = st.number_input("NB Jour Absence", min_value=0, max_value=31, value=0)
    
    submit_button = st.form_submit_button(label="Ajouter")

# Rehefa tsindrina ilay bokotra Ajouter
if submit_button:
    if matricule and nom and prenom: # Hamarinina raha feno ny fepetra fototra
        # Manomana ny angon-drakitra vaovao
        new_worker = {
            "Matricule": matricule,
            "Nom": nom,
            "Prénom": prenom,
            "CE / Département": ce,
            "Date d'embauche": str(date_embauche),
            "Type contrat": type_contrat,
            "Fin contrat": fin_contrat,
            "Solde congé": solde_conge,
            "NB Jour Absence": nb_absence
        }
        # Atao "None" ny kalandrie rehetra ho an'ity mpiasa vaovao ity
        for andro in range(1, 32):
            new_worker[f"{andro:02d}/07"] = "None"
            
        # Ampidirina ao anatin'ny tabilao lehibe
        new_df = pd.DataFrame([new_worker])
        st.session_state.df_rh = pd.concat([st.session_state.df_rh, new_df], ignore_index=True)
        st.sidebar.success(f"Tafiditra soa aman-tsara i {nom} {prenom}!")
    else:
        st.sidebar.error("Misy saha tsy maintsy fenoina (*)")

# 4. FITAOVANA SIVANA SY FIKAROHANA (Ao amin'ny Sidebar ihany)
st.sidebar.markdown("---")
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

# 5. FAMPISEHOANA NY TABILAO LEHIBE (Tableau Global)
st.subheader(f"📋 Tabilao pointage mpiasa ({len(df_filtered)} tafiditra)")

if df_filtered.empty:
    st.info("Mbola tsy misy mpiasa ny tabilao. Ampiasao ilay takelaka fenoina eo amin'ny sisiny havia (Sidebar) mba hampidirana mpiasa vaovao.")
else:
    # Mamorona safidy ho an'ny kalandrie (Dropdown)
    andro_columns = [f"{andro:02d}/07" for andro in range(1, 32)]
    config_colona = {
        col: st.column_config.SelectboxColumn(options=["None", "Présent", "Absent", "Repos", "Congé"])
        for col in andro_columns
    }
    config_colona["Type contrat"] = st.column_config.SelectboxColumn(options=["CDI", "CDD", "Essai", "Stage"])
    config_colona["CE / Département"] = st.column_config.SelectboxColumn(options=["CE 1", "CE 2", "CE 3", "CE 4"])

    # Fampisehoana ilay tabilao azo ovaina mivantana
    edited_df = st.data_editor(
        df_filtered,
        column_config=config_colona,
        use_container_width=True,
        hide_index=True
    )

    # Bokotra hitahirizana ny fanovana natao teo amin'ny tabilao (ohatra: pointage)
    if st.button("💾 Tehirizo ny pointage / fanovana"):
        # Fanavaozana ny data fototra mampiasa ny index
        st.session_state.df_rh.update(edited_df)
        st.success("Tafatahiry soa aman-tsara ny pointage vaovao!")
