import os
import time
import random
from fastapi import HTTPException
import edge_tts
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip, VideoFileClip, CompositeAudioClip, vfx, afx
from services.image_to_video_service import ImageToVideoService, KenBurnsMotionProvider

# Configurações de VOZ/FALA
VOZ_NARRACAO = "pt-BR-FranciscaNeural"
VELOCIDADE_FALA = "-8%"
TOM_FALA = "+0Hz"

def selecionar_musica_fundo() -> str | None:
    """Seleciona uma música aleatória da pasta 'musicas/'."""
    pasta = "musicas"
    if not os.path.exists(pasta):
        return None
    
    arquivos = [os.path.join(pasta, f) for f in os.listdir(pasta) if f.endswith(('.mp3', '.wav'))]
    return random.choice(arquivos) if arquivos else None

async def criar_video_tiktok(texto: str, imagem_path: str, output_filename: str) -> str:
    """
    Cria o vídeo com imagem animada localmente, áudio gerado via edge-tts, música de fundo e legenda.
    """
    audio_path = f"temp_audio_{int(time.time())}.mp3"
    video_final = None

    try:
        # 1. Gerar áudio narração
        comunicador = edge_tts.Communicate(
            text=texto,
            voice=VOZ_NARRACAO,
            rate=VELOCIDADE_FALA,
            pitch=TOM_FALA
        )
        await comunicador.save(audio_path)
        narration_clip = AudioFileClip(audio_path)
        duracao = narration_clip.duration

        # 2. Gerar o clipe de vídeo com Ken Burns localmente
        provider = KenBurnsMotionProvider()
        ai_service = ImageToVideoService(provider=provider)
        
        # O provider local já gera um arquivo de vídeo.
        video_path = await ai_service.generate(imagem_path)
        video_clip = VideoFileClip(video_path)
        fundo_clip = video_clip.with_effects([vfx.Loop(duration=duracao)])

        # 3. Legenda
        try:
            # Tenta carregar uma fonte local; se não existir, usa padrão do sistema ou falha controlada
            font_path = "assets/fonts/Roboto-Regular.ttf"
            if not os.path.exists(font_path):
                raise FileNotFoundError(f"Fonte não encontrada: {font_path}")
            
            texto_clip = TextClip(
                text=texto,
                font_size=46,
                color='white',
                font=font_path,
                method='caption',
                size=(950, None),
                stroke_color='black',
                stroke_width=2
            ).with_start(0).with_duration(duracao).with_position(('center', 1400))

            video_final = CompositeVideoClip([fundo_clip, texto_clip])
        except Exception as e:
            print(f"Aviso ao renderizar texto: {e}. Usando fallback apenas com o fundo.")
            video_final = CompositeVideoClip([fundo_clip])

        # 4. Mixagem de Áudio (Narração + Música)
        musica_path = selecionar_musica_fundo()
        print(f"DEBUG: Musica selecionada: {musica_path}")
        if musica_path:
            try:
                music_clip = AudioFileClip(musica_path)
                print(f"DEBUG: Musica carregada: {musica_path}, duracao: {music_clip.duration}")
                
                # Ajuste de volume e duração
                music_clip = music_clip.with_volume_scaled(0.15).subclipped(0, duracao)
                
                # Fade-out nos últimos 1.5s
                if duracao > 2.0:
                    music_clip = music_clip.with_effects([afx.AudioFadeOut(1.5)])
                
                final_audio = CompositeAudioClip([narration_clip, music_clip])
                print("DEBUG: Audio mixado com musica.")
            except Exception as e:
                print(f"ERRO: Falha ao carregar musica: {e}")
                final_audio = narration_clip
        else:
            print("DEBUG: Nenhuma musica encontrada.")
            final_audio = narration_clip
            
        video_final = video_final.with_audio(final_audio)

        # 5. Exportação
        video_final.write_videofile(
            output_filename,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            logger=None
        )

        # Limpeza
        video_final.close()
        narration_clip.close()
        video_clip.close()
        if 'music_clip' in locals():
            music_clip.close()

        time.sleep(0.5)
        if os.path.exists(audio_path):
            os.remove(audio_path)
        if os.path.exists(video_path):
            os.remove(video_path)

        return output_filename

    except Exception as e:
        # Tenta fechar clips em caso de erro
        if 'video_final' in locals() and video_final:
            video_final.close()
        
        raise HTTPException(status_code=500, detail=f"Erro na renderização do vídeo: {str(e)}")
