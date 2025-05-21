from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Cargar ambos modelos
regression_model = joblib.load('sales_model.pkl')
logistic_model = joblib.load('logistic_model.pkl')

# Variables esperadas por ambos modelos
expected_features = ['shop_id', 'item_id', 'item_category_id', 'month', 'item_price']

@app.route('/forecast_sales', methods=['POST'])
def forecast_sales():
    try:
        data = request.get_json()
        missing = [f for f in expected_features if f not in data]
        if missing:
            return jsonify({'error': f'Faltan variables: {", ".join(missing)}'}), 400

        input_values = [data[feature] for feature in expected_features]
        input_array = np.array([input_values])

        prediction = regression_model.predict(input_array)[0]

        return jsonify({'predicted_sales': round(float(prediction), 2)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_sale_logistic', methods=['POST'])
def predict_sale_logistic():
    try:
        data = request.get_json()
        missing = [f for f in expected_features if f not in data]
        if missing:
            return jsonify({'error': f'Faltan variables: {", ".join(missing)}'}), 400

        input_values = [data[feature] for feature in expected_features]
        input_array = np.array([input_values])

        prediction = logistic_model.predict(input_array)[0]
        probability = logistic_model.predict_proba(input_array)[0][int(prediction)]

        return jsonify({
            'prediction': int(prediction),
            'probability': round(float(probability), 4)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
