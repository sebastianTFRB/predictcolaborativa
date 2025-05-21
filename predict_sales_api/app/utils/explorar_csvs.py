import os
import pandas as pd

# Ruta a tu carpeta de archivos CSV
RUTA = "../../data"  # Cambia si tus archivos están en otra carpeta

# Listar todos los archivos CSV en la ruta
archivos_csv = [f for f in os.listdir(RUTA) if f.endswith(".csv")]

# Leer e imprimir head de cada archivo
for archivo in archivos_csv:
    ruta_completa = os.path.join(RUTA, archivo)
    print(f"\n📄 Archivo: {archivo}")
    try:
        df = pd.read_csv(ruta_completa)
        print(df.head(5))
    except Exception as e:
        print(f"❌ Error leyendo {archivo}: {e}")
