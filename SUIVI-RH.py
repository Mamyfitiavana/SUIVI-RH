import streamlit as st
import pandas as pd

# 1. Configuration ny Pejy Streamlit ho an'ny tabilao lehibe
st.set_page_config(layout="wide", page_title="Rafitra Fitantanana - 2026")

# Kisary famantarana ny asa ao amin'ny Prod
TAG_SAISIE = "✍️"
TAG_COMP = "🔍"

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

# 2. MENU PRINCIPAL LEHIBE EO AMIN'NY SIDEBAR
st.sidebar.title("🎮 Menu lehibe")
pejy_voafidy = st.sidebar.radio(
    "Safidio ny asa tiana hatao:", 
    ["📊 SUIVI RH", "⚙️ SUIVI PROD"]
)

st.sidebar.markdown("---")
st.sidebar.title("🔐 Fidirana (Authentification)")
user_session = st.sidebar.selectbox(
    "Iza no miditra amin'ny site? *",
    ["Admin (Rehetra)", "Responsable CE 1", "Responsable CE 2", "Responsable CE 3", "Responsable CE 4"]
)

# Famaritana ny CE azon'ilay olona jerena sy ovaina mivantana
ce_azo_kitihana = user_session.replace("Responsable ", "").strip() if user_session != "Admin (Rehetra)" else None

# 3. INITIALISATION NY DATA (Session State)
if "df_rh" not in st.session_state:
    columns_rh = ["Matricule", "Nom", "Prénom", "CE / Département", "Date d'embauche", "Type contrat", "Fin contrat", "Solde congé", "NB Jour Absence"] + kalandrie_jolay
    # Ohatra mpiasa vitsivitsy amin'ny CE samihafa ho an'ny RH
    st.session_state.df_rh = pd.DataFrame([
        {"Matricule": "0101", "Nom": "ANDRIA", "Prénom": "Rova", "CE / Département": "CE 1", "Date d'embauche": "2026-01-01", "Type contrat": "CDI", "Fin contrat": "-", "Solde congé": 30, "NB Jour Absence": 0},
        {"Matricule": "0102", "Nom": "RABE", "Prénom": "Koto", "CE / Département": "CE 2", "Date d'embauche": "2026-02-15", "Type contrat": "CDD", "Fin contrat": "2026-12-31", "Solde congé": 15, "NB Jour Absence": 2}
    ], columns=columns_rh)

if "df_prod" not in st.session_state:
    base_columns = ["Matricule", "Nom", "Prénom", "CE / Département", "Total Mensuel (Saisie)", "Total Mensuel (Comp)", "Total Hebdo (Saisie)", "Total Hebdo (Comp)", "Quota Obligatoire", "Status Prime"]
    all_columns_prod = base_columns + kalandrie_jolay
    # Ohatra mpiasa vitsivitsy amin'ny CE samihafa ho an'ny Prod
    mpiasa_p1 = {"Matricule": "627", "Nom": "fanoemzantsoa", "Prénom": "mamy fitiavana", "CE / Département": "CE 1", "Total Mensuel (Saisie)": 20, "Total Mensuel (Comp)": 30, "Total Hebdo (Saisie)": 20, "Total Hebdo (Comp)": 30, "Quota Obligatoire": 150, "Status Prime": "❌ NOK"}
    mpiasa_p2 = {"Matricule": "0621", "Nom": "RAZAFY", "Prénom": "Jean", "CE / Département": "CE 2", "Total Mensuel (Saisie)": 0, "Total Mensuel (Comp)": 0, "Total Hebdo (Saisie)": 0, "Total Hebdo (Comp)": 0, "Quota Obligatoire": 500, "Status Prime": "❌ NOK"}
    
    for col in kalandrie_jolay:
        mpiasa_p1[col] = ""
        mpiasa_p2[col] = ""
    mpiasa_p1["Ven 01"] = f"{TAG_SAISIE}20  |  {TAG_COMP}30"
    st.session_state.df_prod = pd.DataFrame([mpiasa_p1, mpiasa_p2], columns=all_columns_prod)

