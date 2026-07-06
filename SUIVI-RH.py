import streamlit as st
import pandas as pd
import io
from datetime import datetime

# 1. Configuration ny Pejy Streamlit ho an'ny tabilao lehibe
st.set_page_config(layout="wide", page_title="Rafitra Fitantanana - 2026")

# Kisary famantarana ny asa ao amin'ny Prod
TAG_SAISIE = "✍️"
TAG_COMP = "🔍"

# Kalandrie Jolay 2026 (Format ampiasaina amin'ny tabilao lehibe: Mer 01, Jeu 02...)
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
        {"Matricule": "627", "Nom": "fanoemzantsoa", "Prénom": "mamy fitiavana", "CE / Département": "CE 1", "Date d'embauche": "2026-01-01", "Type contrat": "CDI", "Fin contrat": "-", "Solde congé": 30, "NB Jour Absence": 0}
    ], columns=columns_rh)

if "df_prod" not in st.session_state:
    base_columns = ["Matricule", "Nom", "Prénom", "CE / Département", "Total Mensuel (Saisie)", "Total Mensuel (Comp)", "Total Hebdo (Saisie)", "Total Hebdo (Comp)", "Quota Obligatoire", "Status Prime"]
    all_columns_prod = base_columns + kalandrie_jolay
    
    # Atomboka banga mifanaraka amin'ny sary Excel nalendrinao ny mpiasa voalohany
    mpiasa_p1 = {"Matricule": "627", "Nom": "fanoemzantsoa", "Prénom": "mamy fitiavana", "CE / Département": "CE 1", "Total Mensuel (Saisie)": 0, "Total Mensuel (Comp)": 0, "Total Hebdo (Saisie)": 0, "Total Hebdo (Comp)": 0, "Quota Obligatoire": 1000, "Status Prime": "❌ NOK"}
    for col in kalandrie_jolay:
        mpiasa_p1[col] = ""
    st.session_state.df_prod = pd.DataFrame([mpiasa_p1], columns=all_columns_prod)

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
    st.caption(f"Status: **{user_session}**")

    df_rh_all = st.session_state.df_rh

    @st.dialog("➕ Ampidiro ny Mpiasa Vaovao (RH)")
    def ampiditra_rh_form():
        with st.form(key="form_rh_v4", clear_on_submit=True):
            mat = st.text_input("Matricule *")
            nom = st.text_input("Nom *")
            prenom = st.text_input("Prénom *")
            ce = st.selectbox("CE / Département", [ce_mpampiasa] if ce_mpampiasa != "ADMIN" else ["CE 1", "CE 2", "CE 3", "CE 4"], disabled=(ce_mpampiasa != "ADMIN"))
            submit = st.form_submit_button("Tehirizo ny mpiasa RH", use_container_width=True)
            if submit and mat and nom and prenom:
                vaovao = {"Matricule": mat, "Nom": nom, "Prénom": prenom, "CE / Département": ce, "Date d'embauche": "2026-07-01", "Type contrat": "CDI", "Fin contrat": "-", "Solde congé": 0, "NB Jour Absence": 0}
                for col in kalandrie_jolay: vaovao[col] = None
                st.session_state.df_rh = pd.concat([st.session_state.df_rh, pd.DataFrame([vaovao])], ignore_index=True)
                st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Ajouter mpiasa RH vaovao", use_container_width=True, type="primary"): ampiditra_rh_form()
    with col2:
        excel_rh = convert_df_to_excel(df_rh_all)
        st.download_button(label="📥 Télécharger en Excel (RH)", data=excel_rh, file_name="Suivi_RH_Jolay_2026.xlsx", mime="application/vnd.ms-excel", use_container_width=True)
            
    st.markdown("---")
    st.subheader(f"📋 Tabilao Fitantanan-draharaha RH Global ({len(df_rh_all)} mpiasa rehetra)")
    
    config_colona_rh = {col: st.column_config.SelectboxColumn(options=["Présent", "Absent", "Repos", "Congé"]) for col in kalandrie_jolay}
    edited_rh = st.data_editor(df_rh_all, column_config=config_colona_rh, use_container_width=True, hide_index=True)
    
    if st.button("💾 Tehirizo ny fanovana RH", use_container_width=True, type="secondary"):
        for idx, row in edited_rh.iterrows():
            row_ce = df_rh_all.at[idx, "CE / Département"]
            if ce_mpampiasa == "ADMIN" or row_ce == ce_mpampiasa:
                st.session_state.df_rh.iloc[idx] = edited_rh.iloc[idx]
        st.success("Tafatahiry soa aman-tsara ny fanovana!")
        st.rerun()
