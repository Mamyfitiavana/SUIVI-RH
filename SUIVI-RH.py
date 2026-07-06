import streamlit as st
import pandas as pd
import io

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
st.sidebar.title("🔐 Zon'ny Mpampiasa (Profil)")
# Ny rehetra dia afaka mijery ny Global fa ny fanovana no voafetra isaky ny CE
user_session = st.sidebar.selectbox(
    "Iza no miditra amin'ny site? *",
    ["RH / Admin (Manova Rehetra)", "Responsable CE 1", "Responsable CE 2", "Responsable CE 3", "Responsable CE 4"]
)

# Famaritana ny CE an'ilay olona miditra mba hiarovana ny fanovana
ce_mpampiasa = user_session.replace("Responsable ", "").strip() if user_session != "RH / Admin (Manova Rehetra)" else "ADMIN"

# 3. INITIALISATION NY DATA (Session State)
if "df_rh" not in st.session_state:
    columns_rh = ["Matricule", "Nom", "Prénom", "CE / Département", "Date d'embauche", "Type contrat", "Fin contrat", "Solde congé", "NB Jour Absence"] + kalandrie_jolay
    st.session_state.df_rh = pd.DataFrame([
        {"Matricule": "0101", "Nom": "ANDRIA", "Prénom": "Rova", "CE / Département": "CE 1", "Date d'embauche": "2026-01-01", "Type contrat": "CDI", "Fin contrat": "-", "Solde congé": 30, "NB Jour Absence": 0},
        {"Matricule": "0102", "Nom": "RABE", "Prénom": "Koto", "CE / Département": "CE 2", "Date d'embauche": "2026-02-15", "Type contrat": "CDD", "Fin contrat": "2026-12-31", "Solde congé": 15, "NB Jour Absence": 2}
    ], columns=columns_rh)

if "df_prod" not in st.session_state:
    base_columns = ["Matricule", "Nom", "Prénom", "CE / Département", "Total Mensuel (Saisie)", "Total Mensuel (Comp)", "Total Hebdo (Saisie)", "Total Hebdo (Comp)", "Quota Obligatoire", "Status Prime"]
    all_columns_prod = base_columns + kalandrie_jolay
    mpiasa_p1 = {"Matricule": "627", "Nom": "fanoemzantsoa", "Prénom": "mamy fitiavana", "CE / Département": "CE 1", "Total Mensuel (Saisie)": 20, "Total Mensuel (Comp)": 30, "Total Hebdo (Saisie)": 20, "Total Hebdo (Comp)": 30, "Quota Obligatoire": 150, "Status Prime": "❌ NOK"}
    mpiasa_p2 = {"Matricule": "0621", "Nom": "RAZAFY", "Prénom": "Jean", "CE / Département": "CE 2", "Total Mensuel (Saisie)": 0, "Total Mensuel (Comp)": 0, "Total Hebdo (Saisie)": 0, "Total Hebdo (Comp)": 0, "Quota Obligatoire": 500, "Status Prime": "❌ NOK"}
    for col in kalandrie_jolay:
        mpiasa_p1[col] = ""
        mpiasa_p2[col] = ""
    mpiasa_p1["Ven 01"] = f"{TAG_SAISIE}20  |  {TAG_COMP}30"
    st.session_state.df_prod = pd.DataFrame([mpiasa_p1, mpiasa_p2], columns=all_columns_prod)

# Fitaovana mpanova data ho Excel
def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

