
import pandas as pd
import plotly.express as px
from dash import Input, Output
import plotly.graph_objects as go
from plotly.colors import qualitative

# Cargar datos preprocesados
df = pd.read_excel("data/Historical Pitstops Grouped.xlsx")

# Colores personalizados para las escuderías
color_map = {
    "Ferrari": "red",
    "Mercedes": "gray",
    "McLaren": "orange",
    "Red Bull": "purple",
    "Williams": "blue",
    "Aston Martin": "green",
    "Alpine F1 Team": "pink",
    "Haas F1 Team": "black",
    "Manor Marussia": "brown",  # Marrón para Manor Marussia
    "Alfa Romeo": "darkred",   # Rojo oscuro para Alfa Romeo
    "Racing Point": "magenta", # Magenta para Racing Point
    "Alpha Tauri": "navy"      # Azul marino para Alpha Tauri
}

# Generar colores únicos para las escuderías restantes
def generate_unique_colors(teams, base_colors):
    available_colors = iter(base_colors)
    for team in teams:
        if team not in color_map:
            color_map[team] = next(available_colors, "gray")  # Asigna un color o gris si se agotan

# Llamar al generador de colores para todas las escuderías del DataFrame
generate_unique_colors(
    df["escuderia"].unique(), 
    qualitative.Plotly  # Paleta de colores cualitativos de Plotly
)
def register_callbacks(app):
    # Callback para la gráfica de pit stops
    @app.callback(
        Output("pitstop-times-graph", "figure"),
        Input("team-selector", "value")
    )
    def update_pitstop_graph(selected_teams):
        if not selected_teams:
            return px.line(title="Selecciona al menos una escudería")

        # Filtrar los datos por las escuderías seleccionadas
        filtered_df = df[df["escuderia"].isin(selected_teams)]

        # Escuderías con más de un dato (pueden formar líneas)
        multi_year_teams = filtered_df.groupby("escuderia").filter(lambda x: len(x) > 1)

        # Crear el gráfico de líneas solo para las escuderías con múltiples datos
        fig = px.line(
            multi_year_teams,
            x="año",
            y="duration",
            color="escuderia",
            title="Evolución del Tiempo Medio de Pit Stop",
            color_discrete_map=color_map  # Usar colores únicos
        )

        # Escuderías con un único dato (solo un punto)
        single_year_teams = filtered_df.groupby("escuderia").filter(lambda x: len(x) == 1)

        # Añadir puntos grandes para escuderías con un único año
        for team in single_year_teams["escuderia"].unique():
            team_data = single_year_teams[single_year_teams["escuderia"] == team]
            fig.add_trace(go.Scatter(
                x=team_data["año"],
                y=team_data["duration"],
                mode="markers",
                marker=dict(
                    size=12,
                    color=color_map[team],  # Usar el color único asignado
                    symbol="circle"
                ),
                name=team  # Asegurar que la leyenda muestre solo el punto
            ))

        # Configuración del layout del gráfico
        fig.update_layout(
            plot_bgcolor="rgb(248, 248, 248)",  # Fondo muy claro
            xaxis=dict(
                title="Año",
                tickmode="linear",
                tick0=2011,
                dtick=1,
                showgrid=True,  # Mostrar líneas verticales
                gridcolor="rgb(200, 200, 200)",  # Líneas grises claras
                gridwidth=0.5,  # Ancho más fino
                zeroline=False  # No mostrar línea base adicional
            ),
            yaxis=dict(
                title="Duración Promedio (s)",
                showgrid=True,  # Mostrar líneas horizontales
                gridcolor="rgb(200, 200, 200)",  # Líneas grises claras
                gridwidth=0.5,  # Ancho más fino
                zeroline=False  # No mostrar línea base adicional
            ),
            legend=dict(
                title="Escuderías",
                bgcolor="rgba(255, 255, 255, 0.8)",  # Fondo semitransparente para la leyenda
                bordercolor="rgb(200, 200, 200)",
                borderwidth=1
            ),
            font=dict(
                size=12,
                color="rgb(50, 50, 50)"  # Texto gris oscuro
            ),
            title=dict(
                x=0.5,  # Centrar el título
                font=dict(
                    size=18,
                    color="rgb(50, 50, 50)"
                )
            )
        )

        return fig  # <-- ¡Este return es crucial!
        
    @app.callback(
        Output("positions-gained-graph", "figure"),
        Input("year-dropdown", "value")
    )
    def update_positions_graph(selected_year):
        # Cargar datos de posiciones ganadas desde el archivo Excel
        df_positions = pd.read_excel("data/PosicionesGanadasPorPiloto.xlsx")
        
        # Filtrar únicamente los datos del año seleccionado
        df_filtered = df_positions[df_positions["año"] == selected_year]
        
        # Ordenar el DataFrame por número de posiciones ganadas (de mayor a menor)
        df_filtered = df_filtered.sort_values(by="posiciones_ganadas", ascending=False)
        
        # Crear el gráfico de barras usando solo los datos filtrados
        fig = px.bar(
            df_filtered,
            x="nombre_piloto",  # Usar los nombres de los pilotos en el eje X
            y="posiciones_ganadas",  # Usar las posiciones ganadas en el eje Y
            title=f"Posiciones ganadas por piloto en {selected_year}",
            labels={"nombre_piloto": "Piloto", "posiciones_ganadas": "Posiciones Ganadas"},
            color="posiciones_ganadas",  # Colorear barras según el número de posiciones ganadas
            color_continuous_scale=px.colors.sequential.Viridis  # Escala de colores
        )

        # Personalizar el diseño del gráfico
        fig.update_layout(
            plot_bgcolor="rgb(248, 248, 248)",  # Fondo claro
            xaxis=dict(
                title="Piloto",
                categoryorder="total descending"  # Ordenar de mayor a menor
            ),
            yaxis=dict(
                title="Posiciones Ganadas",
            ),
            font=dict(
                size=12,  # Tamaño del texto
                color="rgb(50, 50, 50)"  # Color del texto
            ),
            title=dict(
                font=dict(
                    size=18,  # Tamaño del título
                    color="rgb(50, 50, 50)"  # Color del título
                )
            )
        )

        return fig