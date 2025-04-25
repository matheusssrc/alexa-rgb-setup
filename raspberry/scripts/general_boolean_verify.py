from typing import Tuple

from expression_evaluator import evaluate_expression
from conditions.colors_verify import verify_color_from_alexa
from conditions.free_mode import is_free_mode
from conditions.work_mode import is_work_mode
from conditions.computer_status import is_computer_active

def can_change_color(alexa_json) -> Tuple[bool, str, str]:
    print("Iniciando verificação geral")

    color_found, name, hex_code = verify_color_from_alexa(alexa_json)
    free = is_free_mode()
    work = is_work_mode()
    computer_on = is_computer_active()

    print(f"Cor encontrada? {color_found}")
    print(f"Modo livre ativo? {free}")
    print(f"Modo trabalho ativo? {work}")
    print(f"Computador ligado? {computer_on}")

    expression = "color and computer and (free_mode xor work_mode) and free_mode"
    variables = {
        "color": color_found,
        "free_mode": free,
        "work_mode": work,
        "computer": computer_on
    }

    try:
        condition = evaluate_expression(expression, variables)
    except Exception as e:
        print(f"[ERRO - EXPRESSION] {e}")
        condition = False

    if condition:
        print("Condição geral aprovada. Pode trocar a cor.")
        return True, name, hex_code
    else:
        print("Condição geral negada. Troca de cor bloqueada.")
        return False, "", ""