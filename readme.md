# Projeto de Detecção de Imagens

## Descrição do Projeto
Um projeto desenvolvido pelo Squad 8 para a Chip Tecnologia, proposto pelo Porto Digital e a Universidade Tiradentes.

## Passos de Instalação e Execução

### Clonando o Repositório
Para começar, clone o repositório para o seu ambiente local usando o comando:
```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_DIRETORIO_CLONADO>
```

### Subindo os Contêineres com Docker Compose
Certifique-se de ter o Docker e o Docker Compose instalados no seu sistema. Em seguida, execute:
```bash
docker-compose up --build
```
Isso irá criar e iniciar os três serviços do projeto: **geracao_frame**, **deteccao_e_alerta** e **treinamento_modelo**.

### Variáveis de Ambiente
As variáveis de ambiente utilizadas pelos serviços são:

#### **Geração de Frame**
- `PYTHONUNBUFFERED`: Garante que a saída do Python seja exibida imediatamente.
- `LINK_CAMERA`: URL da câmera conectada ao serviço.
- `LARGURA_IMAGEM`: Largura dos frames capturados.
- `ALTURA_IMAGEM`: Altura dos frames capturados.
- `FOTOS_SEGUNDO`: Número de frames capturados por segundo.

#### **Detecção de Imagens**
- `PYTHONUNBUFFERED`: Garante que a saída do Python seja exibida imediatamente.
- `ALTA_PRECISAO`: Limite mínimo para considerar uma detecção como de alta precisão.
- `BAIXA_PRECISAO`: Limite mínimo para considerar uma detecção como de baixa precisão.
- `LARGURA_IMAGEM` e `ALTURA_IMAGEM`: Dimensões da imagem processada.
- `URL_ENVIO_IMAGEM_API`: URL da API para envio das imagens detectadas.
- `ID_CLASSE_DETECTAR`: ID da classe que será detectada pelo modelo.

#### **Treinamento do Modelo**
- Não há variáveis de ambiente específicas no momento.

### Estrutura de Volumes
Os serviços compartilham volumes para armazenamento e comunicação:
- **`volumeFrame`**: Armazena os frames capturados pelo **Geração de Frame**.
- **`volumeFrameTreinamento`**: Armazena as imagens que necessitam de mais treinamento, alimentado pelo **Detecção de Imagens**.
- **`volumeYolo`**: Armazena o modelo treinado (`best.pt`), utilizado pelo serviço de **Detecção de Imagens**.

## Explicação de Cada Código e Funcionalidades

### Geração de Frame
Este código conecta-se a uma câmera para capturar frames de acordo com as configurações definidas nas variáveis de ambiente. Os frames capturados são armazenados no diretório compartilhado `volumeFrame`, permitindo que outros serviços os utilizem.

### Detecção de Imagens
Monitora o diretório `volumeFrame` e processa as imagens utilizando o modelo YOLO. O fluxo de trabalho é:
1. Detecta objetos nas imagens com base no modelo atual.
2. Para detecções de alta precisão, envia as imagens formatadas para uma API configurada.
3. Para detecções de baixa precisão, salva as imagens para treinamento no diretório `volumeFrameTreinamento`.
4. Atualiza automaticamente o modelo YOLO sempre que um novo arquivo `best.pt` é salvo no volume `volumeYolo`.

### Treinamento do Modelo
Consome imagens do diretório `volumeTreinamento` para treinar o modelo de IA. Após cada execução, salva o modelo mais recente (`best.pt`) no volume `volumeYolo`, permitindo que o serviço de **Detecção de Imagens** utilize a versão atualizada do modelo.

### Fluxo de Integração
1. O serviço **Geração de Frame** captura imagens e as salva no `volumeFrame`.
2. O serviço **Detecção de Imagens** processa os frames, enviando-os para uma API ou salvando para treinamento, dependendo da precisão.
3. O serviço **Treinamento do Modelo** utiliza as imagens do `volumeTreinamento` para treinar o modelo e salvar uma nova versão no `volumeYolo`, que é automaticamente carregada pelo serviço de **Detecção de Imagens**.

## Responsáveis pelo Código
- **João Victor Melo Fontes Linhares**: Responsável pelo Gerador de Frames.
- **Jairo Williams Guedes Lopes Neto**: Responsável pela Detecção de Imagens.
- **Jorge Vitor**: Responsável pelo Treinamento do Modelo.
