# Alexa RGB Setup Control

Este projeto foi desenvolvido como parte da disciplina de **Inteligência Artificial I** na **Antonio Meneghetti Faculdade**.

O objetivo é integrar comandos de voz via **Amazon Alexa** com automação local em Python para controlar as luzes RGB de periféricos conectados ao computador. Atualmente, o projeto está configurado para os seguintes dispositivos:

- **Teclado:** MadLions Nano68 PRO
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
pip install -r requirements.txt
```

### Outros

- [NGROK](https://ngrok.com/) para expor localmente o servidor Flask
- Razer Synapse 3 instalado (para controle do mouse)
- AutoHotkey instalado (para automação via interface)

## Estrutura de Pastas

```
.
├── ahk
│   ├── key_keyboard.ahk         # AHK para automação do site do teclado
│   └── key_mouse.ahk            # AHK para automação do Synapse
├── drivers
│   ├── chromedriver.exe         # Driver do Chrome para Selenium
│   └── ngrok.exe                # Executável do NGROK
├── scripts
│   ├── keyboard.py              # Código que aplica a cor no teclado
│   ├── mouse.py                 # Código que aplica a cor no mouse
│   ├── servidor.py              # Webhook da Alexa (Flask)
│   └── main.py                  # Orquestra a automação geral
├── requirements.txt             # Dependências do projeto
└── README.md
```
## Configurando o Servidor

1. Inicie o servidor local: python servidor.py
2. Em outra aba, execute o NGROK: ngrok http 5000
3. Com a URL gerada, guarde para configurar como endpoint da sua Skill no Alexa Developer Console.

## Configurando a Skill da Alexa

1. Acesse o [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask)
2. Crie uma Skill com o nome "luz setup" e configure o idioma como Português (Brasil)
3. No **Interaction Model**, adicione o intent com o slot `cor` do tipo `AMAZON.Color`
4. Configure exemplos de comandos como:
   - mudar cor do setup para {cor}
   - usar {cor}
   - vermelho, azul, etc.
5. Vá em **Endpoint** e use o endereço do seu NGROK (ex: `https://xxxxx.ngrok-free.app`)
6. Salve e teste usando o **Alexa Test Console** ou diretamente no dispositivo físico

## Finalizando com a Alexa configurada:

1. Com a Alexa configurada na mesma conta do Developer Console, diga: Alexa, mudar cor do setup para azul
2. O comando será processado, e os periféricos mudarão de cor automaticamente.

## Considerações

- Este projeto pode ser expandido para novos dispositivos, integração com automação residencial, armazenamento de histórico de comandos e muito mais.
- Cores suportadas são: vermelho, azul, verde e roxo (você pode expandir o dicionário)
- Você pode ajustar o tempo de espera entre dispositivos conforme seu hardware

## Inteligência Artificial aplicada

Este projeto utiliza inteligência artificial de forma aplicada por meio da integração com a Amazon Alexa — uma assistente virtual baseada em modelos de linguagem natural (NLP). 

A Alexa interpreta comandos de voz, extrai a intenção do usuário e aciona ações automatizadas através de uma Skill personalizada conectada a scripts Python que controlam dispositivos RGB físicos.

Embora o processamento de IA ocorra na camada da Alexa (externa ao código Python local), o projeto ilustra claramente como sistemas inteligentes podem ser integrados com automações físicas no mundo real, alinhando-se aos conceitos de IA simbólica e computação contextual.

## Licença

MIT License

---

**Autor:** Matheus Rossi Carvalho  
**Contato:** [LinkedIn](https://www.linkedin.com/in/matheusrossicarvalho/)
