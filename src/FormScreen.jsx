import { useState } from 'react';

function FormScreen({ onSubmit }) {
  const [month, setMonth] = useState('');

  const [productId, setProductId] = useState('');
  const [shopId, setShopId] = useState('');
  const [categoryId, setCategoryId] = useState('');
  const [price, setPrice] = useState('');
  const [date, setDate] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = () => {
    if (!productId || !shopId || !categoryId || !price || !month) {
      setError('Por favor, complete todos los campos.');
      return;
    }

    setError('');

    onSubmit({
      productId,
      shopId,
      categoryId,
      price,
      month,
    });
  };

  return (
    <div className="App">
      <h1>Predicción de Ventas de Productos Electrónicos</h1>
      {error && <p className="error-message">{error}</p>}

      <div className="form-container">
        <div className="input-fields-container">
          <div className="form-group">
            <label>ID del Producto:</label>
            <input
              type="number"
              value={productId}
              onChange={(e) => setProductId(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label>ID de la Tienda:</label>
            <input
              type="number"
              value={shopId}
              onChange={(e) => setShopId(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label>ID de Categoría:</label>
            <input
              type="number"
              value={categoryId}
              onChange={(e) => setCategoryId(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label>Precio del Producto:</label>
            <input
              type="number"
              step="0.01"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
            />
          </div>

                    <div className="form-group">
            <label>Mes:</label>
            <select value={month} onChange={(e) => setMonth(e.target.value)}>
              <option value="">Seleccionar mes</option>
              <option value="1">Enero</option>
              <option value="2">Febrero</option>
              <option value="3">Marzo</option>
              <option value="4">Abril</option>
              <option value="5">Mayo</option>
              <option value="6">Junio</option>
              <option value="7">Julio</option>
              <option value="8">Agosto</option>
              <option value="9">Septiembre</option>
              <option value="10">Octubre</option>
              <option value="11">Noviembre</option>
              <option value="12">Diciembre</option>
            </select>
          </div>

          <button type="button" onClick={handleSubmit}>
            Obtener Predicción
          </button>
        </div>
      </div>
    </div>
  );
}

export default FormScreen;
