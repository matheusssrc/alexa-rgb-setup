from flask import Flask, request, jsonify
import requests

from general_boolean_verify import can_change_color
from conditions.colors_verify import verify_color_from_alexa
from conditions.work_mode import is_work_mode
from conditions.computer_status import is_computer_active

app = Flask(__name__)

last_color_received = None
WINDOWS_ENDPOINT = "http://192.168.1.116:5050/color"

@app.route("/", methods=["POST"])
def alexa_webhook():
    global last_color_received
    data = request.get_json()

    try:
        # Captura prévia da cor para exibição no log
        color_preview = data["request"]["intent"]["slots"]["cor"]["value"]
        print(f"[ALEXA] Cor recebida: {color_preview}", flush=True)

        # Verifica todas as condições lógicas definidas
        allowed, color_name, hex_code = can_change_color(data)

        if allowed:
            last_color_received = color_name
            print(f"[PERMITIDO] Cor: {color_name} | Hex: {hex_code}", flush=True)

            try:
                response = requests.post(
                    WINDOWS_ENDPOINT,
                    json={"cor": color_name, "hex": hex_code},
                    timeout=2
                )
                print(f"[ENVIADO PARA WINDOWS] Status: {response.status_code}", flush=True)
            except Exception as e:
                print(f"[FALHA AO ENVIAR PARA WINDOWS] {e}", flush=True)

            return build_alexa_response(f"Alterando setup para a cor {color_name}.")

        # Se não foi permitido, analisa os motivos específicos
        color_found, _, _ = verify_color_from_alexa(data)
        computer_is_on = is_computer_active()
        is_in_work_mode = is_work_mode()

        if not color_found:
            print("[BLOQUEADO] Cor não cadastrada no sistema", flush=True)
            return build_alexa_response("Desculpe, a cor ainda não está cadastrada!")
        elif is_in_work_mode:
            print("[BLOQUEADO] Modo trabalho ativo", flush=True)
            return build_alexa_response("Matheus, agora não é hora disto!")
        elif not computer_is_on:
            print("[BLOQUEADO] Computador desligado", flush=True)
            return build_alexa_response("Não é possível trocar a cor se o computador está desligado!")

        print("[BLOQUEADO] Motivo indefinido", flush=True)
        return build_alexa_response("Não foi possível trocar a cor no momento.")

    except Exception as e:
        print(f"[ERRO] {e}", flush=True)
        return build_alexa_response("Desculpe, não consegui entender a cor recebida.")

@app.route("/color", methods=["GET"])
def get_last_color():
    return jsonify({"cor": last_color_received}) if last_color_received else jsonify({"cor": None})

def build_alexa_response(message: str):
    return {
        "version": "1.0",
        "response": {
            "shouldEndSession": True,
            "outputSpeech": {
                "type": "PlainText",
                "text": message
            }
        }
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)