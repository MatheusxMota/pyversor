import re
from urllib.parse import unquote
from fastapi import HTTPException

def extrair_produto_da_url_shopee(url: str) -> str:
    """
    Extrai o nome do produto direto do slug da URL da Shopee.
    """
    if "shopee." not in url:
        raise HTTPException(
            status_code=400,
            detail="Este link não parece ser da Shopee. No momento, apenas links da Shopee são suportados."
        )

    match = re.search(r"/([^/]+)-i\.\d+\.\d+", url)
    if not match:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível identificar o produto a partir da URL da Shopee."
        )

    slug = match.group(1)
    slug_decodificado = unquote(slug)
    titulo = slug_decodificado.replace("-", " ").strip()

    if not titulo:
        raise HTTPException(status_code=400, detail="Produto não identificado a partir da URL.")

    return titulo
