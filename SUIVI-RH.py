import streamlit as st
import pandas as pd

# 1. Fanamafisana ny Pejy Streamlit
st.set_page_config(layout="wide", page_title="Rafitra Fitantanana - 2026")

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
        st.session_state.df_rh = pd.DataFrame(columns=columns_rh)
    st.info("Kitiho ny 'SUIVI PROD' eo amin'ny sidebar raha hijery ny tabilao vaovao.")

# ==================================================================
# PEJY 2 : SUIVI PROD (SYSTEM POP-UP VOADIO)
# ==================================================================
elif pejy_voafidy == "⚙️ SUIVI PROD":
    st.title("⚙️ Rafitra Fitaovana Suivi Production - Jolay 2026")
    
    # Famoronana tabilao ho an'ny Prod ao amin'ny Session State
    if "df_prod" not in st.session_state:
        base_columns = ["Matricule", "Nom", "Prénom", "Total Mensuel (Saisie)", "Total Mensuel (Comp)", "Total Hebdo (Saisie)", "Total Hebdo (Comp)"]
        all_columns_prod = base_columns + kalandrie_jolay
        
        # Mpiasa ohatra mifanaraka amin'ny sarinao
        mpiasa_prod_ohatra = {
            "Matricule": "627", "Nom": "fanoemzantsoa", "Prénom": "mamy fitiavana",
            "Total Mensuel (Saisie)": 200, "Total Mensuel (Comp)": 210,
            "Total Hebdo (Saisie)": 200, "Total Hebdo (Comp)": 210
        }
        for col in kalandrie_jolay:
            mpiasa_prod_ohatra[col] = "" # Atomboka banga
            
        mpiasa_prod_ohatra["Mer 01"] = "200 / 210"
        st.session_state.df_prod = pd.DataFrame([mpiasa_prod_ohatra], columns=all_columns_prod)

    df_prod = st.session_state.df_prod

    # POP-UP 1: HAMPIDIRANA MPIASA PROD VAOVAO
    @st.dialog("➕ Hampiditra Mpiasa ao amin'ny Prod")
    def ampiditra_prod_form():
        with st.form(key="form_prod", clear_on_submit=True):
            mat = st.text_input("Matricule *")
            nom = st.text_input("Nom *")
            prenom = st.text_input("Prénom *")
            submit = st.form_submit_button("Tehirizo ny mpiasa")
            if submit and mat and nom and prenom:
                vaovao = {
                    "Matricule": mat, "Nom": nom, "Prénom": prenom,
                    "Total Mensuel (Saisie)": 0, "Total Mensuel (Comp)": 0,
                    "Total Hebdo (Saisie)": 0, "Total Hebdo (Comp)": 0
                }
                for col in kalandrie_jolay: vaovao[col] = ""
                st.session_state.df_prod = pd.concat([st.session_state.df_prod, pd.DataFrame([vaovao])], ignore_index=True)
                st.rerun()

    # POP-UP 2: FORMULAIRE POP-UP (NAMBOARINA NY KAJY)
    @st.dialog("📝 Ampidiro ny Pointage Journalier")
    def ampiditra_pointage_popup(row_idx, mpiasa_anarana):
        st.write(f"Mpiasa: **{mpiasa_anarana}**")
        with st.form(key="form_pointage_day", clear_on_submit=True):
            andro_voafidy = st.selectbox("Safidio ny Andro:", kalandrie_jolay)
            val_saisie = st.number_input("Isa Saisie:", min_value=0, value=0)
            val_comp = st.number_input("Isa Comparaison:", min_value=0, value=0)
            submit_pointage = st.form_submit_button("💾 Tehirizo ity pointage ity", use_container_width=True)
            
            if submit_pointage:
                # 1. Manoratra mivantana ny pointage amin'ny endrika "Saisie / Comp"
                st.session_state.df_prod.loc[row_idx, andro_voafidy] = f"{val_saisie} / {val_comp}"
                
                # 2. FIKAJIANA NY TOTAL REHETRA ISAKY NY ANDALANA
                total_saisie_mensuel = 0
                total_comp_mensuel = 0
                total_saisie_hebdo = 0
                total_comp_hebdo = 0
                
                for c in kalandrie_jolay:
                    cell_value = st.session_state.df_prod.loc[row_idx, c]
                    if cell_value and "/" in str(cell_value):
                        parts = str(cell_value).split("/")
                        try:
                            s_val = int(parts[0].strip())
                            c_val = int(parts[1].strip())
                            
                            # Kajy Mensuel
                            total_saisie_mensuel += s_val
                            total_comp_mensuel += c_val
                            
                            # Kajy Hebdo (Ohatra: Andro 01 hatramin'ny Andro 07 Jolay)
                            # Ny any aoriana dia alaina amin'ny alalan'ny laharan'ilay daty
                            laharan_andro = int(''.join(filter(str.isdigit, c)))
                            if laharan_andro <= 7:
                                total_saisie_hebdo += s_val
                                total_comp_hebdo += c_val
                        except:
                            pass
                
                # Fanavaozana ny tsanganana rehetra momba ny Total
                st.session_state.df_prod.loc[row_idx, "Total Mensuel (Saisie)"] = total_saisie_mensuel
                st.session_state.df_prod.loc[row_idx, "Total Mensuel (Comp)"] = total_comp_mensuel
                st.session_state.df_prod.loc[row_idx, "Total Hebdo (Saisie)"] = total_saisie_hebdo
                st.session_state.df_prod.loc[row_idx, "Total Hebdo (Comp)"] = total_comp_hebdo
                
                st.success("Tafakajy sy voatahiry soa aman-tsara!")
                st.rerun()

    # 3. BOKOTRA SY FITANTANANA
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Ajouter mpiasa Prod", use_container_width=True, type="primary"):
            ampiditra_prod_form()
    with col2:
        if st.button("🗑️ Reset Tabilao Prod", use_container_width=True):
            st.session_state.df_prod = pd.DataFrame(columns=st.session_state.df_prod.columns)
            st.rerun()

    st.markdown("---")
    st.subheader("📋 Tabilao fampidirana sy fikajiana Production")
    st.caption("💡 Toromarika: Kitiho ny sisiny havia amin'ny andalana misy mpiasa iray mba hampidirana ny pointage-ny.")

    # Fampisehoana ny tabilao mampiasa st.dataframe
    event = st.dataframe(
        df_prod,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row"
    )

    # 4. REHEFA MISY ANDALANA VOAFIDY (SELECTION ROW)
    if event and "rows" in event.selection and event.selection["rows"]:
        # Alaina ny laharan'ilay andalana voafidy amin'ny endrika isa tsotra
        selected_row_index = event.selection["rows"][0]
        
        # Alaina ny anaran'ilay mpiasa voafidy
        mpiasa_nom = f"{df_prod.loc[selected_row_index, 'Nom']} {df_prod.loc[selected_row_index, 'Prénom']}"
        
        st.markdown("---")
        # Mipoitra ny bokotra rehefa nifidy andalana ianao
        if st.button(f"📝 Ampiditra Pointage ho an'i {mpiasa_nom}", type="secondary", use_container_width=True):
            ampiditra_pointage_popup(selected_row_index, mpiasa_nom)
