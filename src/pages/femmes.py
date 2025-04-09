import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path='/femmes')

# =====================
# 🔹 Chargement des données
# =====================
df = pd.read_excel('data/donneurs_geocode_update.xlsx')
# Calcul de l'âge
df['Age'] = df['Date de naissance']

# On filtre directement sur les femmes
df_femmes = df[df['Genre'] == 'Femme'].copy()



# =====================
# 🔹 Styles des KPI
# =====================
kpi_card_style = {
    'background': 'linear-gradient(135deg, #FF7E5F, #FEB47B)',  # Dégradé chaud
    'color': 'white',                       # Texte en blanc
    'padding': '20px',                      # Espace intérieur
    'border-radius': '15px',                # Coins arrondis
    'box-shadow': '0 4px 8px rgba(0,0,0,0.2)',  # Ombre douce
    'width': '70%',                         # Largeur responsive
    'maxWidth': '200px',                    # Limite maximale
    'minWidth': '150px',                    # Limite minimale
    'textAlign': 'center',                  # Texte centré
    'display': 'flex',                      # Flexbox
    'flexDirection': 'column',              # Colonne
    'justifyContent': 'center',             # Centré verticalement
    'alignItems': 'center',                 # Centré horizontalement
    'transition': 'transform 0.3s ease, box-shadow 0.3s ease',  # Transition douce
    'cursor': 'pointer',
}

