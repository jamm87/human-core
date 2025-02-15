from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Función para analizar el contenido de una web y extraer información
def analizar_web(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraer el texto visible
        textos = soup.get_text().lower()

        # Criterios de evaluación
        criterios = {
            "menciona ia": "inteligencia artificial" in textos or "AI" in textos,
            "contenido generado": "generado por ia" in textos or "contenido automático" in textos,
            "uso de automatización": "automatización" in textos or "machine learning" in textos
        }

        # Calcular puntuación
        puntuacion = sum(criterios.values()) * 33  # Máximo 100

        return {"criterios": criterios, "puntuacion": puntuacion}
    
    except Exception as e:
        return {"error": str(e)}

# Ruta API para analizar una web
@app.route('/analizar', methods=['GET'])
def analizar():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL requerida"}), 400
    
    resultado = analizar_web(url)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
