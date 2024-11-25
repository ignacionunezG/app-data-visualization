from dash import Dash
from src.layout import create_layout
from src.callbacks import register_callbacks

# Inicialización de la app
app = Dash(__name__)
app.title = "F1 Data Visualization"
server=app.server

app.layout = create_layout(app)

register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
