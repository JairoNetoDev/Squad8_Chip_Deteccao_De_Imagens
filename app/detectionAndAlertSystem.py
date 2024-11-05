# Instale a biblioteca YOLO
# pip install ultralytics

import os
import cv2
import threading
import requests
import base64
import shutil
import glob
from ultralytics import YOLO


# Definição dos caminhos, com variáveis de ambiente e valores padrão
BASE_PATH = os.getenv('BASE_PATH', '/app')
VOLUME_FRAME_PATH = os.path.join(BASE_PATH, 'volumeFrame')
VOLUME_FRAME_TEMP_PATH = os.path.join(VOLUME_FRAME_PATH, 'temp')
VOLUME_FRAME_TREINAMENTO = os.path.join(BASE_PATH, 'volumeFrameTreinamento')
VOLUME_YOLO = os.path.join(BASE_PATH, 'volumeYolo/best.pt')

# Valores de precisão, obtidos das variáveis de ambiente, com padrão
HIGH_PRECISION = float(os.getenv('HIGH_PRECISION', 0.75))
LOW_PRECISION = float(os.getenv('LOW_PRECISION', 0.5))
LARGURA_IMAGEM = float(os.getenv('LARGURA_IMAGEM', 1280))
ALTURA_IMAGEM = float(os.getenv('ALTURA_IMAGEM', 720))
SEND_IMAGE_TO_API_URL = os.getenv('SEND_IMAGE_TO_API_URL', 'http://localhost:8080/send/')
ID_CLASS_TO_DETECT = int(os.getenv('ID_CLASS_TO_DETECT', 0))

# Função para criar diretórios se não existirem
def existsDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

existsDirectory(VOLUME_FRAME_PATH)
existsDirectory(VOLUME_FRAME_TEMP_PATH)
existsDirectory(VOLUME_FRAME_TREINAMENTO)

# Mova as imagens para o diretório temporário
VOLUME_FRAME_IMAGES = os.path.join(VOLUME_FRAME_PATH, '*.jpg')
for image in glob.glob(VOLUME_FRAME_IMAGES):
    shutil.move(image, VOLUME_FRAME_TEMP_PATH)

# Carrega o modelo YOLO
MODEL = YOLO(VOLUME_YOLO)
VOLUME_FRAME_TEMP_IMAGES = os.path.join(VOLUME_FRAME_TEMP_PATH, '*.jpg')
IMAGES_FROM_MODEL = MODEL(VOLUME_FRAME_TEMP_IMAGES, imgz_size=(LARGURA_IMAGEM, ALTURA_IMAGEM))

# Definição da classe de imagem
class Image:
    def __init__(self, name, image, precision_type, precision):
        self.name = name
        self.image = image
        valid_types = ['medium', 'high']
        self.type = precision_type if precision_type in valid_types else 'low'
        self.precision = precision

    def formatImage(self):
        formatted_image = self.result.plot()
        return formatted_image

# Função para enviar imagem ao servidor
def send_image(image_data, file_name, precision):
    _, buffer = cv2.imencode('.jpg', image_data)
    image_base64 = base64.b64encode(buffer).decode('utf-8')

    payload = {
        "file_name": file_name,
        "image": image_base64,
        "precision": precision,
    }

    try:
        response = requests.post(SEND_IMAGE_TO_API_URL, json=payload)
        response.raise_for_status()
        print(f"Imagem enviada com sucesso: {file_name} / Status: {response.status_code}")
        print("Resposta da API:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar imagem: {file_name} / Erro: {e}")

# Função para salvar imagem original para treinamento
def save_original_image_for_training(image_data, file_name):
    cv2.imwrite(os.path.join(VOLUME_FRAME_TREINAMENTO, file_name), image_data)

# Função para deletar pasta temporária
def delete_volume_frame_temp(tempPath):
    if os.path.exists(tempPath):
        shutil.rmtree(tempPath)
        print(f"Pasta removida: {tempPath}")
    else:
        print(f"A pasta não existe: {tempPath}")

# Função principal de processamento de imagens
def process_images(images):
    for result in images:
        boxes = result.boxes
        file_path = result.path
        file_name = os.path.basename(file_path)
        original_image = result.orig_img

        if boxes:
            for box in boxes:
                class_id = box.cls.item()

                if class_id == ID_CLASS_TO_DETECT:
                    precision = box.conf.item() if box.conf.nelement() > 0 else 0

                    if precision >= HIGH_PRECISION:
                        formatted_image = result.plot()
                        image = Image(file_name, formatted_image, 'high', precision)
                        threading.Thread(target=send_image, args=(image.image, image.name, image.precision)).start()

                    elif LOW_PRECISION <= precision < HIGH_PRECISION:
                        save_original_image_for_training(original_image, file_name)

    delete_volume_frame_temp(VOLUME_FRAME_TEMP_PATH)

# Executa o processamento de imagens
process_images(IMAGES_FROM_MODEL)
