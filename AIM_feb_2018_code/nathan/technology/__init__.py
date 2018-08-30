from ipkiss.technology import TECHNOLOGY as TECH  # Import the base technology from IPKISS.

__all__ = ["TECH"]

TECH.name = "AIMACTIVE"

from technologies.base_ipkiss.admin import *          # Admin: auto-name generator, ...
from .metrics import *                                # grid and unit discretizatin
from .layers import *                                 # process layers, pattern purposes, PPLayers
from .ports import *                                  # pin recognition settings
from .dimension import *                               # design rules and default dimensions for IPKISS

from technologies.base_ipkiss.pcells import *         # Initializes the PCELL tree to add PCELLS to the TECH
# blocks not change!! don't trust these values
from .blocks import *                                 # Block settings for IOColumn

from .wg_traces import *
# from .metal_traces import *

from .display import *
from .gdsii import *
# try:
#     import oatools
#     from .openaccess import *
# except:
#     pass
#
#vfab not changed from IMEC! don't trust these values
from .vfab import *
# from .fibcoup import *

# from .transitions import *                           # Transitions in the auto-transition database - keep this last
from .picazzo_defaults import *
