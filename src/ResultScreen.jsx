import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
  Legend
);

function ResultScreen({ prediction, onBack }) {
  const { predictedSales, logisticPrediction, probability } = prediction;

  const chartData = {
    labels: ['Predicción'],
    datasets: [
      {
        label: 'Unidades estimadas',
        data: [predictedSales],
        borderColor: '#00ffff',
        backgroundColor: 'rgba(0, 255, 255, 0.1)',
        fill: true,
        tension: 0.4,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { display: true },
      title: { display: false },
    },
    scales: { y: { beginAtZero: true } },
  };

  return (
    <div className="App">
      <h1>🎮 Panel de Resultados</h1>

      <div className="grid-result">
        {/* Modelo logístico */}
        <div className="result-box">
          <h2> IA Logística</h2>
          <p>¿Se venderá?: <strong>{logisticPrediction === 1 ? 'SÍ' : 'NO'}</strong></p>
          <p>Confianza: <strong>{(probability * 100).toFixed(2)}%</strong></p>
        </div>

        {/* Modelo de regresión */}
        <div className="result-box">
          <h2> Regresión SVR</h2>
          <p>Unidades estimadas: <strong>{predictedSales}</strong></p>
          <div className="chart-container">
            <Line data={chartData} options={chartOptions} />
          </div>
        </div>
      </div>

      <button onClick={onBack}>⬅ Volver</button>
    </div>
  );
}

export default ResultScreen;