# ==================================================================
# PEJY 1 : SUIVI RH
# ==================================================================
if pejy_voafidy == "📊 SUIVI RH":
    st.title("📊 Rafitra Fitaovana Suivi RH - Jolay 2026")
    st.caption(f"Status: **{user_session}** (Afaka mijery ny mpiasa rehetra)")

    df_rh_all = st.session_state.df_rh

    @st.dialog("➕ Ampidiro ny Mpiasa Vaovao (RH)")
    def ampiditra_rh_form():
        with st.form(key="form_rh_complete", clear_on_submit=True):
            mat = st.text_input("Matricule *")
            nom = st.text_input("Nom *")
            prenom = st.text_input("Prénom *")
            # Raha Responsable CE izy dia ny CE-ny ihany no azony ampidirana mpiasa
            if ce_mpampiasa != "ADMIN":
                ce = st.selectbox("CE / Département", [ce_mpampiasa], disabled=True)
            else:
                ce = st.selectbox("CE / Département *", ["CE 1", "CE 2", "CE 3", "CE 4"])
            submit = st.form_submit_button("Tehirizo ny mpiasa RH", use_container_width=True)
            if submit and mat and nom and prenom:
                vaovao = {"Matricule": mat, "Nom": nom, "Prénom": prenom, "CE / Département": ce, "Date d'embauche": "2026-07-01", "Type contrat": "CDI", "Fin contrat": "-", "Solde congé": 0, "NB Jour Absence": 0}
                for col in kalandrie_jolay: vaovao[col] = None
                st.session_state.df_rh = pd.concat([st.session_state.df_rh, pd.DataFrame([vaovao])], ignore_index=True)
                st.rerun()

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ Ajouter mpiasa RH vaovao", use_container_width=True, type="primary"): ampiditra_rh_form()
    with col2:
        if ce_mpampiasa == "ADMIN" and st.button("🗑️ Reset Tabilao RH (Admin Only)", use_container_width=True):
            st.session_state.df_rh = pd.DataFrame(columns=st.session_state.df_rh.columns)
            st.rerun()
    with col3:
        excel_rh = convert_df_to_excel(df_rh_all)
        st.download_button(label="📥 Télécharger en Excel (RH)", data=excel_rh, file_name="Suivi_RH_Jolay_2026.xlsx", mime="application/vnd.ms-excel", use_container_width=True)
            
    st.markdown("---")
    st.subheader(f"📋 Tabilao Fitantanan-draharaha RH Global ({len(df_rh_all)} mpiasa rehetra)")
    st.info("💡 Fiarovana: Ny olona rehetra dia afaka mijery ny mpiasa rehetra, fa rehefa tsindrina ny bokotra 'Tehirizo ny fanovana RH' eo ambany, dia ny fanovana mpiasa mifanaraka amin'ny CE-nao ihany no heken'ny rafitra.")
    
    config_colona_rh = {col: st.column_config.SelectboxColumn(options=["Présent", "Absent", "Repos", "Congé"]) for col in kalandrie_jolay}
    edited_rh = st.data_editor(df_rh_all, column_config=config_colona_rh, use_container_width=True, hide_index=True)
    
    if st.button("💾 Tehirizo ny fanovana RH", use_container_width=True, type="secondary"):
        # Ny rafitra eto dia manivana mba ho ny andalana an'ny CE-ny ihany no havaozina raha tsy ADMIN izy
        for idx, row in edited_rh.iterrows():
            row_ce = df_rh_all.at[idx, "CE / Département"]
            if ce_mpampiasa == "ADMIN" or row_ce == ce_mpampiasa:
                st.session_state.df_rh.iloc[idx] = edited_rh.iloc[idx]
        st.success("Tafatahiry soa aman-tsara! (Ny fanovana amin'ny CE-nao ihany no nekena)")
        st.rerun()
