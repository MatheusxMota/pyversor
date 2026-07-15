# Pyversor - Gerador Automatizado de Vídeos para Vendas (TikTok & Reels)

O **Pyversor** é uma API desenvolvida com **FastAPI** para automatizar a criação de vídeos de vendas em formato vertical (9:16) perfeitos para TikTok, Instagram Reels e YouTube Shorts.

A aplicação extrai o nome de um produto a partir de um link da Shopee, gera um texto publicitário curto e persuasivo de alta conversão usando o modelo **Llama 3.1** (via Hugging Face), cria uma narração com voz neural humanizada usando o **Microsoft Edge TTS**, aplica animação de zoom/pan (Ken Burns) localmente na imagem do produto, mixa com uma trilha sonora de fundo e compila o vídeo final.

---

## 🛠️ Requisitos

Antes de iniciar, certifique-se de ter os seguintes pré-requisitos instalados em sua máquina:

1. **Python 3.10 ou superior**
2. **FFmpeg** instalado no sistema e adicionado às variáveis de ambiente (necessário para que o `moviepy` processe áudio e vídeo).
3. **Token do Hugging Face** (HF_TOKEN) com permissão para realizar inferências de chat. Você pode obter um gratuitamente em [Hugging Face Settings](https://huggingface.co/settings/tokens).

---

## 🚀 Instalação e Configuração

### 1. Clonar ou Acessar a Pasta do Projeto
Abra o terminal no diretório do projeto:
```bash
cd C:/Users/matheus/Desktop/Pyversor
```

### 2. Ativar o Ambiente Virtual (`venv`)
Se o ambiente virtual ainda não estiver ativo, ative-o:

**No Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```
**No Windows (Prompt de Comando):**
```cmd
.\venv\Scripts\activate.bat
```

### 3. Instalar as Dependências
Instale os pacotes necessários:
```bash
pip install fastapi uvicorn httpx pydantic python-dotenv edge-tts moviepy
```

### 4. Configurar as Variáveis de Ambiente
No diretório raiz do projeto, edite ou crie o arquivo `.env` e insira o seu Token do Hugging Face:
```env
HF_TOKEN=seu_token_aqui
```

---

## 💻 Como Utilizar a Aplicação

### Passo 1: Preparar a Imagem do Produto
1. Vá até a pasta `imagens_produtos/`.
2. Substitua o arquivo existente pela imagem do produto que deseja anunciar.
3. Nomeie a imagem como `image` (por exemplo: `image.png`, `image.jpg`, `image.jpeg` ou `image.webp`).
   > *Nota: O sistema identificará automaticamente a extensão.*

### Passo 2: Adicionar Músicas de Fundo
1. Vá até a pasta `musicas/`.
2. Adicione arquivos de áudio (formato `.mp3` ou `.wav`) que possuam licença de uso comercial livre.
3. O sistema selecionará automaticamente uma dessas faixas para mixar com a narração.

### Passo 3: Configurar Fonte para Legendas
1. Vá até a pasta `assets/fonts/`.
2. Adicione um arquivo de fonte no formato `.ttf` ou `.otf`.
3. Renomeie o arquivo para `Roboto-Regular.ttf` ou atualize o caminho da fonte em `services/video_service.py` (`font_path`).
   > *Nota: Se nenhuma fonte for encontrada, o sistema gerará o vídeo sem a legenda.*

### Passo 4: Iniciar o Servidor FastAPI
Execute o comando a seguir no terminal para iniciar o servidor de desenvolvimento:
```bash
uvicorn app:app --reload
```
O servidor estará rodando em `http://127.0.0.1:8000`.

### Passo 4: Enviar a Requisição de Geração de Vídeo
Você pode fazer uma requisição `POST` para o endpoint `/identificar-e-gerar-video/`.

#### Exemplo de Requisição (JSON Payload)
**Endpoint:** `POST http://127.0.0.1:8000/identificar-e-gerar-video/`

**Corpo da Requisição (Body):**
```json
{
  "url": "https://shopee.com.br/Garrafa-Térmica-Inox-500ml-Com-Sensor-De-Temperatura-Led-i.38274193.847192847"
}
```

O servidor irá:
1. Extrair o termo `"Garrafa Térmica Inox 500ml Com Sensor De Temperatura Led"`.
2. Chamar o Llama 3.1 para gerar o roteiro publicitário.
3. Sintetizar a voz neural.
4. Animar a imagem localmente (zoom/pan) e mixar com a trilha sonora.
5. Renderizar o vídeo final e retornar o arquivo `.mp4` pronto para download.

---

## ⚙️ Configurações Customizáveis no Código

No arquivo `app.py`, você pode ajustar parâmetros fixos no topo do código:

* **`VOZ_NARRACAO`**: Voz neural utilizada para ler o texto. Padrão: `"pt-BR-FranciscaNeural"`. Para voz masculina, mude para `"pt-BR-AntonioNeural"`.
* **`VELOCIDADE_FALA`**: Ajusta o ritmo da fala. Padrão: `"-8%"` (mais calma e natural para vídeos de vendas).
* **`TOM_FALA`**: Ajusta a tonalidade. Padrão: `"+0Hz"`.
