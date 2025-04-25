#!/bin/bash

NGROK_PORT=5000
NGROK_BIN="/usr/local/bin/ngrok"
CHECK_SCRIPT="/home/"SEU_USER"/ngrok/verify_ngrok.py"

function is_port_in_use() {
    nc -z localhost $NGROK_PORT > /dev/null 2>&1
    return $?
}

function is_ngrok_tunnel_active() {
    curl -s http://localhost:4040/api/tunnels | grep -q 'https://'
    return $?
}

function get_current_ngrok_url() {
    curl -s http://localhost:4040/api/tunnels | grep -o 'https://[a-zA-Z0-9.-]*' | head -n 1
}

echo "Iniciando verificação de túnel Ngrok."

# 1. Verifica se já há túnel HTTPS ativo
if is_ngrok_tunnel_active; then
    echo "Túnel do Ngrok já está ativo: $(get_current_ngrok_url)"
else
    echo "Nenhum túnel HTTPS detectado. Reiniciando Ngrok."

    if ! is_port_in_use; then
        echo "Atenção: Nenhum serviço escutando na porta $NGROK_PORT. Túnel não será iniciado."
        exit 1
    fi

    echo "Finalizando qualquer instância anterior do Ngrok."
    pkill ngrok
    sleep 2

    echo "Iniciando novo túnel do Ngrok."
    $NGROK_BIN http $NGROK_PORT --log=stdout > /dev/null &
    sleep 5
fi

# 2. Comparar com endpoint da Alexa e atualizar se necessário
echo "Comparando URL com Alexa e atualizando se necessário."
python3 $CHECK_SCRIPT