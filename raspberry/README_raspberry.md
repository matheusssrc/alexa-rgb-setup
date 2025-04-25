# Módulo: Raspberry

Este módulo é responsável por executar a lógica de verificação e controle da automação de cores utilizando o Raspberry Pi como **servidor intermediário entre a Alexa e o computador principal (Windows)**.

## Funcionalidades

- Recebimento de comandos HTTP da Alexa.
- Verificação de condições lógicas (modo de operação, status do computador, cor cadastrada).
- Avaliação de expressões booleanas.
- Comunicação com a API da Amazon Alexa para atualização dinâmica do endpoint da Skill.
- Monitoramento e manutenção do túnel Ngrok ativo.

## Estrutura de Pastas

```
scripts/
├── conditions/
│   │   ├── colors_verify.py               # Verifica se a cor recebida é válida no sistema
│   │   ├── computer_status.py             # Detecta se o computador principal está ligado na rede
│   │   ├── free_mode.py                   # Ativa o modo livre (aceita comandos sempre)
│   │   └── work_mode.py                   # Ativa o modo trabalho (não aceita comandos durante o horário de trabalho)
│   │
│   ├── tests/
│   │   ├── test_general_boolean.py        # Teste da lógica booleana final
│   │   └── test_general.py                # Teste geral da estrutura lógica do sistema
│   │
│   ├── colors.jsonl                       # Base de dados local com nomes de cores e seus hexadecimais
│   ├── expression_evaluator.py            # Avaliador de expressões booleanas personalizadas
│   ├── general_boolean_verify.py          # Verificação geral baseada em múltiplas condições e modos
│   ├── graph_interface.py                 # Interface gráfica verificadora de resultados mediante os condicionais
│   └── server.py                          # Servidor Flask que recebe os comandos da Alexa via webhook
│
├── services/
│   ├── ngrok-monitor.service              # Inicia automaticamente o túnel Ngrok com base na configuração YAML, garantindo acesso público aos serviços do Raspberry Pi após o boot
│   ├── ngrok.service                      # Executa continuamente o script monitor_ngrok.sh para verificar e atualizar o endpoint da Skill Alexa sempre que o túnel do Ngrok mudar
│   └── server_rgb.service                 # Mantém o servidor Flask (server.py) sempre ativo para receber e processar comandos de cor enviados pela Alexa
│
├── README_raspberry.md
└── requirements_raspberry.txt
```

## Requisitos específicos

- Python 3.8+
- Flask
- requests
- Acesso à API SMAPI da Amazon Alexa
- Ngrok instalado localmente e autenticado
- Conectividade com o computador principal via rede local (ex: ping)

> Todas as dependências estão listadas em `requirements_raspberry.txt` nesta mesma pasta.

## Execução

A execução do módulo no Raspberry Pi segue uma abordagem dividida entre **servidores Python**, **scripts shell** e **serviços `systemd`** para garantir **resiliência** e **automação contínua**.

### 1. Configurando a Skill da Alexa

1. Acesse o [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask).
2. Crie uma nova Skill
3. Vá para a aba **Interaction Model > Intents** e crie um intent.
4. Adicione um slot chamado `cor` com tipo `AMAZON.Color`.
5. Em **Exemplos de Frases (Sample Utterances)**, adicione frases como:
   - mudar cor do setup para {cor}
   - usar {cor}
   - deixar {cor}
   - vermelho, azul, verde...
6. Salve o modelo e vá para a aba **Endpoint**. Configure como HTTPS e insira a URL gerada pelo Ngrok (ex: `https://xxxx.ngrok-free.app`).

### 2. Configurando a Skill da Alexa
1. Acesse: https://developer.amazon.com
2. Crie um Security Profile e Adicione um OAuth Redirect URL: https://localhost/(temporário)
3. Pegue as credenciais geradas:
4. Gere seu Refresh Token Manualmente
5. Realize login com a sua conta da Amazon Developer
4. Copie a URL gerada e pegue seu **CODE** e execute no **CMD**"
curl -X POST https://api.amazon.com/auth/o2/token \
   ```
  curl -X POST https://api.amazon.com/auth/o2/token \
  -d "grant_type=authorization_code&code=SEU_AUTH_CODE&client_id=SEU_CLIENT_ID&client_secret=SEU_CLIENT_SECRET&redirect_uri=https://localhost/"
   ```
5. Salve os dados retornados
6. Atualize os scripts da pasta **ngrok** com os dados gerados.

### 3. Ativação dos Services
1. Crie os services a partir do comando: 
```sudo nano /etc/systemd/system/"NOME_DO_SERVICE"```
2. Coloque os conteúdos dos arquivos da pasta **service**
3. Ative os services com:
```sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable "NOME_DO_SERVICE"
sudo systemctl start "NOME_DO_SERVICE"
```
4. Por fim, reiniciei o raspberry

### Exemplo de fluxo:

1. Alexa envia uma requisição HTTP para o Raspberry via Skill.
2. `server.py` recebe a requisição e chama `general_boolean_verify.py`.
3. O script verifica:
   - Se a cor está cadastrada (`colors_verify.py`)
   - Se o modo livre está ativo (`free_mode.py`)
   - Se o modo trabalho está desativado (`work_mode.py`)
   - Se o computador principal está online (`computer_status.py`)
4. A expressão lógica booleana é montada e avaliada.
5. Se verdadeira, a cor é encaminhada ao computador principal para execução.

---

**Autor do módulo:** Matheus Rossi Carvalho
