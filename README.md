# Alexa RGB Setup Control

O objetivo deste projeto é integrar comandos de voz via **Amazon Alexa** com automação local em Python para controlar as luzes RGB de periféricos conectados ao computador. Atualmente, o projeto está configurado para os seguintes dispositivos:

- **Teclado:** MadLions Nano68 PRO
- **Mouse:** Razer DeathAdder V2 PRO

## Como funciona

Comandos de voz enviados à Alexa ativam uma Skill personalizada, que envia uma requisição HTTP para um servidor local, hospedado em um Raspberry Pi com Ubuntu Server. Esse servidor recebe a cor solicitada e a encaminha para o computador principal de uso, responsável por executar os scripts Python que alteram a cor dos LEDs do teclado e do mouse.

## Funcionalidades

- Reconhecimento de cores por voz via Alexa
- Controle RGB de teclado via Selenium e AutoHotkey
- Controle RGB de mouse Razer via PyAutoGUI e AutoHotkey
- Execução sincronizada entre dispositivos
- Verificação lógica de condições (expressões booleanas)
- Dataset customizado e expansível para reconhecimento de cores em português
- Deploy parcial no Raspberry Pi com túnel HTTP ativo via Ngrok

## Organização do Projeto

Este repositório está dividido em três módulos principais:

- **`computer/`**: scripts principais de automação local no computador com Windows.
- **`ias/`**: scripts e IAs utilizadas no para criação do dataset para cadastramento de cores.
- **`raspberry/`**: scripts executados no Raspberry Pi, que atua como servidor intermediário e gerenciador de condições.

Cada uma dessas pastas contém:

- Um `README.md` explicando brevemente o processo de criação e configuração daquela etapa
- Um `requirements.txt` com as dependências específicas necessárias para execução do respectivo módulo

## Estrutura de Pastas

```
.
├── computer
│   ├── ahk/
│   │   ├── key_keyboard.ahk                   # Script AHK para automatizar a troca de cor no site do teclado
│   │   └── key_mouse.ahk                      # Script AHK para controlar a cor do mouse via Razer Synapse
│   │
│   ├── drivers/
│   │   └── chromedriver.exe                   # Driver do navegador Chrome usado pelo Selenium
│   │
│   ├── scripts/
│   │   ├── keyboard.pyw                       # Script que altera a cor do teclado
│   │   ├── mouse.py                           # Script que altera a cor do mouse
│   │   ├── main.py                            # Orquestrador geral da execução sincronizada
│   │   ├── server_endpoint.py                 # Responsável por se comunicar com o servidor Flask do Raspberry Pi
│   │   └── tests/
│   │       ├── test_keyboard.py               # Teste unitário para o script do teclado
│   │       └── test_mouse.py                  # Teste unitário para o script do mouse
│   │ 
│   ├── README_computer.md
│   └── requirements_computer.txt
│
├── ias
│   ├── hex-pt/
│   │   ├── extract_name-to-hex_dataset.py     # Extrai e estrutura os dados originais para treinamento
│   │   ├── translate_colors_en_pt.py          # Traduz nomes de cores do inglês para o português
│   │   ├── train_name-to-hex_pt.py            # Treina o modelo customizado em português
│   │   ├── test_model_pt_final.py             # Teste final da IA com o modelo treinado
│   │   └── venv-310/                          # Ambiente virtual Python exclusivo para a IA
│   │
│   ├── name-to-hex/
│   │   └── download_name-to-hex.py            # Script para realizar download da IA
│   │
│   ├── opus/
│   │   └── download_opus.py                   # Script para realizar download da IA
│   │
│   ├── README_ia.md
│   └── requirements_ia.txt
│ 
├── raspberry
│   ├── ngrok/
│   │   ├── auth_alexa.py                      # Configura autenticação da API da Alexa Developer
│   │   ├── monitor_ngrok.sh                   # Script shell que mantém o túnel HTTP ativo via Ngrok
│   │   ├── update_skill_endpoint.py           # Atualiza o endpoint da Skill da Alexa automaticamente
│   │   └── verify_ngrok.py                    # Verifica se o túnel está ativo e funcional
│   │
│   ├── scripts/
│   │   ├── conditions/
│   │   │   ├── colors_verify.py               # Verifica se a cor recebida é válida no sistema
│   │   │   ├── computer_status.py             # Detecta se o computador principal está ligado na rede
│   │   │   ├── free_mode.py                   # Ativa o modo livre (aceita comandos sempre)
│   │   │   └── work_mode.py                   # Ativa o modo trabalho (não aceita comandos durante o horário de trabalho)
│   │   │
│   │   ├── tests/
│   │   │   ├── test_general_boolean.py        # Teste da lógica booleana final
│   │   │   └── test_general.py                # Teste geral da estrutura lógica do sistema
│   │   │
│   │   ├── colors.jsonl                       # Base de dados local com nomes de cores e seus hexadecimais
│   │   ├── expression_evaluator.py            # Avaliador de expressões booleanas personalizadas
│   │   ├── general_boolean_verify.py          # Verificação geral baseada em múltiplas condições e modos
│   │   ├── graph_interface.py                 # Interface gráfica verificadora de resultados mediante os condicionais
│   │   └── server.py                          # Servidor Flask que recebe os comandos da Alexa via webhook
│   │
│   ├── services/
│   │   ├── ngrok-monitor.service              # Inicia automaticamente o túnel Ngrok com base na configuração YAML, garantindo acesso público aos serviços do Raspberry Pi após o boot
│   │   ├── ngrok.service                      # Executa continuamente o script monitor_ngrok.sh para verificar e atualizar o endpoint da Skill Alexa sempre que o túnel do Ngrok mudar
│   │   └── server_rgb.service                 # Mantém o servidor Flask (server.py) sempre ativo para receber e processar comandos de cor enviados pela Alexa
│   │
│   ├── README_raspberry.md
│   └── requirements_raspberry.txt
│
├── README.md
└── requirements.txt

```
## Requisitos

- Python 3.8+
- Conta no Amazon Developer Console para criar a Skill Alexa
- Dispositivo Alexa ou uso do simulador Alexa Test Console
- Raspberry Pi com mínimo o modelo 3B, rodando Ubuntu Server 20.04 ou superior
- [NGROK](https://ngrok.com/) para expor localmente o servidor Flask
- Razer Synapse 3 instalado (para controle do mouse)
- AutoHotkey instalado (para automação via interface)

## Considerações

- Este projeto pode ser expandido para novos dispositivos, integração com automação residencial, armazenamento de histórico de comandos e muito mais.
- São mais de 200 cores suportadas (você pode expandir o dataset colors.jsonl)
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