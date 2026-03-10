import re

from parser import Parser


def createAST(formula: str):
    formula = formula.replace(" ", "")

    # Поиск токенов с помощью регулярного выражения:
    #   Выражение, начинающееся с '\'
    #   Число, целое или с плавающей точкой
    #   Одиночная переменная
    #   Скобки и операторы

    tokens = re.findall(r'(\\[a-zA-Z_]+|\d+(?:\.\d+)?|[a-zA-Z]|[+\-*/^_{}()])', formula)

    parser = Parser()

    return parser.parse_to_ast(tokens)


def find_first_var(formula):
    i = 0
    while i < len(formula):
        if formula[i] == '\\':
            i += 1
            while i < len(formula) and formula[i].isalpha():
                i += 1
            continue

        if formula[i].isalpha():
            if formula[i].lower() == 'e':
                i += 1
                continue
            return formula[i]
        i += 1
    return None


def find_deriv(formula: str, var: str = 'x', order: int = 1) -> str:
    ast = createAST(formula)

    # Берем производную n раз
    for i in range(order):
        ast = ast.diff(var)
        
    return ast.latex()


def der_by_var(formula: str, var: str) -> str:
    return find_deriv(formula, var)


def der(formula: str) -> str:
    var = find_first_var(formula)

    if var == None:
        # Если нет переменных, производная = 0
        return "0"

    return find_deriv(formula, var)


print(der("x^2 + x"))