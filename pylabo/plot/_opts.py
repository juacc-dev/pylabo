from pylabo import logging

logger = logging.init("pylabo.plot")


DEFAULT_OPTS = {
    "font_family":  "",
    "font_size":    13,
    "dir":          "plots",
    "ext":          "png",
    "figsize":      (8, 6),
    "dpi":          100,
    "fmt":          "o",
    # "layout":       "compressed",
}

def opts(**kwargs):
    for k, v in kwargs.items():
        if k in DEFAULT_OPTS:
            opts.k = v
        else:
            logger.error("Invalid plot option.")

    return

opts.__dict__ = DEFAULT_OPTS