layout = html.Div([

    html.H2("Analyse des Pottentieles Donneuses de Sang", style={
        'textAlign': 'center',
        'marginBottom': '30px',
        'color': '#2E86C1',
        'fontWeight': 'bold'
    }),

    # =====================
    # 🔹 KPIs
    # =====================
    html.Div([

        html.Div([
            html.I(className="fas fa-users fa-2x", style={'margin-bottom': '10px'}),
            html.H5("Total Femmes"),
            html.H3(id='kpi-total-femmes')
        ], style={**kpi_card_style, 'background': 'linear-gradient(135deg, #FF7E5F, #FEB47B)'}),

        html.Div([
            html.I(className="fas fa-check-circle fa-2x", style={'margin-bottom': '10px'}),
            html.H5("% Éligibles"),
            html.H3(id='kpi-eligibles')
        ], style={**kpi_card_style, 'background': 'linear-gradient(135deg, #36D1DC, #5B86E5)'}),

        html.Div([
            html.I(className="fas fa-birthday-cake fa-2x", style={'margin-bottom': '10px'}),
            html.H4("Âge Moyen"),
            html.H2(id='kpi-age-moyen')
        ], style={**kpi_card_style, 'background': 'linear-gradient(135deg, #43C6AC, #191654)'}),

        html.Div([
            html.I(className="fas fa-tint fa-2x", style={'margin-bottom': '10px'}),
            html.H4("% Déjà Donnée"),
            html.H2(id='kpi-deja-donne')
        ], style={**kpi_card_style, 'background': 'linear-gradient(135deg, #B24592, #F15F79)'}),

        html.Div([
            html.I(className="fas fa-exclamation-triangle fa-2x", style={'margin-bottom': '10px'}),
            html.H4("Raison Dominante:"),
            html.H1(id='kpi-raison-dominante', style={'font-size': '25px'})
        ], style={**kpi_card_style, 'background': 'linear-gradient(135deg, #00C9FF, #92FE9D)'})

    ], style={
        'display': 'flex',
        'justify-content': 'center',
        'gap': '20px',
        'flex-wrap': 'wrap',
        'margin': '30px 0'
    }),

    # =====================
    # 🔹 Filtres
    # =====================
    html.Div([

    html.Div([
        html.Label('Arrondissement :', style={'font-weight': 'bold','color': '#333'}),
        dcc.Dropdown(
            df_femmes['Arrondissement de résidence'].dropna().unique(),
            id='arrondissement-filter-femme',
            multi=True,
            placeholder='Choisissez un ou plusieurs'
        )
    ], style={
        'background': '#f9f9f9',
        'border-radius': '10px',
        'box-shadow': '0 4px 8px rgba(0,0,0,0.1)',
        'padding': '15px',
        'margin': '10px',
        'width': '200px',
        'flex': '1'
    }),

    html.Div([
        html.Label('Niveau d\'étude :', style={'font-weight': 'bold','color': '#333'}),
        dcc.Dropdown(
            df_femmes["Niveau d'etude"].dropna().unique(),
            id='etude-filter-femme',
            multi=True,
            placeholder='Choisissez un ou plusieurs'
        )
    ], style={
        'background': '#f9f9f9',
        'border-radius': '10px',
        'box-shadow': '0 4px 8px rgba(0,0,0,0.1)',
        'padding': '15px',
        'margin': '10px',
        'width': '200px',
        'flex': '1'
    }),

    html.Div([
        html.Label('Situation matrimoniale :', style={'font-weight': 'bold','color': '#333'}),
        dcc.Dropdown(
            df_femmes['Situation Matrimoniale (SM)'].dropna().unique(),
            id='sm-filter-femme',
            multi=True,
            placeholder='Choisissez un ou plusieurs'
        )
    ], style={
        'background': '#f9f9f9',
        'border-radius': '10px',
        'box-shadow': '0 4px 8px rgba(0,0,0,0.1)',
        'padding': '15px',
        'margin': '10px',
        'width': '200px',
        'flex': '1'
    }
    ),
    html.Div([
    html.Label('Profession :', style={'font-weight': 'bold','color': '#333'}),
    dcc.Input(
        id='profession-filter-femme',
        type='text',
        placeholder='Tapez une profession',
        debounce=False,  # déclenche le callback quand l'utilisateur termine sa saisie
        style={
            'width': '100%',
            'padding': '10px',
            'border-radius': '5px',
            'border': '1px solid #ccc' ,
            
        }
    )
    ], style={
        'background': '#f9f9f9',
        'border-radius': '10px',
        'box-shadow': '0 4px 8px rgba(0,0,0,0.1)',
        'padding': '15px',
        'margin': '10px',
        'width': '250px',
        'flex': '1',
        'color': '#333',
    }),


    ], style={
        'display': 'flex',
        'flex-wrap': 'wrap',
        'justify-content': 'center',
        'gap': '20px',
        'margin-bottom': '20px'
    }),
    

    # =====================
    # 🔹 Ligne 2 : Tranche d'âge seule sur une ligne
    # =====================
    html.Div([

        html.Div([
            html.Label('Filtrer par Tranche d\'âge :'),
            dcc.RangeSlider(
                18, 70, step=1, id='age-filter-femme',
                marks={i: str(i) for i in range(18, 71, 5)},
                value=[18, 60]
            )
        ], style={'margin': '20px'}),

    ],
),
    # =====================
    # 🔹 Graphiques
    # =====================
    html.Div([

        html.Div([
            html.H3("Répartition des Donneuses par Tranche d'Âge", style={'textAlign': 'center'}),
            dcc.Graph(id='graph-age-distribution')
        ], style={'flex': '1', 'padding': '20px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'border-radius': '10px'}),

        html.Div([
            html.H3("Répartition par Arrondissement de Résidence", style={'textAlign': 'center'}),
            dcc.Graph(id='graph-arrondissement')
        ], style={'flex': '1', 'padding': '20px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'border-radius': '10px'})

    ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center', 'gap': '20px'}),

    html.Div([
        html.H3("Éligibilité au Don selon la Situation Matrimoniale", style={'textAlign': 'center'}),
        dcc.Graph(id='graph-eligibilite-sm')
    ], style={'padding': '20px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'border-radius': '10px', 'margin-top': '20px'})  

])

# =====================
# 🔹 Callbacks
# =====================
@dash.callback(
    [Output('kpi-total-femmes', 'children'),
        Output('kpi-eligibles', 'children'),
        Output('kpi-age-moyen', 'children'),
        Output('kpi-deja-donne', 'children'),
        Output('kpi-raison-dominante', 'children')],
    [Input('arrondissement-filter-femme', 'value'),
        Input('age-filter-femme', 'value'),
        Input('etude-filter-femme', 'value'),
        Input('sm-filter-femme', 'value'),Input('profession-filter-femme', 'value') ]
)
def update_kpis(arrondissement, age_range, etude, sm , profession):
    dff = df_femmes.copy()

    if arrondissement:
        dff = dff[dff['Arrondissement de résidence'].isin(arrondissement)]
    if etude:
        dff = dff[dff["Niveau d'etude"].isin(etude)]
    if sm:
        dff = dff[dff['Situation Matrimoniale (SM)'].isin(sm)]
    if profession:
        # Ici on filtre si la profession contient la chaîne saisie (insensible à la casse)
        dff = dff[dff['Profession'].str.contains(profession, case=False, na=False)]
    
    dff = dff[(dff['Age'] >= age_range[0]) & (dff['Age'] <= age_range[1])]

    # KPIs
    total_femmes = len(dff)
    
    if total_femmes > 0:
        # Pourcentage de femmes éligibles
        eligibles = dff[dff['ÉLIGIBILITÉ AU DON.'].str.lower() == 'eligible']
        pourcentage_eligibles = round((len(eligibles) / total_femmes) * 100, 1)

        # Âge moyen
        age_moyen = round(dff['Age'].mean(), 1)

        # Pourcentage ayant déjà donné leur sang
        deja_donne = dff[dff['A-t-il (elle) déjà donné le sang'].str.lower() == 'oui']
        pourcentage_deja_donne = round((len(deja_donne) / total_femmes) * 100, 1)

        # Raison dominante d'inéligibilité spécifique aux femmes
        raisons_femmes_cols = [
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
            'Raison de l’indisponibilité de la femme [La DDR est mauvais si <14 jour avant le don]',
            'Raison de l’indisponibilité de la femme [Allaitement ]',
            'Raison de l’indisponibilité de la femme [A accoucher ces 6 derniers mois  ]',
            'Raison de l’indisponibilité de la femme [Interruption de grossesse  ces 06 derniers mois]',
            'Raison de l’indisponibilité de la femme [est enceinte ]'
        ]
        # Compter les occurrences de chaque raison
        raison_counts = {}
        for col in raisons_femmes_cols:
            count = dff[col].str.lower().eq('oui').sum()
            raison_counts[col] = count
        raison_dominante = max(raison_counts, key=raison_counts.get).replace('Raison de l’indisponibilité de la femme', '').replace('Raison de non-eligibilité totale','').strip(' []')

    else:
        pourcentage_eligibles = 0
        age_moyen = 0
        pourcentage_deja_donne = 0
        raison_dominante = "N/A"

    return total_femmes, f"{pourcentage_eligibles} %", f"{age_moyen} ans", f"{pourcentage_deja_donne} %", raison_dominante
@dash.callback(
    [Output('graph-age-distribution', 'figure'),
        Output('graph-arrondissement', 'figure'),
        Output('graph-eligibilite-sm', 'figure')],
    [Input('arrondissement-filter-femme', 'value'),
        Input('age-filter-femme', 'value'),
        Input('etude-filter-femme', 'value'),
        Input('sm-filter-femme', 'value'),
        Input('profession-filter-femme', 'value')]
)
def update_graphs(arrondissement, age_range, etude, sm, profession):
    dff = df_femmes.copy()

    if arrondissement:
        dff = dff[dff['Arrondissement de résidence'].isin(arrondissement)]
    if etude:
        dff = dff[dff["Niveau d'etude"].isin(etude)]
    if sm:
        dff = dff[dff['Situation Matrimoniale (SM)'].isin(sm)]
    if profession:
        dff = dff[dff['Profession'].str.contains(profession, case=False, na=False)]

    dff = dff[(dff['Age'] >= age_range[0]) & (dff['Age'] <= age_range[1])]

    # Graphique de distribution des âges
    fig_age = px.histogram(
        dff,
        x='Age',
        nbins=10,
        title='Distribution des âges',
        color_discrete_sequence=['#FF7E5F'],
        text_auto=True  # Affiche les valeurs sur les barres
    )

    # Personnalisation du layout
    fig_age.update_layout(
        title_x=0.5,  # Centrer le titre
        title_font=dict(size=20, family="Arial", color="darkblue"),
        paper_bgcolor="white",
        plot_bgcolor="rgba(0,0,0,0)",  # Fond transparent
        xaxis_title="Âge",
        yaxis_title="Nombre de personnes",
        font=dict(family="Arial", size=14),
        bargap=0.1  # Espacement entre les barres
    )

    # Ajout du hover personnalisé
    fig_age.update_traces(
        hovertemplate="<b>Âge :</b> %{x}<br><b>Nombre :</b> %{y}<extra></extra>",
        marker=dict(line=dict(color='black', width=1))  # Bordures pour améliorer la lisibilité
    )
    # Amélioration de l'apparence générale
    fig_age.update_layout(
        bargap=0.2,
        xaxis_title='Âge',
        yaxis_title='Nombre de donneuses',
        title={
            'text': '📊 Distribution des âges',
            'x': 0.5,
            'xanchor': 'center',
            'font': dict(size=22, color='#2C3E50')
        },
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        font=dict(size=14, color='#2C3E50'),
        xaxis=dict(
            showgrid=True,
            gridcolor='#F0F0F0',
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#F0F0F0',
            zeroline=False
        )
    )

    # Personnalisation des barres et du texte au survol
    fig_age.update_traces(
        marker_line_width=1.5,
        marker_line_color='white',
        hovertemplate='<b>Âge</b>: %{x}<br><b>Nombre de donneuses</b>: %{y}<extra></extra>',
        textfont=dict(color='#2C3E50', size=12)
    )

    # Graphique 2 : Répartition par arrondissement
    fig_arr = px.bar(
        dff['Arrondissement de résidence'].value_counts().reset_index(),
        x="Arrondissement de résidence", y="count",
        labels={'index': 'Arrondissement', 'Arrondissement de résidence': 'Nombre de donneuses'},
        title="Nombre de donneuses par arrondissement",
        color_discrete_sequence=['#36D1DC']
    )
    fig_arr.update_layout(
        title_x=0.5,  # Centrer le titre
        title_font=dict(size=20, family="Arial", color="darkblue"),
        paper_bgcolor="white",
        plot_bgcolor="rgba(0,0,0,0)",  # Fond transparent
        xaxis_title="Arrondissement",
        yaxis_title="Nombre de donneuses",
        font=dict(family="Arial", size=14),
        xaxis_tickangle=-45,  # Inclinaison des labels pour éviter le chevauchement
        bargap=0.2  # Espacement entre les barres
    )

    # Graphique 3 : Éligibilité selon situation matrimoniale
    # Regrouper et préparer les données
    elig_sm = dff.groupby('Situation Matrimoniale (SM)')['ÉLIGIBILITÉ AU DON.'].value_counts().unstack().fillna(0)

    # Création du graphique
    fig_elig_sm = px.bar(
        elig_sm,
        barmode='stack',
        labels={'value': 'Nombre de donneuses', 'Situation Matrimoniale (SM)': 'Situation matrimoniale'},
        title="Éligibilité au don selon la situation matrimoniale",
        color_discrete_sequence=px.colors.qualitative.Set1,
        text_auto=True  # Afficher directement les valeurs sur les barres
    )

    # Personnalisation du layout
    fig_elig_sm.update_layout(
        title_x=0.5,  # Centrer le titre
        title_font=dict(size=20, family="Arial", color="darkblue"),
        paper_bgcolor="white",
        plot_bgcolor="rgba(0,0,0,0)",  # Fond transparent
        xaxis_title="Situation matrimoniale",
        yaxis_title="Nombre de donneuses",
        font=dict(family="Arial", size=14),
        barmode="stack",
        bargap=0.1  # Réduction de l'espace entre les barres
    )

    # Ajout du hover personnalisé
    fig_elig_sm.update_traces(
        hovertemplate="<b>Situation Matrimoniale :</b> %{x}<br><b>Nombre :</b> %{y}<extra></extra>",
        marker=dict(line=dict(color='white', width=1))  # Bordures pour améliorer la lisibilité
    )

    return fig_age, fig_arr, fig_elig_sm
