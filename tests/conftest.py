# Ajuste de path para permitir 'import core' durante tests sin instalación editable explícita.
import sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))
