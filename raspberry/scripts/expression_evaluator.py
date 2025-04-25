import re

# Define a precedência dos operadores
precedence = {
    'not': 3,
    'and': 2,
    'or': 1,
    'xor': 1
}

def tokenize_expression(expr):
    """
    Quebra a expressão em tokens válidos: operadores, parênteses e variáveis.
    """
    pattern = r"\b(?:and|or|not|xor)\b|[()]|\b[a-zA-Z_][a-zA-Z0-9_]*\b"
    return re.findall(pattern, expr)

def apply_operator(op, a, b=None):
    """
    Aplica o operador lógico entre operandos.
    """
    if op == 'not':
        return not a
    elif op == 'and':
        return a and b
    elif op == 'or':
        return a or b
    elif op == 'xor':
        return (a and not b) or (not a and b)
    raise ValueError(f"Operador inválido: {op}")

def has_higher_or_equal_precedence(op1, op2):
    """
    Compara precedência considerando operadores com mesma prioridade (esquerda para direita).
    """
    return precedence.get(op1, 0) >= precedence.get(op2, 0)

def validate_expression(tokens, variables):
    """
    Valida se a expressão tem apenas variáveis conhecidas e parênteses balanceados.
    """
    open_parens = 0
    last_token = ""
    for token in tokens:
        if token == '(':
            open_parens += 1
        elif token == ')':
            open_parens -= 1
            if open_parens < 0:
                raise ValueError("Parênteses fechados demais")
        elif token not in precedence and token not in variables and token not in ('(', ')'):
            raise ValueError(f"Variável desconhecida: '{token}'")
        elif last_token in precedence and token in precedence and token != 'not':
            raise ValueError(f"Operadores seguidos: '{last_token} {token}'")
        last_token = token
    if open_parens != 0:
        raise ValueError("Parênteses desbalanceados")

def evaluate_expression(expression: str, variables: dict) -> bool:
    """
    Avalia uma expressão booleana como:
    "(color and free_mode) and not (work_mode or not computer)"
    com base em:
    variables = { "color": True, "free_mode": True, ... }
    """
    tokens = tokenize_expression(expression)
    validate_expression(tokens, variables)

    operand_stack = []
    operator_stack = []

    def resolve_operator_stack():
        op = operator_stack.pop()
        if op == 'not':
            a = operand_stack.pop()
            operand_stack.append(apply_operator(op, a))
        else:
            b = operand_stack.pop()
            a = operand_stack.pop()
            operand_stack.append(apply_operator(op, a, b))

    for token in tokens:
        token = token.strip()

        if token in variables:
            operand_stack.append(variables[token])
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                resolve_operator_stack()
            if not operator_stack or operator_stack[-1] != '(':
                raise ValueError("Parênteses desbalanceados")
            operator_stack.pop()  # Remove '('
        elif token in precedence:
            while (operator_stack and operator_stack[-1] in precedence and
                   has_higher_or_equal_precedence(operator_stack[-1], token)):
                resolve_operator_stack()
            operator_stack.append(token)
        else:
            raise ValueError(f"Token inválido: {token}")

    while operator_stack:
        if operator_stack[-1] == '(':
            raise ValueError("Parênteses desbalanceados ao final")
        resolve_operator_stack()

    if len(operand_stack) != 1:
        raise ValueError("Expressão mal formada")

    return operand_stack[0]