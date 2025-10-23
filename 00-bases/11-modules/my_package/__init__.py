
"""
¿Cuál es la diferencia entre módulo y paquete?

- Módulo → archivo .py.
- Paquete → carpeta que contiene uno o más módulos, y un archivo __init__.py (aunque en versiones recientes este archivo puede no ser obligatorio).
mi_paquete/
├── __init__.py
├── modulo1.py
└── modulo2.py
"""
from .math_utils import addition
from .messages import greet, bye
