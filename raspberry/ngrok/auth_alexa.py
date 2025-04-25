import requests

# === CONFIGURAÇÕES ===
CLIENT_ID = "SEU_CLIENT_ID"
CLIENT_SECRET = "SEU_CLIENT_SECRET"
REFRESH_TOKEN = "SEU_REFRESH_TOKEN"
def get_access_token():
    url = "https://api.amazon.com/auth/o2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(" Novo access_token obtido com sucesso:")
        print(token)
        return token
    else:
        print(" Erro ao obter access_token:")
        print(response.status_code, response.text)
        return None

if __name__ == "__main__":
    get_access_token()