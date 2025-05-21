import { useState } from 'react';
import FormScreen from './FormScreen';
import ResultScreen from './ResultScreen';
import { fetchCombinedPrediction } from './services/api';

function App() {
  const [prediction, setPrediction] = useState(null);

  const handleSubmit = async ({ productId, shopId, categoryId, price, month }) => {
    try {
      const result = await fetchCombinedPrediction({ productId, shopId, categoryId, price, month });
      setPrediction(result);
    } catch (err) {
      console.error('Error en la predicción:', err);
      setPrediction('Error');
    }
  };

  const handleBack = () => setPrediction(null);

  return prediction ? (
    <ResultScreen prediction={prediction} onBack={handleBack} />
  ) : (
    <FormScreen onSubmit={handleSubmit} />
  );
}

export default App;
