import requests
import auth_alexa  # Certifique-se de que auth_alexa.py está no mesmo diretório

# CONFIGURAÇÕES
SKILL_ID = "SEU_SKILL_ID"
STAGE = "development"  # ou "live"

def get_ngrok_https_url():
    try:
        response = requests.get("http://localhost:4040/api/tunnels")
        tunnels = response.json()["tunnels"]
        for tunnel in tunnels:
            if tunnel["public_url"].startswith("https://"):
                return tunnel["public_url"]
    except Exception as e:
        print("Erro ao acessar o Ngrok:", e)
        return None

def update_skill_endpoint(access_token, ngrok_url):
    url = f"https://api.amazonalexa.com/v1/skills/{SKILL_ID}/stages/{STAGE}/manifest"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    manifest = {
        "manifest": {
            "publishingInformation": {
                "locales": {
                    "pt-BR": {
                        "name": "Luz Setup"
                    }
                },
                "isAvailableWorldwide": True,
                "testingInstructions": "Testar comandos de voz RGB.",
                "category": "SMART_HOME"
            },
            "apis": {
                "custom": {
                    "endpoint": {
                        "uri": ngrok_url
                    }
                }
            },
            "manifestVersion": "1.0"
        }
    }

    response = requests.put(url, headers=headers, json=manifest)
    if response.status_code == 202:
        print(f"Endpoint da skill atualizado para: {ngrok_url}")
    else:
        print("Erro ao atualizar o endpoint:")
        print(response.status_code, response.text)

if __name__ == "__main__":
    print("Obtendo access_token.")
    token = auth_alexa.get_access_token()
    if not token:
        print("Falha ao obter access_token.")
        exit(1)

    print("Verificando URL do Ngrok.")
    url = get_ngrok_https_url()
    if not url:
        print("URL HTTPS do Ngrok não encontrada.")
        exit(1)

    print("Enviando atualização para a Skill Alexa.")
    update_skill_endpoint(token, url)