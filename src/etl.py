import pandas as pd
import requests

# Función para obtener datos de una temporada y calcular posiciones ganadas/perdidas
def obtener_posiciones_ganadas(año):
    url = f"http://ergast.com/api/f1/{año}/results.json?"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        races = data['MRData']['RaceTable']['Races']

        pilotos_posiciones = {}

        # Recorrer cada carrera del año
        for race in races:
            results = race['Results']

            # Procesar resultados de cada piloto
            for piloto in results:
                driver_id = piloto['Driver']['driverId']
                given_name = piloto['Driver']['givenName']  # Primer nombre del piloto
                family_name = piloto['Driver']['familyName']  # Apellido del piloto
                full_name = f"{given_name} {family_name}"  # Nombre completo del piloto
                
                grid = int(piloto['grid']) if piloto['grid'] != "0" else 0
                position = int(piloto['position']) if piloto['position'] != "0" else 0
                posiciones_ganadas = grid - position

                # Sumar las posiciones ganadas/perdidas por cada piloto
                if driver_id not in pilotos_posiciones:
                    pilotos_posiciones[driver_id] = {
                        "nombre_piloto": full_name,
                        "posiciones_ganadas": 0
                    }
                pilotos_posiciones[driver_id]["posiciones_ganadas"] += posiciones_ganadas

        # Convertir a DataFrame
        df_pilotos = pd.DataFrame([
            {
                "driverId": driver_id,
                "nombre_piloto": data["nombre_piloto"],
                "posiciones_ganadas": data["posiciones_ganadas"],
                "año": año
            }
            for driver_id, data in pilotos_posiciones.items()
        ])
        return df_pilotos

    else:
        print(f"Error al obtener datos del año {año}: {response.status_code}")
        return pd.DataFrame()

# Obtener datos para todas las temporadas
años = list(range(2011, 2025))
df_combined = pd.DataFrame()

for año in años:
    df_año = obtener_posiciones_ganadas(año)
    df_combined = pd.concat([df_combined, df_año], ignore_index=True)

# Guardar resultados en un archivo Excel
df_combined.to_excel("data/PosicionesGanadasPorPiloto.xlsx", index=False)

