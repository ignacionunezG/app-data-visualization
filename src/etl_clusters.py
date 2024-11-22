import pandas as pd
import requests
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np

# 1. Obtener datos de status y circuitos
def obtener_datos_status(año, ronda):
    url_status = f"http://ergast.com/api/f1/{año}/{ronda}/status.json"
    url_circuit = f"http://ergast.com/api/f1/{año}/{ronda}/circuits.json"

    status_response = requests.get(url_status)
    circuit_response = requests.get(url_circuit)

    if status_response.status_code == 200 and circuit_response.status_code == 200:
        status_data = status_response.json()
        circuit_data = circuit_response.json()

        circuit_name = circuit_data["MRData"]["CircuitTable"]["Circuits"][0]["circuitName"]

        status_counts = {status["status"]: int(status["count"]) for status in status_data["MRData"]["StatusTable"]["Status"]}
        return circuit_name, status_counts
    else:
        return None, {}

# 2. Construcción del DataFrame
def generar_dataframe():
    años = list(range(2010, 2024))
    max_rounds = 22  # Número máximo de rondas por temporada (estimado)
    data = []

    for año in años:
        for ronda in range(1, max_rounds + 1):
            try:
                circuito, status_counts = obtener_datos_status(año, ronda)
                if circuito:
                    row = {"Season": año, "Circuit": circuito, **status_counts}
                    data.append(row)
            except Exception as e:
                print(f"Error en {año}, ronda {ronda}: {e}")

    # Reemplazar valores faltantes con 0
    df = pd.DataFrame(data).fillna(0)
    return df

# Generar y guardar el Excel
#df = generar_dataframe()
print("aqui")
#df.to_excel("data/StatusPerCircuit.xlsx", index=False)

# 3. Clustering
def realizar_clustering():
    # Cargar los datos
    df = pd.read_excel("data/StatusPerCircuit.xlsx")
    
    # Agrupar por Circuito y sumar
    grouped = df.groupby("Circuit").sum().drop(columns=["Season"])
    
    # Normalizar datos
    data = grouped.values
    data_normalized = (data - data.mean(axis=0)) / data.std(axis=0)
    
    # Método del codo para determinar el número óptimo de clústeres
    #sil_scores = []
    #k_values = range(2, 10)
    #for k in k_values:
    #    kmeans = KMeans(n_clusters=k, random_state=42)
    #    kmeans.fit(data_normalized)
    #    sil_scores.append(silhouette_score(data_normalized, kmeans.labels_))

    # Mejor número de clústeres
    #best_k = k_values[np.argmax(sil_scores)]
    #print(f"Mejor número de clústeres: {best_k}")
    
    # Realizar clustering
    #optamos por 4 clusters
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    grouped["Cluster"] = kmeans.fit_predict(data_normalized)
    
    # Guardar resultados
    grouped.to_excel("data/CircuitClusters.xlsx")

# Llamar a la función
realizar_clustering()
