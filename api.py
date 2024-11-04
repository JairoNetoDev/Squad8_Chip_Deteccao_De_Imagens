from flask import Flask, request, jsonify
import os
import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.json
    
    if 'image' not in data or 'file_name' not in data or 'precision' not in data:
        return jsonify({"error": "Dados inválidos. Certifique-se de enviar 'image', 'file_name' e 'precision'."}), 400

    image_data = data['image']
    file_name = data['file_name']
    precision = data['precision']

    # Decodifica a imagem base64
    image_bytes = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_bytes))

    # Salva a imagem
    image.save(os.path.join('uploads', file_name))

    print(f"Imagem recebida: {file_name} / Precisão: {precision}")
    return jsonify({"message": f"Imagem {file_name} recebida com sucesso!", "precision": precision}), 201

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)  # Cria a pasta 'uploads' se não existir
    app.run(debug=True)
