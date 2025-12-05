'use client'; // Lado del cliente para interacción del formulario

import { useState } from 'react';

export default function Home() {
  const [cedula, setCedula] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setResult(null);

    try {
      // Obtener datos de la ruta API (lado del servidor)
      const res = await fetch(`/api/search?cedula=${cedula}`);
      if (!res.ok) throw new Error('No encontrado');
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError('No se encontró información para esa cédula.');
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: 'auto' }}>
      <h1>Portal de Consulta por Cédula</h1>
      <form onSubmit={handleSearch}>
        <input
          type="text"
          value={cedula}
          onChange={(e) => setCedula(e.target.value)}
          placeholder="Ingrese la Cédula"
          style={{ padding: '10px', width: '100%', marginBottom: '10px' }}
          required
        />
        <button type="submit" style={{ padding: '10px', width: '100%' }}>Buscar</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {result && (
        <div style={{ marginTop: '20px', border: '1px solid #ccc', padding: '10px' }}>
          <p><strong>Consecutivo:</strong> {result.CONSECUTIVO}</p>
          <p><strong>Asociado:</strong> {result.ASOCIADO}</p>
          <p><strong>Cédula:</strong> {result.CEDULA}</p>
          <p><strong>Evento:</strong> {result.EVENTO}</p>
          <p><strong>Dirección:</strong> {result.DIRECCION}</p>
          <p><strong>Cant. de Sillas:</strong> {result['CANT. DE SILLAS']}</p>
          <p><strong>Asociación:</strong> {result.ASOCIACIÓN}</p>
        </div>
      )}
    </div>
  );
}