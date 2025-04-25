import os
import time
import subprocess

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

def apply_color_keyboard(color_received, hex_color):
    start_time = time.time()

    if not hex_color.startswith("#") or len(hex_color) != 7:
        print(f"[ERRO - TECLADO] Hexadecimal inválido: {hex_color}\n")
        return

    chromedriver_path = r"C:\Users\mathe\OneDrive\Documentos\Python\Projetos\Alexa RGB Setup\computer\drivers\chromedriver.exe"
    ahk_script = r"C:\Users\mathe\OneDrive\Documentos\Python\Projetos\Alexa RGB Setup\computer\ahk\key_keyboard.ahk"

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-logging")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    service = Service(executable_path=chromedriver_path, log_path=os.devnull)
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_script_timeout(30)
    wait = WebDriverWait(driver, 20)

    try:
        print("[TECLADO] Acessando o site\n")
        driver.get("https://hub.fgg.com.cn/")
        time.sleep(1)

        print("[TECLADO] Esperando botão 'Add new equipment'\n")
        add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Add new equipment')]")))
        add_btn.click()
        time.sleep(2)

        print("[TECLADO] Executando AHK\n")
        subprocess.Popen([ahk_script], shell=True)

        print("[TECLADO] Aguardando conexão do dispositivo\n")
        time.sleep(3)

        print("[TECLADO] Aguardando aba Lighting Setting\n")
        lighting_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Lighting Setting')]")))
        lighting_tab.click()

        print("[TECLADO] Aplicando cor no Back Lamp\n")
        color_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.w-full.text-center")))
        color_input.click()
        color_input.send_keys(Keys.CONTROL, 'a')
        time.sleep(0.1)
        color_input.send_keys(Keys.BACKSPACE)
        color_input.send_keys(hex_color)
        color_input.send_keys(Keys.ENTER)
        print(f"[TECLADO] Cor {color_received} aplicada no Back Lamp\n")

        print("[TECLADO] Aplicando cor no Box Lamp\n")
        box_lamp_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Box lamp')]")))
        box_lamp_btn.click()

        box_color_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.w-full.text-center")))
        box_color_input.click()
        box_color_input.send_keys(Keys.CONTROL, 'a')
        time.sleep(0.1)
        box_color_input.send_keys(Keys.BACKSPACE)
        box_color_input.send_keys(hex_color)
        box_color_input.send_keys(Keys.ENTER)
        print(f"[TECLADO] Cor {color_received} aplicada no Box Lamp\n")

        time.sleep(1)

    except TimeoutException as e:
        print("\n[ERRO - TECLADO] TimeoutException: Algo não carregou a tempo")
        print(str(e) + "\n")

    except Exception as e:
        print("\n[ERRO - TECLADO] Erro geral:")
        print(str(e) + "\n")

    finally:
        print("[TECLADO] Fechando navegador\n")
        try:
            driver.quit()
        except:
            pass

        end_time = time.time()
        elapsed = round(end_time - start_time, 2)
        print(f"[TECLADO] Processo finalizado em {elapsed} segundos\n")

# Execução direta via terminal
if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        cor_nome = sys.argv[1]
        hex_cor = sys.argv[2]
        apply_color_keyboard(cor_nome, hex_cor)
    else:
        print("[ERRO] Argumentos insuficientes para execução direta do keyboard.py")