from general_boolean_verify import can_change_color

# Simulação de uma requisição da Alexa com a cor desejada
mock_alexa_data = {
    "request": {
        "intent": {
            "slots": {
                "cor": {
                    "value": "amarelo neon"
                }
            }
        }
    }
}

if __name__ == "__main__":
    print("TESTE DA VERIFICAÇÃO GERAL")

    result, name, hex_code = can_change_color(mock_alexa_data)

    print("\nRESULTADO FINAL")
    if result:
        print(f"Troca de cor PERMITIDA: {name} -> {hex_code}")
    else:
        print("Troca de cor BLOQUEADA pelas condições atuais.")