from ast import *


# Парсер
class Parser:
    def __init__(self):
        self.index = 0

    def parse_to_ast(self, tokens: list):
        self.tokens = tokens
        self.len = len(tokens)

        return self.parse_add_sub()
    
    def current(self):
        if self.index < self.len:
            return self.tokens[self.index]
        else:
            return None

    def parse_add_sub(self):
        node = self.parse_mul_div()

        # Парсим все слагаемые
        while self.current() in ('+', '-'):
            if self.current() == '+':
                self.index += 1
                node = Add(node, self.parse_mul_div())
            else:
                self.index += 1
                node = Sub(node, self.parse_mul_div())

        return node
    
    def parse_mul_div(self):
        node = self.parse_neg_pow()

        # Парсим все множители, в том числе неявные
        while self.current():
            if self.current() in ('*', '/'):
                if self.current() == '*':
                    self.index += 1
                    node = Mul(node, self.parse_neg_pow())
                else:
                    self.index += 1
                    node = Div(node, self.parse_neg_pow())
            elif self.current()[0] == '\\' or \
                 self.current() in ('(', '{') or \
                 self.current().isalpha() and len(self.current()) == 1 or \
                 self.current()[0].isdigit():
                node = Mul(node, self.parse_neg_pow())
            else:
                break
        
        return node
    
    def parse_neg_pow(self):
        # Парсим минус и степень
        if self.current() == '-':
            self.index += 1
            return Neg(self.parse_neg_pow())
        
        node = self.parse_const_var_brackets()
        if self.current() == '^':
            self.index += 1
            node = Pow(node, self.parse_neg_pow())

        return node
    
    def parse_const_var_brackets(self):
        # Парсим скобки, константы, переменные и функции
        if self.current() == '(':
            self.index += 1
            node = self.parse_add_sub()
            if self.current() == ')':
                self.index += 1
            return node
        if self.current() == '{':
            self.index += 1
            node = self.parse_add_sub()
            if self.current() == '}':
                self.index += 1
            return node

        if self.current()[0].isdigit():
            if '.' in self.current():
                node = Const(float(self.current()))
            else:
                node = Const(int(self.current()))
            self.index += 1
            return node

        if self.current().isalpha() and len(self.current()) == 1:
            if self.current() == 'e':
                self.index += 1
                return E_Const()
            else:
                name = self.current()
                self.index += 1
                return Var(name)

        if self.current()[0] == '\\':
            return self.parse_function()

    def parse_function(self):
        # Парсим функции, начинающиеся с \ в Latex
        function = self.current()
        self.index += 1
        if function == '\\frac':
            return Div(self.parse_const_var_brackets(),
                       self.parse_const_var_brackets())
        if function == '\\log_':
            return Log(self.parse_const_var_brackets(),
                       self.parse_const_var_brackets())

        func_map = {
            '\\sin': Sin, '\\cos': Cos, '\\tan': Tan, '\\cot': Cot,
            '\\sinh': Sinh, '\\cosh': Cosh, '\\tanh': Tanh, '\\coth': Coth,
            '\\exp': Exp, '\\ln': Ln
        }

        if function in func_map:
            return func_map[function](self.parse_const_var_brackets())