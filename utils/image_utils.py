import os

# Antes de gerar um novo vídeo, basta substituir esse arquivo pela imagem
# do produto atual (mantendo o nome "image", só mudando a extensão se precisar).
PASTA_IMAGENS_PRODUTOS = "imagens_produtos"
NOME_ARQUIVO_IMAGEM = "image"
EXTENSOES_ACEITAS = [".png", ".jpg", ".jpeg", ".webp"]

def buscar_imagem_local() -> str | None:
    """
    Procura, na pasta local de imagens do projeto, um arquivo com nome fixo.
    """
    if not os.path.isdir(PASTA_IMAGENS_PRODUTOS):
        os.makedirs(PASTA_IMAGENS_PRODUTOS, exist_ok=True)
        return None

    for extensao in EXTENSOES_ACEITAS:
        caminho_candidato = os.path.join(PASTA_IMAGENS_PRODUTOS, f"{NOME_ARQUIVO_IMAGEM}{extensao}")
        if os.path.exists(caminho_candidato):
            return caminho_candidato

    return None
