import os
import time
import subprocess
import pyautogui

def apply_color_mouse(hex_color):
    print("[MOUSE] Iniciando aplicação da cor...")

    start_time = time.time()  # Início da contagem

    razer_path = r"C:\Program Files (x86)\Razer\Synapse3\WPFUI\Framework\Razer Synapse 3 Host\Razer Synapse 3.exe"
    ahk_script = r"C:\Users\mathe\OneDrive\Documentos\Python\Projetos\Alexa RGB Setup\ahk\key_mouse.ahk"

    # Abre o Razer Synapse
    subprocess.Popen([razer_path])
    time.sleep(5)

    # Executa o AHK para posicionar no campo HEX
    subprocess.Popen([ahk_script], shell=True)
    print("[INFO] Script AHK executado. Aguardando posicionamento no campo...")
    time.sleep(5)

    # Garante foco e edita o campo de cor
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.press('backspace')
    time.sleep(0.2)
    pyautogui.typewrite(hex_color)
    time.sleep(0.3)

    print(f"[MOUSE] Cor {hex_color} aplicada com sucesso. Aguardando fechamento...")

    # Tempo extra para o AHK clicar em SALVAR e encerrar
    time.sleep(3)

    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)
    print(f"[MOUSE] Finalizado com sucesso em {elapsed_time} segundos.")