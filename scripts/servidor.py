from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# Armazena a última cor recebida
last_color = None

@app.route("/", methods=["POST"])
def alexa_webhook():
    global last_color
    data = request.get_json()

    try:
        color = data["request"]["intent"]["slots"]["cor"]["value"]
        color = color.strip().lower()
        last_color = color

        print(f"[ALEXA] Cor recebida: {color}")

        # Chama o main.py automaticamente
        print("[AÇÃO] Executando main.py para aplicar a cor...")
        subprocess.Popen(["python", "main.py"])

        return {
            "version": "1.0",
            "response": {
                "shouldEndSession": True,
                "outputSpeech": {
                    "type": "PlainText",
                    "text": f"Mudando cor do setup para {color}"
                }
            }
        }

    except Exception as e:
        print("[ERRO]", e)
        return {
            "version": "1.0",
            "response": {
                "shouldEndSession": True,
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Desculpe, não entendi a cor."
                }
            }
        }

@app.route("/cor", methods=["GET"])
def catch_color():
    return jsonify({"cor": last_color}) if last_color else jsonify({"cor": None})

if __name__ == "__main__":
    app.run(port=5000)
