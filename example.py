from main import der, der_by_var, find_gradient, find_deriv

# Примеры работы:

print('f(x) = x^2 + 3x + 5')
print("f'(x) =", der('x^2 + 3x + 5'))
print()


print('f(x) = \\sin(x)')
print("f'(x) =", der('\\sin(x)'))
print()


print('f(x) = \\sin(x) + \\cos(x)')
print("f'(x) =", der('\\sin(x) + \\cos(x)'))
print()


print('f(x) = \\tan(x)^x')
print("f'(x) =", der('\\tan(x)^x'))
print()


print('f(x, y) = x^2 + y^2')
print('∂f/∂x =', der_by_var('x^2 + y^2', 'x'))
print('∂f/∂y =', der_by_var('x^2 + y^2', 'y'))
print()


print('f(x) = x^2 + 4x + 6')
print("f'(x) =",find_deriv('x^2 + 4x + 6', 'x', 1))
print("f''(x) =",find_deriv('x^2 + 4x + 6', 'x', 2))
print("f'''(x) =",find_deriv('x^2 + 4x + 6', 'x', 3))
print()


print('f(x, y) = x^2 + y^2')
print('∇f =', find_gradient('x^2 + y^2'))
print()