# ==================================================================
# PEJY 2 : SUIVI PROD (TAPANY FAHAROA - MISY IMPORT EXCEL AUTOMATIQUE)
# ==================================================================
elif pejy_voafidy == "⚙️ SUIVI PROD":
    st.title("⚙️ Rafitra Fitaovana Suivi Production - Jolay 2026")
    st.caption(f"Status: **{user_session}**")

    df_prod_all = st.session_state.df_prod
    df_prod_filtered = df_prod_all[df_prod_all["CE / Département"] == ce_mpampiasa] if ce_mpampiasa != "ADMIN" else df_prod_all

    tab1, tab2 = st.tabs(["📋 TABILAO GLOBAL (Mijery ny Rehetra)", "📝 INTEGRATION & IMPORTATION EXCEL"])

    # --- TAB 1 : TABILAO GLOBAL ---
    with tab1:
        st.subheader("📋 Tabilao pointage Production Global (Ny mpiasa rehetra)")
        st.markdown(f"**Toro-marika:** &nbsp;&nbsp;&nbsp;&nbsp; {TAG_SAISIE} = **Saisie** &nbsp;&nbsp;|&nbsp;&nbsp; {TAG_COMP} = **Comparaison**")
        
        @st.dialog("➕ Hampiditra Mpiasa ao amin'ny Prod")
        def ampiditra_prod_form():
            with st.form(key="form_prod_complete_final_p2_v4", clear_on_submit=True):
                mat = st.text_input("Matricule *")
                nom = st.text_input("Nom *")
                prenom = st.text_input("Prénom *")
                quota_init = st.number_input("Quota holatrarina:", min_value=0, value=1000)
                ce = st.selectbox("CE / Département", [ce_mpampiasa] if ce_mpampiasa != "ADMIN" else ["CE 1", "CE 2", "CE 3", "CE 4"], disabled=(ce_mpampiasa != "ADMIN"))
                submit = st.form_submit_button("Tehirizo ny mpiasa vaovao", use_container_width=True)
                if submit and mat and nom and prenom:
                    vaovao = {"Matricule": mat, "Nom": nom, "Prénom": prenom, "CE / Département": ce, "Total Mensuel (Saisie)": 0, "Total Mensuel (Comp)": 0, "Total Hebdo (Saisie)": 0, "Total Hebdo (Comp)": 0, "Quota Obligatoire": quota_init, "Status Prime": "❌ NOK"}
                    for col in kalandrie_jolay: vaovao[col] = ""
                    st.session_state.df_prod = pd.concat([st.session_state.df_prod, pd.DataFrame([vaovao])], ignore_index=True)
                    st.rerun()

        col_add, col_xlsx = st.columns(2)
        with col_add:
            if st.button("➕ Ajouter mpiasa Prod vaovao", use_container_width=True, type="primary"): ampiditra_prod_form()
        with col_xlsx:
            excel_prod = convert_df_to_excel(df_prod_all)
            st.download_button(label="📥 Télécharger en Excel (Prod)", data=excel_prod, file_name="Suivi_Production_Jolay_2026.xlsx", mime="application/vnd.ms-excel", use_container_width=True)

        st.markdown("---")
        st.dataframe(df_prod_all, use_container_width=True, hide_index=True)
    # --- TAB 2 : GESTION & IMPORTATION EXCEL ---
    with tab2:
        st.subheader("🚀 Fampidirana Pointage mandeha ho azy amin'ny Excel")
        st.write("Mampidira fichier Excel (tahaka ilay amin'ny sary) misy tsanganana `Date du traitement`, `Identifiant`, `Opérations`, ary `Total actes` mba hamenoana ny tabilao ho azy.")
        
        # 1. NY FARITRA MAMPIDITRA RAkitra EXCEL (File Uploader)
        uploaded_file = st.file_uploader("Safidio ilay fichier Excel (.xlsx):", type=["xlsx"])
        
        if uploaded_file is not None:
            if st.button("🚀 LANCER L'IMPORTATION AUTOMATIQUE", use_container_width=True, type="primary"):
                try:
                    # Mamaky an'ilay fichier Excel nampidirina
                    df_excel = pd.read_excel(uploaded_file)
                    
                    # Manadio ny lohatenin'ny tsanganana mba tsy hisy erreur d'espace
                    df_excel.columns = [c.strip() for c in df_excel.columns]
                    
                    count_success = 0
                    
                    # Tetezina ny andalana rehetra ao anatin'ilay Excel nampidirinao
                    for index, row in df_excel.iterrows():
                        # Maka ny Matricule (Identifiant ao anatin'ny Excel)
                        matricule_excel = str(row['Identifiant']).strip()
                        
                        # Maka ny Daty ary fantarina hoe andro faha-firy izy ao amin'ny volana Jolay
                        raw_date = row['Date du traitement']
                        try:
                            # Mamadika ny daty ho endrika dila (Object Date)
                            if isinstance(raw_date, str):
                                dt = datetime.strptime(raw_date.strip(), "%Y-%m-%d")
                            else:
                                dt = pd.to_datetime(raw_date)
                            andro_isa = dt.day # Laharan'ny andro (ohatra: 20)
                        except:
                            continue # Tsy raharahina raha diso daty
                        
                        # Karohina hoe aiza io andro io ao anatin'ilay kalandrie_jolay (ohatra: "Ven 20")
                        target_col = None
                        for col_kalandrie in kalandrie_jolay:
                            if f" {andro_isa:02d}" in col_kalandrie:
                                target_col = col_kalandrie
                                break
                                
                        if not target_col:
                            continue
                            
                        # Karohina ny mpiasa manana an'io Matricule io ao amin'ny st.session_state.df_prod
                        # Ary hamarinina raha manana alalana amin'ilay CE ilay user
                        for idx_state, row_state in st.session_state.df_prod.iterrows():
                            if str(row_state['Matricule']).strip() == matricule_excel:
                                row_ce = row_state['CE / Département']
                                
                                # Fiarovana: raha tsy ADMIN ianao, ny mpiasa ao amin'ny CE-nao ihany no azonao ovaina
                                if ce_mpampiasa != "ADMIN" and row_ce != ce_mpampiasa:
                                    continue
                                    
                                # Alaina ny pointage efa tao amin'ilay case taloha (raha nisy)
                                current_val = str(st.session_state.df_prod.at[idx_state, target_col])
                                s_current, c_current = 0, 0
                                if "|" in current_val:
                                    try:
                                        p_parts = current_val.split("|")
                                        s_current = int(p_parts[0].replace(TAG_SAISIE, "").strip())
                                        c_current = int(p_parts[1].replace(TAG_COMP, "").strip())
                                    except: pass
                                    
                                # Hijerena ny karazana asa (Saisie sa Comparaison) ao amin'ny tsanganana Opérations
                                op_type = str(row['Opérations']).strip().lower()
                                act_value = int(row['Total actes'])
                                
                                if "saisie" in op_type:
                                    s_current = act_value
                                else:
                                    c_current = act_value
                                    
                                # Manoratra ny isa vaovao miaraka amin'ny kisary pro ao anatin'ilay case
                                st.session_state.df_prod.at[idx_state, target_col] = f"{TAG_SAISIE}{s_current}  |  {TAG_COMP}{c_current}"
                                count_success += 1
                                
                    # 2. RE-CALCUL AUTOMATIQUE NY TOTAL REHETRA SY NY PRIME HO AN'NY MPIASA REHETRA
                    for idx_state, row_state in st.session_state.df_prod.iterrows():
                        total_saisie_mensuel, total_comp_mensuel, total_saisie_hebdo, total_comp_hebdo = 0, 0, 0, 0
                        quota = int(row_state["Quota Obligatoire"])
                        
                        for c in kalandrie_jolay:
                            cell_value = st.session_state.df_prod.at[idx_state, c]
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
                                
                        st.session_state.df_prod.at[idx_state, "Total Mensuel (Saisie)"] = total_saisie_mensuel
                        st.session_state.df_prod.at[idx_state, "Total Mensuel (Comp)"] = total_comp_mensuel
                        st.session_state.df_prod.at[idx_state, "Total Hebdo (Saisie)"] = total_saisie_hebdo
                        st.session_state.df_prod.at[idx_state, "Total Hebdo (Comp)"] = total_comp_hebdo
                        st.session_state.df_prod.at[idx_state, "Status Prime"] = "✅ OK" if total_saisie_mensuel >= quota else "❌ NOK"
                        
                    st.success(f"🎉 Vita soa aman-tsara! Pointage miisa {count_success} no nampidirina ary voakajy avokoa ny total rehetra.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Misy fahadisoana teo am-pamakiana ilay Excel: {str(e)}. Hamarino tsara raha misy ny tsanganana `Identifiant`, `Date du traitement`, `Opérations`, ary `Total actes`.")

        st.markdown("---")
        st.subheader("📋 Pointage tabilao feno")
        # Fampisehoana ihany koa ny tabilao feno kalandrie eo ambany mba ho hita avy hatrany ny fiovana
        st.dataframe(df_prod_filtered, use_container_width=True, hide_index=True)
