import time
import requests
from scripts.keyboard import apply_color_keyboard
from scripts.mouse import apply_color_mouse

# Dicionário de cores
map_colors = {
    "vermelho": "#ff0000",
    "azul": "#0000ff",
    "verde": "#00ff00",
    "roxo": "#800080"
}

try:
    response = requests.get("http://localhost:5000/cor", timeout=3)
    if response.ok:
        color_received = response.json().get("cor")

        if color_received:
            hex_color = map_colors.get(color_received.lower())

            if hex_color:
                print(f"[INFO] Cor recebida: {color_received} → {hex_color}")

                # TECLADO
                apply_color_keyboard(color_received, hex_color)
                print("[MAIN] Aguardando finalização do teclado (20s)...")
                time.sleep(20)

                # MOUSE
                apply_color_mouse(hex_color)
                print("[MAIN] Aguardando finalização do mouse (15s)...")
                time.sleep(15)

                print("[MAIN] Processo de sincronização concluído com sucesso.")

            else:
                print(f"[AVISO] Cor '{color_received}' não está mapeada.")
        else:
            print("[INFO] Nenhuma cor definida no servidor.")
    else:
        print("[ERRO] Resposta inválida do servidor.")

except Exception as e:
    print(f"[EXCEÇÃO] {e}")
