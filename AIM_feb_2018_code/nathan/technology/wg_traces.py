############################################################################################
# Waveguide traces:
# 
# Contains the default waveguide template for IPKISS and PICAZZO
############################################################################################

from ipkiss.technology import get_technology
from ipkiss.technology.technology import TechnologyTree, DelayedInitTechnologyTree

TECH = get_technology()

class TechWgTree(DelayedInitTechnologyTree):
    def initialize(self):
        from WgTemplate import StripWgTemplate

        self.WIRE = StripWgTemplate()
        self.DEFAULT = self.WIRE

TECH.PCELLS.WG = TechWgTree()


# Auto-transition database. Required for components that automatically taper between different waveguide types.
class TransitionTree(DelayedInitTechnologyTree):

    def initialize(self):

        from ipkiss3.pcell.trace.transitions.auto_transition.auto_transition_db import AutoTransitionDatabase
        db = AutoTransitionDatabase()
        self.AUTO_TRANSITION_DATABASE = db

TECH.PCELLS.TRANSITION = TransitionTree()


# Generic traces - required for Ipkiss.
# ##################################################################################################
# WARNING: The constants below are not used in the imec PDK. They're only required for IPKISS.     #
# ##################################################################################################

TECH.TRACE = TechnologyTree()
TECH.TRACE.DEFAULT_LAYER = TECH.PPLAYER.WG.COR
TECH.TRACE.CONTROL_SHAPE_LAYER = TECH.PPLAYER.WG.TRACE
TECH.TRACE.BEND_RADIUS = 5.0
TECH.TRACE.DRAW_CONTROL_SHAPE = False

TECH.DEFAULT_WAVELENGTH = 1.55

TECH.WG_DEFAULTS = TechnologyTree()
TECH.WG_DEFAULTS.N_EFF = 2.4
TECH.WG_DEFAULTS.N_GROUP = 4.3
TECH.WG_DEFAULTS.LOSS_DB_PERM = 200.0
TECH.WG_DEFAULTS.CORE_LAYER = TECH.PPLAYER.WG.COR

TECH.WG.CORE_WIDTH = 0.4
# TECH.WG.CLADDING_WIDTH = 4.0
TECH.WG.BEND_RADIUS = 5.0
