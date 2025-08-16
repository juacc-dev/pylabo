import numpy as np
# from scipy import special
from pylabo.analysis.fit import Function


constant = Function(
    lambda x, c:
        c,
    ["C"],
    r"$C$"
)

linear = Function(
    lambda x, m, b:
        m * x + b,
    ["m", "b"],
    r"$m x + b$"
)

linear_homog = Function(
    lambda x, m:
        m * x,
    ["m"],
    r"$m x$"
)

exp = Function(
    lambda x, x0, k:
        k * np.exp(x - x0),
    ["x_0", "k"],
    r"k e^{x - x_0}"
)

cos = Function(
    lambda x, a, omega, delta:
        a * np.cos(omega * x + delta),
    ["A", "w", "d"],
    r"$A \cos(\omega x + \delta)$"
)

sin = Function(
    lambda x, a, omega, delta:
        a * np.sin(omega * x + delta),
    ["A", "w", "d"],
    r"$A \sin(\omega x + \delta)$"
)


# def polynomial(n: int):
#     def func(x, *args):
#         sum = 0
#         for i in range(len(args)):
#             sum += args[i] * x ** i
#         return sum

#     params = ["a" + str(k) for k in range(n)]
#     return Function(
#         func,
#         params
#     )
