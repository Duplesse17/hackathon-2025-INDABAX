import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/donneurs')

# Styles pour les KPI cards
kpi_card_style = {
    'background': 'linear-gradient(135deg, #FF7E5F, #FEB47B)',  # Dégradé !
    'color': 'white',
    'padding': '10px',
    'border-radius': '15px',
    'box-shadow': '0 4px 8px rgba(0,0,0,0.2)',
    'width': '220px',
    'textAlign': 'center',
    'display': 'flex',
    'flexDirection': 'column',
    'justifyContent': 'center',
    'alignItems': 'center',
    'transition': 'transform 0.2s',
    'cursor': 'pointer'
}

# Lecture des données donneurs
df_donneurs_original = pd.read_excel("data/donneurs_2019_nettoye.xlsx")

# Nettoyage basique
df_donneurs_original['Age'] = pd.to_numeric(df_donneurs_original['Age'], errors='coerce')
df_donneurs_original = df_donneurs_original.dropna(subset=['Age', 'Sexe'])

# Fonction pour filtrer les données
def filter_data(age_range, sexe, groupe_sanguin):
    df = df_donneurs_original.copy()
    df = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]

    if sexe:
        df = df[df['Sexe'].isin(sexe)]

    if groupe_sanguin:
        df = df[df['Groupe Sanguin ABO / Rhesus'].isin(groupe_sanguin)]

    return df

# Layout de l'application
layout = dbc.Container([

    html.Br(),

    html.Div([
        html.H1("🩸 Analyse des Donneurs de Sang 2019", className="text-center mb-4 fw-bold", style={'color': '#2c3e50'}),
        #html.P("Un aperçu statistique sur la population des donneurs", className="text-center text-muted mb-5")
    ]),

    # ========================
    # KPIs (placeholders)
    # ========================
    dbc.Row(id='kpi-cards', justify="center", className="mb-5 gx-4"),

    # ========================
    # FILTRES
    # ========================
        # Première ligne avec Sexe et Groupe Sanguin
    dbc.Row([
        # Filtre Sexe
        dbc.Col([
            html.Label("Filtrer par Sexe :"),
            dcc.Dropdown(
                id='sexe-filter',
                options=[{'label': sexe, 'value': sexe} for sexe in df_donneurs_original['Sexe'].unique()],
                multi=True,
                placeholder="Choisissez le sexe"
            )
        ], md=6),

        # Filtre Groupe Sanguin
        dbc.Col([
            html.Label("Filtrer par Groupe Sanguin :"),
            dcc.Dropdown(
                id='groupe-sanguin-filter',
                options=[{'label': groupe, 'value': groupe} for groupe in df_donneurs_original['Groupe Sanguin ABO / Rhesus'].unique()],
                multi=True,
                placeholder="Choisissez le groupe sanguin"
            )
        ], md=6),
    ], className="mb-4"),  # petite marge en dessous

    # Deuxième ligne avec le filtre Âge seul
    dbc.Row([
        dbc.Col([
            html.Label("Filtrer par Âge :"),
            dcc.RangeSlider(
                id='age-filter',
                min=int(df_donneurs_original['Age'].min()),
                max=int(df_donneurs_original['Age'].max()),
                step=1,
                marks={i: str(i) for i in range(
                    int(df_donneurs_original['Age'].min()),
                    int(df_donneurs_original['Age'].max()) + 1, 10)
                },
                value=[
                    int(df_donneurs_original['Age'].min()),
                    int(df_donneurs_original['Age'].max())
                ]
            )
        ], md=12),  # prend toute la largeur
    ], className="mb-5"),

    # ========================
    # Graphiques (placeholders)
    # ========================
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Répartition des donneurs par sexe", className="card-title text-center"),
                dcc.Graph(id='fig-sexe', config={"displayModeBar": False})
            ])
        ], className="shadow-sm rounded-4"), md=6),
        dbc.Col(
    dbc.Card(
        dbc.CardBody([
            html.Div([
                # Icône en haut pour donner du sens
                html.Div([
                    html.I(className="fas fa-tint", style={
                        'fontSize': '30px',
                        'color': '#3498DB',
                        'marginBottom': '10px'
                    }),
                ], style={'textAlign': 'center'}),

                # Valeur principale
                html.Span(id='pourcentage-sang-total', style={
                    'fontSize': '90px',  # Moins gros pour être plus élégant
                    'fontWeight': '800',
                    'color': '#3498DB',
                    'textShadow': '1px 3px 10px rgba(0,0,0,0.15)',
                    'display': 'block',
                    'marginBottom': '15px',
                    'letterSpacing': '2px'
                }),

                # Sous-titre
                html.H6("Donations Sang Total", style={
                    'fontWeight': '600',
                    'color': '#5f6368',
                    'marginBottom': '8px'
                }),

                # Description additionnelle
                html.Strong("donation de type F en 2019", style={
                    'fontSize': '16px',
                    'color': '#2C3E50',
                    'display': 'block'
                }),
            ], style={'textAlign': 'center'})  # Centrage global
                ]),
                className="shadow rounded-4",  # Shadow plus douce
                style={
                    'backgroundColor': '#ffffff',
                    'border': '1px solid #f0f0f0',
                    'padding': '20px',
                    'transition': '0.3s',
                    'cursor': 'pointer'
                }
            ),
            md=6,
        ),

    ], className="mb-4 gx-4"),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H5("Répartition des groupes sanguins", className="card-title text-center"),
                    dcc.Graph(id='fig-groupe', config={"displayModeBar": False})
                ])
            ], className="shadow-sm rounded-4"), md=6),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Distribution des âges", className="card-title text-center"),
                dcc.Graph(id='fig-age', config={"displayModeBar": False})
            ])
        ], className="shadow-sm rounded-4"), md=6),
    ], className="mb-5 gx-4"),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H5("Répartition des Phénotypes", className="card-title text-center"),
                    dcc.Graph(id='fig-phenotype', config={"displayModeBar": False})
                ])
            ], className="shadow-sm rounded-4"), md=12
        ),
    ], className="mb-5 gx-4")
])

