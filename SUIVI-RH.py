import streamlit as st
import pandas as pd

# 1. Configuration ny Pejy Streamlit
st.set_page_config(layout="wide", page_title="Rafitra Fitantanana - 2026")

# Kisary famantarana
TAG_SAISIE = "✍️"
TAG_COMP = "🔍"

# Kalandrie Jolay 2026
anaran_andro = ["Mer", "Jeu", "Ven", "Sam", "Dim", "Lun", "Mar"]
kalandrie_jolay = []
for i in range(1, 32):
    index_andro = (i + 1) % 7
    anarana = anaran_andro[index_andro]
    kalandrie_jolay.append(f"{anarana} {i:02d}")

# 2. MENU PRINCIPAL EO AMIN'NY SIDEBAR
st.sidebar.title("🎮 Menu lehibe")
pejy_voafidy = st.sidebar.radio("Safidio ny asa tiana hatao:", ["📊 SUIVI RH", "⚙️ SUIVI PROD"])

st.sidebar.markdown("---")
st.sidebar.title("🔐 Fidirana (Authentification)")
# Eto no isafidianana ny zon'ny olona miditra amin'ny site
user_session = st.sidebar.selectbox(
    "Iza no miditra amin'ny site? *",
    ["Admin (Rehetra)", "Responsable CE 1", "Responsable CE 2", "Responsable CE 3", "Responsable CE 4"]
)

# ------------------------------------------------------------------
# INITIALISATION NY DATA (Session State)
# ------------------------------------------------------------------
if "df_prod" not in st.session_state:
    base_columns = ["Matricule", "Nom", "Prénom", "CE / Département", "Total Mensuel (Saisie)", "Total Mensuel (Comp)", "Total Hebdo (Saisie)", "Total Hebdo (Comp)"]
    all_columns_prod = base_columns + kalandrie_jolay
    
    # Ohatra mpiasa vitsivitsy amin'ny CE samy hafa mba hizahana toetra ilay rafitra fiarovana
    mpiasa_1 = {"Matricule": "627", "Nom": "fanoemzantsoa", "Prénom": "mamy fitiavana", "CE / Département": "CE 1", "Total Mensuel (Saisie)": 0, "Total Mensuel (Comp)": 0, "Total Hebdo (Saisie)": 0, "Total Hebdo (Comp)": 0}
    mpiasa_2 = {"Matricule": "0621", "Nom": "RAZAFY", "Prénom": "Jean", "CE / Département": "CE 1", "Total Mensuel (Saisie)": 0, "Total Mensuel (Comp)": 0, "Total Hebdo (Saisie)": 0, "Total Hebdo (Comp)": 0}
    mpiasa_3 = {"Matricule": "0840", "Nom": "ANDRIA", "Prénom": "Rova", "CE / Département": "CE 2", "Total Mensuel (Saisie)": 0, "Total Mensuel (Comp)": 0, "Total Hebdo (Saisie)": 0, "Total Hebdo (Comp)": 0}
    
    for col in kalandrie_jolay:
        mpiasa_1[col] = ""
        mpiasa_2[col] = ""
        mpiasa_3[col] = ""
        
    st.session_state.df_prod = pd.DataFrame([mpiasa_1, mpiasa_2, mpiasa_3], columns=all_columns_prod)

if "df_rh" not in st.session_state:
    columns_rh = ["Matricule", "Nom", "Prénom", "CE / Département", "Date d'embauche", "Type contrat", "Fin contrat", "Solde congé", "NB Jour Absence"] + kalandrie_jolay
    st.session_state.df_rh = pd.DataFrame(columns=columns_rh)

# ==================================================================
# PEJY 1 : SUIVI RH
# ==================================================================
if pejy_voafidy == "📊 SUIVI RH":
    st.title("📊 Rafitra Fitaovana Suivi RH - Jolay 2026")
    st.info("Kitiho ny 'SUIVI PROD' eo amin'ny sidebar raha hijery ny tabilao vaovao misy fiarovana.")

