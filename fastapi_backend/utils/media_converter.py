"""
Utilitário para conversão de links de mídia do Google Drive e YouTube
"""
import re
from typing import Optional

def convert_google_drive_link(url: str, media_type: str = "view") -> str:
    """
    Converte links do Google Drive para formatos reproduzíveis
    
    Args:
        url: URL original do Google Drive
        media_type: "view" para PDFs, "audio" para áudios, "video" para vídeos
    
    Returns:
        URL convertida para reprodução/visualização
    """
    if not url or "drive.google.com" not in url:
        return url
    
    # Extrair file ID do Google Drive
    file_id_match = re.search(r'/file/d/([a-zA-Z0-9-_]+)', url)
    if not file_id_match:
        return url
    
    file_id = file_id_match.group(1)
    
    if media_type == "view" or media_type == "pdf":
        # Para PDFs - visualização direta
        return f"https://drive.google.com/file/d/{file_id}/preview"
    elif media_type == "audio" or media_type == "video":
        # Para áudio/vídeo - download direto
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    else:
        # Padrão - visualização
        return f"https://drive.google.com/file/d/{file_id}/preview"

def convert_youtube_link(url: str) -> dict:
    """
    Converte links do YouTube para formatos reproduzíveis
    
    Args:
        url: URL original do YouTube
    
    Returns:
        Dict com URLs convertidas
    """
    if not url or "youtu" not in url:
        return {"original": url, "embed": url, "thumbnail": ""}
    
    # Extrair video ID do YouTube
    video_id = None
    
    # Formato youtu.be/VIDEO_ID
    if "youtu.be/" in url:
        video_id_match = re.search(r'youtu\.be/([a-zA-Z0-9-_]+)', url)
        if video_id_match:
            video_id = video_id_match.group(1)
    
    # Formato youtube.com/watch?v=VIDEO_ID
    elif "youtube.com/watch" in url:
        video_id_match = re.search(r'[?&]v=([a-zA-Z0-9-_]+)', url)
        if video_id_match:
            video_id = video_id_match.group(1)
    
    if not video_id:
        return {"original": url, "embed": url, "thumbnail": ""}
    
    return {
        "original": url,
        "embed": f"https://www.youtube.com/embed/{video_id}",
        "thumbnail": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
        "video_id": video_id
    }

def process_media_urls(item_data: dict) -> dict:
    """
    Processa todas as URLs de mídia em um item
    
    Args:
        item_data: Dados do item com URLs
    
    Returns:
        Dados processados com URLs convertidas
    """
    processed_data = item_data.copy()
    
    # Processar URL de áudio
    if "audio_url" in processed_data and processed_data["audio_url"]:
        audio_url = processed_data["audio_url"]
        if "drive.google.com" in audio_url:
            processed_data["audio_url"] = convert_google_drive_link(audio_url, "audio")
            processed_data["audio_url_original"] = audio_url
    
    # Processar URL de vídeo
    if "video_url" in processed_data and processed_data["video_url"]:
        video_url = processed_data["video_url"]
        if "youtu" in video_url:
            youtube_data = convert_youtube_link(video_url)
            processed_data["video_url"] = youtube_data["embed"]
            processed_data["video_url_original"] = video_url
            processed_data["video_thumbnail"] = youtube_data["thumbnail"]
        elif "drive.google.com" in video_url:
            processed_data["video_url"] = convert_google_drive_link(video_url, "video")
            processed_data["video_url_original"] = video_url
    
    # Processar URL de partitura
    if "sheet_music_url" in processed_data and processed_data["sheet_music_url"]:
        sheet_url = processed_data["sheet_music_url"]
        if "drive.google.com" in sheet_url:
            processed_data["sheet_music_url"] = convert_google_drive_link(sheet_url, "pdf")
            processed_data["sheet_music_url_original"] = sheet_url
    
    return processed_data

def validate_media_urls(item_data: dict) -> list:
    """
    Valida URLs de mídia e retorna lista de erros
    
    Args:
        item_data: Dados do item para validar
    
    Returns:
        Lista de erros encontrados
    """
    errors = []
    
    # Validar URL de áudio
    if "audio_url" in item_data and item_data["audio_url"]:
        audio_url = item_data["audio_url"]
        if not (audio_url.startswith("http") or audio_url.startswith("https")):
            errors.append("URL de áudio deve começar com http:// ou https://")
    
    # Validar URL de vídeo
    if "video_url" in item_data and item_data["video_url"]:
        video_url = item_data["video_url"]
        if not (video_url.startswith("http") or video_url.startswith("https")):
            errors.append("URL de vídeo deve começar com http:// ou https://")
    
    # Validar URL de partitura (obrigatória)
    if "sheet_music_url" in item_data:
        sheet_url = item_data["sheet_music_url"]
        if not sheet_url:
            errors.append("URL da partitura é obrigatória")
        elif not (sheet_url.startswith("http") or sheet_url.startswith("https")):
            errors.append("URL da partitura deve começar com http:// ou https://")
    
    return errors

# Exemplos de uso
if __name__ == "__main__":
    # Teste com links fornecidos
    audio_link = "https://drive.google.com/file/d/1XRwHe9d8jJRqU3DxR49b4dkVID__douV/view"
    pdf_link = "https://drive.google.com/file/d/1VGXRT8KwcrbxsCiRJb8Izu_GUnQkA662/view"
    video_link = "https://youtu.be/YWFoYaiGNWM"
    
    print("=== CONVERSÃO DE LINKS ===")
    print(f"Áudio original: {audio_link}")
    print(f"Áudio convertido: {convert_google_drive_link(audio_link, 'audio')}")
    print()
    print(f"PDF original: {pdf_link}")
    print(f"PDF convertido: {convert_google_drive_link(pdf_link, 'pdf')}")
    print()
    print(f"Vídeo original: {video_link}")
    print(f"Vídeo convertido: {convert_youtube_link(video_link)}")
