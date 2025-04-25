import os
import time
import subprocess
import pyautogui
import pygetwindow as gw

def wait_for_window(title, timeout=30):
    print("[MOUSE] Aguardando janela do Razer Synapse abrir...")
    start = time.time()
    while time.time() - start < timeout:
        windows = gw.getWindowsWithTitle(title)
        if windows:
            windows[0].activate()
            print("[MOUSE] Janela encontrada e ativada.")
            return True
        time.sleep(1)
    print("[MOUSE] Tempo de espera esgotado.")
    return False

def apply_color_mouse(color_received, hex_color):
    print("[MOUSE] Iniciando aplicação da cor...\n")
    start_time = time.time()

    razer_path = r"C:\Program Files (x86)\Razer\Synapse3\WPFUI\Framework\Razer Synapse 3 Host\Razer Synapse 3.exe"
    ahk_script = r"C:\Users\mathe\OneDrive\Documentos\Python\Projetos\Alexa RGB Setup\computer\ahk\key_mouse.ahk"

    try:
        subprocess.Popen([razer_path])
        time.sleep(3)

        subprocess.Popen([ahk_script], shell=True)
        print("[MOUSE] Abrindo Razer Synapse e aplicando a troca de cor\n")

        if wait_for_window("Razer Synapse"):
            time.sleep(6)

            pyautogui.typewrite(hex_color)
            time.sleep(0.2)
            pyautogui.press('enter')

            print(f"[MOUSE] Cor {color_received} aplicada com sucesso\n")
        else:
            print("[MOUSE] Janela do Razer Synapse não encontrada, abortando aplicação de cor.")

    except Exception as e:
        print(f"\n[ERRO - MOUSE] Exceção durante aplicação:\n{e}\n")

    finally:
        time.sleep(1)
        elapsed_time = round(time.time() - start_time, 2)
        print(f"[MOUSE] Finalizado com sucesso em {elapsed_time} segundos\n")
