# Sistema de Detecção de Imagens com YOLO e Envio via API

Este projeto utiliza a biblioteca YOLO para detectar objetos em imagens, com um sistema de filtro de precisão para decidir se as imagens devem ser enviadas para uma API ou armazenadas para treinamento futuro.

## Funcionalidades

- **Organização de Imagens**: As imagens são movidas para um diretório temporário para facilitar o processamento.
- **Detecção de Objetos com YOLO**: Processa as imagens com YOLO para detectar uma classe específica de objetos.
- **Filtragem por Precisão**: Imagens com precisão alta são enviadas para uma API, e as de precisão média são armazenadas para treinamento.
- **Envio para API**: As imagens detectadas são enviadas para uma URL especificada.

## Pré-requisitos

1. **Python 3.7** ou superior.
2. **YOLO**: Instale a biblioteca YOLO utilizando o comando:
   ```bash
   pip install ultralytics
   ```
3. **Outras Dependências**:
   - `opencv-python`: Serve para manipulação de imagens.
   - `requests`: Utilizado para enviar imagens para a API.
   - `base64`: Codifica as imagens em base64.
   - `shutil`: Utilizado para mover arquivos.
   - `glob`: Serve para encontrar arquivos em um diretório.

## Configuração

Para configurar o projeto, defina as seguintes variáveis de ambiente, ou deixe-as com valores padrão:

- `BASE_PATH`: Caminho base do projeto (padrão: `C:/Deteccao-Yolo/`).
- `VOLUME_FRAME_PATH`: Caminho para o diretório onde as imagens de entrada são armazenadas (padrão: `BASE_PATH/volumeFrame`).
- `VOLUME_FRAME_TEMP_PATH`: Diretório temporário onde as imagens para processamento são movidas.
- `VOLUME_FRAME_TREINAMENTO`: Diretório para armazenar imagens para treinamento futuro (padrão: `BASE_PATH/volumeFrameTreinamento`).
- `VOLUME_YOLO`: Caminho para o modelo YOLO treinado (padrão: `BASE_PATH/volumeYolo/best.pt`).
- `SEND_IMAGE_TO_API_URL`: URL da API para onde as imagens detectadas serão enviadas (padrão: `http://localhost:8080/send/`).

### Variáveis de Precisão

- `HIGH_PRECISION`: Limite mínimo para alta precisão (padrão: `0.75`).
- `LOW_PRECISION`: Limite mínimo para precisão média (padrão: `0.5`).

## Estrutura do Código

### Principais Componentes

- **Classe `Image`**: Representa uma imagem detectada, contendo o nome, a imagem formatada e a precisão.
- **Função `send_image`**: Envia a imagem para a API no formato base64.
- **Função `process_images`**: Processa cada imagem para detectar objetos da classe especificada, aplicando o filtro de precisão.
- **Função `delete_volume_frame_temp`**: Limpa o diretório temporário após o processamento.

## Executando o Programa

1. Defina as variáveis de ambiente conforme necessário.
2. Coloque as imagens de entrada no diretório especificado em `VOLUME_FRAME_PATH`.
3. Execute o programa:

   ```bash
   python script.py
   ```

## Exemplo de Configuração de Variáveis de Ambiente

Você pode definir as variáveis diretamente no terminal ou em um arquivo `.env`:

```bash
export BASE_PATH="C:/Deteccao-Yolo"
export VOLUME_FRAME_PATH="${BASE_PATH}/volumeFrame"
export VOLUME_FRAME_TEMP_PATH="${VOLUME_FRAME_PATH}/temp"
export VOLUME_TREINAMENTO="${BASE_PATH}/volumeFrameTreinamento"
export VOLUME_YOLO="${BASE_PATH}/volumeYolo/best.pt"
export SEND_IMAGE_TO_API_URL="http://localhost:8080/send/"
export HIGH_PRECISION=0.8
export LOW_PRECISION=0.6

```

## Observações

- O programa utiliza `threading` para enviar imagens de forma assíncrona, permitindo o processamento de múltiplas imagens simultaneamente.
- O diretório temporário é removido automaticamente após o processamento.