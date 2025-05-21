from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Cargar el modelo entrenado
model = joblib.load('sales_model.pkl')

# Variables que espera el modelo (en orden)
expected_features = ['shop_id', 'item_id', 'item_category_id', 'month', 'item_price']

@app.route('/forecast_sales', methods=['POST'])
def forecast_sales():
    try:
        data = request.get_json()

        # Validar que estén todas las variables requeridas
        missing = [feature for feature in expected_features if feature not in data]
        if missing:
            return jsonify({'error': f'Faltan variables: {", ".join(missing)}'}), 400

        # Construir input en el mismo orden que el modelo espera
        input_values = [data[feature] for feature in expected_features]
        input_array = np.array([input_values])

        # Hacer la predicción
        prediction = model.predict(input_array)[0]

        return jsonify({
            'predicted_sales': round(float(prediction), 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
