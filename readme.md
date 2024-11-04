Aqui está o README atualizado, incluindo alguns ajustes para refletir melhor as mudanças feitas no código:

---

# Sistema de Detecção de Imagens com YOLO e Envio via API

Este projeto utiliza a biblioteca YOLO para detectar objetos em imagens, aplicando um sistema de filtragem baseado na precisão para decidir se as imagens devem ser enviadas para uma API ou armazenadas para treinamento futuro.

## Funcionalidades

- **Organização de Imagens**: As imagens são movidas para um diretório temporário para facilitar o processamento.
- **Detecção de Objetos com YOLO**: Processa as imagens com YOLO para detectar uma classe específica de objetos.
- **Filtragem por Precisão**: Imagens com alta precisão são enviadas para uma API, enquanto as de precisão média são armazenadas para treinamento.
- **Envio para API**: As imagens detectadas são enviadas para uma URL especificada.

## Pré-requisitos

1. **Python 3.7** ou superior.
2. **YOLO**: Instale a biblioteca YOLO utilizando o comando:
   ```bash
   pip install ultralytics
   ```
3. **Outras Dependências**:
   - `opencv-python-headless`: Para manipulação de imagens.
   - `requests`: Para enviar imagens para a API.
   - `base64`: Para codificação de imagens em base64.
   - `shutil` e `glob`: Para manipulação de arquivos e diretórios.

Instale as dependências restantes com o comando:
   ```bash
   pip install opencv-python-headless requests
   ```

## Configuração

Para configurar o projeto, defina as seguintes variáveis de ambiente ou deixe-as com valores padrão. Elas podem ser configuradas diretamente no terminal, em um arquivo `.env`, ou no `Dockerfile`.

### Variáveis de Diretório

- `BASE_PATH`: Caminho base do projeto (padrão: `/app`).
- `VOLUME_FRAME_PATH`: Caminho para o diretório onde as imagens de entrada são armazenadas (padrão: `BASE_PATH/volumeFrame`).
- `VOLUME_FRAME_TEMP_PATH`: Diretório temporário para armazenar imagens durante o processamento.
- `VOLUME_FRAME_TREINAMENTO`: Diretório para salvar imagens para treinamento (padrão: `BASE_PATH/volumeFrameTreinamento`).
- `VOLUME_YOLO`: Caminho para o modelo YOLO treinado (padrão: `BASE_PATH/volumeYolo/best.pt`).
- `SEND_IMAGE_TO_API_URL`: URL da API para envio das imagens detectadas (padrão: `http://localhost:8080/send/`).

### Variáveis de Precisão

- `HIGH_PRECISION`: Limite mínimo para alta precisão (padrão: `0.75`).
- `LOW_PRECISION`: Limite mínimo para precisão média (padrão: `0.5`).
- `ID_CLASS_TO_DETECT`: ID da classe de objeto a ser detectada (padrão: `0`).

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
   python detectionAndAlertSystem.py
   ```

## Exemplo de Configuração de Variáveis de Ambiente

Você pode definir as variáveis diretamente no terminal ou em um arquivo `.env`:

```bash
export BASE_PATH="C:/Deteccao-Yolo"
export VOLUME_FRAME_PATH="${BASE_PATH}/volumeFrame"
export VOLUME_TREINAMENTO="${BASE_PATH}/volumeFrameTreinamento"
export VOLUME_YOLO="${BASE_PATH}/volumeYolo/best.pt"
export SEND_IMAGE_TO_API_URL="http://localhost:8080/send/"
export HIGH_PRECISION=0.8
export LOW_PRECISION=0.6
export ID_CLASS_TO_DETECT=0
```

## Observações

- O programa utiliza `threading` para envio assíncrono de imagens, permitindo o processamento paralelo de múltiplas imagens.
- O diretório temporário é automaticamente removido após o processamento, mantendo o ambiente limpo para futuras execuções.

---

Esse README fornece uma visão detalhada e atualizada do projeto, cobrindo as mudanças realizadas e instruindo sobre a configuração e execução no ambiente Docker.
