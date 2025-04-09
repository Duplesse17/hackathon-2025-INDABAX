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

    # Boutons pour basculer entre les collapses
    dbc.Row([
        dbc.Col([
            dbc.Button("Prédire l'éligibilité", id="toggle-predict", color="primary", className="mb-3 me-2"),
            dbc.Button("Ajouter de nouvelles données", id="toggle-add-data", color="secondary", className="mb-3"),
        ], className="text-center")
    ]),

    # Message d'erreur pour l'authentification
    html.Div(id='auth-error', className='text-center mt-4 text-danger fw-bold', style={'fontSize': '18px'}),

    # Collapse pour la prédiction
    dbc.Collapse(
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
        id="collapse-predict",
        is_open=True  # Par défaut, cette section est ouverte
    ),

    # Collapse pour ajouter de nouvelles données
    dbc.Collapse(
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Ajouter de nouvelles données", className="bg-secondary text-white text-center"),
                    dbc.CardBody([
                        dbc.Label("Âge (colonne appelée 'Date de naissance')", className="fw-bold"),
                        dcc.Input(id='new-age', type='number', placeholder='Entrez l\'âge', className='form-control mb-2'),

                        create_dropdown('new-genre', 'Genre', label_encoders['Genre'].classes_),
                        create_dropdown('new-niveau-etude', "Niveau d'étude", label_encoders["Niveau d'etude"].classes_),
                        create_dropdown('new-situation-matrimoniale', "Situation Matrimoniale", label_encoders['Situation Matrimoniale (SM)'].classes_),
                        create_dropdown('new-profession', 'Profession', label_encoders['Profession'].classes_),

                        dbc.Label("Arrondissement de Résidence", className="fw-bold"),
                        dcc.Input(id='new-arrondissement', type='text', placeholder='Entrez l\'arrondissement', className='form-control mb-2'),

                        dbc.Label("Quartier de Résidence", className="fw-bold"),
                        dcc.Input(id='new-quartier', type='text', placeholder='Entrez le quartier', className='form-control mb-2'),

                        create_dropdown('new-nationalite', 'Nationalité', label_encoders['Nationalité'].classes_),
                        create_dropdown('new-religion', 'Religion', label_encoders['Religion'].classes_),

                        create_dropdown('don-sang', "Avez-vous déjà donné le sang ?", label_encoders['A-t-il (elle) déjà donné le sang'].classes_),
                        dbc.Label("Si oui, préciser la date du dernier don", className="fw-bold"),
                        dcc.DatePickerSingle(
                            id='new-date-naissance',
                            date=None,
                            display_format='YYYY-MM-DD',
                            placeholder='Date de dernier don',
                            style={'width': '100%'}
                        ),

                        dbc.Label("Taux d’hémoglobine (g/dl)", className="fw-bold"),
                        dcc.Input(id='new-hemoglobine', type='number', placeholder='Ex: 13.5', className='form-control mb-2'),

                        dbc.Label("Éligibilité au Don", className="fw-bold"),
                        dcc.Dropdown(
                            id="eligibilite-don",
                            options=[
                                {"label": "Éligible", "value": "eligible"},
                                {"label": "Temporairement non éligible", "value": "temporaire"},
                                {"label": "Définitivement non éligible", "value": "definitive"},
                            ],
                            placeholder="Sélectionnez l'éligibilité",
                            className="mb-3"
                        ),

                        # Champs dynamiques pour les raisons
                        html.Div(id="eligibilite-raison-fields"),

                        dbc.Label("Latitude", className="fw-bold"),
                        dcc.Input(id='latitude', type='number', placeholder='Ex: 12.3456', className='form-control mb-2'),

                        dbc.Label("Longitude", className="fw-bold"),
                        dcc.Input(id='longitude', type='number', placeholder='Ex: 45.6789', className='form-control mb-2'),

                        dbc.Button('Enregistrer', id='save-btn', n_clicks=0, color='success', className='mt-3 w-100')
                    ])
                ], className="shadow")
            ], md=12)
        ]),
        id="collapse-add-data",
        is_open=False  # Par défaut, cette section est fermée
    ),

    # Résultats
    dbc.Row([
        dbc.Col([
            html.Div(id='prediction-result', className='text-center mt-4 text-success fw-bold', style={'fontSize': '22px'}),
            html.Div(id='save-result', className='text-center mt-4 text-info fw-bold', style={'fontSize': '22px'})
        ])
    ])
], fluid=True)

