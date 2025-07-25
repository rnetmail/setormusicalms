# fastapi_backend/crud/__init__.py
# Versão 02 25/07/2025 14:30

# Importa os módulos CRUD para que possam ser acessados através do pacote.
from . import user
from . import repertorio
from . import agenda
from . import recado
from . import historia
from . import galeria

# A lista __all__ define quais módulos são exportados quando se utiliza "from crud import *"
__all__ = [
    "user",
    "repertorio",
    "agenda",
    "recado",
    "historia",
    "galeria",
]
