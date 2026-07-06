import streamlit as st
import pandas as pd
import numpy as np

# 1. Fanamafisana ny Pejy Streamlit
st.set_page_config(layout="wide", page_title="Rafitra Fitantanana - 2026")

# Kalandrie Jolay 2026 ho an'ny RH sy Prod
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

# 2. MENU PRINCIPAL
st.sidebar.title("🎮 Menu lehibe")
pejy_voafidy = st.sidebar.radio("Safidio ny asa tiana hatao:", ["📊 SUIVI RH", "⚙️ SUIVI PROD"])

# ==================================================================
# PEJY 1 : SUIVI RH (Mitazona ny teo aloha)
# ==================================================================
if pejy_voafidy == "📊 SUIVI RH":
    st.title("📊 Rafitra Fitaovana Suivi RH - Jolay 2026")
    
    if "df_rh" not in st.session_state:
        columns_rh = ["Matricule", "Nom", "Prénom", "CE / Département", "Date d'embauche", "Type contrat", "Fin contrat", "Solde congé", "NB Jour Absence"] + kalandrie_jolay
        mpiasa_ohatra = {"Matricule": "MAT-0001", "Nom": "RAKOTO", "Prénom": "Jean", "CE / Département": "CE 1", "Date d'embauche": "2026-01-01", "Type contrat": "CDI", "Fin contrat": "-", "Solde congé": 30, "NB Jour Absence": 0}
        for andro in kalandrie_jolay: mpiasa_ohatra[andro] = None
        st.session_state.df_rh = pd.DataFrame([mpiasa_ohatra], columns=columns_rh)

    # (Bokotra sy Formulaire RH mbola ao anatiny...)
    # ... (tsy novaina ny kaody RH teo aloha mba ho fohy ny soratra eto) ...
    st.info("Kitiho ny 'SUIVI PROD' eo amin'ny sidebar raha hijery ny tabilao vaovao.")

# ==================================================================
# PEJY 2 : SUIVI PROD (ILAY VAOVAO NY TORIMARIKA)
# ==================================================================
elif pejy_voafidy == "⚙️ SUIVI PROD":
    st.title("⚙️ Rafitra Fitaovana Suivi Production - Jolay 2026")
    
    # Famoronana lohatenin'ny tsanganana ho an'ny Prod (Saisie sy Comp isan'andro)
    columns_prod_days = []
    for andro in kalandrie_jolay:
        columns_prod_days.append(f"{andro} (Saisie)")
        columns_prod_days.append(f"{andro} (Comp)")

    # Famoronana tabilao banga misy mpiasa ohatra iray avy amin'ny sary Excel
    if "df_prod" not in st.session_state:
        base_columns = ["Matricule", "Nom", "Prénom", "Total Mensuel (Saisie)", "Total Mensuel (Comp)", "Total Hebdo (Saisie)", "Total Hebdo (Comp)"]
        all_columns_prod = base_columns + columns_prod_days
        
        mpiasa_prod_ohatra = {
            "Matricule": "627",
            "Nom": "fanoemzantsoa",
            "Prénom": "mamy fitiavana",
            "Total Mensuel (Saisie)": 200,
            "Total Mensuel (Comp)": 210,
            "Total Hebdo (Saisie)": 200,
            "Total Hebdo (Comp)": 210
        }
        # Atomboka amin'ny 0 ny andro rehetra fa ny andro voalohany fotsy ohatra teo ihany no asiana 200 sy 210
        for col in columns_prod_days:
            mpiasa_prod_ohatra[col] = 0
            
        # Ohatra nampidirina avy amin'ny sarinao (Andro voalohany)
        mpiasa_prod_ohatra[f"{kalandrie_jolay[0]} (Saisie)"] = 200
        mpiasa_prod_ohatra[f"{kalandrie_jolay[0]} (Comp)"] = 210
        
        st.session_state.df_prod = pd.DataFrame([mpiasa_prod_ohatra], columns=all_columns_prod)

    df_prod = st.session_state.df_prod

    # 3. POP-UP HAMPIDIRANA MPIASA PROD VAOVAO
    @st.dialog("➕ Hampiditra Mpiasa ao amin'ny Prod")
    def ampiditra_prod_form():
        with st.form(key="form_prod", clear_on_submit=True):
            mat = st.text_input("Matricule *")
            nom = st.text_input("Nom *")
            prenom = st.text_input("Prénom *")
            submit = st.form_submit_button("Tehirizo", use_container_width=True)
            
            if submit and mat and nom and prenom:
                vaovao = {
                    "Matricule": mat, "Nom": nom, "Prénom": prenom,
                    "Total Mensuel (Saisie)": 0, "Total Mensuel (Comp)": 0,
                    "Total Hebdo (Saisie)": 0, "Total Hebdo (Comp)": 0
                }
                for col in columns_prod_days: vaovao[col] = 0
                st.session_state.df_prod = pd.concat([st.session_state.df_prod, pd.DataFrame([vaovao])], ignore_index=True)
                st.rerun()

    # Bokotra sy Fitaovana eo ambonin'ny tabilao
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Ajouter mpiasa Prod", use_container_width=True, type="primary"):
            ampiditra_prod_form()
    with col2:
        if st.button("🗑️ Reset Tabilao Prod", use_container_width=True):
            st.session_state.df_prod = pd.DataFrame(columns=st.session_state.df_prod.columns)
            st.rerun()

    st.markdown("---")
    st.subheader(f"📋 Tabilao fampidirana sy fikajiana Production ({len(df_prod)} mpiasa)")

    if df_prod.empty:
        st.info("Mbola tsy misy mpiasa ny tabilao Prod.")
    else:
        # Fampisehoana ilay tabilao azo ovaina
        edited_prod_df = st.data_editor(
            df_prod,
            use_container_width=True,
            hide_index=True,
            # Tsy avela hovaina tanana ny Total satria ny system no mikajy azy ho azy avy eo
            disabled=["Total Mensuel (Saisie)", "Total Mensuel (Comp)", "Total Hebdo (Saisie)", "Total Hebdo (Comp)"]
        )

        # 4. KAJY AUTOMATIQUE REHEFA TSINDRINA NY "TEHIRIZO"
        if st.button("💾 Kajio ny Total ary Tehirizo", use_container_width=True):
            # Mitady ny tsanganana rehetra misy "Saisie" sy "Comp" mba hanaovana calcul
            saisie_cols = [c for c in columns_prod_days if "(Saisie)" in c]
            comp_cols = [c for c in columns_prod_days if "(Comp)" in c]
            
            # Kajy ny Total Mensuel ho an'ny andalana tsirairay
            edited_prod_df["Total Mensuel (Saisie)"] = edited_prod_df[saisie_cols].sum(axis=1)
            edited_prod_df["Total Mensuel (Comp)"] = edited_prod_df[comp_cols].sum(axis=1)
            
            # Ohatra fotsiny: ny Total Hebdo dia raisintsika ho an'ny 7 andro voalohany aloha
            edited_prod_df["Total Hebdo (Saisie)"] = edited_prod_df[saisie_cols[:7]].sum(axis=1)
            edited_prod_df["Total Hebdo (Comp)"] = edited_prod_df[comp_cols[:7]].sum(axis=1)
            
            # Tehirizina ao amin'ny system
            st.session_state.df_prod = edited_prod_df
            st.success("Tafakajy sy voatahiry soa aman-tsara ny Total Mensuel sy Hebdomadaire rehetra!")
            st.rerun()
