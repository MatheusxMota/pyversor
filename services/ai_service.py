import os
import httpx
from fastapi import HTTPException

HF_TOKEN = os.getenv("HF_TOKEN")

async def chamar_hugging_face_ia(nome_produto: str) -> str:
    """
    Envia o nome do produto para o modelo Llama 3.1 via Hugging Face.
    """
    if not HF_TOKEN:
        raise HTTPException(status_code=500, detail="Token do Hugging Face não configurado no arquivo .env")

    api_url = "https://router.huggingface.co/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Você é um copywriter focado em vendas rápidas no TikTok. Crie um texto de venda "
                    "ultra persuasivo com no máximo 25 palavras sobre o produto fornecido. Não use emojis, mas pode usar"
                    "gatilhos de escassez ou desejo. Responda APENAS com o texto de vendas, sem qualquer "
                    "introdução ou comentário."
                )
            },
            {
                "role": "user",
                "content": f"Produto: {nome_produto}"
            }
        ],
        "max_tokens": 80,
        "temperature": 0.6
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(api_url, headers=headers, json=payload)
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Erro de conexão com a Hugging Face: {str(e)}")

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"Erro na IA do Hugging Face ({response.status_code}): {response.text}"
        )

    dados_resposta = response.json()

    try:
        texto_final = dados_resposta["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError):
        raise HTTPException(status_code=500, detail=f"Resposta inesperada da IA: {dados_resposta}")

    return texto_final