# ==================================================================
# PEJY 2 : SUIVI PROD (VERSION GLOBALEMENT CONSULTABLE)
# ==================================================================
elif pejy_voafidy == "⚙️ SUIVI PROD":
    st.title("⚙️ Rafitra Fitaovana Suivi Production - Jolay 2026")
    st.caption(f"Status: **{user_session}** (Afaka mijery ny mpiasa rehetra)")

    df_prod_all = st.session_state.df_prod

    # ZARAINA HO TABS ROA MADIO NY PEJY
    tab1, tab2 = st.tabs(["📋 TABILAO GLOBAL (Mijery ny Rehetra)", "📝 AMPIDIRO POINTAGE (Isaky ny CE)"])

    # --- TAB 1 : TABILAO GLOBAL (REHETRA REHETRA DIA AFAKA MIJERY) ---
    with tab1:
        st.subheader("📋 Tabilao pointage Production Global (Ny mpiasa rehetra)")
        st.markdown(f"**Toro-marika:** &nbsp;&nbsp;&nbsp;&nbsp; {TAG_SAISIE} = **Saisie** &nbsp;&nbsp;|&nbsp;&nbsp; {TAG_COMP} = **Comparaison**")
        
        @st.dialog("➕ Hampiditra Mpiasa ao amin'ny Prod")
        def ampiditra_prod_form():
            with st.form(key="form_prod_complete_final_p2", clear_on_submit=True):
                mat = st.text_input("Matricule *")
                nom = st.text_input("Nom *")
                prenom = st.text_input("Prénom *")
                quota_init = st.number_input("Quota holatrarina:", min_value=0, value=1000)
                if ce_mpampiasa != "ADMIN":
                    ce = st.selectbox("CE / Département", [ce_mpampiasa], disabled=True)
                else:
                    ce = st.selectbox("CE / Département *", ["CE 1", "CE 2", "CE 3", "CE 4"])
                submit = st.form_submit_button("Tehirizo ny mpiasa vaovao", use_container_width=True)
                if submit and mat and nom and prenom:
                    vaovao = {"Matricule": mat, "Nom": nom, "Prénom": prenom, "CE / Département": ce, "Total Mensuel (Saisie)": 0, "Total Mensuel (Comp)": 0, "Total Hebdo (Saisie)": 0, "Total Hebdo (Comp)": 0, "Quota Obligatoire": quota_init, "Status Prime": "❌ NOK"}
                    for col in kalandrie_jolay: vaovao[col] = ""
                    st.session_state.df_prod = pd.concat([st.session_state.df_prod, pd.DataFrame([vaovao])], ignore_index=True)
                    st.rerun()

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("➕ Ajouter mpiasa Prod vaovao", use_container_width=True, type="primary"): ampiditra_prod_form()
        with col2:
            if ce_mpampiasa == "ADMIN" and st.button("🗑️ Reset Tabilao Prod (Admin Only)", use_container_width=True):
                st.session_state.df_prod = pd.DataFrame(columns=st.session_state.df_prod.columns)
                st.rerun()
        with col3:
            # Fitaovana mampidina Excel ho an'ny Prod Global
            excel_prod = convert_df_to_excel(df_prod_all)
            st.download_button(label="📥 Télécharger en Excel (Prod)", data=excel_prod, file_name="Suivi_Production_Jolay_2026.xlsx", mime="application/vnd.ms-excel", use_container_width=True)

        st.markdown("---")
        # Eto dia ny mpiasa 1000 manontolo (Global) no mipoitra ho an'ny rehetra jerena
        st.dataframe(df_prod_all, use_container_width=True, hide_index=True)

    # --- TAB 2 : AMPIDIRO POINTAGE (FIAROVANA REHEFA HANAMPY DATA) ---
    with tab2:
        st.subheader("📝 Fampidirana Pointage Journalier Production")
        st.info(f"💡 Fiarovana: Ny mpiasa rehetra no hita eo amin'ny tabilao, saingy ny mpiasa ao amin'ny CE-nao ihany no azonao ampidirana pointage.")
        st.write("Kitiho ny boribory kely eo ankavian'ny andalana misy mpiasa iray mba hampidirana pointage.")
        
        @st.dialog("📝 Fampidirana Pointage")
        def ampiditra_pointage_popup(actual_row_idx, mpiasa_anarana):
            with st.form(key="form_popup_p2_pro_secured_final", clear_on_submit=True):
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

        # Fampisehoana ny tabilao fohy ho an'ny mpiasa rehetra (Global)
        df_short_view = df_prod_all[["Matricule", "Nom", "Prénom", "CE / Département", "Quota Obligatoire", "Status Prime"]]
        event = st.dataframe(df_short_view, use_container_width=True, hide_index=True, on_select="rerun", selection_mode="single-row")
        
        if event and "rows" in event.selection and event.selection["rows"]:
            idx = event.selection["rows"][0] if isinstance(event.selection["rows"], list) else event.selection["rows"]
            row_data = df_prod_all.iloc[idx]
            
            mpiasa_nom = f"{row_data['Nom']} {row_data['Prénom']}"
            row_ce = row_data['CE / Département']
            
            st.markdown("---")
            # HAMARININA NY CONDITION FIAROVANA: Raha tsy mitovy ny CE dia lavina ny fidirana amin'ny Pop-up
            if ce_mpampiasa != "ADMIN" and row_ce != ce_mpampiasa:
                st.error(f"❌ Voarara: Mpiasa ao amin'ny **{row_ce}** ity voafididy ity. Ny mpiasa ao amin'ny **{ce_mpampiasa}** ihany no manana alalana hovainao.")
            else:
                if st.button(f"📝 Hanampy Pointage ho an'i {mpiasa_nom} ({row_ce})", type="primary", use_container_width=True):
                    ampiditra_pointage_popup(idx, mpiasa_nom)
