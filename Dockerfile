# Escolha a imagem base
FROM python:3.13

# Instale o OpenCV
RUN pip install opencv-python-headless ultralytics requests

# Define variáveis de ambiente para geração de frames e configurações do YOLO
ENV LARGURA_IMAGEM=1280
ENV ALTURA_IMAGEM=720
ENV FOTOS_SEGUNDO=5

# Diretório base e subdiretórios
ENV BASE_PATH="/app"
ENV VOLUME_FRAME_PATH="${BASE_PATH}/volumeFrame"
ENV VOLUME_FRAME_TEMP_PATH="${VOLUME_FRAME_PATH}/temp"
ENV VOLUME_TREINAMENTO="${BASE_PATH}/volumeFrameTreinamento"
ENV VOLUME_YOLO="${BASE_PATH}/volumeYolo/best.pt"

# URL da API para enviar as imagens processadas
ENV SEND_IMAGE_TO_API_URL="http://localhost:8080/send/"

# Valores de precisão para detecção YOLO
ENV HIGH_PRECISION=0.75
ENV LOW_PRECISION=0.5

# Classe a ser detectada
ENV ID_CLASS_TO_DETECT=0

# Crie diretórios necessários
RUN mkdir -p ${VOLUME_FRAME_PATH} ${VOLUME_FRAME_TEMP_PATH} ${VOLUME_TREINAMENTO}

# Copie o código para o container
COPY /app /app

# Defina o diretório de trabalho
WORKDIR /app

# Execute o código ao iniciar o container
CMD ["python", "geracaoFrame_v2.py"]