# ==================================================================
# PEJY 1 : SUIVI RH (VERSION ULTRA-SECURISEE ISAKY NY CE)
# ==================================================================
if pejy_voafidy == "📊 SUIVI RH":
    st.title("📊 Rafitra Fitaovana Suivi RH - Jolay 2026")
    if ce_azo_kitihana:
        st.warning(f"🔒 Fomba fiasa voafetra: Ny mpiasa ao amin'ny **{ce_azo_kitihana}** ihany no azonao jerena sy ovaina.")

    df_rh_all = st.session_state.df_rh
    df_rh_filtered = df_rh_all[df_rh_all["CE / Département"] == ce_azo_kitihana] if ce_azo_kitihana else df_rh_all

    @st.dialog("➕ Ampidiro ny Mpiasa Vaovao (RH)")
    def ampiditra_rh_form():
        with st.form(key="form_rh_secure", clear_on_submit=True):
            mat = st.text_input("Matricule *")
            nom = st.text_input("Nom *")
            prenom = st.text_input("Prénom *")
            ce = st.selectbox("CE / Département", [ce_azo_kitihana] if ce_azo_kitihana else ["CE 1", "CE 2", "CE 3", "CE 4"], disabled=(ce_azo_kitihana is not None))
            submit = st.form_submit_button("Tehirizo ny mpiasa RH", use_container_width=True)
            if submit and mat and nom and prenom:
                vaovao = {"Matricule": mat, "Nom": nom, "Prénom": prenom, "CE / Département": ce, "Date d'embauche": "2026-07-01", "Type contrat": "CDI", "Fin contrat": "-", "Solde congé": 0, "NB Jour Absence": 0}
                for col in kalandrie_jolay: vaovao[col] = None
                st.session_state.df_rh = pd.concat([st.session_state.df_rh, pd.DataFrame([vaovao])], ignore_index=True)
                st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Ajouter mpiasa RH", use_container_width=True, type="primary"): ampiditra_rh_form()
    with col2:
        if user_session == "Admin (Rehetra)" and st.button("🗑️ Reset Tabilao RH", use_container_width=True):
            st.session_state.df_rh = pd.DataFrame(columns=st.session_state.df_rh.columns)
            st.rerun()
            
    st.markdown("---")
    st.subheader(f"📋 Tabilao Fitantanan-draharaha RH ({len(df_rh_filtered)} mpiasa hita)")
    
    # Fampisehoana ilay tabilao RH voasivana ho azy ho an'izay CE miditra
    config_colona_rh = {col: st.column_config.SelectboxColumn(options=["Présent", "Absent", "Repos", "Congé"]) for col in kalandrie_jolay}
    edited_rh = st.data_editor(df_rh_filtered, column_config=config_colona_rh, use_container_width=True, hide_index=True)
    
    if st.button("💾 Tehirizo ny fanovana RH", use_container_width=True):
        st.session_state.df_rh.update(edited_rh)
        st.success("Tafatahiry soa aman-tsara ny fanovana RH!")
        st.rerun()
