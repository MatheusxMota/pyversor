# Pyversor - Automação de Vídeos para Vendas

O **Pyversor** é uma solução de engenharia para automação de criação de conteúdo audiovisual, desenhada especificamente para maximizar conversão em plataformas de mídia vertical como **TikTok**, **Instagram Reels** e **YouTube Shorts**.

## 🚀 Funcionalidades Principais

*   **Renderização Inteligente:** Sistema de composição de vídeo em duas camadas:
    *   **Background:** Imagem do produto com *cover* e efeito de *blur* para preenchimento total do frame 9:16.
    *   **Foreground:** Imagem original ajustada via *contain* para máxima visibilidade, sem cortes.
*   **Copywriting Orientado a Conversão:** Integração com LLMs (via Hugging Face) para criação de roteiros de vendas baseados na URL do produto.
*   **Engenharia de Áudio:** Sintetização de narração natural (Edge TTS) e mixagem inteligente com trilhas sonoras de fundo, incluindo suporte a *fades* automáticos.
*   **Legendas Dinâmicas:** Aplicação automática de legendas estilizadas no vídeo.

---

## 🛠️ Stack Tecnológica

*   **Linguagem:** Python 3.10+
*   **Web Framework:** FastAPI
*   **Vídeo & Áudio:** MoviePy & FFmpeg
*   **IA & NLP:** Hugging Face Transformers (Llama 3.1) & Microsoft Edge TTS

---

## ⚙️ Instalação e Configuração

### 1. Pré-requisitos
*   [FFmpeg](https://ffmpeg.org/) instalado e adicionado ao `PATH` do sistema.
*   Python 3.10 ou superior.

### 2. Preparação do Ambiente
```bash
# Clone o projeto
git clone <url-do-repositorio>
cd pyversor

# Configure o ambiente virtual e instale as dependências
python -m venv venv
# No Windows:
.\venv\Scripts\Activate.ps1
# No Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configuração de Variáveis
Crie um arquivo `.env` na raiz:
```env
HF_TOKEN=seu_token_huggingface_aqui
```

---

## 🖥️ Como Utilizar

1.  **Imagem do Produto:** Coloque a imagem em `imagens_produtos/` (nomeie como `image.*`).
2.  **Músicas:** Adicione arquivos `.mp3` ou `.wav` em `musicas/`.
3.  **Execução:**
    ```bash
    uvicorn app:app --reload
    ```
4.  **Endpoint API:** Acesse `http://127.0.0.1:8000/docs` para visualizar a interface Swagger e realizar testes via `POST /identificar-e-gerar-video/`.

---

## 🐛 Troubleshooting & Suporte

*   **Vídeo sem música:** Verifique os logs de saída do servidor (`DEBUG` e `ERRO`) ao realizar a requisição.
*   **Erro de renderização:** Certifique-se de que o FFmpeg está instalado corretamente (`ffmpeg -version` no terminal).
*   **Fonte da Legenda:** A fonte padrão é buscada em `assets/fonts/Roboto-Regular.ttf`.

---

## 📂 Estrutura do Projeto

*   `/services`: Contém a lógica de negócio principal (AI, Vídeo, Imagem).
*   `/utils`: Funções utilitárias auxiliares.
*   `/musicas`: Repositório de áudios de fundo.
*   `/app.py`: Entrada da API e rotas principais.
