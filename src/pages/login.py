from dash import html, dcc, Input, Output, State, callback, ctx
import dash

# ✅ Enregistre la page
dash.register_page(__name__, path='/login', name="Connexion")

# ✅ Exemple d'utilisateurs
USERS = {
    "admin": "admin123",
    "duplesse": "hackathon2025",
    "user": "password"
}

layout = html.Div([
    dcc.Location(id="redirect", refresh=True),  # Composant pour la redirection
    html.H2("Connexion", className="mb-4"),

    dcc.Input(
        id="username", type="text", placeholder="Nom d'utilisateur", className="form-control mb-3", debounce=True
    ),
    dcc.Input(
        id="password", type="password", placeholder="Mot de passe", className="form-control mb-3", debounce=True
    ),
    
    html.Button("Se connecter", id="login-button", className="btn btn-danger mb-3"),

    html.Div(id="login-message", className="text-danger mb-3"),
])

@callback(
    Output("login-message", "children"),
    Output("auth-status", "data"),  # Mise à jour du store global
    Output("redirect", "href"),     # Redirection après connexion
    Input("login-button", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True
)
def login(n_clicks, username, password):
    if username in USERS and USERS[username] == password:
        return f"✅ Bienvenue {username} !", True, "/donneurs"  # Redirige vers la page des donneurs
    return "❌ Nom d'utilisateur ou mot de passe incorrect.", False, dash.no_update