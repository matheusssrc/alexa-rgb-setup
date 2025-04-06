# Alexa RGB Setup Control

Este projeto foi desenvolvido como parte da disciplina de **Inteligência Artificial I** na **Antonio Meneghetti Faculdade**.

O objetivo é integrar comandos de voz via **Amazon Alexa** com automação local em Python para controlar as luzes RGB de periféricos conectados ao computador. Atualmente, o projeto está configurado para os seguintes dispositivos:

- **Teclado:** MadLion Nano68 PRO
- **Mouse:** Razer DeathAdder V2 PRO

## Como funciona

Comandos de voz enviados à Alexa ativam uma Skill personalizada, que envia uma requisição para um servidor local via webhook (exposto com NGROK). O servidor então aciona os scripts Python responsáveis por alterar as cores dos LEDs do teclado e mouse.

## Funcionalidades

- Reconhecimento de cores por voz usando Alexa
- Controle individual de:
  - Back Lamp e Box Lamp do teclado (via Selenium + site do fabricante)
  - Iluminação do mouse (via Razer Synapse + AutoHotkey + PyAutoGUI)
- Execução sequencial e sincronizada dos dois periféricos
- Arquitetura modular e reutilizável

## Requisitos

### Python

- Python 3.8+
- ChromeDriver (compatível com sua versão do Google Chrome)
- Instalar dependências com:

```
pip install flask selenium pyautogui requests
```

### Outros

- AutoHotkey instalado e no PATH do sistema
- Conta Amazon com Alexa configurada
- Conta no Alexa Developer Console
- NGROK configurado para expor sua API local

## Estrutura de arquivos

```
📁 Projeto/
├── servidor.py              # Recebe comandos da Alexa
├── main.py                  # Orquestra a execução dos periféricos
├── keyboard.py              # Controla o teclado via Selenium
├── mouse.py                 # Controla o mouse via AHK + PyAutoGUI
├── key_keyboard.ahk         # Script AutoHotkey para o teclado
├── key_mouse.ahk            # Script AutoHotkey para o mouse
├── chromedriver.exe         # Driver necessário para o Selenium
└── README.md                # Este arquivo
```

## Como usar

1. Inicie o servidor local:
```
python servidor.py
```

2. Em outra aba, execute o NGROK:
```
ngrok http 5000
```
Copie a URL gerada e configure como endpoint da sua Skill no Alexa Developer Console.

3. Com a Alexa configurada na mesma conta do Developer Console, diga:
```
Alexa, mudar cor do setup para azul
```

4. O comando será processado, e os periféricos mudarão de cor automaticamente.

## Comandos disponíveis

- "Alexa, mudar cor do setup para azul"
- "Alexa, trocar a luz do setup para vermelho"
- "Alexa, luz setup verde"
- Entre outros (com base nos intents da Skill configurada)

## Considerações finais

Este projeto pode ser expandido para novos dispositivos, integração com automação residencial, armazenamento de histórico de comandos e muito mais.


## Inteligência Artificial aplicada

Este projeto utiliza inteligência artificial de forma aplicada por meio da integração com a Amazon Alexa — uma assistente virtual baseada em modelos de linguagem natural (NLP). 

A Alexa interpreta comandos de voz, extrai a intenção do usuário e aciona ações automatizadas através de uma Skill personalizada conectada a scripts Python que controlam dispositivos RGB físicos.

Embora o processamento de IA ocorra na camada da Alexa (externa ao código Python local), o projeto ilustra claramente como sistemas inteligentes podem ser integrados com automações físicas no mundo real, alinhando-se aos conceitos de IA simbólica e computação contextual.


## Licença

MIT License