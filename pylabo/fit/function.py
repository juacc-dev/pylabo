def split_params(n, x, *args):
    return args[:n], args[n:]


class Function:
    """
    Mathematical function with information about the parameters.
    """

    def __init__(
        self,
        f,               # Callable
        param_str: list[str],  # Parameter names
        eq: str = None      # LaTeX formula
    ):
        self.f = f
        self.param_str = param_str
        self.eq = eq

    def __add__(self, other):
        def f(x, *args):
            n = len(self.param_str)
            args1, args2 = split_params(n, x, *args)

            return self.f(x, *args1) + other.f(x, *args2)

        return Function(
            f,
            self.param_str + other.param_str,
            "Equation not supported"
        )

    def __sub__(self, other):
        def f(x, *args):
            n = len(self.param_str)
            args1, args2 = split_params(n, x, *args)

            return self.f(x, *args1) - other.f(x, *args2)

        return Function(
            f,
            self.param_str + other.param_str,
            "Equation not supported"
        )

    def __mul__(self, other):
        def f(x, *args):
            n = len(self.param_str)
            args1, args2 = split_params(n, x, *args)

            return self.f(x, *args1) * other.f(x, *args2)

        return Function(
            f,
            self.param_str + other.param_str,
            "Equation not supported"
        )

    def __truediv__(self, other):
        def f(x, *args):
            n = len(self.param_str)
            args1, args2 = split_params(n, x, *args)

            return self.f(x, *args1) / other.f(x, *args2)

        return Function(
            f,
            self.param_str + other.param_str,
            "Equation not supported"
        )

    # This is function composition: f & g -> f(g(x))
    def __and__(self, other):
        def f(x, *args):
            n = len(self.param_str)
            args1, args2 = split_params(n, x, *args)

            return self.f(other.f(x, *args2), *args2)

        return Function(
            f,
            self.param_str + other.param_str,
            "Equation not supported"
        )


class FittedFunction(Function):
    """
    Function class together with numeric parameters and information about the
    fit.
    """

    def __init__(
        self,
        func: Function,
        param_val: list[float],  # Optimal parameters
        param_cov: list[float],  # Covariance matrix
        param_err: list[float],  # Parameter uncertainty
        xlim: tuple[float],      # Interval of the data
        residue,                 # y_data - y_fit
        tests=None               # table with chi squared and stuff
    ):
        super().__init__(
            func.f,
            func.param_str,
            func.eq
        )

        self.param_val = param_val
        self.param_cov = param_cov
        self.param_err = param_err
        self.xlim = xlim
        self.residue = residue
        self.tests = tests
