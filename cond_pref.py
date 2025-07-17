import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import gc

# Affichage du logo local (optionnel)
image = Image.open("logo_saham.png")
st.image(image, width=200)

# Titre de l'application
st.title("Dashboard - Conditions Préférentielles des Clients")

# 1. Chargement sécurisé du fichier
uploaded_file = st.file_uploader("📂 Téléchargez le fichier Excel", type=["xlsx"])

if uploaded_file:
    try:
        # Lecture directe en mémoire (pas d'enregistrement sur disque)
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        # 🔍 Aperçu sécurisé
        st.subheader("📋 Aperçu des données chargées")
        st.dataframe(df)

        # 2. 🎯 Vision Client
        if 'code_client' in df.columns:
            st.subheader("🎯 Vision Client")
            client_id = st.selectbox("Sélectionnez un client", df['code_client'].unique())
            st.dataframe(df[df['code_client'] == client_id])
        else:
            st.warning("⚠️ Colonne 'Client_ID' non trouvée.")

        # 3. 🔄 Vision par Code Opération
        if 'code_operation' in df.columns:
            st.subheader("🔄 Vision par Code Opération")
            op_counts = df['code_operation'].value_counts().reset_index()
            op_counts.columns = ['Code Opération', 'Nombre de Conditions']
            fig_op = px.bar(op_counts, x='Code Opération', y='Nombre de Conditions',
                            title="Répartition par Code Opération")
            st.plotly_chart(fig_op)
        else:
            st.warning("⚠️ Colonne 'Code_Operation' non trouvée.")

        # 4. 🏢 Vision par Agence
        if 'code_agence' in df.columns and 'code_client' in df.columns:
            st.subheader("🏢 Vision par Agence")
            agence_counts = df.groupby('code_agence')['code_client'].nunique().reset_index()
            agence_counts.columns = ['Code Agence', 'Nombre de Clients']
            fig_ag = px.bar(agence_counts, x='Code Agence', y='Nombre de Clients',
                            title="Nombre de Clients par Agence")
            st.plotly_chart(fig_ag)
        else:
            st.warning("⚠️ Colonnes 'Code_Agence' ou 'Client_ID' manquantes.")

        # 5. 🔍 Filtres dynamiques
        st.subheader("🔎 Filtres dynamiques")
        agence_filtre = st.multiselect("Filtrer par agence", options=df['code_agence'].unique() if 'code_agence' in df.columns else [])
        op_filtre = st.multiselect("Filtrer par opération", options=df['code_operation'].unique() if 'code_operation' in df.columns else [])

        df_filtré = df.copy()
        if agence_filtre:
            df_filtré = df_filtré[df_filtré['code_agence'].isin(agence_filtre)]
        if op_filtre:
            df_filtré = df_filtré[df_filtré['code_operation'].isin(op_filtre)]

        st.dataframe(df_filtré)

        # 6. 🔐 Nettoyage mémoire pour sécurité
        del df, df_filtré, op_counts, agence_counts
        gc.collect()

    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
else:
    st.info("Veuillez charger un fichier Excel pour démarrer.")
