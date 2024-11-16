from dash import html, dcc

def create_layout(app):
    return html.Div([
        html.H1("Evolución del tiempo medio de Pit Stops por Escudería", style={"textAlign": "center"}),

        # Dropdown para seleccionar escuderías
        dcc.Dropdown(
            id="team-selector",
            options=[],
            placeholder="Selecciona escuderías",
            multi=True
        ),

        # Gráfico de líneas
        dcc.Graph(id="pitstop-times-graph")
    ])
