# fastapi_backend/utils/media_converter.py
# Versão 16 17/07/2025 17:21
import re
from typing import Optional, Dict

def convert_google_drive_link(url: str, media_type: str = "view") -> str:
    """
    Converte um link de compartilhamento do Google Drive para um formato de
    download direto (para áudio/vídeo) ou visualização embutida (PDF).
    Se o link não for do Google Drive, ele é retornado sem alterações.
    """
    if not isinstance(url, str) or "drive.google.com" not in url:
        return url
    
    match = re.search(r'/file/d/([a-zA-Z0-9-_]+)', url)
    if not match:
        return url # Retorna a URL original se o padrão não for encontrado
    
    file_id = match.group(1)
    
    if media_type in ("audio", "video", "download"):
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    
    if media_type in ("view", "pdf"):
        return f"https://drive.google.com/file/d/{file_id}/preview"
        
    return url

def convert_youtube_link(url: str) -> Optional[Dict[str, str]]:
    """
    Extrai o ID de um vídeo do YouTube de vários formatos de URL e retorna
    um dicionário com a URL de embed e a URL da thumbnail.
    """
    if not isinstance(url, str) or "youtu" not in url:
        return None
    
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9-_]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9-_]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9-_]{11})',
    ]
    
    video_id = None
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            break
            
    if not video_id:
        return None
    
    return {
        "embed_url": f"https://www.youtube.com/embed/{video_id}",
        "thumbnail_url": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
    }

def process_media_urls(item_data: dict) -> dict:
    """
    Processa um dicionário de dados de um item, convertendo as URLs de mídia
    para formatos adequados e adicionando a URL da thumbnail do vídeo.
    """
    processed_data = item_data.copy()
    
    # Processa URL de áudio (Google Drive)
    if processed_data.get("audio_url"):
        processed_data["audio_url"] = convert_google_drive_link(processed_data["audio_url"], "audio")
    
    # Processa URL de vídeo (YouTube)
    if processed_data.get("video_url"):
        youtube_data = convert_youtube_link(processed_data["video_url"])
        if youtube_data:
            processed_data["video_url"] = youtube_data["embed_url"]
            # Adiciona a URL da thumbnail ao dicionário de dados processados.
            processed_data["video_thumbnail_url"] = youtube_data["thumbnail_url"]
    
    # Processa URL da partitura (PDF no Google Drive)
    if processed_data.get("sheet_music_url"):
        processed_data["sheet_music_url"] = convert_google_drive_link(processed_data["sheet_music_url"], "pdf")
    
    return processed_data
