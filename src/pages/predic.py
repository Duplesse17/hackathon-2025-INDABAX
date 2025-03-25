import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import joblib

# ============================== CONFIGURATION ==============================

dash.register_page(__name__, path='/prediction')

# Charger le modèle et les encodeurs
model = joblib.load("data/eligibility_model.pkl")
label_encoders = joblib.load("data/label_encoders.pkl")
target_encoder = joblib.load("data/target_label_encoder.pkl")

# ============================== LAYOUT ==============================

def create_dropdown(id, label, options):
    return dbc.Row([
        dbc.Label(label, className="fw-bold"),
        dcc.Dropdown(id=id, options=[{'label': val, 'value': val} for val in options], placeholder=f"Sélectionnez {label.lower()}")
    ])

layout = dbc.Container([
    html.H1("Prédiction d'Éligibilité au Don de Sang", className="text-center mt-4 mb-4 text-primary"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Informations Personnelles", className="bg-primary text-white text-center"),
                dbc.CardBody([
                    dbc.Label("Âge", className="fw-bold"),
                    dcc.Input(id='age', type='number', placeholder='Entrez votre âge', className='form-control mb-2'),
                    create_dropdown('genre', 'Genre', label_encoders['Genre'].classes_),
                    create_dropdown('niveau_etude', "Niveau d'étude", label_encoders["Niveau d'etude"].classes_),
                    create_dropdown('situation_matrimoniale', "Situation Matrimoniale", label_encoders['Situation Matrimoniale (SM)'].classes_),
                    create_dropdown('profession', 'Profession', label_encoders['Profession'].classes_),
                ])
            ], className="mb-3 shadow")
        ], md=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Autres Informations", className="bg-primary text-white text-center"),
                dbc.CardBody([
                    create_dropdown('nationalite', 'Nationalité', label_encoders['Nationalité'].classes_),
                    create_dropdown('religion', 'Religion', label_encoders['Religion'].classes_),
                    create_dropdown('don_sang', "Avez-vous déjà donné le sang ?", label_encoders['A-t-il (elle) déjà donné le sang'].classes_),
                    dbc.Label("Taux d’hémoglobine (g/dl)", className="fw-bold mt-2"),
                    dcc.Input(id='hemoglobine', type='number', placeholder='Ex: 13.5', className='form-control'),
                    
                    dbc.Button('Prédire', id='predict-btn', n_clicks=0, color='primary', className='mt-3 w-100')
                ])
            ], className="shadow")
        ], md=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Div(id='prediction-result', className='text-center mt-4 text-success fw-bold', style={'fontSize': '22px'})
        ])
    ])
], fluid=True)

# ============================== CALLBACK ==============================
@dash.callback(
    Output("prediction-result", "children"),
    Input("predict-btn", "n_clicks"),
    State("age", "value"),
    State("genre", "value"),
    State("niveau_etude", "value"),
    State("situation_matrimoniale", "value"),
    State("profession", "value"),
    State("nationalite", "value"),
    State("religion", "value"),
    State("don_sang", "value"),
    State("hemoglobine", "value")
)
def predict(n_clicks, age, genre, niveau_etude, situation_matrimoniale, profession, nationalite, religion, don_sang, hemoglobine):
    if n_clicks > 0 and None not in [age, genre, niveau_etude, situation_matrimoniale, profession, nationalite, religion, don_sang, hemoglobine]:
        features = ['Age', 'Genre', "Niveau d'etude", 'Situation Matrimoniale (SM)',
                    'Profession', 'Nationalité', 'Religion', 'A-t-il (elle) déjà donné le sang',
                    'Taux d’hémoglobine']
        
        input_data = pd.DataFrame(columns=features)
        input_data.loc[0] = [0] * len(features)
        
        input_data["Age"] = age
        input_data["Taux d’hémoglobine"] = hemoglobine
        input_data["Genre"] = label_encoders["Genre"].transform([genre])[0]
        input_data["Niveau d'etude"] = label_encoders["Niveau d'etude"].transform([niveau_etude])[0]
        input_data["Situation Matrimoniale (SM)"] = label_encoders["Situation Matrimoniale (SM)"].transform([situation_matrimoniale])[0]
        input_data["Profession"] = label_encoders["Profession"].transform([profession])[0]
        input_data["Nationalité"] = label_encoders["Nationalité"].transform([nationalite])[0]
        input_data["Religion"] = label_encoders["Religion"].transform([religion])[0]
        input_data["A-t-il (elle) déjà donné le sang"] = label_encoders["A-t-il (elle) déjà donné le sang"].transform([don_sang])[0]

        prediction_encoded = model.predict(input_data)[0]
        prediction_label = target_encoder.inverse_transform([prediction_encoded])[0]
        
        return f"✅ Résultat : {prediction_label}"
    
    return ""