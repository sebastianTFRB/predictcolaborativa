import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
import joblib
import os

# 📌 Cargar datasets
print("Cargando archivos...")
sales = pd.read_csv("data/sales_train.csv")
items = pd.read_csv("data/items.csv")
shops = pd.read_csv("data/shops.csv")

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

# Filtrar outliers
monthly_sales = monthly_sales[(monthly_sales['item_cnt_month'] >= 0) & (monthly_sales['item_cnt_month'] <= 20)]

# Selección de features
features = ['shop_id', 'item_id', 'item_category_id', 'month', 'item_price']
target = 'item_cnt_month'

X = monthly_sales[features].fillna(0)
y = monthly_sales[target]

# División de datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenamiento del modelo
print("Entrenando modelo SVM...")
model = SVR(kernel='rbf', C=1.0, epsilon=0.2)
model.fit(X_train, y_train)

# Evaluación
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"🔍 Mean Squared Error: {mse:.4f}")

# Guardar modelo
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/sales_model.pkl", compress=3)
print("✅ Modelo guardado en model/sales_model.pkl")
