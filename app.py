import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder


# Charger le modèle pré-entraîné
model = joblib.load('xgbr.sav')  

# Titre de l'application
st.title("Prédiction du taux de CO2")

# Charger les données sur lesquelles vous souhaitez effectuer des prédictions
data_model = pd.read_csv('data_model.csv')
carrosserie_options = data_model['Carrosserie'].unique()

# Widget pour sélectionner le type de carrosserie
carrosserie = st.selectbox("Sélectionnez le type de carrosserie du véhicule", carrosserie_options)

# Widgets pour saisir la masse ordma
masse_min, masse_max = st.slider("Sélectionnez la fourchette de masse en ordre de marche",
                                 min_value=int(data_model['masse_ordma_min'].min()),
                                 max_value=int(data_model['masse_ordma_max'].max()),
                                 value=(int(data_model['masse_ordma_min'].mean()),
                                int(data_model['masse_ordma_max'].mean())))

# Bouton pour lancer la prédiction
if st.button("Prédire le taux de CO2"):
    # Création d'un DataFrame pour la prédiction
    input_data = pd.DataFrame({
        'Carrosserie': [carrosserie],
        'masse_ordma_min': [masse_min],
        'masse_ordma_max': [masse_max]
    })

    # Encode la colonne Carrosserie comme une variable catégorique
    le = LabelEncoder()
    input_data['Carrosserie'] = le.fit_transform(input_data['Carrosserie'])
    
    # Prédiction basée sur les entrées de l'utilisateur
    prediction = model.predict(input_data)
    
    # Affichage de la prédiction
    st.write(f"Prédiction du taux de CO2 : {prediction[0]:.2f} g/km")
