import os
import time
import cv2
import threading
import requests
import base64
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ultralytics import YOLO

# Configurações de Caminhos
BASE_PATH = os.path.join('Squad8_Chip_Deteccao_De_Imagens/app')
VOLUME_FRAME_PATH = os.path.join(BASE_PATH, 'volumeFrame')
VOLUME_FRAME_TEMP_PATH = os.path.join(VOLUME_FRAME_PATH, 'temp')
VOLUME_FRAME_TREINAMENTO = os.path.join(BASE_PATH, 'volumeFrameTreinamento')
VOLUME_YOLO = os.path.join(BASE_PATH, 'volumeYolo')

# Configurações de Ambiente
HIGH_PRECISION = float(os.getenv('HIGH_PRECISION', 0.75))
LOW_PRECISION = float(os.getenv('LOW_PRECISION', 0.5))
LARGURA_IMAGEM = float(os.getenv('LARGURA_IMAGEM', 1280))
ALTURA_IMAGEM = float(os.getenv('ALTURA_IMAGEM', 720))
SEND_IMAGE_TO_API_URL = os.getenv('SEND_IMAGE_TO_API_URL', 'http://127.0.0.1:5000/upload')
ID_CLASS_TO_DETECT = int(os.getenv('ID_CLASS_TO_DETECT', 0))
TIME_TO_UPDATE_MODEL = int(os.getenv('TIME_TO_UPDATE_MODEL', 3600))
TIME_TO_INSERT_INTO_TEMP = int(os.getenv('TIME_TO_INSERT_INTO_TEMP', 2))

# Função para obter o modelo mais recente
def get_latest_best():
    return max([os.path.join(VOLUME_YOLO, f) for f in os.listdir(VOLUME_YOLO)], key=os.path.getctime)

# Inicializa o modelo YOLO
def initialize_model():
    latest_model_path = get_latest_best()
    print(f"Carregando o modelo: {latest_model_path}")
    return YOLO(latest_model_path)

# Inicialização do modelo
MODEL = initialize_model()

# Funções Utilitárias
def exists_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

exists_directory(VOLUME_FRAME_PATH)
exists_directory(VOLUME_FRAME_TEMP_PATH)
exists_directory(VOLUME_FRAME_TREINAMENTO)

# Classe de Representação de Imagem
class Image:
    def __init__(self, name, image, precision_type, precision):
        self.name = name
        self.image = image
        valid_types = ['medium', 'high']
        self.type = precision_type if precision_type in valid_types else 'low'
        self.precision = precision

# Funções de Manipulação de Imagem
def move_images_from_volume_frame_to_temp(limit=10):
    count = 0
    for file_name in os.listdir(VOLUME_FRAME_PATH):
        if file_name.endswith('.jpg'):
            src_path = os.path.join(VOLUME_FRAME_PATH, file_name)
            dest_path = os.path.join(VOLUME_FRAME_TEMP_PATH, file_name)
            
            shutil.move(src_path, dest_path)
            print(f"Imagem movida para temp: {dest_path}")
            
            count += 1
            if count >= limit:
                break

def send_image_to_api(image_data, file_name, precision):
    _, buffer = cv2.imencode('.jpg', image_data)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    payload = {
        "file_name": file_name,
        "image": image_base64,
        "precision": precision,
    }
    try:
        requests.post(SEND_IMAGE_TO_API_URL, json=payload)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar imagem: {file_name} / Erro: {e}")

def save_original_image_for_training(image_data, file_name):
    cv2.imwrite(os.path.join(VOLUME_FRAME_TREINAMENTO, file_name), image_data)

def delete_volume_frame_temp(temp_path):
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
    exists_directory(temp_path)

# Processamento de Imagens
def process_images():
    global MODEL  # Garantir que o modelo seja atualizado dentro desta função
    print(get_latest_best())
    move_images_from_volume_frame_to_temp()
    images = MODEL(os.path.join(VOLUME_FRAME_TEMP_PATH, '*.jpg'))

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
                        threading.Thread(target=send_image_to_api, args=(image.image, image.name, image.precision)).start()
                    elif LOW_PRECISION <= precision < HIGH_PRECISION:
                        threading.Thread(target=save_original_image_for_training, args=(original_image, file_name)).start()

    delete_volume_frame_temp(VOLUME_FRAME_TEMP_PATH)

# Monitoramento de Alterações na Pasta YOLO
class VolumeYoloHandler(FileSystemEventHandler):
    def on_created(self, event):
        global MODEL
        if event.src_path.endswith(".pt"):
            time.sleep(TIME_TO_UPDATE_MODEL)
            MODEL = initialize_model() 

    def on_modified(self, event):
        global MODEL
        if event.src_path.endswith(".pt"):  
            time.sleep(TIME_TO_UPDATE_MODEL)  
            MODEL = initialize_model() 

# Configuração do Observador de Arquivos
volume_yolo_handler = VolumeYoloHandler()
observer = Observer()
observer.schedule(volume_yolo_handler, path=VOLUME_YOLO, recursive=False)
observer.start()

# Execução do Processamento de Imagens em Loop
try:
    while True:
        if any(file.endswith('.jpg') for file in os.listdir(VOLUME_FRAME_PATH)):
            process_images()
        time.sleep(TIME_TO_INSERT_INTO_TEMP)
except KeyboardInterrupt:
    observer.stop()
observer.join()
