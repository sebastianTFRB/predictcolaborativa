import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib
import os

# Cargar datos
print("Cargando archivos...")
sales = pd.read_csv("data/sales_train.csv")
items = pd.read_csv("data/items.csv")

# Preprocesamiento
print("Procesando...")
sales['date'] = pd.to_datetime(sales['date'], format='%d.%m.%Y')
sales['month'] = sales['date'].dt.month

# Agregación mensual
monthly_sales = sales.groupby(
    ['date_block_num', 'shop_id', 'item_id']
).agg({
    'item_price': 'mean',
    'item_cnt_day': 'sum'
}).reset_index()

monthly_sales.rename(columns={'item_cnt_day': 'item_cnt_month'}, inplace=True)
monthly_sales['month'] = monthly_sales['date_block_num'] % 12

# Categoría del ítem
monthly_sales = monthly_sales.merge(items[['item_id', 'item_category_id']], on='item_id', how='left')

# Crear variable de clasificación (venta: sí o no)
monthly_sales['was_sold'] = (monthly_sales['item_cnt_month'] > 0).astype(int)

# Features y target
features = ['shop_id', 'item_id', 'item_category_id', 'month', 'item_price']
X = monthly_sales[features].fillna(0)
y = monthly_sales['was_sold']

# Submuestreo para acelerar
X, _, y, _ = train_test_split(X, y, train_size=10000, stratify=y, random_state=42)

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenamiento
print("Entrenando modelo Logístico...")
model = LogisticRegression(max_iter=200, solver='liblinear')
model.fit(X_train, y_train)

# Evaluación
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
print(f"✅ Accuracy: {acc:.4f}")
print("📊 Matriz de confusión:")
print(cm)

# Guardar modelo
os.makedirs("model", exist_ok=True)
joblib.dump(model, "app/model/logistic_model.pkl")
print("Modelo guardado como model/logistic_model.pkl")
# Mostrar las variables que usaremos para la predicción
print("\nVariables esperadas para predicción:")
for var in features:
    print(f"- {var}")
