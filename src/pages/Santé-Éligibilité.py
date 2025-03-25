import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import re 

# ============================== CONFIGURATION ==============================

# Enregistrement de la page
dash.register_page(__name__, path='/sante-eligibilite')

# ============================== DATA LOADING ==============================

# Chargement des données
df = pd.read_excel('data/donneurs_geocode_update.xlsx')

# Prétraitement : Calcul de l'âge à partir de la date de naissance
df['Age'] = df['Date de naissance']

# Fonction pour extraire le contenu des crochets
def extraire_contenu(categorie):
    resultat = re.findall(r'\[(.*?)\]', categorie)
    return resultat[0] if resultat else categorie

# Nettoyage : Remplacer les NaN dans les colonnes de raisons par "Aucun"
raisons_sante_cols = [
    'Raison de non-eligibilité totale  [Antécédent de transfusion]',
    'Raison de non-eligibilité totale  [Porteur(HIV,hbs,hcv)]',
    'Raison de non-eligibilité totale  [Opéré]',
    'Raison de non-eligibilité totale  [Drepanocytaire]',
    'Raison de non-eligibilité totale  [Diabétique]',
    'Raison de non-eligibilité totale  [Hypertendus]',
    'Raison de non-eligibilité totale  [Asthmatiques]',
    'Raison de non-eligibilité totale  [Cardiaque]',
    'Raison de non-eligibilité totale  [Tatoué]',
    'Raison de non-eligibilité totale  [Scarifié]',
]

raisons_femme_cols = [
    'Raison de l’indisponibilité de la femme [La DDR est mauvais si <14 jour avant le don]',
    'Raison de l’indisponibilité de la femme [Allaitement ]',
    'Raison de l’indisponibilité de la femme [A accoucher ces 6 derniers mois  ]',
    'Raison de l’indisponibilité de la femme [Interruption de grossesse  ces 06 derniers mois]',
    'Raison de l’indisponibilité de la femme [est enceinte ]',
]

# Remplacer les NaN par "Aucun"
df[raisons_sante_cols + raisons_femme_cols] = df[raisons_sante_cols + raisons_femme_cols].fillna('Aucun')

# ============================== LAYOUT ==============================

# STYLE POUR CHAQUE GRAPHIQUE
graph_card_style = {
    'width': '48%',
    'marginBottom': '30px',
    'backgroundColor': '#FFFFFF',
    'padding': '10px',
    'borderRadius': '10px',
    'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
}

layout = html.Div([
    html.H2("Tableau de bord - Santé & Éligibilité", style={
        'textAlign': 'center',
        'marginBottom': '30px',
        'color': '#2E86C1',
        'fontWeight': 'bold'
    }),

    # ========== FILTRES EN PLEINE LARGEUR ==========
    html.Div([
    
    # 1ère ligne : Religion - Arrondissement - Sexe
    html.Div([
        html.Div([
            html.Label('Filtrer par Religion :'),
            dcc.Dropdown(
                df['Religion'].dropna().unique(),
                id='religion-filter',
                multi=True
            )
        ], style={'width': '30%', 'display': 'inline-block', 'margin': '10px'}),
        
        html.Div([
            html.Label('Filtrer par Arrondissement :'),
            dcc.Dropdown(
                df['Arrondissement de résidence'].dropna().unique(),
                id='arrondissement-filter',
                multi=True
            )
        ], style={'width': '30%', 'display': 'inline-block', 'margin': '10px'}),
        
        html.Div([
            html.Label('Filtrer par Sexe :'),
            dcc.Dropdown(
                df['Genre'].dropna().unique(),
                id='sexe-filter',
                multi=True
            )
        ], style={'width': '30%', 'display': 'inline-block', 'margin': '10px'})
    ], style={'width': '100%', 'display': 'flex'}),
    
    
    # 2ème ligne : Filtre sur l'âge
    html.Div([
        html.Label("Filtrer par Âge :"),
        dcc.RangeSlider(
            id='age-filter',
            min=int(df['Age'].min()),
            max=int(df['Age'].max()),
            step=1,
            marks={i: str(i) for i in range(
                int(df['Age'].min()),
                int(df['Age'].max()) + 1, 10)
            },
            value=[
                int(df['Age'].min()),
                int(df['Age'].max())
            ]
        )
    ], style={
        'margin': '20px 10px',
        'width': '95%',
        'backgroundColor': '#f9f9f9',
        'padding': '15px',
        'borderRadius': '8px'
    }),
    
    
    # 3ème ligne : Situation matrimoniale - Profession
    html.Div([
        html.Div([
            html.Label('Situation matrimoniale :'),
            dcc.Dropdown(
                df['Situation Matrimoniale (SM)'].dropna().unique(),
                id='sm-filter-femme',
                multi=True,
                placeholder='Choisissez une option'
            )
        ], style={
            'width': '48%',
            'display': 'inline-block',
            'margin': '10px'
        }),
        
        html.Div([
            html.Label('Profession :'),
            dcc.Input(
                id='profession-filter-femme',
                type='text',
                placeholder='Tapez une profession',
                debounce=False,
                style={
                    'width': '100%',
                    'padding': '8px'
                }
            )
        ], style={
            'width': '48%',
            'display': 'inline-block',
            'margin': '10px'
        })
        
    ], style={'width': '100%', 'display': 'flex'})
    
], style={'width': '100%'})
,

    # ========== GRAPHIQUES (2 PAR LIGNE) ==========
    html.Div([
        
        # Graphique 1
        html.Div([
            dcc.Graph(id='eligibilite-pie', style={'height': '400px'})
        ], style=graph_card_style),

        # Graphique 2
        html.Div([
            dcc.Graph(id='raisons-sante-bar', style={'height': '400px'})
        ], style=graph_card_style),

        # Graphique 3
        html.Div([
            dcc.Graph(id='raisons-femmes-bar', style={'height': '400px'})
        ], style=graph_card_style),

        # Graphique 4- Date du dernier don

        html.Div([
            dcc.Graph(id='dernier-don-hist', style={'height': '400px'})
        ], style=graph_card_style),
        # Graphique 5 -
        html.Div([
            dcc.Graph(id='hemoglobine-hist', style={'height': '400px'})
        ], style={
            'width': '100%',
            'marginBottom': '30px',
            'backgroundColor': '#FFFFFF',
            'padding': '10px',
            'borderRadius': '10px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
        }),

    ], style={
        'display': 'flex',
        'flexWrap': 'wrap',
        'justifyContent': 'space-between'
    },)
])