# ==================================================================
# PEJY 2 : SUIVI PROD (VERSION MISY FIAROVANA NY CE)
# ==================================================================
elif pejy_voafidy == "⚙️ SUIVI PROD":
    st.title("⚙️ Rafitra Fitaovana Suivi Production - Jolay 2026")
    
    df_prod = st.session_state.df_prod

    # DETERMINATION NY CE AZON'ILAY OLONA KITIHANA
    ce_azo_kitihana = None
    if user_session != "Admin (Rehetra)":
        ce_azo_kitihana = user_session.replace("Responsable ", "").strip()
        st.warning(f"🔒 Fomba fiasa voafetra: Ny mpiasa ao amin'ny **{ce_azo_kitihana}** ihany no azonao jerena sy ovaina.")

    # POP-UP 1: HAMPIDIRANA MPIASA PROD VAOVAO
    @st.dialog("➕ Hampiditra Mpiasa ao amin'ny Prod")
    def ampiditra_prod_form():
        with st.form(key="form_prod_secure", clear_on_submit=True):
            mat = st.text_input("Matricule *")
            nom = st.text_input("Nom *")
            prenom = st.text_input("Prénom *")
            # Raha mpiasa tsotra izy dia ny CE misy azy ihany no azony ampidirana mpiasa
            if ce_azo_kitihana:
                ce = st.selectbox("CE / Département", [ce_azo_kitihana], disabled=True)
            else:
                ce = st.selectbox("CE / Département *", ["CE 1", "CE 2", "CE 3", "CE 4"])
                
            submit = st.form_submit_button("Tehirizo ny mpiasa vaovao", use_container_width=True)
            if submit and mat and nom and prenom:
                vaovao = {
                    "Matricule": mat, "Nom": nom, "Prénom": prenom, "CE / Département": ce,
                    "Total Mensuel (Saisie)": 0, "Total Mensuel (Comp)": 0, "Total Hebdo (Saisie)": 0, "Total Hebdo (Comp)": 0
                }
                for col in kalandrie_jolay: vaovao[col] = ""
                st.session_state.df_prod = pd.concat([st.session_state.df_prod, pd.DataFrame([vaovao])], ignore_index=True)
                st.rerun()

    # POP-UP 2: FORMULAIRE POINTAGE (FIAROVANA ULTRA-PRO)
    @st.dialog("📝 Ampidiro ny Pointage Journalier")
    def ampiditra_pointage_popup(row_idx, mpiasa_anarana, mpiasa_ce):
        # LAHURANA FIAROVANA: Hamarinina raha mifanaraka ny CE
        if ce_azo_kitihana and mpiasa_ce != ce_azo_kitihana:
            st.error(f"❌ Tsy manana alalana hanova ny mpiasa ao amin'ny {mpiasa_ce} ianao!")
            return
            
        st.write(f"Mpiasa hovaina: **{mpiasa_anarana}** ({mpiasa_ce})")
        with st.form(key="form_pointage_secure_day", clear_on_submit=True):
            andro_voafidy = st.selectbox("Safidio ny Andro:", kalandrie_jolay)
            val_saisie = st.number_input(f"{TAG_SAISIE} Isa avy amin'ny SAISIE:", min_value=0, value=0, step=1)
            val_comp = st.number_input(f"{TAG_COMP} Isa avy amin'ny COMPARAISON:", min_value=0, value=0, step=1)
            
            st.markdown("---")
            submit_pointage = st.form_submit_button("💾 Tehirizo ato amin'ny tabilao", use_container_width=True)
            
            if submit_pointage:
                st.session_state.df_prod.at[row_idx, andro_voafidy] = f"{TAG_SAISIE}{val_saisie}  |  {TAG_COMP}{val_comp}"
                
                # FIKAJIANA NY TOTAL
                total_saisie_mensuel, total_comp_mensuel, total_saisie_hebdo, total_comp_hebdo = 0, 0, 0, 0
                for c in kalandrie_jolay:
                    cell_value = st.session_state.df_prod.at[row_idx, c]
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
                
                st.session_state.df_prod.at[row_idx, "Total Mensuel (Saisie)"] = total_saisie_mensuel
                st.session_state.df_prod.at[row_idx, "Total Mensuel (Comp)"] = total_comp_mensuel
                st.session_state.df_prod.at[row_idx, "Total Hebdo (Saisie)"] = total_saisie_hebdo
                st.session_state.df_prod.at[row_idx, "Total Hebdo (Comp)"] = total_comp_hebdo
                st.success("Voatahiry soa aman-tsara!")
                st.rerun()

    # FILTER DATA AVY AMIN'NY ZON'ILAY USER
    df_filtered = df_prod.copy()
    if ce_azo_kitihana:
        # Sivanina avy hatrany ny tabilao mba tsy ho hitany ny an'ny hafa
        df_filtered = df_filtered[df_filtered["CE / Département"] == ce_azo_kitihana]

    # BOKOTRA SY FITANTANANA
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Ajouter mpiasa Prod vaovao", use_container_width=True, type="primary"):
            ampiditra_prod_form()
    with col2:
        # Ny Admin ihany no afaka manao Reset ny tabilao iray manontolo
        if user_session == "Admin (Rehetra)":
            if st.button("🗑️ Reset Tabilao Prod (Admin Only)", use_container_width=True):
                st.session_state.df_prod = pd.DataFrame(columns=st.session_state.df_prod.columns)
                st.rerun()
        else:
            st.button("🗑️ Reset Tabilao (Voarara)", use_container_width=True, disabled=True)

    st.markdown("---")
    st.subheader(f"📋 Tabilao pointage Production ({len(df_filtered)} mpiasa hita)")
    st.markdown(f"**Toro-marika:** &nbsp;&nbsp;&nbsp;&nbsp; {TAG_SAISIE} = **Saisie** &nbsp;&nbsp;|&nbsp;&nbsp; {TAG_COMP} = **Comparaison**")

    # Fampisehoana ny tabilao voasivana ho azy
    event = st.dataframe(df_filtered, use_container_width=True, hide_index=True, on_select="rerun", selection_mode="single-row")

    # 4. REHEFA MISY ANDALANA VOAFIDY
    if event and "rows" in event.selection and event.selection["rows"]:
        selected_row_idx = event.selection["rows"]
        
        # Alaina ny angon-drakitra marina mampiasa .iloc avy amin'ilay tabilao voasivana
        row_data = df_filtered.iloc[selected_row_idx]
        mpiasa_nom = f"{row_data['Nom']} {row_data['Prénom']}"
        mpiasa_ce = row_data['CE / Département']
        
        # Pitihina ny laharana tena izy ao amin'ny st.session_state.df_prod mba hanaovana fanovana
        real_idx = df_prod[(df_prod['Matricule'] == row_data['Matricule'])].index[0]
        
        st.markdown("---")
        if st.button(f"📝 Ampiditra Pointage ho an'i {mpiasa_nom} ({mpiasa_ce})", type="secondary", use_container_width=True):
            ampiditra_pointage_popup(real_idx, mpiasa_nom, mpiasa_ce)
