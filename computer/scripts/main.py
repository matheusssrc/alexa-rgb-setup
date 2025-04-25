import time
import sys
import os
import psutil
import subprocess
from keyboard import apply_color_keyboard
from mouse import apply_color_mouse

lock_file = "main.lock"

def remove_lock():
    if os.path.exists(lock_file):
        try:
            os.remove(lock_file)
        except Exception as e:
            print("\n[ERRO - MAIN] Falha ao remover o arquivo de bloqueio:")
            print(f"{e}\n")

def is_already_running():
    current_pid = os.getpid()
    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and proc.info['pid'] != current_pid and "main.py" in ' '.join(cmdline):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return False

# Verifica se já existe uma instância rodando
if is_already_running():
    print("[INFO - MAIN] Já existe um main.py rodando, encerrando esta execução")
    sys.exit(0)

# Cria o arquivo de lock contendo o PID atual
try:
    with open(lock_file, "w") as f:
        f.write(str(os.getpid()))
except Exception as e:
    print(f"[ERRO - MAIN] Falha ao criar o arquivo de bloqueio:\n{e}")
    sys.exit(1)

start_time = time.time()

try:
    if len(sys.argv) < 3:
        print("\n[ERRO - MAIN] Argumentos insuficientes. Esperado: nome da cor e hexadecimal\n")
        remove_lock()
        sys.exit(1)

    color_name = sys.argv[1].lower()
    hex_color = sys.argv[2].lower()

    print(f"\n[MAIN] Cor recebida: {color_name} -> {hex_color}\n")

    print("[MAIN] Iniciando processo no teclado (chamando keyboard.pyw via import)\n")
    apply_color_keyboard(color_name, hex_color)
    time.sleep(1)

    print("[MAIN] Iniciando processo no mouse\n")
    apply_color_mouse(color_name, hex_color)

    total_time = round(time.time() - start_time, 2)
    print(f"\n[MAIN] Processo finalizado com sucesso em {total_time} segundos\n")

except Exception as e:
    print(f"\n[ERRO - MAIN] Exceção inesperada:\n{e}\n")

finally:
    remove_lock()