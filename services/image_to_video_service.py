import os
import time
import numpy as np
from abc import ABC, abstractmethod
from PIL import Image, ImageFilter
from moviepy import ImageClip, CompositeVideoClip

TARGET_SIZE = (1080, 1920)  # largura, altura — formato TikTok/Reels 9:16
BLUR_RADIUS = 40


class BaseI2VProvider(ABC):
    @abstractmethod
    async def generate_video(self, image_path: str, output_path: str) -> str:
        pass


class KenBurnsMotionProvider(BaseI2VProvider):
    async def generate_video(self, image_path: str, output_path: str) -> str:
        print(f"INFO: Gerando clipe de vídeo estático para {image_path}")
        if not os.path.exists(image_path):
            raise Exception(f"Arquivo de imagem não encontrado: {image_path}")

        duration = 10
        target_w, target_h = TARGET_SIZE

        original = Image.open(image_path).convert("RGB")
        img_w, img_h = original.size

        # --- Camada de fundo: cobre o frame inteiro (cover) + blur ---
        cover_scale = max(target_w / img_w, target_h / img_h)
        bg_img = original.resize(
            (round(img_w * cover_scale), round(img_h * cover_scale)),
            Image.LANCZOS
        )
        left = (bg_img.width - target_w) / 2
        top = (bg_img.height - target_h) / 2
        bg_img = bg_img.crop((left, top, left + target_w, top + target_h))
        bg_img = bg_img.filter(ImageFilter.GaussianBlur(BLUR_RADIUS))
        background_clip = ImageClip(np.array(bg_img)).with_duration(duration)

        # --- Camada principal: cabe inteira no frame (contain), sem cortar nada ---
        fit_scale = min(target_w / img_w, target_h / img_h)
        foreground_clip = (
            ImageClip(image_path)
            .with_duration(duration)
            .resized(fit_scale)
            .with_position("center")
        )

        video_clip = CompositeVideoClip(
            [background_clip, foreground_clip],
            size=TARGET_SIZE
        )

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
