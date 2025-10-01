import streamlit as st
import pandas as pd
import plotly.express as px

# Données d'exemple intégrées
SAMPLE_IMPORTS = pd.DataFrame({
    'Produit': ['Composant A', 'Composant B', 'Produit C', 'Composant A', 'Produit D'],
    'Code_HS': ['8542.32', '8471.40', '9018.90', '8471.40', '8542.32'],
    'Pays_Origine': ['Chine', 'Allemagne', 'France', 'Inde', 'USA'],
    'Valeur_€': [10000, 15000, 8000, 12000, 9000],
    'Quantité': [100, 50, 200, 80, 120]
})

SAMPLE_TARIFS = pd.DataFrame({
    'Code_HS': ['8542.32', '8471.40', '9018.90'],
    'Droits_%': [7.0, 8.0, 12.0]
})

def main():
    st.set_page_config(page_title="Assistant Douanier", layout="wide")
    st.title("🛃 Assistant Douanier - Optimisation des Coûts")
    
    # Initialisation de l'état de session
    if 'use_sample_data' not in st.session_state:
        st.session_state.use_sample_data = False
    
    # Upload
    st.sidebar.header("📁 Import des données")
    imports_file = st.sidebar.file_uploader("imports.csv", type=['csv'])
    tarifs_file = st.sidebar.file_uploader("tarifs.csv", type=['csv'])
    
    # ===== GUIDE UTILISATEUR =====
    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Conseil démo :** Importez vos fichiers ou utilisez les données exemple")
    
    # Bouton pour charger les données exemple
    if st.sidebar.button("🎯 Charger les données exemple", type="secondary"):
        st.session_state.use_sample_data = True
        st.rerun()
    
    # Indicateur d'étape
    if not imports_file and not tarifs_file and not st.session_state.use_sample_data:
        st.warning("📁 **Étape 1 :** Importer imports.csv et tarifs.csv OU cliquer sur 'Charger les données exemple'")
    elif st.session_state.use_sample_data:
        st.success("🎯 **Mode démo activé :** Données exemple chargées")
    elif imports_file and not tarifs_file:
        st.warning("📊 **Étape 2 :** Importer tarifs.csv")
    elif tarifs_file and not imports_file:
        st.warning("📁 **Étape 2 :** Importer imports.csv")
    # =============================
    
    # Vérifier si on a des données à traiter
    has_data = (imports_file and tarifs_file) or st.session_state.use_sample_data
    
    if has_data:
        # ===== INDICATEUR CHARGEMENT =====
        with st.spinner('Analyse des données en cours...'):
            if imports_file and tarifs_file:
                # Utiliser les fichiers uploadés
                imports = pd.read_csv(imports_file)
                tarifs = pd.read_csv(tarifs_file)
                data_source = "vos fichiers"
            else:
                # Utiliser les données exemple
                imports = SAMPLE_IMPORTS
                tarifs = SAMPLE_TARIFS
                data_source = "données exemple"
            
            # Fusion et calculs
            df = imports.merge(tarifs, on='Code_HS', how='left')
            df['Droits_Calculés'] = df['Valeur_€'] * df['Droits_%'] / 100
            df['Coût_Total'] = df['Valeur_€'] + df['Droits_Calculés']
        # =================================
        
        # ===== MESSAGE SUCCÈS PROFESSIONNEL =====
        st.success(f"🛃 Analyse terminée : {len(df)} opérations traitées ({data_source})")
        # ========================================
        
        # VISUALISATIONS
        st.subheader("📊 Aperçu des données")
        st.dataframe(df.head())
        
        # MÉTRIQUES
        total_valeur = df['Valeur_€'].sum()
        total_droits = df['Droits_Calculés'].sum()
        total_cout = df['Coût_Total'].sum()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Valeur marchande", f"{total_valeur:,.0f} €")
        col2.metric("Droits de douane", f"{total_droits:,.0f} €")
        col3.metric("Coût total", f"{total_cout:,.0f} €")
        
        # DIAGRAMME EN BARRES
        st.subheader("📈 Répartition par produit")
        fig = px.bar(df.groupby('Produit')['Coût_Total'].sum().reset_index(), 
                    x='Produit', y='Coût_Total',
                    title="Coût total par produit",
                    color='Produit')
        st.plotly_chart(fig)
        
        # TABLEAU RÉCAPITULATIF
        st.subheader("📋 Synthèse par produit")
        recap_produits = df.groupby('Produit').agg({
            'Valeur_€': 'sum',
            'Droits_Calculés': 'sum',
            'Coût_Total': 'sum',
            'Quantité': 'sum'
        }).round(2)
        st.dataframe(recap_produits)
        
        # INFORMATION SUR LES DONNÉES EXEMPLE
        if st.session_state.use_sample_data:
            st.sidebar.markdown("---")
            st.sidebar.info("""
            **📋 Données exemple utilisées :**
            - 5 opérations d'import
            - 3 codes HS différents
            - 5 pays d'origine
            """)
            
            # Bouton pour revenir au mode upload
            if st.sidebar.button("🔄 Revenir au mode upload", type="primary"):
                st.session_state.use_sample_data = False
                st.rerun()

if __name__ == "__main__":
    main()
