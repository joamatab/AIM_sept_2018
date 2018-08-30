######################################################################
# Settings for blocks and adapters (Required for IOFibCoup in Picazzo)
######################################################################

from ipkiss.technology import get_technology
TECH = get_technology()
from ipkiss.technology.technology import TechnologyTree

TECH.BLOCKS = TechnologyTree()
TECH.BLOCKS.DEFAULT_YSPACING = 35.0
TECH.BLOCKS.DEFAULT_WIDTH = 500.0