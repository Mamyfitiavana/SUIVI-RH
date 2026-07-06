import streamlit as st
import pandas as pd
import io
from datetime import datetime

# 1. Configuration ny Pejy Streamlit ho an'ny tabilao lehibe
st.set_page_config(layout="wide", page_title="Rafitra Fitantanana - 2026")

# Kisary famantarana ny asa ao amin'ny Prod
TAG_SAISIE = "✍️"
TAG_COMP = "🔍"

# Kalandrie Jolay 2026 (NY 1 JOLAY 2026 DIA ALAROBIA = MER)
anaran_andro = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
teny_malagasy = {"Wed": "Mer", "Thu": "Jeu", "Fri": "Ven", "Sat": "Sam", "Sun": "Dim", "Mon": "Lun", "Tue": "Mar"}

kalandrie_jolay = []
alahady_list = []

for i in range(1, 32):
    date_obj = datetime(2026, 7, i)
    andro_eng = date_obj.strftime("%a")
    andro_mg = teny_malagasy[andro_eng]
    
    format_daty = f"{andro_mg} {i:02d}"
    kalandrie_jolay.append(format_daty)
    if andro_mg == "Dim":
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
        with st.form(key="form_rh_v8", clear_on_submit=True):
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
# PEJY 2 : SUIVI PROD (TAPANY FAHAROA)
# ==================================================================
elif pejy_voafidy == "⚙️ SUIVI PROD":
    st.title("⚙️ Rafitra Fitaovana Suivi Production - Jolay 2026")
    st.caption(f"Status: **{user_session}**")

    df_prod_all = st.session_state.df_prod

    tab1, tab2 = st.tabs(["📋 TABILAO GLOBAL (Mijery ny Rehetra)", "📝 INTEGRATION & IMPORTATION EXCEL"])

    # --- TAB 1 : TABILAO GLOBAL ---
    with tab1:
        st.subheader("📋 Tabilao pointage Production Global (Ny mpiasa rehetra)")
        st.markdown(f"**Toro-marika:** &nbsp;&nbsp;&nbsp;&nbsp; {TAG_SAISIE} = **Saisie** &nbsp;&nbsp;|&nbsp;&nbsp; {TAG_COMP} = **Comparaison**")
        
        @st.dialog("➕ Hampiditra Mpiasa ao amin'ny Prod")
        def ampiditra_prod_form():
            with st.form(key="form_prod_p2_v8_complete", clear_on_submit=True):
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
    # --- TAB 2 : GESTION & IMPORTATION EXCEL (VERSION RE-CORRIGEE 100%) ---
    with tab2:
        st.subheader("🚀 Fampidirana Pointage mandeha ho azy amin'ny Excel")
        st.write("Mampidira fichier Excel misy tsanganana `Date du traitement`, `Identifiant`, `Opérations`, ary `Total actes` mba hamenoana ny tabilao ho azy.")
        
        uploaded_file = st.file_uploader("Safidio ilay fichier Excel (.xlsx):", type=["xlsx"])
        
        if uploaded_file is not None:
            if st.button("🚀 LANCER L'IMPORTATION AUTOMATIQUE", use_container_width=True, type="primary"):
                try:
                    df_excel = pd.read_excel(uploaded_file)
                    df_excel.columns = [c.strip() for c in df_excel.columns]
                    
                    count_success = 0
                    
                    for index, row in df_excel.iterrows():
                        matricule_excel = str(row['Identifiant']).strip()
                        raw_date = row['Date du traitement']
                        
                        try:
                            if isinstance(raw_date, str):
                                dt = pd.to_datetime(raw_date.strip())
                            else:
                                dt = pd.to_datetime(raw_date)
                            andro_isa = dt.day
                        except:
                            continue
                        
                        target_col = None
                        for col_kalandrie in kalandrie_jolay:
                            if f" {andro_isa:02d}" in col_kalandrie:
                                target_col = col_kalandrie
                                break
                                
                        if not target_col:
                            continue
                            
                        for idx_state, row_state in st.session_state.df_prod.iterrows():
                            if str(row_state['Matricule']).strip() == matricule_excel:
                                row_ce = row_state['CE / Département']
                                
                                if ce_mpampiasa != "ADMIN" and row_ce != ce_mpampiasa:
                                    continue
                                    
                                current_val = str(st.session_state.df_prod.at[idx_state, target_col]).strip()
                                s_current, c_current = 0, 0
                                
                                if "|" in current_val:
                                    try:
                                        p_parts = current_val.split("|")
                                        s_current = int(p_parts[0].replace(TAG_SAISIE, "").strip())
                                        c_current = int(p_parts[1].replace(TAG_COMP, "").strip())
                                    except: pass
                                    
                                op_type = str(row['Opérations']).strip().lower()
                                
                                try:
                                    act_value = int(float(str(row['Total actes']).strip()))
                                except:
                                    continue
                                    
                                if "saisie" in op_type:
                                    s_current = act_value
                                else:
                                    c_current = act_value
                                    
                                st.session_state.df_prod.at[idx_state, target_col] = f"{TAG_SAISIE}{s_current}  |  {TAG_COMP}{c_current}"
                                count_success += 1
                                
                    # RE-CALCUL AUTOMATIQUE NY TOTAL REHETRA
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
                        
                    st.success(f"🎉 Vita soa aman-tsara! Pointage miisa {count_success} no nampidirina avy amin'ny Excel ary voakajy ho azy ny total.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Misy fahadisoana teo am-pamakiana ilay Excel: {str(e)}.")

        st.markdown("---")
        st.subheader("📋 Pointage tabilao feno")
        
        @st.dialog("📝 Fampidirana Pointage Journalier Manuelle")
        def ampiditra_pointage_popup(actual_row_idx, mpiasa_anarana):
            with st.form(key="form_popup_p2_v8_man_fixed", clear_on_submit=True):
                andro_voafidy = st.selectbox("Safidio ny Andro:", kalandrie_jolay)
                val_saisie = st.number_input("Isa Saisie:", min_value=0, value=0, step=1)
                val_comp = st.number_input("Isa Comparaison:", min_value=0, value=0, step=1)
                quota_change = st.number_input("Quota?", min_value=0, value=int(st.session_state.df_prod.at[actual_row_idx, "Quota Obligatoire"]))
                submit_pointage = st.form_submit_button("💾 Tehirizo", use_container_width=True)
                
                if submit_pointage:
                    st.session_state.df_prod.at[actual_row_idx, andro_voafidy] = f"{TAG_SAISIE}{val_saisie}  |  {TAG_COMP}{val_comp}"
                    st.session_state.df_prod.at[actual_row_idx, "Quota Obligatoire"] = quota_change
                    st.success("Voatahiry!")
                    st.rerun()

        # Fampisehoana ny tabilao feno
        event = st.dataframe(st.session_state.df_prod, use_container_width=True, hide_index=True, on_select="rerun", selection_mode="single-row")
        
        if event and "rows" in event.selection and event.selection["rows"]:
            idx = event.selection["rows"]
            # NAMBOARINA NY EXTRACTION INDEX MBA TSY HISY VALUEERROR INTSONY
            if len(idx) > 0:
                real_idx = idx[0]
                row_data = st.session_state.df_prod.iloc[real_idx]
                row_ce = row_data['CE / Département']
                mpiasa_nom = f"{row_data['Nom']} {row_data['Prénom']}"
                
                st.markdown("---")
                # NY FIAROVANA SY NY CONDITION MATANJAKA:
                if ce_mpampiasa != "ADMIN" and row_ce != ce_mpampiasa:
                    st.error(f"❌ Voarara ny fanovana: Mpiasa ao amin'ny **{row_ce}** i {mpiasa_nom}. Ny mpiasa ao amin'ny **{ce_mpampiasa}** ihany no azonao ampidirana pointage.")
                else:
                    if st.button(f"📝 Hanampy Pointage ho an'i {mpiasa_nom}", type="primary", use_container_width=True):
                        ampiditra_pointage_popup(real_idx, mpiasa_nom)
