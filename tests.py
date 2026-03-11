# Тесты

from main import der, find_deriv, find_gradient

assert der("5") == "0"
assert der("x") == "1"
assert find_deriv("x", 'y') == "0"

assert der("\\frac{x}{y}") == "\\frac{y}{y^{2}}"
assert der("x^2") == "2 * x"
assert der("x*x") == "x + x"
assert der("xx") == "x + x"

assert der("x + x") == "2"
assert der("x - x") == "0"

assert der("\\sin(x)") == "\\cos(x)"
assert der("\\cos(x)") == "-(\\sin(x))"
assert der("\\tan(x)") == "\\frac{1}{\\cos(x)^{2}}"

assert der("\\sinh(x)") == "\\cosh(x)"
assert der("\\cosh(x)") == "\\sinh(x)"

assert der("\\exp(x)") == "\\exp(x)"
assert der("\\ln(x)") == "\\frac{1}{x}"

assert find_gradient("a*b*c") == ['b * c', 'a * c', 'a * b']


print("Все тесты прошли успешно!")