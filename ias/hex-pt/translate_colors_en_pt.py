import os
import json
from transformers import MarianMTModel, MarianTokenizer

# Caminhos
base_dir = r"Escolha o caminho onde salvou o extract dataset"
input_jsonl = os.path.join(base_dir, "hex-pt", "colors_extract_name-to-hex.jsonl")
output_jsonl = os.path.join(base_dir, "hex-pt", "colors_pt_expanded.jsonl")
opus_model_path = os.path.join(base_dir, "opus")

# Carrega modelo
print("Carregando modelo OPUS")
tokenizer = MarianTokenizer.from_pretrained(opus_model_path)
model = MarianMTModel.from_pretrained(opus_model_path)

def translate_text(text):
    prompt = f">>pt<< {text}"
    tokens = tokenizer(prompt, return_tensors="pt", padding=True)
    output = model.generate(**tokens)
    return tokenizer.decode(output[0], skip_special_tokens=True).lower()

def clean_translation(text):
    text = text.lower().strip()

    substitutions = {
        "claroa": "clara", "escuroa": "escura",
        "luminosa": "clara", "macia": "clara", "leve": "claro",
        "fresca": "fria", "fresco": "frio", "neona": "neon",
        "cinzento": "cinza", "gris": "cinza",
        "oscuro": "escuro", "pálido": "opaco", "dál": "verde azulado",
        "cor-de-rosa": "rosa", "castanho": "marrom", "castanha": "marrom",
        "beige": "bege", "cyan": "ciano", "berinjela": "salmão opaco",
    }

    for k, v in substitutions.items():
        text = text.replace(k, v)

    return text.replace("-", " ").strip()

def average_hex(hex_list):
    r = g = b = 0
    for hexcode in hex_list:
        hexcode = hexcode.lstrip("#")
        r += int(hexcode[0:2], 16)
        g += int(hexcode[2:4], 16)
        b += int(hexcode[4:6], 16)
    n = len(hex_list)
    return "#{:02x}{:02x}{:02x}".format(r // n, g // n, b // n)

def expandir_genero(nome: str, hexcode: str) -> list[dict]:
    neutras = {"rosa", "lilás", "bege", "violeta", "magenta", "lavanda", "coral", "salmão", "cinza", "neon"}
    modificadores = {"claro", "escuro", "profundo", "brilhante", "opaco", "quente", "frio"}

    def feminino(palavra): return palavra[:-1] + "a" if palavra.endswith("o") else palavra
    def masculino(palavra): return palavra[:-1] + "o" if palavra.endswith("a") else palavra

    resultados = set()
    partes = nome.strip().lower().split()
    if not partes:
        return [{"input": nome.strip(), "output": hexcode}]

    base = partes[0]
    mod = partes[1] if len(partes) > 1 else None

    if base in neutras:
        resultados.add(nome.strip())
    else:
        masc = f"{masculino(base)} {masculino(mod)}" if mod else masculino(base)
        fem = f"{feminino(base)} {feminino(mod)}" if mod else feminino(base)
        resultados.add(masc.strip())
        resultados.add(fem.strip())

    return [{"input": cor, "output": hexcode} for cor in resultados]

# Carrega dados
with open(input_jsonl, "r", encoding="utf-8") as f:
    english_data = [json.loads(l) for l in f]

# Tradução
traduzidos = {}
for idx, item in enumerate(english_data, 1):
    nome_en = item["input"]
    hexcode = item["output"]
    nome_en_str = ", ".join(nome_en) if isinstance(nome_en, list) else nome_en

    traduzido = translate_text(nome_en_str)
    brutos = [n.strip() for n in traduzido.split(",")]
    limpos = {clean_translation(n) for n in brutos if n}

    for nome_pt in limpos:
        if nome_pt not in traduzidos:
            traduzidos[nome_pt] = []
        traduzidos[nome_pt].append(hexcode)

    print(f"[{idx}] {nome_en_str:25} → {', '.join(limpos):35} → {hexcode}")

# Geração final com expansão
linhas_finais = []
for nome, hex_list in traduzidos.items():
    hex_medio = average_hex(hex_list)
    linhas_finais.extend(expandir_genero(nome, hex_medio))

# Remove duplicatas (nome + hex)
linhas_finais = list({(l['input'], l['output']): l for l in linhas_finais}.values())
linhas_finais.sort(key=lambda x: x["input"])

# Salva
with open(output_jsonl, "w", encoding="utf-8") as f:
    for linha in linhas_finais:
        f.write(json.dumps(linha, ensure_ascii=False) + "\n")

print(f"\n✅ Tradução finalizada. {len(linhas_finais)} cores salvas em:\n{output_jsonl}")