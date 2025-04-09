import dash
from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.LUX,
        "https://use.fontawesome.com/releases/v5.8.1/css/all.css",
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css'
    ],
    suppress_callback_exceptions=True
)

# 🎨 STYLES
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "backgroundColor": "#f8f9fa",
    "boxShadow": "2px 0px 5px rgba(0,0,0,0.1)",
    "borderRadius": "0 1rem 0rem 0",
    "transition": "all 0.4s ease",
    "zIndex": "999"
}
SIDEBAR_STYLE_DARK = SIDEBAR_STYLE.copy()
SIDEBAR_STYLE_DARK.update({
    "backgroundColor": "#343a40",
    "color": "#f8f9fa"
})
CONTENT_STYLE = {
    "marginLeft": "18rem",
    "marginRight": "2rem",
    "padding": "2rem 1rem 5rem 1rem",
    "backgroundColor": "#f1f3f4",
    "minHeight": "100vh",
    "transition": "all 0.4s ease"
}
CONTENT_STYLE_DARK = CONTENT_STYLE.copy()
CONTENT_STYLE_DARK.update({
    "backgroundColor": "#343a40",
    "color": "#f8f9fa"
})
FOOTER_STYLE = {
    "position": "fixed",
    "bottom": "0",
    "left": "16.02rem",
    "right": "0",
    "height": "70px",
    "backgroundColor": "#f8f9fa",
    "padding": "10px",
    "boxShadow": "0px -2px 5px rgba(0,0,0,0.1),",
}
FOOTER_STYLE_DARK = FOOTER_STYLE.copy()
FOOTER_STYLE_DARK.update({
    "backgroundColor": "#343a40",
    "color": "#f8f9fa"
})

NAV_LINK_STYLE = {
    "marginBottom": "0.7rem",
    "fontWeight": "500",
    "fontSize": "16px",
    "transition": "all 0.3s ease",
    "borderRadius": "0.5rem",
    "padding": "0.5rem 1rem"
}

# SIDEBAR
def create_sidebar():
    return html.Div(
        [
            html.H2("D🩸n de Sang", className="display-7 text-danger fw-bold"),
            html.Hr(),
            html.P("Analyse & Suivi", className="text-muted"),
            dbc.Nav(
                [
                    dbc.NavLink("🏠 Accueil", href="/", active="exact", className="nav-hover"),
                    dbc.NavLink("🩺 Santé & Éligibilité", href="/sante-eligibilite", active="exact"),
                    dbc.NavLink("👩‍⚕️ Analyse Femmes", href="/femmes", active="exact"),
                    dbc.NavLink("🩸 Les Donneurs", href="/donneurs", active="exact"),
                    dbc.NavLink("📊 Es-tu un Éligible ?", href="/prediction", active="exact"),
                    dbc.NavLink("📝 À Propos", href="/about", active="exact"),
                ],
                vertical=True,
                pills=True,
                className="flex-column"
            ),
        ],
        id="sidebar",
        className="d-flex flex-column p-3",  # ⛔ bg-light retiré
    )


# HEADER
def create_header():
    return dbc.Navbar(
        dbc.Container([
            # Titre du dashboard
            html.Div([
                html.Span("Dashboard", style={"color": "#ffffff", "fontWeight": "bold", "fontSize": "1.5rem"}),
                html.Span(" Suivi", style={"color": "#ffc107", "fontSize": "1.5rem"}),
                html.Span(" 🇨🇲", style={"fontSize": "1.5rem"})
            ], className="d-flex align-items-center"),

            # Espace entre le titre et les éléments de droite
            html.Div(style={"flexGrow": "1"}),  # pousse les éléments à droite

            # Élément de droite pour écran large (visible à partir de md)
            html.Div([
                dbc.Switch(id="dark-mode-toggle", label="🌙 Mode Sombre", value=False, className="me-3"),
                dbc.Button("Se déconnecter", id="logout-btn", color="secondary", outline=True, n_clicks=0)
            ], className="d-none d-md-flex align-items-center"),

            
        ]),
        color="danger",
        dark=True,
        sticky="top",
        className="shadow-sm",
        style={
            "borderRadius": "0.75rem",
            "marginBottom": "1rem",
            "padding": "0.6rem 1.5rem",
            "height": "65px",
        },
    )



# FOOTER
def create_footer():
    return html.Footer([
        html.Div([
            html.A(html.I(className="fab fa-github fa-lg"), href="https://github.com/Duplesse17/hackathon-2025-INDABAX.git", className="me-3 text-dark", target="_blank"),
            html.A(html.I(className="fab fa-linkedin fa-lg"), href="https://www.linkedin.com/company/indabax-cameroon/", className="me-3 text-primary", target="_blank"),
            html.A(html.I(className="fab fa-twitter fa-lg"), href="https://twitter.com", className="me-3 text-info", target="_blank"),
            html.P("© 2025 TensorPulse Group | Powered by Dash", className="text-center text-muted mt-2 mb-0"),
        ], className="text-center"),
    ], id="footer", style=FOOTER_STYLE)

# BOUTON TOP
def create_scroll_to_top_button():
    return html.Div(
        html.A("⬆️", href="#", className="btn btn-danger rounded-circle shadow", style={
            "position": "fixed",
            "bottom": "100px",
            "right": "50px",
            "fontSize": "24px",
            "padding": "10px 15px",
            "zIndex": "999"
        })
    )

# ✅ APP LAYOUT FINAL
app.layout = html.Div([
    dcc.Location(id="url"),
    dcc.Store(id='dark-mode', data=False),
    dcc.Store(id='auth-status',storage_type="session", data=False),  # Authentification ici

    create_sidebar(),
    html.Div([
        create_header(),

        html.Div(dash.page_container, style={
            "flex": "1",
            "overflowY": "auto",
            "paddingBottom": "2rem"
        }),

        create_footer(),
        create_scroll_to_top_button()
    ],
        id="content",
        style={
            "display": "flex",
            "flexDirection": "column",
            "marginLeft": "18rem",
            "marginRight": "2rem",
            "padding": "0",
            "backgroundColor": "#f1f3f4",
            "minHeight": "100vh",
            "minWidth": "810px",  # Taille minimale
            "maxWidth": "100vw",  # Taille maximale (max largeur de l'écran)
            "maxHeight": "1080px",  # Taille maximale (max hauteur de l'écran)
            "overflow": "auto"  
        }
    )
])

# 🌙 DARK MODE
@app.callback(
    Output("sidebar", "style"),
    Output("content", "style"),
    Output("footer", "style"),
    Input("dark-mode-toggle", "value")
)
def toggle_dark_mode(is_dark):
    if is_dark:
        return SIDEBAR_STYLE_DARK, CONTENT_STYLE_DARK, FOOTER_STYLE_DARK
    return SIDEBAR_STYLE, CONTENT_STYLE, FOOTER_STYLE

# 🔐 DECONNEXION
@app.callback(
    Output("auth-status", "data", allow_duplicate=True),
    Input("logout-btn", "n_clicks"),
    prevent_initial_call=True
)
def logout_user(n_clicks):
    return False



# 🚀 RUN
if __name__ == "__main__":
    app.run_server(debug=True,port=8050)
# app.run_server(debug=True, port=8050) 