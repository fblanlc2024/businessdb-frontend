import sympy as sp
import string
from sympy.abc import x
from random import randint

# Symbol generator
def random_symbol():
    symbols = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
    symbol = random.choice(symbols)
    return sp.symbols(symbol)

# Problem Generators
def random_linear():
    m, b = random_symbol(), random_symbol()
    m_val = sp.Rational(sp.randint(-10, 10))
    b_val = sp.Rational(sp.randint(-10, 10))
    return m*m_val + b*b_val

def random_quadratic():
    a, b, c, x = random_symbol(), random_symbol(), random_symbol(), random_symbol()
    a_val = sp.Rational(sp.randint(-10, 10))
    b_val = sp.Rational(sp.randint(-10, 10))
    c_val = sp.Rational(sp.randint(-10, 10))
    return a*a_val*x**2 + b*b_val*x + c*c_val

def random_rational():
    x = sp.symbols('x')
    numerator = random_quadratic()
    denominator = random_linear()
    return numerator/denominator

def random_exponential():
    a, b, x = random_symbol(), random_symbol(), random_symbol()
    a_val = sp.Rational(sp.randint(1, 10))
    b_val = sp.Rational(sp.randint(2, 10))
    return a*a_val * b**b_val*x

def random_logarithmic():
    a, b, x = random_symbol(), random_symbol(), random_symbol()
    a_val = sp.Rational(sp.randint(1, 10))
    b_val = sp.Rational(sp.randint(2, 10))
    return a*a_val * sp.log(b_val*x)

def random_trig():
    a, b, c, d, x = random_symbol(), random_symbol(), random_symbol(), random_symbol(), random_symbol()
    a_val = sp.Rational(sp.randint(-10, 10))
    b_val = sp.Rational(sp.randint(-10, 10))
    c_val = sp.Rational(sp.randint(-10, 10))
    d_val = sp.Rational(sp.randint(-10, 10))
    funcs = [sp.sin, sp.cos, sp.tan]
    return a*a_val * funcs[sp.randint(0, 2)](b*b_val*x + c*c_val) + d*d_val

def random_polynomial(degree=3):
    coeffs = [randint(1, 10) for _ in range(degree + 1)]
    return Poly(coeffs, x)

def random_piecewise():
    condition = x < 0
    return Piecewise((sin(x), condition), (cos(x), True))

def random_abs_function():
    a = randint(1, 10)
    b = randint(-10, 10)
    return Abs(a * x + b)

def random_radical_function():
    a = randint(1, 10)
    b = randint(-10, 10)
    return sqrt(a * x + b)

def random_linear_with_y():
    a, b, c = random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)
    return a*x + b*y - c

def random_quadratic_without_linear():
    a, c = random.randint(1, 10), random.randint(1, 10)
    return a*x**2 + c

def random_rational_quadratic():
    a, b, c, d = random.randint(1, 10), random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)
    return (a*x**2 + b)/(c*x**2 + d)

def get_correct_answer(equation):
    return sp.solve(equation)

def get_incorrect_answers(correct_answer, num_choices=3):
    incorrect_answers = set()
    while len(incorrect_answers) < num_choices:
        perturbation = random.randint(-10, 10)
        incorrect_answer = correct_answer + perturbation
        if incorrect_answer != correct_answer:
            incorrect_answers.add(incorrect_answer)
    return list(incorrect_answers)