from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Cargar modelo entrenado
model = joblib.load('logistic_model.pkl')

# Variables requeridas
expected_features = ['shop_id', 'item_id', 'item_category_id', 'month', 'item_price']

@app.route('/predict_sale_logistic', methods=['POST'])
def predict_sale():
    try:
        data = request.get_json()

        # Validar presencia de todas las variables
        if not all(feature in data for feature in expected_features):
            return jsonify({'error': 'Faltan variables. Se requieren: ' + ', '.join(expected_features)}), 400

        # Extraer valores en el orden correcto
        input_values = [data[feature] for feature in expected_features]
        input_array = np.array([input_values])  # Convertir a array 2D

        # Predecir
        prediction = model.predict(input_array)[0]
        probability = model.predict_proba(input_array)[0][int(prediction)]

        return jsonify({
            'prediction': int(prediction),
            'probability': round(probability, 4)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