# ============================== CALLBACK ==============================

@dash.callback(
    Output('eligibilite-pie', 'figure'),
    Output('raisons-sante-bar', 'figure'),
    Output('raisons-femmes-bar', 'figure'),
    Output('dernier-don-hist', 'figure'),
    Output('hemoglobine-hist', 'figure'),
    Input('sexe-filter', 'value'),
    Input('age-filter', 'value'),
    Input('religion-filter', 'value'),
    Input('arrondissement-filter', 'value'),
    Input('sm-filter-femme', 'value'),
    Input('profession-filter-femme', 'value')
)
def update_graphs(selected_genres, selected_age, selected_religions,
                  selected_arrondissements, selected_sm, selected_profession):
    
    # =========================
    # Étape 1 : Copier le dataframe
    # =========================
    filtered_df = df.copy()

    # =========================
    # Étape 2 : Filtrage dynamique
    # =========================

    # Filtrer par Sexe
    if selected_genres:
        filtered_df = filtered_df[filtered_df['Genre'].isin(selected_genres)]

    # Filtrer par Âge
    if selected_age:
        filtered_df = filtered_df[
            (filtered_df['Age'] >= selected_age[0]) &
            (filtered_df['Age'] <= selected_age[1])
        ]

    # Filtrer par Religion
    if selected_religions:
        filtered_df = filtered_df[filtered_df['Religion'].isin(selected_religions)]

    # Filtrer par Arrondissement de résidence
    if selected_arrondissements:
        filtered_df = filtered_df[filtered_df['Arrondissement de résidence'].isin(selected_arrondissements)]

    # Filtrer par Situation matrimoniale
    if selected_sm:
        filtered_df = filtered_df[filtered_df['Situation Matrimoniale (SM)'].isin(selected_sm)]

    # Filtrer par Profession (filtre texte)
    if selected_profession:
        # On fait un filtre insensible à la casse, sur si "selected_profession" est inclus dans "Profession"
        filtered_df = filtered_df[
            filtered_df['Profession'].str.contains(selected_profession, case=False, na=False)
        ]

    # ========================
    # Étape 3 : FIGURES
    # ========================

    # === 1. Répartition Éligibilité ===
    if not filtered_df.empty:
        eligibilite_counts = (
            filtered_df['ÉLIGIBILITÉ AU DON.']
            .value_counts()
            .reset_index()
        )
        eligibilite_counts.columns = ['ÉLIGIBILITÉ AU DON.', 'count']

        fig_eligibilite = px.pie(
            eligibilite_counts,
            values='count',
            names='ÉLIGIBILITÉ AU DON.',
            title="Répartition de l'Éligibilité au Don",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
    else:
        fig_eligibilite = px.pie(title="Aucune donnée à afficher")

    # === 2. Raisons de Non-Éligibilité (Santé Générale) ===
    if not filtered_df.empty:
        sante_counts = (
            filtered_df[raisons_sante_cols]
            .apply(lambda x: x[x.isin(['Oui'])].value_counts())  # Comptage des "Oui"
            .sum()
            .reset_index()
            .rename(columns={'index': 'Raison', 0: 'Nombre'})
        )

        sante_counts['Raison'] = sante_counts['Raison'].apply(extraire_contenu)
        sante_counts = sante_counts.sort_values(by='Nombre', ascending=True)
    
        fig_raisons_sante = px.bar(
            sante_counts,
            x='Nombre',
            y='Raison',
            orientation='h',
            title="Raisons d'Inéligibilité (Santé Générale)",
            text_auto=True,
            color='Nombre',
            color_continuous_scale='reds'
        )
        fig_raisons_sante.update_layout(xaxis_tickangle=-45)
    else:
        fig_raisons_sante = px.bar(title="Aucune donnée à afficher")

    # === 3. Raisons d’Indisponibilité chez les Femmes ===
    femmes_df = filtered_df[filtered_df['Genre'] == 'Femme']

    if not femmes_df.empty:
        femmes_counts = (
            femmes_df[raisons_femme_cols]
            .apply(lambda x: x[x.isin(['Oui'])].value_counts())
            .sum()
            .reset_index()
            .rename(columns={'index': 'Raison', 0: 'Nombre'})
        )

        femmes_counts['Raison'] = femmes_counts['Raison'].apply(extraire_contenu)

        fig_raisons_femmes = px.bar(
            femmes_counts,
            x='Nombre',
            y='Raison',
            orientation='h',
            title="Raisons d'Indisponibilité chez les Femmes",
            text_auto=True,
            color='Nombre',
            color_continuous_scale='Oranges'
        )
        fig_raisons_femmes.update_layout(xaxis_tickangle=-45)
    else:
        fig_raisons_femmes = px.bar(title="Aucune donnée à afficher")

    # === 4. Histogramme du Taux d’Hémoglobine ===
    if not filtered_df.empty and 'Taux d’hémoglobine' in filtered_df.columns:
        filtered_df['Taux d’hémoglobine'] = (
            filtered_df['Taux d’hémoglobine'].astype(str)
            .str.replace('g/dl', '', case=False, regex=False)
            .str.replace(' ', '', regex=False)
            .str.replace(',', '.', regex=False)
            .str.replace('123.1','12.1',regex=False)
            .str.replace('111.9','11.9',regex=False)
            .astype(float)
        )

        df_hemoglobine = filtered_df.dropna(subset=['Taux d’hémoglobine'])
        df_counts = df_hemoglobine['Taux d’hémoglobine'].value_counts().reset_index()
        df_counts.columns = ['Taux d’hémoglobine', 'Nombre de personnes']
        df_counts = df_counts.sort_values(by='Taux d’hémoglobine')

        fig_hemoglobine = px.line(
            df_counts,
            x='Taux d’hémoglobine',
            y='Nombre de personnes',
            title="Distribution du Taux d’Hémoglobine",
            markers=True,
            line_shape="spline",
            color_discrete_sequence=['#E74C3C']
        )

        fig_hemoglobine.update_layout(
            title={
                'text': "Distribution du Taux d’Hémoglobine",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=24, color='#2C3E50')
            },
            xaxis=dict(
                title="Taux d’Hémoglobine (g/dL)",
                titlefont=dict(size=16, color='#7F8C8D'),
                tickfont=dict(size=14),
                gridcolor='#ECF0F1',
                zeroline=False
            ),
            yaxis=dict(
                title="Nombre de Personnes",
                titlefont=dict(size=16, color='#7F8C8D'),
                tickfont=dict(size=14),
                gridcolor='#ECF0F1',
                zeroline=False
            ),
            plot_bgcolor='#FFFFFF',
            paper_bgcolor='#FFFFFF',
            hovermode='x unified',
            margin=dict(l=50, r=50, t=80, b=50)
        )

        fig_hemoglobine.update_traces(
            marker=dict(
                size=8,
                color='#E74C3C',
                line=dict(width=2, color='#C0392B')
            ),
            line=dict(width=3),
            hovertemplate='<b>Taux d’Hémoglobine</b>: %{x} g/dL<br><b>Nombre de Personnes</b>: %{y}<extra></extra>'
        )

    else:
        fig_hemoglobine = px.histogram(title="Aucune donnée à afficher")
    
    
    # Convertir en datetime
    filtered_df['Si oui preciser la date du dernier don.'] = pd.to_datetime(
        filtered_df['Si oui preciser la date du dernier don.'], format="%d/%m/%Y",errors='coerce'
    )

    # Extraire uniquement l'année
    filtered_df['Année'] = filtered_df['Si oui preciser la date du dernier don.'].dt.year

    # Grouper par année et compter le nombre de dons
    time_series = (
        filtered_df.groupby('Année')
        .size()
        .reset_index(name='Nombre de dons')
        .sort_values('Année')  # Tri croissant
    )

    # Créer un graphique en courbe
    fig = px.line(
        time_series,
        x='Année',
        y='Nombre de dons',
        title="Évolution des Dernier dons par année",
        labels={'Année': 'Année', 'Nombre de dons': 'Nombre de dons'},
        markers=True,
        color_discrete_sequence=['#2E86C1']
    )

    # Améliorer l'apparence
    fig.update_layout(
        xaxis_title="Année",
        yaxis_title="Nombre de dons",
        hovermode="x",
        plot_bgcolor='rgba(248, 249, 250, 1)',
        paper_bgcolor='rgba(255, 255, 255, 1)',
        font=dict(family="Arial, sans-serif", size=12, color="#2E86C1"),
        xaxis=dict(showgrid=True, gridcolor='rgba(200, 200, 200, 0.5)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(200, 200, 200, 0.5)'),
        margin=dict(l=40, r=40, t=50, b=40),
    )


    return fig_eligibilite, fig_raisons_sante, fig_raisons_femmes, fig,fig_hemoglobine
