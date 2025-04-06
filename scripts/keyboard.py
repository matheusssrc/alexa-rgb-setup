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
    start_time = time.time()  # Início da contagem

    chromedriver_path = os.path.join(os.getcwd(), "chromedriver.exe")
    ahk_script = r"C:\Users\mathe\OneDrive\Documentos\Python\Projetos\Alexa RGB Setup\ahk\key_keyboard.ahk"

    options = Options()
    options.add_argument("--start-maximized")

    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 20)

    try:
        print("Acessando o site...")
        driver.get("https://hub.fgg.com.cn/")

        print("Adiciona o Equipamento...")
        add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Add new equipment')]")))
        add_btn.click()

        print("Executando script AHK para conectar o dispositivo...")
        subprocess.Popen([ahk_script], shell=True)

        print("Aguardando conexão do dispositivo...")
        time.sleep(8)

        print("Aguardando aba Lighting Setting...")
        lighting_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Lighting Setting')]")))
        lighting_tab.click()

        # === BACK LAMP ===
        print("Aplicando cor no Back Lamp...")
        color_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.w-full.text-center")))
        color_input.click()
        color_input.send_keys(Keys.CONTROL, 'a')
        time.sleep(0.1)
        color_input.send_keys(Keys.BACKSPACE)
        color_input.send_keys(hex_color)
        color_input.send_keys(Keys.ENTER)
        print(f"Cor {color_received} aplicada no Back Lamp.")

        # === BOX LAMP ===
        print("Aplicando cor no Box Lamp...")
        box_lamp_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Box lamp')]")))
        box_lamp_btn.click()

        box_color_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.w-full.text-center")))
        box_color_input.click()
        box_color_input.send_keys(Keys.CONTROL, 'a')
        time.sleep(0.1)
        box_color_input.send_keys(Keys.BACKSPACE)
        box_color_input.send_keys(hex_color)
        box_color_input.send_keys(Keys.ENTER)
        print(f"Cor {color_received} aplicada no Box Lamp.")

        time.sleep(2)

    except TimeoutException as e:
        print("TimeoutException: Algo não carregou a tempo.")
        print(str(e))

    except Exception as e:
        print("Erro geral:")
        print(str(e))

    finally:
        print("Fechando navegador...")
        driver.quit()

        end_time = time.time()
        elapsed = round(end_time - start_time, 2)
        print(f"[KEYBOARD] Processo finalizado em {elapsed} segundos.")