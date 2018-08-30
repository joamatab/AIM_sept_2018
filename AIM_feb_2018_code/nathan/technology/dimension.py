############################################################################################
# Design rule and dimension settings:
#
# This file contains default settings which are used throughout IPKISS and PICAZZO
# - Some global settings
# - Per process layer settings, like minimum width, default width, default bend radius, ....
############################################################################################

from ipkiss.technology import get_technology
from ipkiss.technology.technology import TechnologyTree
from ipkiss.geometry.shapes.basic import ShapeRectangle
from ipkiss.geometry.coord import Coord2

TECH = get_technology()

TECH.TECH = TechnologyTree()
TECH.TECH.MINIMUM_LINE = 0.130
TECH.TECH.MINIMUM_SPACE = 0.150

############
# WG
############
TECH.WG = TechnologyTree()
TECH.WG.CORE_WIDTH = 0.4                                                         # Default waveguide width on WG layer (core)
TECH.WG.WIRE_WIDTH = TECH.WG.CORE_WIDTH  # ipkiss3 compatibility
TECH.WG.CLADDING_WIDTH = 5.0
TECH.WG.SPACING = 2.0                                                             # Default waveguide spacing (center-to-center)
TECH.WG.SHORT_STRAIGHT = 2.0                                                      # Default length of a short straight waveguide, used in routing algorithms
TECH.WG.SHORT_TRANSITION_LENGTH = 5.0                                             # Default length of simple transitions (tapers)
TECH.WG.EXPANDED_WIDTH = 0.8                                                      # Default width of expanded waveguides (used in automatically flaring out waveguides)
TECH.WG.EXPANDED_STRAIGHT = 5.0                                                   # Default length of a straight for an expanded waveguide (used in automatically flairing out waveguides)
TECH.WG.EXPANDED_TAPER_LENGTH = 3.0                                               # Default taper length of expanded waveguides (used in automatically flaring out waveguides)
TECH.WG.TRENCH_WIDTH = 2.0                                                        # Required for Ipkiss 2.4 compatibility
TECH.WG.BEND_RADIUS = 5.0                                                         # Default bend radius for strip waveguides
TECH.WG.DC_SPACING = TECH.WG.CORE_WIDTH + 0.18
TECH.WG.SHORT_TAPER_LENGTH = 5.0                                                  # Required for Picazzo 2.4 compatibility
TECH.WG.ANGLE_STEP = 1.0


TECH.CONTAINER = TechnologyTree()
TECH.CONTAINER.TERMINATE_PORTS = TechnologyTree()
TECH.CONTAINER.TERMINATE_PORTS.CHILD_SUFFIX = "termination"
TECH.CONTAINER.TERMINATE_PORTS.TERMINATION_INSTANCE_PREFIX = "termination"