# ========================
# CALLBACKS
# ========================
@dash.callback(
    Output('kpi-cards', 'children'),
    Output('fig-sexe', 'figure'),
    Output('fig-age', 'figure'),
    Output('fig-groupe', 'figure'),
    Output('fig-phenotype', 'figure'),
    Output('pourcentage-sang-total', 'children'),

    Input('age-filter', 'value'),
    Input('sexe-filter', 'value'),
    Input('groupe-sanguin-filter', 'value')
)
def update_dashboard(age_range, sexe, groupe_sanguin):
    df_filtered = filter_data(age_range, sexe, groupe_sanguin)

    # ========================
    # KPIs
    # ========================
    total_donneurs = len(df_filtered)
    nb_hommes = (df_filtered['Sexe'] == 'M').sum()
    nb_femmes = (df_filtered['Sexe'] == 'F').sum()
    age_moyen = df_filtered['Age'].mean() if total_donneurs > 0 else 0
    groupe_dominant = df_filtered['Groupe Sanguin ABO / Rhesus'].mode()[0] if total_donneurs > 0 else "-"
    df_phenotypes = df_filtered['Phenotype'].value_counts().reset_index()
    df_phenotypes.columns = ['Phénotype', 'Nombre']

    df_dons = df_filtered['Type de donation'].value_counts().reset_index()
    df_dons.columns = ['Type de donation', 'Nombre']

    nb_sang_total = df_dons[df_dons['Type de donation'] == 'F']['Nombre'].values[0] if 'F' in df_dons['Type de donation'].values else 0
    pourcentage_sang_total = (nb_sang_total / total_donneurs * 100) if total_donneurs > 0 else 0

    # ========================
    # Graphiques
    # ========================
    fig_sexe = px.pie(
        df_filtered,
        names='Sexe',
        title='Répartition par Sexe',
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.3  # Ajout d'un trou pour un effet "donut"
    )

    # Personnalisation du layout
    fig_sexe.update_layout(
        title_x=0.5,  # Centrer le titre
        title_font=dict(size=20, family="Arial", color="darkblue"),
        paper_bgcolor="white",  # Couleur de fond
        font=dict(family="Arial", size=14)
    )

    # Affichage des valeurs en pourcentage sur le graphique
    fig_sexe.update_traces(
        textinfo='percent+label',
        marker=dict(line=dict(color='white', width=2)) , # Améliorer la lisibilité
        hovertemplate="<b>Sexe :</b> %{label}<br><b>Nombre :</b> %{value}<extra></extra>"
    )

        # Histogramme stylisé de la distribution des âges avec valeurs affichées
    fig_age = px.histogram(
        df_filtered,
        x='Age',
        nbins=20,
        color='Sexe',
        title='Distribution des Âges',
        color_discrete_map={'M': '#3498db', 'F': '#e74c3c'},
        barmode='overlay',
        opacity=0.7,
        text_auto=True  # ✅ Affiche la valeur au-dessus des barres
    )

    # Personnalisation avancée de la mise en page
    fig_age.update_layout(
        title={
            'text': "Distribution des Âges par Sexe",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=24, color='#2C3E50')
        },
        xaxis=dict(
            title="Âge",
            titlefont=dict(size=16, color='#7F8C8D'),
            tickfont=dict(size=14),
            gridcolor='#ECF0F1'
        ),
        yaxis=dict(
            title="Nombre de Personnes",
            titlefont=dict(size=16, color='#7F8C8D'),
            tickfont=dict(size=14),
            gridcolor='#ECF0F1'
        ),
        legend=dict(
            title='Sexe',
            font=dict(size=14),
            orientation='h',
            x=0.5,
            xanchor='center',
            y=1.1
        ),
        bargap=0.2,
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        hovermode='x unified',
        margin=dict(l=50, r=50, t=80, b=50)
    )

    # Personnalisation des barres au survol et des annotations de texte
    fig_age.update_traces(
        customdata=df_filtered[['Sexe']],
        marker_line_width=1,
        marker_line_color='white',
        hovertemplate='<b>Âge</b>: %{x}<br><b>Nombre de Personnes</b>: %{y}<br>}<extra></extra>',
        textfont=dict(color='#2C3E50', size=12),  # Couleur et taille du texte
        textposition='outside'  # Affiche les valeurs au-dessus des barres
    )


    df_groupes = df_filtered['Groupe Sanguin ABO / Rhesus'].value_counts().reset_index()
    df_groupes.columns = ['Groupe Sanguin', 'Nombre']

    # Graphique pour les Groupes Sanguins
    fig_groupe = px.bar(
        df_groupes,
        x='Groupe Sanguin',
        y='Nombre',
        title='Répartition Groupe Sanguin / Rhesus',
        color='Groupe Sanguin',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        text_auto=True  # Affiche directement les valeurs sur les barres
    )

    # Personnalisation du layout
    fig_groupe.update_layout(
        title_x=0.5,  # Centrer le titre
        title_font=dict(size=20, family="Arial", color="darkblue"),
        paper_bgcolor="white",
        plot_bgcolor="rgba(0,0,0,0)",  # Fond transparent
        xaxis_title="Groupe Sanguin",
        yaxis_title="Nombre de personnes",
        font=dict(family="Arial", size=14)
    )

    # Ajout du hover personnalisé
    fig_groupe.update_traces(
        hovertemplate="<b>Groupe Sanguin :</b> %{x}<br><b>Nombre :</b> %{y}<extra></extra>"
    )

    # Graphique pour les Phénotypes
    fig_phenotype = px.bar(
        df_phenotypes,
        x='Phénotype',
        y='Nombre',
        title='Répartition des Phénotypes',
        color='Phénotype',
        color_discrete_sequence=px.colors.qualitative.Prism,
        text_auto=True  # Affiche directement les valeurs sur les barres
    )

    # Personnalisation du layout
    fig_phenotype.update_layout(
        title_x=0.5,  # Centrer le titre
        title_font=dict(size=20, family="Arial", color="darkblue"),
        paper_bgcolor="white",
        plot_bgcolor="rgba(0,0,0,0)",  # Fond transparent
        xaxis_title="Phénotype",
        yaxis_title="Nombre de personnes",
        font=dict(family="Arial", size=14)
    )

    # Ajout du hover personnalisé
    fig_phenotype.update_traces(
        hovertemplate="<b>Phénotype :</b> %{x}<br><b>Nombre :</b> %{y}<extra></extra>"
    )

    # ========================
    # KPI CARDS
    # ========================
    kpi_cards = html.Div([

        html.Div([
            html.I(className="fas fa-users fa-2x", style={'margin-bottom': '10px'}),
            html.H4("Total Donneurs"),
            html.H2(f"{total_donneurs}")
        ], style={**kpi_card_style, 'background': 'linear-gradient(135deg, #43cea2, #185a9d)'}),

        html.Div([
            html.I(className="fas fa-mars fa-2x", style={'margin-bottom': '10px'}),
            html.H4("Hommes"),
            html.H2(f"{nb_hommes}")
        ], style={**kpi_card_style, 'background': 'linear-gradient(135deg, #36D1DC, #5B86E5)'}),

        html.Div([
            html.I(className="fas fa-venus fa-2x", style={'margin-bottom': '10px'}),
            html.H4("Femmes"),
            html.H2(f"{nb_femmes}")
        ], style={**kpi_card_style, 'background': 'linear-gradient(135deg, #FF758C, #FF7EB3)'}),

        html.Div([
            html.I(className="fas fa-birthday-cake fa-2x", style={'margin-bottom': '10px'}),
            html.H4("Âge Moyen"),
            html.H2(f"{age_moyen:.1f} ans")
        ], style={**kpi_card_style, 'background': 'linear-gradient(135deg, #F7971E, #FFD200)'}),

        html.Div([
            html.I(className="fas fa-tint fa-2x", style={'margin-bottom': '10px'}),
            html.H4("Groupe Dominant"),
            html.H2(f"{groupe_dominant}")
        ], style={**kpi_card_style, 'background': 'linear-gradient(135deg, #4A00E0, #8E2DE2)'}),

    ], style={
        'display': 'flex',
        'justify-content': 'center',
        'gap': '20px',
        'flex-wrap': 'wrap',
        'margin': '30px 0'
    })

    return kpi_cards, fig_sexe, fig_age, fig_groupe, fig_phenotype, f"{pourcentage_sang_total:.0f}%"
