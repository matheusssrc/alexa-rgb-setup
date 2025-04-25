from expression_evaluator import evaluate_expression

def test_expression(color, free_mode, work_mode, computer):
    expression = "color and computer and (free_mode xor work_mode) and free_mode"
    variables = {
        "color": color,
        "free_mode": free_mode,
        "work_mode": work_mode,
        "computer": computer
    }

    try:
        result = evaluate_expression(expression, variables)
        status = " APROVADO" if result else "NEGADO"
    except Exception as e:
        result = None
        status = f"[ERRO] {e}"

    print(f"\n Teste com valores:")
    print(f"  color: {color}")
    print(f"  free_mode: {free_mode}")
    print(f"  work_mode: {work_mode}")
    print(f"  computer: {computer}")
    print(f"  -> Resultado: {status}")


# Lista de testes
scenarios = [
    (True,  True,  False, True),  # Deve aprovar
    (True,  False, True,  True),  # Deve negar
    (True,  True,  True,  True),  # Deve negar
    (True,  False, False, True),  # Deve negar
    (True,  True,  False, False), # Deve negar
    (False, True,  False, True),  # Deve negar
]

if __name__ == "__main__":
    for c in scenarios:
        test_expression(*c)