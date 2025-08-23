import pandas as pd


def split_params(n, x, *args):
    """Function for internal use. It's common functionality for operator
    overloading."""

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
            self.param_str + other.param_str
        )

    def __sub__(self, other):
        def f(x, *args):
            n = len(self.param_str)
            args1, args2 = split_params(n, x, *args)

            return self.f(x, *args1) - other.f(x, *args2)

        return Function(
            f,
            self.param_str + other.param_str
        )

    def __mul__(self, other):
        def f(x, *args):
            n = len(self.param_str)
            args1, args2 = split_params(n, x, *args)

            return self.f(x, *args1) * other.f(x, *args2)

        return Function(
            f,
            self.param_str + other.param_str
        )

    def __truediv__(self, other):
        def f(x, *args):
            n = len(self.param_str)
            args1, args2 = split_params(n, x, *args)

            return self.f(x, *args1) / other.f(x, *args2)

        return Function(
            f,
            self.param_str + other.param_str
        )

    # This is function composition: f & g -> f(g(x))
    def __and__(self, other):
        def f(x, *args):
            n = len(self.param_str)
            args1, args2 = split_params(n, x, *args)

            return self.f(other.f(x, *args2), *args2)

        return Function(
            f,
            self.param_str + other.param_str
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
        self.residue = residue
        self.tests = tests

    def report(self) -> pd.DataFrame:
        """Create a dataframe with the results of the fit: tests (like reduced
        chi squared) and optimal parameters, the latter with their uncertainty.
        """

        # 1st column: parameter names
        names = list(self.tests.keys()) + self.param_str

        # 2nd column: values / optimal values
        values = list(self.tests.values()) + list(self.param_val)

        # 3rd column: uncertainty. Tests don't have any
        errors = [None for _ in range(
            len(self.tests))] + list(self.param_err)

        df = pd.DataFrame({
            "Parámetro": pd.Series(names),
            "Valor": pd.Series(values),
            "Error": pd.Series(errors)
        })

        return df
