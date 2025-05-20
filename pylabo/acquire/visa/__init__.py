pyvisa_installed = False

try:
    import pyvisa

except ImportError:
    pyvisa_installed = True

if pyvisa_installed:
    from . visa import find_instruments, Instrument
    from . oscil import Oscilloscope
    from . fungen import FunctionGenerator, Funs
