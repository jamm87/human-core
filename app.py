from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai
import os

app = Flask(__name__)

# Configurar clave de OpenAI
oai_api_key = os.getenv("OPENAI_API_KEY")

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

        # Generar análisis con OpenAI
        if oai_api_key:
            openai.api_key = oai_api_key
            prompt = f"Analiza el siguiente contenido y evalúa su relación con la IA: {textos[:1000]}"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "Eres un experto en inteligencia artificial."},
                          {"role": "user", "content": prompt}]
            )
            analisis_ai = response["choices"][0]["message"]["content"]
        else:
            analisis_ai = "API Key no configurada."

        return {"criterios": criterios, "puntuacion": puntuacion, "analisis_ai": analisis_ai}
    
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