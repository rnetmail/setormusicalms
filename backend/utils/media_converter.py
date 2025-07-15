# setormusicalms/backend/utils/media_converter.py
import re

def convert_google_drive_link(url: str, media_type: str = "view") -> str:
    """
    Converte um link de compartilhamento do Google Drive para um link de
    visualização direta ou download.

    Args:
        url (str): O URL de compartilhamento do Google Drive.
        media_type (str): O tipo de link a ser gerado. Pode ser 'view'
                          para visualização ou 'download' para baixar.

    Returns:
        str: O URL convertido. Se o formato do URL de entrada for inválido,
             retorna o URL original.
    """
    # Regex para extrair o ID do arquivo do link do Google Drive
    match = re.search(r"/file/d/([a-zA-Z0-9_-]+)", url)
    if not match:
        return url  # Retorna o URL original se não encontrar o ID

    file_id = match.group(1)

    if media_type == "download":
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    
    # O padrão é o link de visualização direta
    return f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"

