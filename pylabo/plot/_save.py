import matplotlib.pyplot as plt
from pathlib import Path
import logging
from . _opts import opts

logger = logging.getLogger("pylabo.plot")

def save(
    filename: str,
    append: str = None,
    **kwargs
):
    plt.tight_layout()

    if append is not None:
        filename += f"-{append}"

    filename += f".{opts.ext}"

    path = Path(opts.dir) / filename

    logger.info(f"Saving figure at '{path}'.")

    path.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(path, **kwargs)


def show():
    plt.tight_layout()
    plt.show()
    plt.close()
