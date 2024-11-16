import pandas as pd
import plotly.express as px
from dash import Input, Output

# Cargar datos preprocesados
df = pd.read_excel("data/pitstop_data.xlsx")

def register_callbacks(app):
    @app.callback(
        Output("pitstop-times-graph", "figure"),
        Input("team-selector", "value")
    )
    def update_graph(selected_teams):
        if not selected_teams:
            return px.line(title="Selecciona al menos una escudería")

        # Filtrar datos según escuderías seleccionadas
        filtered_df = df[df["Escudería"].isin(selected_teams)]

        # Crear gráfico de líneas
        fig = px.line(
            filtered_df,
            x="Año",
            y="Tiempo Medio de Pit Stop",
            color="Escudería",
            title="Evolución del Tiempo Medio de Pit Stop"
        )

        fig.update_layout(legend_title="Escuderías", xaxis_title="Año", yaxis_title="Tiempo (s)")
        return fig