# ============================== CALLBACKS ==============================

@dash.callback(
    Output("eligibilite-raison-fields", "children"),
    Input("eligibilite-don", "value"),
    State("new-genre", "value")
)
def update_eligibilite_fields(eligibilite, genre):
    # Raisons d'indisponibilité (temporaire)
    raisons_indisponibilite = html.Div(
        [
            dbc.Label("Raisons d'Indisponibilité (Temporaire)", className="fw-bold"),
            dbc.Checklist(
                options=[
                    {"label": "Est sous anti-biothérapie", "value": "antibiotherapie"},
                    {"label": "Taux d’hémoglobine bas", "value": "hemoglobine-bas"},
                    {"label": "Date de dernier don < 3 mois", "value": "dernier-don"},
                    {"label": "IST récente (Exclu VIH, Hbs, Hcv)", "value": "ist-recente"},
                ],
                id="raison-indisponibilite",
                inline=False,
                className="mb-3"
            ),
            dbc.Label("Autres raisons, préciser", className="fw-bold"),
            dcc.Input(
                id="autres-raisons",
                type="text",
                placeholder="Précisez d'autres raisons",
                className="form-control mb-2"
            )
        ],
        style={"display": "block" if eligibilite == "temporaire" else "none"}
    )

    # Raisons spécifiques aux femmes
    raisons_femmes = html.Div(
        [
            dbc.Label("Raisons d'Indisponibilité Spécifiques aux Femmes", className="fw-bold"),
            dbc.Checklist(
                options=[
                    {"label": "La DDR est mauvaise si <14 jours avant le don", "value": "ddr-mauvais"},
                    {"label": "Allaitement", "value": "allaitement"},
                    {"label": "A accouché ces 6 derniers mois", "value": "accouchement"},
                    {"label": "Interruption de grossesse ces 6 derniers mois", "value": "interruption"},
                    {"label": "Est enceinte", "value": "enceinte"},
                ],
                id="new-raison-indisponibilite-femme",
                inline=False,
                className="mb-3"
            ),
            dbc.Label("Date de Dernières Règles (DDR)", className="fw-bold"),
            dcc.DatePickerSingle(
                id='new-date-ddr',
                date=None,
                display_format='YYYY-MM-DD',
                placeholder='Date de Dernières Règles (DDR)',
                style={'width': '100%'}
            )
        ],
        style={"display": "block" if eligibilite == "temporaire" and genre == "Femme" else "none"}
    )

    # Raisons de non-éligibilité (définitive)
    raisons_non_eligibilite = html.Div(
        [
            dbc.Label("Raisons de Non-Éligibilité (Définitive)", className="fw-bold"),
            dbc.Checklist(
                options=[
                    {"label": "Antécédent de transfusion", "value": "transfusion"},
                    {"label": "Porteur (HIV, Hbs, Hcv)", "value": "porteur"},
                    {"label": "Opéré", "value": "opere"},
                    {"label": "Drépanocytaire", "value": "drepanocytaire"},
                    {"label": "Diabétique", "value": "diabetique"},
                    {"label": "Hypertendu", "value": "hypertendu"},
                    {"label": "Asthmatique", "value": "asthmatique"},
                    {"label": "Cardiaque", "value": "cardiaque"},
                    {"label": "Tatoué", "value": "tatoue"},
                    {"label": "Scarifié", "value": "scarifie"},
                ],
                id="raison-non-eligibilite",
                inline=False,
                className="mb-3"
            )
        ],
        style={"display": "block" if eligibilite == "definitive" else "none"}
    )

    return html.Div([raisons_indisponibilite, raisons_femmes, raisons_non_eligibilite])                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

