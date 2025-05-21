const API = import.meta.env.VITE_API_URL;

export const fetchCombinedPrediction = async ({ productId, shopId, categoryId, price, month }) => {
  const payload = {
    item_id: parseInt(productId),
    shop_id: parseInt(shopId),
    item_category_id: parseInt(categoryId),
    item_price: parseFloat(price),
    month: parseInt(month),
  };

  const [forecastRes, logisticRes] = await Promise.all([
    fetch(`${API}/forecast_sales`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    }),
    fetch(`${API}/predict_sale_logistic`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    }),
  ]);

  if (!forecastRes.ok || !logisticRes.ok) {
    throw new Error('Error en una o ambas predicciones');
  }

  const forecastData = await forecastRes.json();
  const logisticData = await logisticRes.json();

  return {
    predictedSales: forecastData.predicted_sales,
    logisticPrediction: logisticData.prediction,
    probability: logisticData.probability,
  };
};
