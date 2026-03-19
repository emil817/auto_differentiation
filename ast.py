# Абстрактное синтаксическое дерево
class Node:
    # Базовый класс для узла
    def diff(self, var: str):
        """
        Метод для нахождения производной по var
        """

        raise NotImplementedError

    def latex(self) -> str:
        """
        Метод для получения latex-представления узла
        """

        raise NotImplementedError

    def has_var(self, var: str) -> bool:
        """
        Метод для проверки, зависит ли узел от переменной
        """

        raise NotImplementedError
    
    def simplify(self):
        """
        Метод для упрощения узла
        """

        return self


class Const(Node):
    def __init__(self, value):
        self.value = value

    def has_var(self, var):
        return False

    def diff(self, var):
        return Const(0)

    def latex(self):
        return str(self.value)


class Var(Node):
    def __init__(self, name):
        self.name = name

    def has_var(self, var):
        return self.name == var

    def diff(self, var):
        if self.name == var:
            return Const(1)
        else:
            return Const(0)

    def latex(self):
        return self.name


class E_Const(Node):
    def diff(self, var):
        return Const(0)
    
    def has_var(self, var):
        return False

    def latex(self):
        return "e"


class Add(Node):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def has_var(self, var):
        return self.left.has_var(var) or self.right.has_var(var)

    def diff(self, var):
        return Add(self.left.diff(var), self.right.diff(var))
        
    def latex(self):
        return f"{self.left.latex()} + {self.right.latex()}"
    
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()

        if isinstance(left, Const) and isinstance(right, Const):
            return Const(left.value + right.value)
        
        if isinstance(left, Const):
            if left.value == 0:
                return right
        
        if isinstance(right, Const):
            if right.value == 0:
                return left
        
        return Add(left, right)


class Sub(Node):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def has_var(self, var):
        return self.left.has_var(var) or self.right.has_var(var)

    def diff(self, var):
        return Sub(self.left.diff(var), self.right.diff(var))

    def latex(self):
        if isinstance(self.right, Add) or isinstance(self.right, Sub):
            return f"{self.left.latex()} - ({self.right.latex()})"

        return f"{self.left.latex()} - {self.right.latex()}"
    
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()

        if isinstance(left, Const) and isinstance(right, Const):
            return Const(left.value - right.value)

        if isinstance(left, Const):
            if left.value == 0:
                return Neg(right)

        if isinstance(right, Const):
            if right.value == 0:
                return left

        return Sub(left, right)


class Mul(Node):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def has_var(self, var):
        return self.left.has_var(var) or self.right.has_var(var)

    def diff(self, var):
        # (uv)' = u'v + uv'
        return Add(Mul(self.left.diff(var), self.right), Mul(self.left, self.right.diff(var)))

    def latex(self):
        if isinstance(self.left, Add) or isinstance(self.left, Sub):
            left = "(" + self.left.latex() + ")"
        else:
            left = self.left.latex()
        
        if isinstance(self.right, Add) or isinstance(self.right, Sub):
            right = "(" + self.right.latex() + ")"
        else:
            right = self.right.latex()

        return f"{left} * {right}"
    
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()

        if isinstance(left, Const) and isinstance(right, Const):
            return Const(left.value * right.value)

        if isinstance(left, Const):
            if left.value == 0:
                return Const(0)
            if left.value == 1:
                return right

        if isinstance(right, Const):
            if right.value == 0:
                return Const(0)
            if right.value == 1:
                return left

        return Mul(left, right)


class Div(Node):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def has_var(self, var):
        return self.left.has_var(var) or self.right.has_var(var)

    def diff(self, var):
        # (u/v)' = (u'v - uv') / v^2
        u, v = self.left, self.right
        num = Sub(Mul(u.diff(var), v), Mul(u, v.diff(var)))
        den = Pow(v, Const(2))
        return Div(num, den)

    def latex(self):
        return "\\frac{" + self.left.latex() + "}{" + self.right.latex() + "}"

    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()

        if isinstance(left, Const):
            if left.value == 0:
                return Const(0)

        if isinstance(right, Const):
            if right.value == 1:
                return left

        return Div(left, right)


