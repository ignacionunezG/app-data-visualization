from dash import Dash
from src.layout import create_layout
from src.callbacks import register_callbacks

# Inicialización de la app
app = Dash(__name__)
app.title = "F1 Data Visualization"

# Configuración del layout
app.layout = create_layout(app)

# Registro de los callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
