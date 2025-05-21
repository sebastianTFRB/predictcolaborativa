import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import joblib
import os

# 📌 Cargar datasets
print("Cargando archivos...")
sales = pd.read_csv("data/sales_train.csv")
items = pd.read_csv("data/items.csv")

# 📌 Preprocesamiento
print("Procesando datos...")
sales['date'] = pd.to_datetime(sales['date'], format='%d.%m.%Y')
sales['month'] = sales['date'].dt.month

# Agregación mensual por item y tienda
monthly_sales = sales.groupby(
    ['date_block_num', 'shop_id', 'item_id']
).agg({
    'item_price': 'mean',
    'item_cnt_day': 'sum'
}).reset_index()

monthly_sales.rename(columns={'item_cnt_day': 'item_cnt_month'}, inplace=True)

# Agregar columna de mes
monthly_sales['month'] = monthly_sales['date_block_num'] % 12

# Agregar categoría del ítem
monthly_sales = monthly_sales.merge(items[['item_id', 'item_category_id']], on='item_id', how='left')

# Filtrar outliers extremos
monthly_sales = monthly_sales[
    (monthly_sales['item_cnt_month'] >= 0) & (monthly_sales['item_cnt_month'] <= 20)
]

# 🔽 Reducir datos para entrenamiento más rápido
monthly_sales = monthly_sales.sample(n=10000, random_state=42)

# Definir features y target
features = ['shop_id', 'item_id', 'item_category_id', 'month', 'item_price']
target = 'item_cnt_month'

X = monthly_sales[features].fillna(0)
y = monthly_sales[target]

# Escalado de features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Dividir datos
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Entrenamiento del modelo
print("Entrenando modelo SVM con escalado...")
model = SVR(kernel='rbf', C=1.0, epsilon=0.2)
model.fit(X_train, y_train)

# Evaluación
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"🔍 Mean Squared Error: {mse:.4f}")

# Guardar modelo y scaler
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/sales_model.pkl", compress=3)
joblib.dump(scaler, "model/scaler.pkl", compress=3)
print("✅ Modelo y scaler guardados en /model")

# Mostrar variables usadas para predicción
print("\n🔑 Variables esperadas para predicción:")
for var in features:
    print(f"- {var}")

# Mostrar las variables que se deben enviar para predicción
print("\n🔑 Variables esperadas para predicción:")
for var in features:
    print(f"- {var}")

# Prueba rápida con datos de ejemplo
print("\n🔎 Realizando prueba de predicción con datos simulados...")

# Ejemplo manual (puedes modificar estos valores)
test_input = {
    'shop_id': 9,
    'item_id': 589,
    'item_category_id': 89,
    'month': 1,
    'item_price': 999.0
}

# Convertir a DataFrame en el mismo orden que las features
input_df = pd.DataFrame([test_input], columns=features)
predicted_sales = model.predict(input_df)[0]

print(f"📦 Predicción estimada de ventas: {round(predicted_sales, 2)} unidades")

