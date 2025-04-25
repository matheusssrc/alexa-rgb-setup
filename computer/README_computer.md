# Módulo: Computador Principal (Windows)

Este módulo é responsável por executar os comandos finais que alteram as cores RGB dos periféricos (teclado e mouse), após a **interpretação de voz feita pela Alexa e o processamento de lógica realizado no Raspberry Pi**.

## Funcionalidades

- Aplicação de cores no teclado via Selenium + AutoHotkey
- Aplicação de cores no mouse via PyAutoGUI + AutoHotkey
- Execução sincronizada dos dois periféricos
- Verificação de instância única para evitar conflitos
- Escuta passiva dos comandos vindos do servidor Flask (Raspberry Pi)
- Suporte a testes independentes para cada periférico
- Execução automatizada via Agendador de Tarefas do Windows

## Estrutura de Pastas

```
computer
├── ahk/
│   ├── key_keyboard.ahk                   # Script AHK para automatizar a troca de cor no site do teclado
│   └── key_mouse.ahk                      # Script AHK para controlar a cor do mouse via Razer Synapse
│
├── drivers/
│   └── chromedriver.exe                   # Driver do navegador Chrome usado pelo Selenium
│
├── scripts/
│   ├── keyboard.pyw                       # Script que altera a cor do teclado
│   ├── mouse.py                           # Script que altera a cor do mouse
│   ├── main.py                            # Orquestrador geral da execução sincronizada
│   ├── server_endpoint.py                 # Responsável por se comunicar com o servidor Flask do Raspberry Pi
│   └── tests/
│       ├── test_keyboard.py               # Teste unitário para o script do teclado
│       └── test_mouse.py                  # Teste unitário para o script do mouse
│ 
├── README_computer.md
└── requirements_computer.txt
```

## Requisitos específicos

- Google Chrome + ChromeDriver compatível
- AutoHotkey instalado
- Razer Synapse 3 configurado

> Todas as dependências estão listadas em `requirements_computer.txt` nesta mesma pasta.

## Execução

Este módulo deve estar em execução no computador principal com Windows, preferencialmente por meio do **Agendador de Tarefas** do sistema, para garantir sua inicialização automática ao ligar o PC.

### Instalação dos Requisitos específicos

- Realize a instalação do Python
- Realize download do ChromeDriver, se não tiver o Google Chrome, será necesário instalar
- AutoHotKey
- Razer Synapse 3
- Instale as dependências via `requirements_computer.txt`
```
pip install -r requirements_computer.txt
```

### Execução automática no Windows (Recomendado)

Para garantir que `server_endpoint.py` seja iniciado junto ao sistema:

- Abra o **Agendador de Tarefas** do Windows.
- Crie uma nova tarefa.
- Defina o gatilho como "Ao iniciar o computador" ou "Ao fazer logon".
- A ação deve ser: **Iniciar um programa** → `pythonw.exe` com o caminho absoluto para `server_endpoint.py`
- Certifique-se de marcar a opção “executar com privilégios mais altos” e configurar para executar mesmo que o usuário não esteja logado (opcional).

### Exemplo de fluxo:

1. O Raspberry Pi envia a cor recebida da Alexa para o computador.
2. O script `server_endpoint.py` escuta a requisição.
3. O `main.py` é acionado automaticamente e:
   - Inicia o `keyboard.pyw`
   - Após a finalização, inicia o `mouse.py`
Obs: Poderá testar a execução dos scripts utilizando `test_keyboard.py` e `test_mouse.py`

---

**Autor do módulo:** Matheus Rossi Carvalho
