from . _opts import opts, DEFAULT_OPTS
from . _data_plot import data
from . _fit_plot import data_and_fit
from . _save import save, show

opts.__dict__ = DEFAULT_OPTS
opts(**DEFAULT_OPTS)
