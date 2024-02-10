import requests
import pandas as pd
import sys

def get_to_csv(url, nombre_archivo="datos_descargados_actualizados.csv"):
    response = requests.get(url)
    if response.status_code == 200:
        with open(nombre_archivo, 'w') as file:
            file.write(response.text)
        print(f"Archivo {nombre_archivo} guardado con éxito.")
    else:
        print(f"Error al descargar los datos: Código de estado {response.status_code}")

def procesar_datos(df):
    # Verificar y manejar valores faltantes
    if df.isnull().values.any():
        df = df.dropna()  # Eliminar filas con valores faltantes

    # Verificar y eliminar filas repetidas
    df = df.drop_duplicates()

    # Eliminando valores atipicos
    for columna in df.select_dtypes(include=['float64', 'int64']).columns:
        Q1 = df[columna].quantile(0.25)
        Q3 = df[columna].quantile(0.75)
        IQR = Q3 - Q1
        filtro = (df[columna] >= (Q1 - 1.5 * IQR)) & (df[columna] <= (Q3 + 1.5 * IQR))
        df = df[filtro]

    # Creando una columna para categorizar por edades
    bins = [0, 12, 19, 39, 59, float('inf')]
    labels = ['Niño', 'Adolescente', 'Joven Adulto', 'Adulto', 'Adulto Mayor']
    df['Categoria Edad'] = pd.cut(df['age'], bins=bins, labels=labels)

    # Guardando el DataFrame procesado como un archivo CSV
    df.to_csv('datos_procesados_actualizados.csv', index=False)

get_to_csv(sys.argv[1])
print("Datos descargados satisfactoriamente!")
df = pd.read_csv("datos_descargados_actualizados.csv")

procesar_datos(df)
print("Datos procesados satisfactoriamente!")