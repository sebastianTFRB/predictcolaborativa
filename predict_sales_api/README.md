Predict Future Sales - Backend API
Este proyecto implementa dos modelos de machine learning para predecir ventas de productos electrónicos utilizando Flask como framework de backend. El entrenamiento se realiza a partir del dataset de Kaggle: "Predict Future Sales".

POST http://localhost:5000/forecast_sales
POST http://localhost:5000/predict_sale_logistic


Estructura del proyecto
kotlin
Copiar
Editar
proyecto/
├── data/
│   ├── sales_train.js
│   ├── items.js
│   ├── shops.csv
│   ├── item_categories.csv
│   └── test.csv
├── model/
│   ├── logistic_model.pkl
│   └── sales_model.pkl
├── predictorLOG.py
├── predictorREG.py
├── train_model.py
├── train_logistic.py
└── README.md
Requisitos
Python 3.8 o superior

pip

Instalación de dependencias
nginx
Copiar
Editar
pip install -r requirements.txt
Si no tienes requirements.txt, instala manualmente:

nginx
Copiar
Editar
pip install pandas numpy scikit-learn flask joblib
Entrenamiento de modelos
Modelo de regresión (SVR)
nginx
Copiar
Editar
python train_model.py
Este script entrena un modelo de regresión que estima el número de unidades vendidas. El modelo se guarda como model/sales_model.pkl.

Modelo de regresión logística
nginx
Copiar
Editar
python train_logistic.py
Este script entrena un modelo de clasificación binaria que predice si un producto se venderá o no. El modelo se guarda como model/logistic_model.pkl.

Servidores Flask
Predictor de ventas (regresión)
nginx
Copiar
Editar
python predictorREG.py
Puerto: 5001

Endpoint: /forecast_sales

Método: POST

csvON de entrada:

json
Copiar
Editar
{
  "shop_id": 5,
  "item_id": 5037,
  "item_category_id": 19,
  "month": 11,
  "item_price": 999.0
}
Respuesta:

json
Copiar
Editar
{
  "predicted_sales": 2.75
}
Clasificación de venta (regresión logística)
nginx
Copiar
Editar
python predictorLOG.py
Puerto: 5000

Endpoint: /predict_sale_logistic

Método: POST

JSON de entrada:

json
Copiar
Editar
{
  "shop_id": 5,
  "item_id": 5037,
  "item_category_id": 19,
  "month": 11,
  "item_price": 999.0
}
Respuesta:

json
Copiar
Editar
{
  "prediction": 1,
  "probability": 0.9957
}