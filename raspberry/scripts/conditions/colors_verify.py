from flask import Flask, request, jsonify
import json
from typing import Tuple

app = Flask(__name__)

COLORS_FILE_PATH = "/home/matheus/scripts/colors.jsonl"

def verify_color_from_alexa(data: dict) -> Tuple[bool, str, str]:
    """
    Extrai a cor do JSON da Alexa e verifica se ela existe no colors.jsonl.
    Retorna:
    - (True, nome, hexadecimal) se a cor for encontrada
    - (False, "", "") caso contrário
    """
    try:
        color_name = data["request"]["intent"]["slots"]["cor"]["value"]
        color_name = color_name.strip().lower()
        print(f"Cor recebida da Alexa: '{color_name}'")

        with open(COLORS_FILE_PATH, "r", encoding="utf-8") as file:
            for line in file:
                try:
                    record = json.loads(line)
                    input_name = record.get("input", "").strip().lower()
                    hex_value = record.get("output", "").strip().lower()

                    if input_name == color_name:
                        print(f"Cor encontrada: {input_name} -> {hex_value}")
                        return True, input_name, hex_value

                except json.JSONDecodeError:
                    print("Linha inválida no arquivo, ignorando.")
                    continue

        print("Cor não encontrada no arquivo.")
        return False, "", ""

    except KeyError:
        print("Erro: estrutura inválida ou campo 'cor' ausente.")
        return False, "", ""
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {COLORS_FILE_PATH}")
        return False, "", ""
    except Exception as e:
        print(f"Erro inesperado ao verificar a cor: {e}")
        return False, "", ""

# Rota opcional para testes externos (como requisições HTTP diretas)
@app.route("/", methods=["POST"])
def receive_color_from_alexa():
    data = request.get_json()
    found, name, hex_code = verify_color_from_alexa(data)

    if found:
        return jsonify({
            "color_found": True,
            "name": name,
            "hex": hex_code
        })
    else:
        return jsonify({"color_found": False})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100)