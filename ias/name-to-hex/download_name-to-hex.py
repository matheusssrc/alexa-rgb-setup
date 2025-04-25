from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

# Caminho de destino
model_id = "oddadmix/name-to-hex"
save_path = r"Escolha o caminho para salvar o modelo"

# Nome do modelo original
model_name = "oddadmix/name-to-hex"

print("Baixando tokenizer")
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.save_pretrained(save_path)

print("Baixando modelo")
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
model.save_pretrained(save_path)

print(f"Modelo salvo com sucesso em:\n{save_path}")