# ==================================================================
# PEJY 2 : SUIVI PROD (VERSION FIXEE SY AZO ANTOKA 100%)
# ==================================================================
elif pejy_voafidy == "⚙️ SUIVI PROD":
    st.title("⚙️ Rafitra Fitaovana Suivi Production - Jolay 2026")
    if ce_azo_kitihana:
        st.warning(f"🔒 Fomba fiasa voafetra: Ny mpiasa ao amin'ny **{ce_azo_kitihana}** ihany no azonao jerena sy ovaina.")

    df_prod_all = st.session_state.df_prod
    df_prod_filtered = df_prod_all[df_prod_all["CE / Département"] == ce_azo_kitihana] if ce_azo_kitihana else df_prod_all

    # TABS ROA MADIO NY PEJY
    tab1, tab2 = st.tabs(["📋 TABILAO GLOBAL", "📝 AMPIDIRO POINTAGE"])

    # --- TAB 1 : TABILAO GLOBAL ---
    with tab1:
        st.subheader("📋 Tabilao pointage Production Global")
        st.markdown(f"**Toro-marika:** &nbsp;&nbsp;&nbsp;&nbsp; {TAG_SAISIE} = **Saisie** &nbsp;&nbsp;|&nbsp;&nbsp; {TAG_COMP} = **Comparaison**")
        
        @st.dialog("➕ Hampiditra Mpiasa ao amin'ny Prod")
        def ampiditra_prod_form():
            with st.form(key="form_prod_complete_final", clear_on_submit=True):
                mat = st.text_input("Matricule *")
                nom = st.text_input("Nom *")
                prenom = st.text_input("Prénom *")
                quota_init = st.number_input("Quota holatrarina:", min_value=0, value=1000)
                ce = st.selectbox("CE / Département", [ce_azo_kitihana] if ce_azo_kitihana else ["CE 1", "CE 2", "CE 3", "CE 4"], disabled=(ce_azo_kitihana is not None))
                submit = st.form_submit_button("Tehirizo ny mpiasa vaovao", use_container_width=True)
                if submit and mat and nom and prenom:
                    vaovao = {"Matricule": mat, "Nom": nom, "Prénom": prenom, "CE / Département": ce, "Total Mensuel (Saisie)": 0, "Total Mensuel (Comp)": 0, "Total Hebdo (Saisie)": 0, "Total Hebdo (Comp)": 0, "Quota Obligatoire": quota_init, "Status Prime": "❌ NOK"}
                    for col in kalandrie_jolay: vaovao[col] = ""
                    st.session_state.df_prod = pd.concat([st.session_state.df_prod, pd.DataFrame([vaovao])], ignore_index=True)
                    st.rerun()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Ajouter mpiasa Prod vaovao", use_container_width=True, type="primary"): ampiditra_prod_form()
        with col2:
            if user_session == "Admin (Rehetra)" and st.button("🗑️ Reset Tabilao Prod", use_container_width=True):
                st.session_state.df_prod = pd.DataFrame(columns=st.session_state.df_prod.columns)
                st.rerun()

        st.markdown("---")
        st.dataframe(df_prod_filtered, use_container_width=True, hide_index=True)

    # --- TAB 2 : AMPIDIRO POINTAGE (FIAROVANA INDEX FIXEE) ---
    with tab2:
        st.subheader("📝 Fampidirana Pointage Journalier Production")
        st.write("💡 Kitiho ny boribory kely eo ankavian'ny andalana misy mpiasa iray, avy eo tsindrio ilay bokotra lehibe manga mipoitra eo ambany.")
        
        @st.dialog("📝 Fampidirana Pointage")
        def ampiditra_pointage_popup(actual_row_idx, mpiasa_anarana):
            with st.form(key="form_popup_p2_pro_fixed", clear_on_submit=True):
                andro_voafidy = st.selectbox("Safidio ny Andro:", kalandrie_jolay)
                val_saisie = st.number_input("Isa Saisie:", min_value=0, value=0, step=1)
                val_comp = st.number_input("Isa Comparaison:", min_value=0, value=0, step=1)
                quota_change = st.number_input("Quota holatrarina?", min_value=0, value=int(st.session_state.df_prod.at[actual_row_idx, "Quota Obligatoire"]))
                submit_pointage = st.form_submit_button("💾 Tehirizo ity pointage ity", use_container_width=True)
                
                if submit_pointage:
                    st.session_state.df_prod.at[actual_row_idx, andro_voafidy] = f"{TAG_SAISIE}{val_saisie}  |  {TAG_COMP}{val_comp}"
                    st.session_state.df_prod.at[actual_row_idx, "Quota Obligatoire"] = quota_change
                    
                    # RE-CALCUL AUTOMATIQUE
                    total_saisie_mensuel, total_comp_mensuel, total_saisie_hebdo, total_comp_hebdo = 0, 0, 0, 0
                    for c in kalandrie_jolay:
                        cell_value = st.session_state.df_prod.at[actual_row_idx, c]
                        if cell_value and "|" in str(cell_value):
                            try:
                                parts = str(cell_value).split("|")
                                s_val = int(parts[0].replace(TAG_SAISIE, "").strip())
                                c_val = int(parts[1].replace(TAG_COMP, "").strip())
                                total_saisie_mensuel += s_val
                                total_comp_mensuel += c_val
                                laharan_andro = int(''.join(filter(str.isdigit, c)))
                                if laharan_andro <= 7:
                                    total_saisie_hebdo += s_val
                                    total_comp_hebdo += c_val
                            except: pass
                    
                    st.session_state.df_prod.at[actual_row_idx, "Total Mensuel (Saisie)"] = total_saisie_mensuel
                    st.session_state.df_prod.at[actual_row_idx, "Total Mensuel (Comp)"] = total_comp_mensuel
                    st.session_state.df_prod.at[actual_row_idx, "Total Hebdo (Saisie)"] = total_saisie_hebdo
                    st.session_state.df_prod.at[actual_row_idx, "Total Hebdo (Comp)"] = total_comp_hebdo
                    st.session_state.df_prod.at[actual_row_idx, "Status Prime"] = "✅ OK" if total_saisie_mensuel >= quota_change else "❌ NOK"
                    st.success("Tafatahiry sy voakajy soa aman-tsara!")
                    st.rerun()

        # Fampisehoana fohy (Namboarina ny anaran'ny colonnes mba hifanaraka tsara sady tsy misy KeyError)
        df_short_view = df_prod_filtered[["Matricule", "Nom", "Prénom", "CE / Département", "Quota Obligatoire", "Status Prime"]]
        event = st.dataframe(df_short_view, use_container_width=True, hide_index=True, on_select="rerun", selection_mode="single-row")
        
        if event and "rows" in event.selection and event.selection["rows"]:
            idx = event.selection["rows"][0] # Alaina ny laharana voalohany amin'ilay lisitra
            row_data = df_prod_filtered.iloc[idx]
            
            # Karohina ny laharana tena izy ao amin'ny fitahirizana lehibe (df_prod) mampiasa Matricule
            real_idx = st.session_state.df_prod[st.session_state.df_prod['Matricule'] == row_data['Matricule']].index[0]
            
            st.markdown("---")
            if st.button(f"📝 Hanampy Pointage ho an'i {row_data['Nom']} {row_data['Prénom']}", type="primary", use_container_width=True):
                ampiditra_pointage_popup(real_idx, f"{row_data['Nom']} {row_data['Prénom']}")
