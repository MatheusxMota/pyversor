# Pyversor - Gerador Automatizado de Vídeos para Vendas

O **Pyversor** é uma solução completa para automatizar a criação de vídeos de alta conversão para TikTok, Reels e YouTube Shorts.

## 🚀 O que o Pyversor oferece
- **Arquitetura Moderna:** Vídeos renderizados com sistema de duas camadas (fundo desfocado e imagem centralizada em *contain*), garantindo visual limpo sem cortes indesejados.
- **Roteiros Inteligentes:** Criação de textos publicitários persuasivos utilizando o modelo Llama 3.1.
- **Voz Neural:** Narração natural com Microsoft Edge TTS.
- **Mixagem Profissional:** Integração automática de narração com trilhas sonoras de fundo.
- **Legendas Automáticas:** Adição de legendas legíveis e estilosas diretamente no vídeo.

---

## 🛠️ Requisitos de Sistema

- Python 3.10 ou superior
- FFmpeg (instalado e configurado no PATH)
- Token do Hugging Face (HF_TOKEN)

---

## ⚙️ Instalação e Execução

### 1. Configuração do Ambiente
```bash
# Clone o projeto e entre na pasta
cd C:/Users/matheus/Desktop/Pyversor

# Instale as dependências a partir do arquivo fornecido
pip install -r requirements.txt
```

### 2. Configuração
Crie um arquivo `.env` na raiz do projeto com o seu token:
```env
HF_TOKEN=seu_token_aqui
```

### 3. Execução
Inicie o servidor de desenvolvimento:
```bash
uvicorn app:app --reload
```

---

## 💡 Como Funciona
A aplicação recebe a URL de um produto, processa a imagem para o formato vertical (9:16), gera um roteiro, sintetiza o áudio, aplica efeitos de fundo, mixa a trilha sonora e gera um arquivo `.mp4` pronto para postagem.

*Mais informações sobre desenvolvimento podem ser encontradas em `DEVELOPMENT_NOTES.md`.*
