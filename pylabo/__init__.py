import pylabo.logs
import pylabo.plot
import pylabo.fit
import pylabo.proc
import pylabo.args
import pylabo.visa

def defaults():
    # Parse CLI arguments
    pylabo.args.parse()

    # Default config
    pylabo.logs.config.setup()
    pylabo.plot.config.setup()
