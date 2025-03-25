import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/about')

layout = dbc.Container([

    # Titre principal
    dbc.Row(
        dbc.Col(
            html.H1("À Propos de TensorPulse", className="text-center text-info mt-4 mb-4"),
        )
    ),

    # Contexte Hackathon
    dbc.Row([
        dbc.Col([
            html.H4("📌 Contexte", className="text-warning"),
            html.P("""
                Ce projet a été conçu dans le cadre du Hackathon 2025 organisé par IndabaX Cameroon. 
                Cet événement met en lumière l'innovation en Intelligence Artificielle, en stimulant 
                la créativité des jeunes talents africains pour résoudre des problématiques concrètes et 
                d'impact social majeur.
            """, style={"text-align": "justify", "font-size": "16px"})
        ])
    ]),

    # Présentation de l'équipe
    dbc.Row([
        dbc.Col([
            html.H4("👨🏽‍💻 Notre Équipe : TensorPulse", className="text-warning"),
            html.P("""
                TensorPulse est une équipe composée de trois passionnés de data science et d'intelligence artificielle. 
                Ensemble, nous partageons une vision commune : utiliser la donnée pour améliorer la santé publique, 
                avec un focus sur la promotion du don de sang volontaire.
            """, style={"text-align": "justify", "font-size": "16px"}),

            html.Ul([
                html.Li("🔸 Nangmo Feulfack Annick Duplesse - Data Analyst & Dashboard Developer"),
                html.Li("🔸 Meffo Léa - Data Scientist & Machine Learning Engineer"),
                html.Li("🔸 Pavel - Backend Developer & Data Engineer"),
            ], style={"font-size": "16px"})
        ])
    ]),

    # Objectifs du projet
    dbc.Row([
        dbc.Col([
            html.H4("🎯 Objectifs du Projet", className="text-warning"),
            html.P("""
                L’objectif principal est de concevoir un tableau de bord interactif dédié à l’analyse 
                des donneuses de sang. Grâce à ce dashboard, nous visons à :
            """, style={"text-align": "justify", "font-size": "16px"}),

            html.Ul([
                html.Li("Faciliter le suivi des profils de donneuses."),
                html.Li("Optimiser les campagnes de sensibilisation et de collecte de sang."),
                html.Li("Fournir des visualisations claires pour une prise de décision rapide."),
                html.Li("Favoriser l'accès à des statistiques fiables pour les autorités de santé."),
            ], style={"font-size": "16px"})
        ])
    ]),

    # Données utilisées
    dbc.Row([
        dbc.Col([
            html.H4("🗂️ Données utilisées", className="text-warning"),
            html.P("""
                Les données exploitées proviennent d'un fichier CSV contenant des informations sur les donneuses : 
                Sexe, Âge, Type de donation, Groupe Sanguin (ABO / Rhésus), Phénotype,  Taux d’hémoglobine...
            """, style={"text-align": "justify", "font-size": "16px"})
        ])
    ]),

    # Outils & Technologies
    dbc.Row([
        dbc.Col([
            html.H4("🛠️ Outils & Technologies", className="text-warning"),
            html.Ul([
                html.Li("Python 3"),
                html.Li("Dash & Dash Bootstrap Components"),
                html.Li("Plotly pour les visualisations interactives"),
                html.Li("Pandas pour la manipulation de données"),
            ], style={"font-size": "16px"})
        ])
    ]),

    # Résultats et perspectives
    dbc.Row([
        dbc.Col([
            html.H4("🔚 Résultats & Perspectives", className="text-warning"),
            html.P("""
                Ce tableau de bord met en avant une visualisation interactive des données cliniques sur les donneuses de sang.
                Nous envisageons d’intégrer des modules de prédiction afin d’identifier les donneuses à risque faible, 
                ainsi que de nouveaux indicateurs pour soutenir les campagnes de don.
            """, style={"text-align": "justify", "font-size": "16px"})
        ])
    ]),

    # Footer
    dbc.Row(
        dbc.Col(
            html.P("Projet présenté au Hackathon 2025 IndabaX Cameroon par l'équipe TensorPulse.",
                    className="text-center text-muted mt-4 mb-2"),
        )
    )

], fluid=True)
