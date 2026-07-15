import time
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from utils.shopee_utils import extrair_produto_da_url_shopee
from utils.image_utils import buscar_imagem_local
from services.ai_service import chamar_hugging_face_ia
from services.video_service import criar_video_tiktok

app = FastAPI(title="Gerador de Vídeos Automatizado - Imagem Local")

class LinkInput(BaseModel):
    url: str

@app.post("/identificar-e-gerar-video/")
async def identificar_e_gerar_video(input_dados: LinkInput):
    """
    Fluxo completo: extrai nome da URL, busca a imagem, gera a copy via IA e gera o vídeo.
    """
    # 1. Extrai o nome do produto
    produto_identificado = extrair_produto_da_url_shopee(input_dados.url)

    # 2. Busca a imagem "atual" na pasta local
    imagem_local_path = buscar_imagem_local()

    # 3. Obtém a copy da IA
    texto_vendas = await chamar_hugging_face_ia(produto_identificado)

    # 4. Gera o arquivo de vídeo
    nome_saida_video = f"video_{int(time.time())}.mp4"
    video_gerado_path = await criar_video_tiktok(
        texto=texto_vendas,
        imagem_path=imagem_local_path,
        output_filename=nome_saida_video
    )

    # 5. Retorna o vídeo
    return FileResponse(
        path=video_gerado_path,
        media_type="video/mp4",
        filename=nome_saida_video
    )