class Pow(Node):
    def __init__(self, left, right):
        self.left, self.right = left, right
    
    def has_var(self, var):
        return self.left.has_var(var) or self.right.has_var(var)
    
    def diff(self, var):
        f, g = self.left, self.right

        # Если ни база, ни степень не зависят от переменной
        if not self.has_var(var): return Const(0)

        # Если степень константа: (x^n)' = n * x^{n-1} * x'
        if not g.has_var(var):
            return Mul(Mul(g, Pow(f, Sub(g, Const(1)))), f.diff(var))

        # (f^g)' = (e^{g \ln f})' = f^g * (g' \ln f + g f' / f)
        inner_diff = Add(Mul(g.diff(var), Ln(f)), Mul(g, Div(f.diff(var), f)))
        return Mul(self, inner_diff)

    def latex(self):
        if isinstance(self.left, Add) or isinstance(self.left, Sub) or \
           isinstance(self.left, Mul):
            return "(" + self.left.latex() + ")^{" + self.right.latex() + "}"

        return self.left.latex() + "^{" + self.right.latex() + "}"

    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()

        if isinstance(right, Const):
            if right.value == 0:
                return Const(1)
            if right.value == 1:
                return left

        if isinstance(left, Const):
            if left.value == 0:
                return Const(0)
            if left.value == 1:
                return Const(1)      

        return Pow(left, right)


class Log(Node):
    precedence = 4
    def __init__(self, base, arg):
        self.base, self.arg = base, arg

    def has_var(self, var):
        return self.base.has_var(var) or self.arg.has_var(var)

    def diff(self, var):
        # log_{b} (a) = ln (a) / ln (b)
        return Div(Ln(self.arg), Ln(self.base)).diff(var)

    def latex(self):
        return "\\log_{" + self.base.latex()+ "}" + f"({self.arg.latex()})"
    
    def simplify(self):
        return Log(self.base.simplify(), self.arg.simplify())


class Neg(Node):
    def __init__(self, arg):
        self.arg = arg

    def has_var(self, var):
        return self.arg.has_var(var)

    def diff(self, var):
        return Neg(self.arg.diff(var))

    def latex(self):
        return f"-({self.arg.latex()})"
    
    def simplify(self):
        a = self.arg.simplify()
        if isinstance(a, Const):
            return Const(-a.value)

        return Neg(a)


class FuncNode(Node):
    func_name = ""
    def __init__(self, arg):
        self.arg = arg

    def has_var(self, var):
        return self.arg.has_var(var)

    def latex(self):
        return f"\\{self.func_name}({self.arg.latex()})"

    def simplify(self):
        return self.__class__(self.arg.simplify())


class Sin(FuncNode):
    func_name = "sin"
    def diff(self, var):
        return Mul(Cos(self.arg), self.arg.diff(var))


class Cos(FuncNode):
    func_name = "cos"
    def diff(self, var):
        return Mul(Neg(Sin(self.arg)), self.arg.diff(var))


class Tan(FuncNode):
    func_name = "tan"
    def diff(self, var):
        return Div(self.arg.diff(var), Pow(Cos(self.arg), Const(2)))


class Cot(FuncNode):
    func_name = "cot"
    def diff(self, var):
        return Neg(Div(self.arg.diff(var), Pow(Sin(self.arg), Const(2))))


class Sinh(FuncNode):
    func_name = "sinh"
    def diff(self, var):
        return Mul(Cosh(self.arg), self.arg.diff(var))


class Cosh(FuncNode):
    func_name = "cosh"
    def diff(self, var):
        return Mul(Sinh(self.arg), self.arg.diff(var))


class Tanh(FuncNode):
    func_name = "tanh"
    def diff(self, var):
        return Div(self.arg.diff(var), Pow(Cosh(self.arg), Const(2)))


class Coth(FuncNode):
    func_name = "coth"
    def diff(self, var):
        return Neg(Div(self.arg.diff(var), Pow(Sinh(self.arg), Const(2))))


class Exp(FuncNode):
    func_name = "exp"
    def diff(self, var):
        return Mul(Exp(self.arg), self.arg.diff(var))


class Ln(FuncNode):
    func_name = "ln"
    def diff(self, var):
        return Div(self.arg.diff(var), self.arg)


class Sqrt(FuncNode):
    func_name = "sqrt"
    def diff(self, var):
        return Div(self.arg.diff(var), Mul(Const(2), Sqrt(self.arg)))
