############################################################################################
# pin/port settings:
# 
# Contains the default port settings used by IPKISS and PICAZZO
############################################################################################

from ipkiss.technology import get_technology
from ipkiss.technology.technology import TechnologyTree

TECH = get_technology()

TECH.PORT = TechnologyTree()
TECH.PORT.DEFAULT_LAYER = TECH.PPLAYER.NONE.PIN  # Default layer for drawing pins
TECH.PORT.DEFAULT_LENGTH = 0.1              # Default length of a PIN
