from flask import Flask, request, jsonify
import subprocess
import os
import time
import psutil

app = Flask(__name__)

last_color = None
last_hex = None
lock_file = "main.lock"
LOCK_TIMEOUT = 600  # 10 minutos

# Caminho do main.py e do pythonw.exe
script_path = r"C:\Users\mathe\OneDrive\Documentos\Python\Projetos\Alexa RGB Setup\computer\scripts\main.py"
pythonw_path = r"C:\Users\mathe\AppData\Local\Programs\Python\Python313\pythonw.exe"

def is_main_running():
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and "main.py" in ' '.join(cmdline):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return False

def is_main_locked():
    if not os.path.exists(lock_file):
        return False

    last_modified = os.path.getmtime(lock_file)
    now = time.time()
    if now - last_modified > LOCK_TIMEOUT:
        print("[INFO] Arquivo de bloqueio antigo detectado. Será removidoger", flush=True)
        os.remove(lock_file)
        return False

    if not is_main_running():
        print("[INFO] Arquivo de bloqueio encontrado, mas main.py NÃO está rodando. Será removido", flush=True)
        os.remove(lock_file)
        return False

    return True

@app.route("/color", methods=["POST"])
def receive_color():
    global last_color, last_hex
    data = request.get_json()

    color = data.get("cor")
    hex_code = data.get("hex")

    if color and hex_code:
        last_color = color.strip().lower()
        last_hex = hex_code.strip().lower()

        print(f"[RECEBIDO] Cor: {last_color} | Hex: {last_hex}", flush=True)

        if not is_main_locked():
            try:
                print(f"[AÇÃO] Executando main.py com: {last_color} {last_hex}", flush=True)

                with open(lock_file, "w") as f:
                    f.write("executando")

                subprocess.Popen([pythonw_path, script_path, last_color, last_hex])
            except Exception as e:
                print(f"[ERRO] Falha ao iniciar main.py: {e}", flush=True)
        else:
            print("[INFO] main.py já está em execução, ignorando novo pedido", flush=True)

        return jsonify({"status": "recebido", "cor": last_color, "hex": last_hex}), 200

    return jsonify({"erro": "Cor e/ou hex não fornecidos"}), 400

@app.route("/color", methods=["GET"])
def get_color():
    return jsonify({
        "cor": last_color,
        "hex": last_hex
    }) if last_color and last_hex else jsonify({"cor": None, "hex": None})

if __name__ == "__main__":
    print("Servidor ativo na porta 5050", flush=True)
    app.run(host="0.0.0.0", port=5050)