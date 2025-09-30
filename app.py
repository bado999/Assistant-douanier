import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.set_page_config(page_title="Assistant Douanier", layout="centered")
    st.title("🛃 Assistant Douanier - Version Démo")
    
    # Upload simple
    st.sidebar.header("📁 Import des données")
    imports_file = st.sidebar.file_uploader("imports.csv", type=['csv'])
    tarifs_file = st.sidebar.file_uploader("tarifs.csv", type=['csv'])
    
    if imports_file and tarifs_file:
        # Chargement basique
        imports = pd.read_csv(imports_file)
        tarifs = pd.read_csv(tarifs_file)
        
        # Merge simple
        df = imports.merge(tarifs, on='Code_HS', how='left')
        
        # Calcul basique
        df['Droits_Calculés'] = df['Valeur_€'] * df['Droits_%'] / 100
        df['Coût_Total'] = df['Valeur_€'] + df['Droits_Calculés']
        
        # Affichage simple
        st.subheader("📊 Aperçu des données")
        st.dataframe(df.head())
        
        st.subheader("💰 Coûts totaux")
        total_valeur = df['Valeur_€'].sum()
        total_droits = df['Droits_Calculés'].sum()
        total_cout = df['Coût_Total'].sum()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Valeur marchande", f"{total_valeur:,.0f} €")
        col2.metric("Droits de douane", f"{total_droits:,.0f} €")
        col3.metric("Coût total", f"{total_cout:,.0f} €")
        
        # Graphique simple
        st.subheader("📈 Répartition par produit")
        fig = px.bar(df.groupby('Produit')['Coût_Total'].sum().reset_index(), 
                    x='Produit', y='Coût_Total')
        st.plotly_chart(fig)
        
    else:
        st.info("ℹ️ Pour commencer, importez les fichiers imports.csv et tarifs.csv")
        st.markdown("""
        **Fichiers nécessaires :**
        - `imports.csv` : Produit, Code_HS, Pays_Origine, Valeur_€, Quantité
        - `tarifs.csv` : Code_HS, Droits_%
        """)

if __name__ == "__main__":
    main()