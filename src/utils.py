import requests
import pandas as pd

def fetch_pitstop_data():
    years = range(2011, 2025)
    teams_data = []

    for year in years:
        response = requests.get(f"http://ergast.com/api/f1/{year}/pitstops.json?limit=1000")
        if response.status_code == 200:
            data = response.json()
            # Procesar datos aquí según la estructura de la API Ergast
            # teams_data.append({...})
    
    # Convertir a DataFrame y guardar
    df = pd.DataFrame(teams_data)
    df.to_excel("data/pitstop_data.xlsx", index=False)
