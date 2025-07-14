# Guia de Conversão de Mídia - Setor Musical MS

## 🎯 Objetivo

Este guia explica como o sistema converte automaticamente os links de mídia do Google Drive e YouTube para formatos reproduzíveis no site.

---

## 🔄 Conversões Implementadas

### 1. **Google Drive - Áudio**

**Problema:** Links do Google Drive não reproduzem diretamente
```
❌ Original: https://drive.google.com/file/d/1XRwHe9d8jJRqU3DxR49b4dkVID__douV/view
```

**Solução:** Conversão para download direto
```
✅ Convertido: https://drive.google.com/uc?export=download&id=1XRwHe9d8jJRqU3DxR49b4dkVID__douV
```

### 2. **Google Drive - PDF (Partituras)**

**Problema:** Links do Google Drive não exibem PDF em iframe
```
❌ Original: https://drive.google.com/file/d/1VGXRT8KwcrbxsCiRJb8Izu_GUnQkA662/view
```

**Solução:** Conversão para preview mode
```
✅ Convertido: https://drive.google.com/file/d/1VGXRT8KwcrbxsCiRJb8Izu_GUnQkA662/preview
```

### 3. **YouTube - Vídeos**

**Problema:** Links do YouTube não funcionam em embed
```
❌ Original: https://youtu.be/YWFoYaiGNWM
```

**Solução:** Conversão para embed player
```
✅ Convertido: https://www.youtube.com/embed/YWFoYaiGNWM
🖼️ Thumbnail: https://img.youtube.com/vi/YWFoYaiGNWM/maxresdefault.jpg
```

---

## 🛠️ Como Funciona

### Processo Automático

1. **Usuário cadastra mídia** com link original
2. **Sistema detecta** o tipo de link (Google Drive ou YouTube)
3. **Conversão automática** acontece no backend
4. **URLs convertidas** são salvas no banco
5. **Frontend usa** as URLs convertidas para reprodução

### Código de Conversão

```python
def convert_google_drive_link(url: str, media_type: str = "view") -> str:
    # Extrai o file ID do Google Drive
    file_id_match = re.search(r'/file/d/([a-zA-Z0-9-_]+)', url)
    file_id = file_id_match.group(1)
    
    if media_type == "audio":
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    elif media_type == "pdf":
        return f"https://drive.google.com/file/d/{file_id}/preview"
```

---

## 📋 Formatos Suportados

### Google Drive
- ✅ **Áudio:** MP3, WAV, M4A, OGG
- ✅ **Vídeo:** MP4, AVI, MOV, WMV
- ✅ **PDF:** Partituras e documentos
- ✅ **Imagens:** JPG, PNG, GIF

### YouTube
- ✅ **Vídeos:** Todos os formatos do YouTube
- ✅ **Playlists:** Suporte a vídeos individuais
- ✅ **Shorts:** Links curtos youtu.be

### Outros
- ✅ **Links diretos:** HTTP/HTTPS para qualquer mídia
- ✅ **Streaming:** URLs de serviços de streaming

---

## 🎵 Exemplos Práticos

### Cadastro de Repertório Coral

**Título:** Ave Maria - Schubert  
**Áudio:** `https://drive.google.com/file/d/1XRwHe9d8jJRqU3DxR49b4dkVID__douV/view`  
**Partitura:** `https://drive.google.com/file/d/1VGXRT8KwcrbxsCiRJb8Izu_GUnQkA662/view`  
**Vídeo:** `https://youtu.be/YWFoYaiGNWM`

**Resultado no Sistema:**
- 🎵 **Áudio reproduz** automaticamente no player
- 📄 **PDF abre** em visualizador integrado
- 🎬 **Vídeo reproduz** em player YouTube embed

### Cadastro de Agenda Orquestra

**Evento:** Ensaio Sinfonia nº 5 - Beethoven  
**Material:** `https://drive.google.com/file/d/ABC123/view`

**Resultado:**
- 📄 **Partitura disponível** para visualização
- 🔗 **Link original preservado** para referência

---

## ⚙️ Configuração Técnica

### Validação de URLs

O sistema valida automaticamente:
- ✅ **Formato correto** (http/https)
- ✅ **Domínios permitidos** (Google Drive, YouTube)
- ✅ **File IDs válidos** para Google Drive
- ✅ **Video IDs válidos** para YouTube

### Tratamento de Erros

```python
def validate_media_urls(item_data: dict) -> list:
    errors = []
    
    if "audio_url" in item_data and item_data["audio_url"]:
        if not item_data["audio_url"].startswith(("http://", "https://")):
            errors.append("URL de áudio deve começar com http:// ou https://")
    
    return errors
```

### Cache e Performance

- **URLs convertidas** são salvas no banco
- **Conversão única** por item cadastrado
- **Fallback** para URL original em caso de erro

---

## 🔧 Manutenção

### Logs de Conversão

```bash
# Verificar conversões realizadas
grep "media_converter" /var/log/fastapi.log

# Testar conversão manual
python3 utils/media_converter.py
```

### Atualização de Regras

Para adicionar novos tipos de mídia:

1. **Editar** `utils/media_converter.py`
2. **Adicionar** nova função de conversão
3. **Testar** com URLs de exemplo
4. **Deploy** da atualização

### Troubleshooting

**Problema:** Áudio não reproduz
- ✅ Verificar se URL foi convertida
- ✅ Testar URL convertida diretamente
- ✅ Verificar permissões do Google Drive

**Problema:** PDF não abre
- ✅ Verificar se arquivo é público no Google Drive
- ✅ Testar URL de preview diretamente
- ✅ Verificar se é realmente um PDF

**Problema:** Vídeo não carrega
- ✅ Verificar se vídeo é público no YouTube
- ✅ Testar URL de embed diretamente
- ✅ Verificar se Video ID foi extraído corretamente

---

## 📞 Suporte

### Comandos Úteis

```bash
# Testar conversão específica
python3 -c "
from utils.media_converter import convert_google_drive_link
print(convert_google_drive_link('SUA_URL_AQUI', 'audio'))
"

# Validar URLs em lote
python3 -c "
from utils.media_converter import validate_media_urls
data = {'audio_url': 'SUA_URL', 'sheet_music_url': 'SUA_URL'}
print(validate_media_urls(data))
"
```

### Contato Técnico

- **Arquivo:** `/utils/media_converter.py`
- **Testes:** `/tests/test_media_conversion.py`
- **Logs:** Disponíveis via API `/api/logs/media`

---

**Última Atualização:** 11 de Janeiro de 2025  
**Versão:** 1.0.1  
**Status:** Funcionando ✅

