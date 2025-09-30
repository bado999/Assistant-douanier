import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.set_page_config(page_title="Assistant Douanier", layout="wide")
    st.title("🛃 Assistant Douanier - Optimisation des Coûts")
    
    # Upload
    st.sidebar.header("📁 Import des données")
    imports_file = st.sidebar.file_uploader("imports.csv", type=['csv'])
    tarifs_file = st.sidebar.file_uploader("tarifs.csv", type=['csv'])
    
    # ===== GUIDE UTILISATEUR =====
    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Conseil démo :** Importez d'abord imports.csv puis tarifs.csv")
    
    if not imports_file:
        st.warning("📁 **Étape 1 :** Importer imports.csv")
    elif not tarifs_file:
        st.warning("📊 **Étape 2 :** Importer tarifs.csv")
    # =============================
    
    if imports_file and tarifs_file:
        # ===== INDICATEUR CHARGEMENT =====
        with st.spinner('Analyse en cours...'):
            imports = pd.read_csv(imports_file)
            tarifs = pd.read_csv(tarifs_file)
            
            df = imports.merge(tarifs, on='Code_HS', how='left')
            df['Droits_Calculés'] = df['Valeur_€'] * df['Droits_%'] / 100
            df['Coût_Total'] = df['Valeur_€'] + df['Droits_Calculés']
        # =================================
        
        # ===== MESSAGE SUCCÈS PROFESSIONNEL =====
        st.success(f"🛃 Analyse terminée : {len(df)} opérations douanières calculées")
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
                    title="Coût total par produit")
        st.plotly_chart(fig)
        
        # TABLEAU RÉCAPITULATIF
        st.subheader("📋 Synthèse par produit")
        recap_produits = df.groupby('Produit').agg({
            'Valeur_€': 'sum',
            'Droits_Calculés': 'sum',
            'Coût_Total': 'sum'
        }).round(2)
        st.dataframe(recap_produits)

if __name__ == "__main__":
    main()
