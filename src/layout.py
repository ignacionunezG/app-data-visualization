from dash import html, dcc
import pandas as pd

# Cargar los datos para obtener la lista de escuderías
df = pd.read_excel("src/data/Historical Pitstops Grouped.xlsx")
teams = df["escuderia"].unique()  # Obtener las escuderías únicas

# Cargar los datos para obtener la lista inicial de pilotos por año
df_positions = pd.read_excel("src/data/PosicionesGanadasPorPiloto.xlsx")
years = sorted(df_positions["año"].unique())  # Años únicos

# Cargar datos de clústeres y circuitos
clusters_df = pd.read_excel("src/data/CircuitClusters.xlsx")
clusters = clusters_df["Clasificacion Circuito"].unique()

def create_layout(app):
    return html.Div(
        style={
            "backgroundColor": "rgb(240, 240, 240)",
            "height": "100vh",
            "padding": "20px",
            "fontFamily": "Arial, sans-serif"
        },
        children=[
            # Título principal
            html.H1(
                "Evolución del tiempo medio de Pit Stops por Escudería (2011-2024)",
                style={
                    "textAlign": "center",
                    "color": "rgb(30, 30, 30)",
                    "marginBottom": "20px",
                    "fontSize": "2.5em",
                },
            ),
            # Gráfica de pit stops con selector de equipos
            html.Div(
                style={"display": "flex", "justifyContent": "space-between", "gap": "20px"},
                children=[
                    html.Div(
                        dcc.Graph(id="pitstop-times-graph"),
                        style={"flex": "3"}
                    ),
                    html.Div(
                        dcc.Checklist(
                            id="team-selector",
                            options=[{"label": team, "value": team} for team in teams],
                            value=[],
                            labelStyle={"display": "block", "cursor": "pointer", "color": "rgb(30, 30, 30)"},
                        ),
                        style={
                            "flex": "1",
                            "height": "60vh",
                            "overflowY": "auto",
                            "backgroundColor": "rgb(250, 250, 250)",
                            "padding": "20px",
                            "borderRadius": "10px",
                            "border": "1px solid rgb(200, 200, 200)",
                            "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                        },
                    ),
                ],
            ),
            # Título de la segunda gráfica
            html.H1(
                "Posiciones ganadas por piloto cada temporada",
                style={"textAlign": "center", "color": "black", "padding": "20px"}
            ),
            # Dropdown para seleccionar el año
            html.Div(
                children=[
                    dcc.Dropdown(
                        id="year-dropdown",
                        options=[{"label": str(year), "value": year} for year in years],
                        value=years[0],  # Año inicial por defecto
                        clearable=False,
                        style={"width": "50%", "margin": "0 auto"}
                    )
                ],
                style={"textAlign": "center", "marginBottom": "20px"}
            ),
            # Contenedor de la gráfica de posiciones ganadas
            html.Div(
                dcc.Graph(id="positions-gained-graph"),
                style={
                    "width": "100%",
                    "backgroundColor": "rgb(250, 250, 250)",
                    "padding": "20px",
                    "borderRadius": "10px",
                    "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"
                }
            ),
            # Título para los circuitos
            html.H1("Análisis de Circuitos de F1", style={"textAlign": "center"}),

            # Selector de clasificación de circuitos
            html.Div(
                children=[
                    html.Label("Selecciona la clasificación de los circuitos:", style={"fontWeight": "bold"}),
                    dcc.Dropdown(
                        id="cluster-dropdown",
                        options=[{"label": clasif, "value": clasif} for clasif in clusters],
                        placeholder="Selecciona una clasificación",
                        style={"width": "50%", "margin": "0 auto"}
                    ),
                ],
                style={"textAlign": "center", "marginBottom": "20px"}
            ),

            # Selector de circuito
            html.Div(
                children=[
                    html.Label("Selecciona un circuito:", style={"fontWeight": "bold"}),
                    dcc.Dropdown(
                        id="circuit-dropdown",
                        options=[],  # Se llenará dinámicamente
                        placeholder="Selecciona un circuito",
                        style={"width": "50%", "margin": "0 auto"}
                    ),
                ],
                style={"textAlign": "center", "marginBottom": "20px"}
            ),

            # Gráfico Treemap de estadísticas del circuito
            html.Div(
                dcc.Graph(id="circuit-stats-graph"),
                style={"width": "80%", "margin": "0 auto", "marginTop": "20px"}
            )
        ]
    )
