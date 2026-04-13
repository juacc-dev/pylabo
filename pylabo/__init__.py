import pylabo.logs
import pylabo.plot
import pylabo.args

def defaults():
    # Parse CLI arguments
    pylabo.args.parse()

    # Default config
    pylabo.logs.config.setup()
    pylabo.plot.config.setup()
