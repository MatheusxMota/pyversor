import os
import time
import asyncio
import httpx
from abc import ABC, abstractmethod

class BaseI2VProvider(ABC):
    @abstractmethod
    async def generate_video(self, image_path: str, output_path: str) -> str:
        pass

from moviepy import ImageClip, CompositeVideoClip, ColorClip
from services.video_effects import apply_ken_burns_effect

class KenBurnsMotionProvider(BaseI2VProvider):
    async def generate_video(self, image_path: str, output_path: str) -> str:
        print(f"INFO: Aplicando efeito Ken Burns localmente para {image_path}")
        if not os.path.exists(image_path):
            raise Exception(f"Arquivo de imagem não encontrado: {image_path}")

        # Duração padrão para o clipe gerado localmente (ajustável conforme necessidade)
        duration = 10 
        
        # Cria o clipe de imagem
        image_clip = ImageClip(image_path).with_duration(duration)
        
        # Aplica redimensionamento e efeito
        image_clip = image_clip.resized(width=1080 * 1.2)
        image_clip = apply_ken_burns_effect(image_clip, duration, zoom_factor=0.2)
        
        # Composição em fundo vertical (tamanho TikTok)
        base_vertical = ColorClip(size=(1080, 1920), color=(15, 15, 15), duration=duration)
        video_clip = CompositeVideoClip([base_vertical, image_clip.with_position('center')])
        
        # Exporta o clipe
        video_clip.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            logger=None
        )
        
        video_clip.close()
        
        return output_path

class ImageToVideoService:
    def __init__(self, provider: BaseI2VProvider):
        self.provider = provider
        
    async def generate(self, image_path: str, output_folder: str = "temp_videos") -> str:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            
        output_path = os.path.join(output_folder, f"ai_video_{int(time.time())}.mp4")
        return await self.provider.generate_video(image_path, output_path)
