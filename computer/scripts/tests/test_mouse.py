import sys
import os

# Adiciona o diretório pai ao sys.path para importar corretamente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mouse import apply_color_mouse

# Cor de teste
cor_nome = "vermelho"
hex_cor = "#ff0000"

print(f"Testando cor: {cor_nome} ({hex_cor})")
apply_color_mouse(cor_nome, hex_cor)
