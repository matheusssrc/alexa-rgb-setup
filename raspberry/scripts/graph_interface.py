from tkinter import *
from expression_evaluator import evaluate_expression

# Simulando os valores reais coletados (você pode depois tornar isso editável)
variables = {
    "color": True,
    "free_mode": True,
    "work_mode": False,
    "computer": True
}

def avaliar():
    expr = entrada.get()
    try:
        result = evaluate_expression(expr, variables)
        resultado_label.config(text=f"Resultado: {result}", fg="green")
    except Exception as e:
        resultado_label.config(text=f"Erro: {e}", fg="red")

# Interface Gráfica
root = Tk()
root.title("Avaliador Lógico - Alexa RGB")
root.geometry("600x300")

# Entrada de expressão
Label(root, text="Digite a expressão lógica:").pack(pady=5)
entrada = Entry(root, width=80)
entrada.insert(0, "(color and free_mode) and not (work_mode or not computer)")
entrada.pack(pady=5)

# Botão de avaliação
Button(root, text="Avaliar", command=avaliar, bg="blue", fg="white").pack(pady=10)

# Mostrar os valores atuais das variáveis
valores_frame = Frame(root)
valores_frame.pack(pady=5)
Label(valores_frame, text="Valores atuais das condições:").grid(row=0, column=0, columnspan=2)

for idx, (var, val) in enumerate(variables.items(), start=1):
    Label(valores_frame, text=f"{var}:").grid(row=idx, column=0, sticky=W)
    Label(valores_frame, text=str(val)).grid(row=idx, column=1, sticky=W)

# Resultado da avaliação
resultado_label = Label(root, text="", font=("Arial", 12, "bold"))
resultado_label.pack(pady=10)

# Iniciar a janela
root.mainloop()