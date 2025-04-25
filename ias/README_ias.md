# Módulo: Inteligência Artificial (Geração de Dataset de Cores)

Este módulo é responsável por gerar um dataset expandido e traduzido de cores em português com seus respectivos códigos hexadecimais, utilizando dois modelos de IA disponíveis no Hugging Face. Ele **utiliza modelos pré-treinados para gerar dados confiáveis** para o projeto Alexa RGB Setup.

## Funcionalidades

- Geração automática de nomes de cores em inglês com seus hexadecimais
- Tradução para português com correções linguísticas
- Expansão para formas masculinas e femininas
- Geração do dataset final limpo e organizado

## Estrutura de Pastas

```
ias
├── hex-pt/
│   ├── extract_name-to-hex_dataset.py     # Extrai e estrutura os dados originais para treinamento
│   ├── translate_colors_en_pt.py          # Traduz nomes de cores do inglês para o português
│   ├── train_name-to-hex_pt.py            # Treina o modelo customizado em português
│   ├── test_model_pt_final.py             # Teste final da IA com o modelo treinado
│   └── venv-310/                          # Ambiente virtual Python exclusivo para a IA
│
├── name-to-hex/
│   └── download_name-to-hex.py            # Script para realizar download da IA
│
├── opus/
│   └── download_opus.py                   # Script para realizar download da IA
│
├── README_ia.md
└── requirements_ia.txt
```
## Requisitos específicos

- Token de autenticação Hugging Face
- Acesso à internet para download dos modelos

> Todas as dependências estão listadas em `requirements_ia.txt` nesta mesma pasta.

## Execução

### Criação do Ambiente Virtual e Instalação dos Requisitos específicos

1. Crie um ambiente virtual com Python 3.10 (exigido por `transformers`)
2. Instale as dependências via `requirements_computer.txt`
```
pip install -r requirements_computer.txt
```

### 1. Download dos modelos
- `download_name-to-hex.py` -> baixa o modelo que converte nome para HEX
- `download_opus.py` -> baixa o modelo de tradução para português

**Ambos os modelos foram baixados via `transformers` e hospedados localmente.**
> É recomendado autenticar previamente com o Hugging Face utilizando um token pessoal:  
> https://huggingface.co/settings/tokens

### 2. Extração inicial em inglês
- `extract_name-to-hex_dataset.py`:
  - Gera uma lista combinatória de nomes com modificadores (ex: "deep blue")
  - Utiliza `name-to-hex` para gerar `colors_extract_name-to-hex.jsonl`
  - Evita duplicatas e agrupa sinônimos

### 3. Tradução para português e expansão
- `translate_colors_en_pt.py`:
  - Usa o modelo OPUS para traduzir os nomes do dataset
  - Aplica correções linguísticas e padronização de nomes
  - Expande nomes para formas masculinas e femininas
  - Gera o arquivo final `colors_pt_expanded.jsonl`

### Exemplo de fluxo

1. Geração de nomes com modelo `name-to-hex`
2. Tradução e padronização com modelo OPUS
3. Expansão e limpeza → geração final do `colors_pt_expanded.jsonl`

---

**Autor do módulo:** Matheus Rossi Carvalho