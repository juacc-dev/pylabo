from pylabo.lib.opts import Options
opts = Options()

# Possible backends are NI-VISA (default) and PyVISA-Py ("@py")
opts.backend = ""  # NI-VISA

opts.startup_sleep = 0.2  # 200 ms
