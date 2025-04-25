import os
import json
from transformers import pipeline

# Paths
model_path = r"Caminho onde salvou o name-to-hex"
output_jsonl = r"Escolha o caminho para salvar o data"

# Base color names
base_colors = [
    "red", "green", "blue", "yellow", "orange", "pink", "purple", "brown", "black", "white", "gray",
    "cyan", "magenta", "lime", "teal", "indigo", "violet", "silver", "gold", "olive", "beige", "salmon"
]

modifiers = [
    "light", "dark", "deep", "bright", "pale", "soft", "neon", "dull", "warm", "cool"
]

# Generate combinations
color_inputs = set(base_colors)
for base in base_colors:
    for mod in modifiers:
        color_inputs.add(f"{mod} {base}")
        color_inputs.add(f"{base} {mod}")

# Manual additions
extra_colors = [
    "sky blue", "forest green", "mint green", "cherry red", "sand brown",
    "midnight blue", "eggplant", "peach", "coral", "rose"
]
color_inputs.update(extra_colors)
color_inputs = sorted(color_inputs)

# Load existing data
hex_to_names = {}

if os.path.exists(output_jsonl):
    with open(output_jsonl, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            names = item["input"]
            if isinstance(names, str):
                names = [names]
            hex_to_names[item["output"]] = set(map(str.lower, names))

# Load model
generator = pipeline("text2text-generation", model=model_path)

# Extraction process
new_count = 0
kept_count = 0
merged_count = 0

print("Iniciando extração incremental\n")

for color_name in color_inputs:
    color_lower = color_name.lower().strip()

    if any(color_lower in names for names in hex_to_names.values()):
        print(f"[Já existente] {color_name}")
        kept_count += 1
        continue

    result = generator(color_name, max_length=10)[0]["generated_text"].strip()

    if result.startswith("#") and len(result) == 7:
        if result in hex_to_names:
            hex_to_names[result].add(color_lower)
            print(f"[Agrupado] {color_name:25} -> {result}")
            merged_count += 1
        else:
            hex_to_names[result] = {color_lower}
            print(f"[Novo]     {color_name:25} -> {result}")
            new_count += 1
    else:
        print(f"[Ignorado] {color_name:25} -> {result}")

# Build final lines
final_lines = []
for hexcode, names in hex_to_names.items():
    sorted_names = sorted(names)
    input_field = sorted_names[0] if len(sorted_names) == 1 else sorted_names
    final_lines.append({"input": input_field, "output": hexcode})

# Sort output
final_lines.sort(key=lambda x: x["input"] if isinstance(x["input"], str) else x["input"][0])

# Save JSONL
os.makedirs(os.path.dirname(output_jsonl), exist_ok=True)
with open(output_jsonl, "w", encoding="utf-8") as f:
    for line in final_lines:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")

# Summary
print("\nExtração concluída.")
print(f"Novos adicionados  : {new_count}")
print(f"Agrupados (sinônimos): {merged_count}")
print(f"Ignorados/iguais   : {kept_count}")
print(f"Total final        : {len(final_lines)} hexadecimais únicos")