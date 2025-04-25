from transformers import MarianMTModel, MarianTokenizer
import os

# Caminho de destino para salvar o modelo MarianMT
save_path = r"Escolha o caminho para salvar o modelo"
model_name = "Helsinki-NLP/opus-mt-en-ROMANCE"

print("Baixando tokenizer do Opus")
tokenizer = MarianTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(save_path)

print("Baixando modelo Opus")
model = MarianMTModel.from_pretrained(model_name)
model.save_pretrained(save_path)

print(f"Modelo Opus salvo em: {save_path}")