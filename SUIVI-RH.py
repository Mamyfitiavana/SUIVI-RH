import streamlit as st
import pandas as pd
import numpy as np

# 1. Fanamafisana ny Pejy Streamlit
st.set_page_config(layout="wide", page_title="Suivi RH - Jolay 2026")

st.title("📊 Rafitra Fitaovana Suivi RH - Jolay 2026")

# 2. Famoronana Angon-drakitra Simmulation (Ho an'ny mpiasa 1000)
# Mba tsy ho mavesatra ny fampidinana pejy, mampiasa cache isika
@st.cache_data
def load_initial_data():
    np.random.seed(42)
    isa_mpiasa = 1000
    
    # Miteraka data fototra
    data = {
        "Matricule": [f"MAT-{i:04d}" for i in range(1, isa_mpiasa + 1)],
        "Nom": [f"Nom_{i}" for i in range(1, isa_mpiasa + 1)],
        "Prénom": [f"Prénom_{i}" for i in range(1, isa_mpiasa + 1)],
        "Date d'embauche": pd.date_range(start="2020-01-01", periods=isa_mpiasa, freq="D").strftime("%Y-%m-%d"),
        "Type contrat": np.random.choice(["CDI", "CDD", "Essai", "Stage"], size=isa_mpiasa),
        "Fin contrat": np.random.choice(["-", "2026-12-31", "2027-06-30"], size=isa_mpiasa),
        "CE / Département": np.random.choice(["CE 1", "CE 2", "CE 3", "CE 4"], size=isa_mpiasa),
        "Solde congé": np.random.randint(0, 30, size=isa_mpiasa),
        "NB Jour Absence": np.random.randint(0, 5, size=isa_mpiasa)

    }
    
    # Manampy ny andro 1 hatramin'ny 31 ho an'ny Jolay
    for andro in range(1, 32):
        data[f"{andro:02d}/07"] = "Présent" # Default status ho an'ny andro rehetra
        
    return pd.DataFrame(data)

# Mampiditra ny data ao amin'ny Session State mba ho azo ovaina sy tehirizina
if "df_rh" not in st.session_state:
    st.session_state.df_rh = load_initial_data()

df = st.session_state.df_rh

# 3. Fizarana Pejy: Fitaovana Sivana (Filtre par CE)
st.sidebar.header("🔍 Sivana sy Fikarohana")
lisitra_ce = ["REHETRA"] + list(df["CE / Département"].unique())
ce_voafidy = st.sidebar.selectbox("Safidio ny CE / Département:", lisitra_ce)

# Fikarohana mivantana amin'ny anarana na Matricule
fikarohana = st.sidebar.text_input("Mikaroka mpiasa (Nom/Matricule):")

# Fampiharana ny sivana amin'ny data
df_filtered = df.copy()
if ce_voafidy != "REHETRA":
    df_filtered = df_filtered[df_filtered["CE / Département"] == ce_voafidy]
if fikarohana:
    df_filtered = df_filtered[
        df_filtered["Nom"].str.contains(fikarohana, case=False) | 
        df_filtered["Matricule"].str.contains(fikarohana, case=False)
    ]

# 4. Fampisehoana ny Tabilao Lehibe (Tableau Global & Pointage)
st.subheader(f"📋 Lisitry ny mpiasa ({len(df_filtered)} hita)")
st.write("Azonao ovaina mivantana ny 'Type contrat', 'Solde congé', ary ny andro 01 hatramin'ny 31 ao amin'ny tabilao.")

# Mamorona lisitra hisafidianana amin'ny kalandrie (Dropdown)
andro_columns = [f"{andro:02d}/07" for andro in range(1, 32)]
config_colona = {
    col: st.column_config.SelectboxColumn(options=["Présent", "Absent", "Repos", "Congé"])
    for col in andro_columns
}
config_colona["Type contrat"] = st.column_config.SelectboxColumn(options=["CDI", "CDD", "Essai", "Stage"])

# Fampisehoana ilay tabilao azo ovaina
edited_df = st.data_editor(
    df_filtered,
    column_config=config_colona,
    use_container_width=True,
    hide_index=True
)

# Fanavaozana ny data rafitra rehefa misy ovaina
if st.button("💾 Tehirizo ny fanovana rehetra"):
    st.session_state.df_rh.update(edited_df)
    st.success("Tafatandrina soa aman-tsara ny fanovana nataonao!")
