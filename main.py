from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse  # Agrega JSONResponse para depuración
import json
from pathlib import Path

app = FastAPI()

# Cargar datos una vez al inicio
data_path = Path(__file__).parent / "data.json"
with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    print("Datos cargados exitosamente:")  # Log para verificar carga
    print(json.dumps(data, indent=4))  # Imprime todo el JSON para inspeccionar

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Página principal (sin cambios)
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Portal de Consulta por Cédula</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; }
            input, button { padding: 10px; width: 100%; margin-bottom: 10px; }
            .result { margin-top: 20px; border: 1px solid #ccc; padding: 10px; }
        </style>
    </head>
    <body>
        <h1>Portal de Consulta por Cédula</h1>
        <form action="/search" method="get">
            <input type="text" name="cedula" placeholder="Ingrese la Cédula" required>
            <button type="submit">Buscar</button>
        </form>
    </body>
    </html>
    """

@app.get("/search")
async def search(cedula: str = Query(...)):
    print(f"Cédula recibida: '{cedula}'")  # Log para ver qué llega exactamente
    # Buscar la fila coincidente, ignorando espacios y case (por si acaso)
    match = next((row for row in data if row.get("CEDULA", "").strip() == cedula.strip()), None)
    print(f"Coincidencia encontrada: {match}")  # Log para ver si hay match

    if not match:
        return JSONResponse({"error": "No se encontró información para esa cédula."})

    # Si quieres devolver HTML en lugar de JSON (para ver resultados en el navegador):
    result_html = f"""
    <div class="result">
        <p><strong>Consecutivo:</strong> {match.get('CONSECUTIVO', 'N/A')}</p>
        <p><strong>Asociado:</strong> {match.get('ASOCIADO', 'N/A')}</p>
        <p><strong>Cédula:</strong> {match.get('CEDULA', 'N/A')}</p>
        <p><strong>Evento:</strong> {match.get('EVENTO', 'N/A')}</p>
        <p><strong>Dirección:</strong> {match.get('DIRECCION', 'N/A')}</p>
        <p><strong>Cant. de Sillas:</strong> {match.get('CANT. DE SILLAS', 'N/A')}</p>
        <p><strong>Asociación:</strong> {match.get('ASOCIACIÓN', 'N/A')}</p>
    </div>
    """
    return HTMLResponse(result_html)