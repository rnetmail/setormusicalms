# fastapi_backend/utils/media_converter.py
# Versão 20 16/07/2025 22:18
import re
from typing import Optional, Dict

def convert_google_drive_link(url: str, media_type: str = "view") -> str:
    """
    Converte links do Google Drive para formatos de visualização ou download direto.
    """
    if not url or "drive.google.com" not in url:
        return url
    
    # Extrai o ID do ficheiro do URL do Google Drive
    file_id_match = re.search(r'/file/d/([a-zA-Z0-9-_]+)', url)
    if not file_id_match:
        return url
    
    file_id = file_id_match.group(1)
    
    # URL para download direto (usado para áudio)
    if media_type in ("audio", "video", "download"):
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    
    # URL para visualização embutida (iframe para PDFs/Vídeos)
    if media_type in ("view", "pdf"):
        return f"https://drive.google.com/file/d/{file_id}/preview"
        
    return url

def convert_youtube_link(url: str) -> Dict[str, str]:
    """
    Converte um link do YouTube para um formato 'embed' e extrai a thumbnail.
    """
    if not url or "youtu" not in url:
        return {"original": url, "embed": url, "thumbnail": ""}
    
    video_id = None
    # Tenta extrair o ID de diferentes formatos de URL do YouTube
    patterns = [
        r'youtu\.be/([a-zA-Z0-9-_]+)',
        r'watch\?v=([a-zA-Z0-9-_]+)',
        r'embed/([a-zA-Z0-9-_]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            break
            
    if not video_id:
        return {"original": url, "embed": url, "thumbnail": ""}
    
    return {
        "original": url,
        "embed": f"https://www.youtube.com/embed/{video_id}",
        "thumbnail": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
        "video_id": video_id
    }

def process_media_urls(item_data: dict) -> dict:
    """
    Aplica as conversões de URL para todos os campos de mídia relevantes num dicionário.
    """
    processed_data = item_data.copy()
    
    # Processa URL de áudio (Google Drive)
    if "audio_url" in processed_data and processed_data.get("audio_url"):
        processed_data["audio_url"] = convert_google_drive_link(processed_data["audio_url"], "audio")
    
    # Processa URL de vídeo (YouTube)
    if "video_url" in processed_data and processed_data.get("video_url"):
        if "youtu" in processed_data["video_url"]:
            youtube_data = convert_youtube_link(processed_data["video_url"])
            processed_data["video_url"] = youtube_data["embed"]
            # Poderíamos adicionar a thumbnail aos dados aqui se o modelo a suportasse
            # processed_data["video_thumbnail"] = youtube_data["thumbnail"]
    
    # Processa URL da partitura (PDF no Google Drive)
    if "sheet_music_url" in processed_data and processed_data.get("sheet_music_url"):
        processed_data["sheet_music_url"] = convert_google_drive_link(processed_data["sheet_music_url"], "pdf")
    
    return processed_data