@dash.callback(
    Output("collapse-predict", "is_open"),
    Output("collapse-add-data", "is_open"),
    Output("auth-error", "children"),  # Affiche un message d'erreur
    Input("toggle-predict", "n_clicks"),
    Input("toggle-add-data", "n_clicks"),
    State("collapse-predict", "is_open"),
    State("collapse-add-data", "is_open"),
    State("auth-status", "data"),  # Vérifie l'état d'authentification
    prevent_initial_call=True
)
def toggle_collapse(n_clicks_predict, n_clicks_add, is_open_predict, is_open_add, auth_status):
    ctx = dash.ctx
    if ctx.triggered_id == "toggle-predict":
        return not is_open_predict, False, ""  # Ouvre la prédiction et ferme l'ajout
    elif ctx.triggered_id == "toggle-add-data":
        if auth_status:  # Vérifie si l'utilisateur est authentifié
            return False, not is_open_add, ""  # Ouvre l'ajout et ferme la prédiction
        else:
            return is_open_predict, is_open_add, "❌ Vous devez être connecté pour ajouter des données."
    return is_open_predict, is_open_add, ""

@dash.callback(
    Output("save-result", "children"),
    Input("save-btn", "n_clicks"),
    State("new-date-naissance", "date"),
    State("new-niveau-etude", "value"),
    State("new-genre", "value"),
    State("new-situation-matrimoniale", "value"),
    State("new-profession", "value"),
    State("new-arrondissement", "value"),
    State("new-quartier", "value"),
    State("new-nationalite", "value"),
    State("new-religion", "value"),
    State("don-sang", "value"),
    State("new-hemoglobine", "value"),
    State("raison-indisponibilite", "value"),  # Raisons générales d'indisponibilité
    State("new-raison-indisponibilite-femme", "value"),  # Raisons spécifiques aux femmes
    State("new-date-ddr", "date"),  # Date de Dernières Règles
    State("raison-non-eligibilite", "value"),  # Raisons de non-éligibilité
    State("autres-raisons", "value"),
    State("latitude", "value"),
    State("longitude", "value"),
    prevent_initial_call=True
)

def save_data(n_clicks, date_naissance, niveau_etude, genre, situation_matrimoniale, profession,
              arrondissement, quartier, nationalite, religion, don_sang, hemoglobine,
              raison_indisponibilite, raison_indisponibilite_femme, date_ddr,
              raison_non_eligibilite, autres_raisons, latitude, longitude):
    if n_clicks > 0:
        # Vérifiez si des champs obligatoires sont manquants
        required_fields = [date_naissance, niveau_etude, genre, situation_matrimoniale, profession,
                           arrondissement, quartier, nationalite, religion, don_sang, hemoglobine]
        if None in required_fields:
            return "❌ Veuillez remplir tous les champs obligatoires."

        # Gérer les valeurs manquantes pour les champs dynamiques
        raison_indisponibilite = ", ".join(raison_indisponibilite) if raison_indisponibilite else None
        raison_indisponibilite_femme = ", ".join(raison_indisponibilite_femme) if raison_indisponibilite_femme else None
        raison_non_eligibilite = ", ".join(raison_non_eligibilite) if raison_non_eligibilite else None

        # Créez un dictionnaire pour les données
        data = {
            "Date de naissance": date_naissance,
            "Niveau d'etude": niveau_etude,
            "Genre": genre,
            "Situation Matrimoniale (SM)": situation_matrimoniale,
            "Profession": profession,
            "Arrondissement de résidence": arrondissement,
            "Quartier de Résidence": quartier,
            "Nationalité": nationalite,
            "Religion": religion,
            "A-t-il (elle) déjà donné le sang": don_sang,
            "Taux d’hémoglobine": hemoglobine,
            "Raison indisponibilité": raison_indisponibilite,
            "Raisons spécifiques aux femmes": raison_indisponibilite_femme,
            "Date de Dernières Règles (DDR)": date_ddr,
            "Raison de non-eligibilité totale": raison_non_eligibilite,
            "Autre raisons, preciser": autres_raisons,
            "Latitude": latitude,
            "Longitude": longitude
        }

        # Convertir en DataFrame
        df = pd.DataFrame([data])

        # Sauvegarder dans un fichier Excel
        file_path = "data/donneurs_geocode_update.xlsx"
        try:
            # Vérifiez si le fichier existe et est valide
            with pd.ExcelWriter(file_path, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
                df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
            return "✅ Données enregistrées avec succès."
        except (FileNotFoundError, ValueError, OSError):
            # Si le fichier n'existe pas ou est corrompu, recréez-le
            wb = Workbook()
            wb.save(file_path)
            df.to_excel(file_path, index=False)
            return "✅ Fichier recréé et données enregistrées avec succès."
        except Exception as e:
            return f"❌ Une erreur s'est produite lors de l'enregistrement : {e}"

    
    

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