from moviepy import ImageClip

def apply_ken_burns_effect(image_clip: ImageClip, duration: float, zoom_factor: float = 0.2) -> ImageClip:
    """
    Aplica um efeito de zoom lento (Ken Burns) em um ImageClip.
    
    Args:
        image_clip: O clipe de imagem do MoviePy.
        duration: Duração total do clipe.
        zoom_factor: Quanto aumentar o zoom ao longo do tempo (0.2 = 20% de aumento).
        
    Returns:
        Um novo ImageClip com a transformação de zoom aplicada.
    """
    
    def zoom_func(t):
        # Aumenta o zoom de 1.0 (original) até 1.0 + zoom_factor
        return 1.0 + zoom_factor * (t / duration)

    # Aplica o redimensionamento baseado na função de tempo
    return image_clip.resized(zoom_func)
