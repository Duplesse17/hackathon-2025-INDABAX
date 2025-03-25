import dash
from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from dash import clientside_callback, ClientsideFunction


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
    "zIndex": "999"  # important pour rester visible
}

SIDEBAR_STYLE_DARK = SIDEBAR_STYLE.copy()
SIDEBAR_STYLE_DARK.update({
    "backgroundColor": "#343a40",
    "color": "#f8f9fa"
})

# On enlève minHeight, on gère autrement la hauteur
CONTENT_STYLE = {
    "marginLeft": "18rem",
    "marginRight": "2rem",
    "padding": "2rem 1rem 5rem 1rem",  # padding-bottom augmenté
    "backgroundColor": "#f1f3f4",
    "minHeight": "100vh",
    "transition": "all 0.4s ease"
}

CONTENT_STYLE_DARK = CONTENT_STYLE.copy()
CONTENT_STYLE_DARK.update({
    "backgroundColor": "#212529",
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

CARD_STYLE = {
    "backgroundColor": "#ffffff",
    "borderRadius": "1rem",
    "padding": "2rem",
    "boxShadow": "0 4px 12px rgba(0,0,0,0.1)",
    "transition": "transform 0.3s ease-in-out, background-color 0.4s ease"
}

FOOTER_STYLE = {
    "position": "fixed",
    "bottom": "0",
    "left": "16.02rem",  # Décalage égal à la sidebar
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
}
)

CARD_STYLE_DARK = CARD_STYLE.copy()
CARD_STYLE_DARK.update({
    "backgroundColor": "#343a40",
    "color": "#f8f9fa"
})

# SIDEBAR NAVIGATION
def create_sidebar():
    return html.Div(
        [
            html.H2("🩸 Don de Sang", className="display-7 text-danger fw-bold "),
            html.Hr(),
            html.P("Analyse & Suivi", className="text-muted"),
            dbc.Nav(
                [
                    dbc.NavLink("🏠 Accueil", href="/", active="exact", style=NAV_LINK_STYLE, className="nav-hover"),
                    dbc.NavLink("🩺 Santé & Éligibilité", href="/sante-eligibilite", active="exact", style=NAV_LINK_STYLE, className="nav-hover"),
                    dbc.NavLink("👩‍⚕️ Analyse Femmes", href="/femmes", active="exact", style=NAV_LINK_STYLE, className="nav-hover"),
                    dbc.NavLink("🩸 Les Donneurs", href="/donneurs", active="exact", style=NAV_LINK_STYLE, className="nav-hover"),
                    dbc.NavLink("📊 Es tu un Élligible ?", href="/prediction", active="exact", style=NAV_LINK_STYLE, className="nav-hover"),
                    dbc.NavLink("📝 A Propos", href="/about", active="exact", style=NAV_LINK_STYLE, className="nav-hover"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        id="sidebar",
        style=SIDEBAR_STYLE
    )

# HEADER avec icône et toggle
def create_header():
    return dbc.Navbar(
        dbc.Container([

            html.Div([
                html.I(className="fas fa-tint fa-2x text-light me-2"),
                html.Span("Dashboard", style={"color": "#ffffff", "fontWeight": "bold", "fontSize": "2rem"}),
                html.Span(" Suivi", style={"color": "#ffc107", "fontSize": "2rem"}),
                html.Span(" 🇨🇲", style={"fontSize": "2rem"})
            ], className="d-flex align-items-center"),

            dbc.Switch(id="dark-mode-toggle", label="🌙 Mode Sombre", value=False, className="ms-auto")

        ]),

        color= "danger",  # 👈 Rouge classique Bootstrap
        dark=True,
        sticky="top",
        className="shadow-sm",
        style={
            "borderRadius": "0.75rem",
            "marginBottom": "1rem",
            "padding": "0.6rem 1.5rem",
            "height": "65px"
        }
    )


# FOOTER FIXE EN BAS
def create_footer():
    return html.Footer([
        html.Div([
            html.A(html.I(className="fab fa-github fa-lg"), href="https://github.com/Duplesse17/hackathon-2025-INDABAX.git", className="me-3 text-dark",target="_blank"),
            html.A(html.I(className="fab fa-linkedin fa-lg"), href="https://www.linkedin.com/company/indabax-cameroon/", className="me-3 text-primary",target="_blank"),
            html.A(html.I(className="fab fa-twitter fa-lg"), href="https://twitter.com", className="me-3 text-info",target="_blank"),
            html.P("© 2025 TensorPulse Group | Powered by Dash", className="text-center text-muted mt-2 mb-0"),
        ], className="text-center"),
        
    ],id="footer",
    style= FOOTER_STYLE)

# BOUTON SCROLL TO TOP
def create_scroll_to_top_button():
    return html.Div(
        html.A("⬆️", href="#", className="btn btn-danger rounded-circle shadow", style={
            "position": "fixed",
            "bottom": "100px",  # on le décale à cause du footer
            "right": "50px",
            "fontSize": "24px",
            "padding": "10px 15px",
            "zIndex": "999"
        })
    )

# ✅ Layout avec callbacks pour Dark Mode
app.layout = html.Div([  # Ce Div englobe tout
    dcc.Location(id="url"),
    dcc.Store(id='dark-mode', data=False),

    # Sidebar
    create_sidebar(),

    # Contenu principal avec flexbox
    html.Div([
        create_header(),

        # Le contenu scrollable
        html.Div(
            dash.page_container,
            style={
                "flex": "1",
                "overflowY": "auto",  # Scroll vertical
                "paddingBottom": "2rem"
            }
        ),

        # Footer sticky en bas
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
            "minHeight": "100vh",  # Prend toute la hauteur de la fenêtre
        }
    )
])


# CALLBACK POUR LE DARK MODE
@app.callback(
    Output("sidebar", "style"),
    Output("content", "style"),
    Output("footer","style"),
    Input("dark-mode-toggle", "value")
)
def toggle_dark_mode(is_dark):
    if is_dark:
        return SIDEBAR_STYLE_DARK, CONTENT_STYLE_DARK , FOOTER_STYLE_DARK
    else:
        return SIDEBAR_STYLE, CONTENT_STYLE , FOOTER_STYLE

if __name__ == "__main__":
    app.run_server(debug=True)
