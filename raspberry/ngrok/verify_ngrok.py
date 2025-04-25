import requests
import json
import sys

# ======= CONFIGURAÇÕES =======
SKILL_ID = "SEU_SKILL_ID"
STAGE = "development"
NGROK_API = "http://localhost:4040/api/tunnels"
AUTH_SCRIPT = "/home/SEU_USER/ngrok/auth_alexa.py"

# ======= 1. Obter access_token =======
try:
    exec(open(AUTH_SCRIPT).read())
    access_token = get_access_token()
except Exception as e:
    print(f"Erro ao obter access_token: {e}")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# ======= 2. Obter URL pública do Ngrok =======
def get_ngrok_url():
    try:
        r = requests.get(NGROK_API)
        r.raise_for_status()
        tunnels = r.json().get("tunnels", [])
        for t in tunnels:
            if t["public_url"].startswith("https://"):
                return t["public_url"]
    except Exception as e:
        print(f"Erro ao consultar o Ngrok: {e}")
    return None

# ======= 3. Obter endpoint atual da Skill Alexa =======
def get_alexa_url():
    try:
        url = f"https://api.amazonalexa.com/v1/skills/{SKILL_ID}/stages/{STAGE}/manifest"
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        return data["manifest"]["apis"]["custom"]["endpoint"]["uri"]
    except Exception as e:
        print(f"Erro ao consultar endpoint da Skill: {e}")
    return None

# ======= 4. Atualizar endpoint no manifesto completo =======
def update_alexa_url(new_url):
    manifest_url = f"https://api.amazonalexa.com/v1/skills/{SKILL_ID}/stages/{STAGE}/manifest"

    # Obter o manifesto atual
    r = requests.get(manifest_url, headers=headers)
    if r.status_code != 200:
        print("Erro ao obter manifesto atual:", r.status_code, r.text)
        return

    current_manifest = r.json()

    try:
        current_manifest["manifest"]["apis"]["custom"]["endpoint"]["uri"] = new_url
    except KeyError:
        print("Erro: estrutura do manifesto não contém endpoint custom.")
        return

    # Enviar PUT com o manifesto completo
    r = requests.put(manifest_url, headers=headers, data=json.dumps(current_manifest))
    if r.status_code == 202:
        print(f"Endpoint atualizado para: {new_url}")
    else:
        print(f"Erro ao atualizar endpoint: {r.status_code} — {r.text}")

# ======= 5. Execução do processo =======
ngrok_url = get_ngrok_url()
alexa_url = get_alexa_url()

if ngrok_url and alexa_url:
    if ngrok_url.strip() != alexa_url.strip():
        print("URLs diferentes. Atualizando Skill.")
        update_alexa_url(ngrok_url)
    else:
        print("URLs iguais. Nenhuma ação necessária.")
else:
    print("Falha ao obter URLs para comparação.")