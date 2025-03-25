import dash
from dash import html, dcc, Input, Output
from dash import clientside_callback, ClientsideFunction
import plotly.express as px
import pandas as pd
from dash_extensions import EventListener

dash.register_page(__name__, path='/')

# =====================
# 🔹 Chargement des données
# =====================
df = pd.read_excel('data/donneurs_geocode_update.xlsx')


df['Age'] = df['Date de naissance']
# =====================
# 🔹 Layout
# =====================

kpi_style = {
    'width': '20%',  # ou '18%' si tu préfères
    'padding': '15px',
    'border': '1px solid #ddd',
    'border-radius': '10px',
    'box-shadow': '2px 2px 2px lightgrey',
    'textAlign': 'center'
}

kpi_card_style = {
    'background': 'linear-gradient(135deg, #FF7E5F, #FEB47B)',  # Dégradé !
    'color': 'white',
    'padding': '20px',
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
kpi_card_hover = {
    'transform': 'scale(1.05)',
}

layout = html.Div(id='pdf-content', children=[
    html.H2("Tableau de bord - Pottentiel Donneur", style={
        'textAlign': 'center',
        'marginBottom': '30px',
        'color': '#2E86C1',
        'fontWeight': 'bold'
    }),
    # KPIs
    html.Div([
        html.Div([
        html.I(className="fas fa-users fa-2x", style={'margin-bottom': '10px'}),
        html.H4("Donneurs Pottentiel"),
        html.H2(id='kpi-total')
    ], style=kpi_card_style),

    html.Div([
        html.I(className="fas fa-female fa-2x", style={'margin-bottom': '10px'}),
        html.H4("Taux de Femmes"),
        html.H2(id='kpi-femmes')
    ], style={**kpi_card_style, 'background': 'linear-gradient(135deg, #B24592, #F15F79)'}),

    html.Div([
        html.I(className="fas fa-birthday-cake fa-2x", style={'margin-bottom': '10px'}),
        html.H4("Âge Moyen"),
        html.H2(id='kpi-age')
    ], style={**kpi_card_style, 'background': 'linear-gradient(135deg, #43C6AC, #191654)'}),

    html.Div([
        html.I(className="fas fa-map-marker-alt fa-2x", style={'margin-bottom': '10px'}),
        html.H4("Arrondissement Dominant"),
        html.H2(id='kpi-arrondissement')
    ], style={**kpi_card_style, 'background': 'linear-gradient(135deg, #36D1DC, #5B86E5)'}),

    html.Div([
        html.I(className="fas fa-check-circle fa-2x", style={'margin-bottom': '10px'}),
        html.H4("Taux d'Éligibilité"),
        html.H2(id='kpi-eligibilite')
    ], style={**kpi_card_style, 'background': 'linear-gradient(135deg, #00C9FF, #92FE9D)'})
    
], style={
    'display': 'flex',
    'justify-content': 'center',
    'gap': '20px',
    'flex-wrap': 'wrap',
    'margin': '30px 0'
}),

        
    # Filtres
    html.Div([
        html.Label('Filtrer par Religion :'),
        dcc.Dropdown(
            df['Religion'].dropna().unique(),
            id='religion-filter',
            multi=True
        )
    ], style={'width': '25%', 'display': 'inline-block', 'margin': '10px'}),

    html.Div([
        html.Label('Filtrer par Arrondissement :'),
        dcc.Dropdown(
            df['Arrondissement de résidence'].dropna().unique(),
            id='arrondissement-filter',
            multi=True
        )
    ], style={'width': '25%', 'display': 'inline-block', 'margin': '10px'}),

    html.Div([
        html.Label('Filtrer par Sexe :'),
        dcc.Dropdown(
            df['Genre'].dropna().unique(),
            id='sexe-filter',
            multi=True
        )
    ], style={'width': '20%', 'display': 'inline-block', 'margin': '10px'}),
    html.Div([
        html.Label('Filtrer par Éligibilité au don :'),
        dcc.Dropdown(
            df['ÉLIGIBILITÉ AU DON.'].dropna().unique(),
            id='eligibilite-filter',
            multi=True
        )
    ], style={'width': '23%', 'display': 'inline-block', 'margin': '10px'}),

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
    ], style={'margin': '20px'}),

    
    html.Button('Exporter PDF', id='export-button', n_clicks=0, style={'margin': '10px'}),
    # DCC Store juste pour déclencher la callback JS
    dcc.Store(id='pdf-trigger'),
    # Carte uniquement
    html.Div([
        dcc.Graph(id='map-donateurs')
    ])
])

clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='download_pdf'),
    Output('pdf-trigger', 'data'),
    Input('export-button', 'n_clicks')
)


def export_pdf(event):
    if event:
        print("🖨️ Bouton Export PDF cliqué !")
        # 👉 Ici, ajoute ton code d'export PDF avec weasyprint ou autre
        # Par exemple, tu pourrais appeler ta fonction export_pdf(ton_dataframe)
        return "Export lancé !"
    return dash.no_update

@dash.callback(
    [Output('map-donateurs', 'figure'),
     Output('kpi-total', 'children'),
     Output('kpi-femmes', 'children'),
     Output('kpi-age', 'children'),
     Output('kpi-arrondissement', 'children'),
     Output('kpi-eligibilite', 'children')],
    [Input('religion-filter', 'value'),
     Input('arrondissement-filter', 'value'),
     Input('sexe-filter', 'value'),
     Input('age-filter', 'value'),
     Input('eligibilite-filter', 'value')]
)
def update_graphs_and_kpis(religion, arrondissement, sexe, age_range, eligiblite):
    dff = df.copy()

    if eligiblite:
        dff = dff[dff['ÉLIGIBILITÉ AU DON.'].isin(eligiblite)]
    if religion:
        dff = dff[dff['Religion'].isin(religion)]
    if arrondissement:
        dff = dff[dff['Arrondissement de résidence'].isin(arrondissement)]
    if sexe:
        dff = dff[dff['Genre'].isin(sexe)]

    dff['Date de naissance'] = pd.to_datetime(dff['Date de naissance'], errors='coerce')
    dff = dff[dff['Date de naissance'].notna()]

    dff['Age'] = pd.to_datetime('today').year - dff['Date de naissance'].dt.year
    dff = dff[(dff['Age'] >= age_range[0]) & (dff['Age'] <= age_range[1])]

    # KPIs
    total_donneurs = len(dff)
    pourcentage_femmes = 0
    age_moyen = 0
    arrondissement_dominant = "N/A"
    taux_eligibilite = 0

    if total_donneurs > 0:
        femmes_count = len(dff[dff['Genre'] == 'Femme'])
        pourcentage_femmes = round((femmes_count / total_donneurs) * 100, 1)

        age_moyen = round(dff['Age'].mean(), 1)

        arrondissement_counts = dff['Arrondissement de résidence'].value_counts()
        arrondissement_dominant = arrondissement_counts.idxmax() if not arrondissement_counts.empty else "N/A"

        eligibles_count = len(dff[dff['ÉLIGIBILITÉ AU DON.'].str.lower() == 'eligible'])
        taux_eligibilite = round((eligibles_count / total_donneurs) * 100, 1) if total_donneurs > 0 else 0


    # 1️⃣ Regrouper les donneurs par quartier et arrondissement
    agg_df = dff.groupby(['Arrondissement de résidence', 'Quartier de Résidence']).agg({
        'Latitude': 'mean',
        'Longitude': 'mean'
    })

    # Ajoute la taille du groupe (nombre de donneurs)
    agg_df['Nombre de Donneurs'] = dff.groupby(['Arrondissement de résidence', 'Quartier de Résidence']).size().values

    # Si besoin, reset_index
    agg_df = agg_df.reset_index()

    # 2️⃣ Créer la carte avec scatter_mapbox (version verte 🌿)
    map_fig = px.scatter_mapbox(
        agg_df,
        lat='Latitude',
        lon='Longitude',
        size='Nombre de Donneurs',
        color='Arrondissement de résidence',  # Couleur par arrondissement
        color_discrete_sequence=px.colors.sequential.Viridis_r,  # Palette verte / jaune
        hover_name='Quartier de Résidence',
        zoom=6,  # Zoom plus proche
        size_max=60,  # Cercles plus gros
        opacity=0.7,  # Un peu plus opaque
        mapbox_style='open-street-map',  
        title='🌍 Répartition des Donneurs Pottentiel de Sang par Quartier'
    )

    # 3️⃣ Customisation : Contours, couleurs plus flashy, etc.
    map_fig.update_traces(marker=dict(
        sizemode='area',
        opacity=0.8,
        #line=dict(width=2, color='white')  # Contour blanc plus épais
    ))

    # 4️⃣ Layout pour l'esthétique générale
    map_fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        paper_bgcolor='rgba(0,0,0,0)',  # Fond transparent
        font=dict(color='Black'),  # Texte blanc sur fond sombre
        title_font=dict(size=24, color='limegreen', family='Arial Black')
    )

    




    return map_fig, total_donneurs, f"{pourcentage_femmes} %", f"{age_moyen} ans", arrondissement_dominant, f"{taux_eligibilite} %"