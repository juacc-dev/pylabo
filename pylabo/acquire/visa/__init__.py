import logging
logger = logging.getLogger("pylabo.acquire")

try:
    import pyvisa

    import pylabo.acquire.visa.visa
    import pylabo.acquire.visa.fungen
    import pylabo.acquire.visa.oscil

except ImportError:
    logger.error("PyVisa not installed.")
