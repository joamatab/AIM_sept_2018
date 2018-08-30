############################################################################################
# Metal traces:
# 
# Contains the default metal template for IPKISS and PICAZZO
############################################################################################

from ipkiss.technology import get_technology
from ipkiss.technology.technology import DelayedInitTechnologyTree

TECH = get_technology()

class TechWireTree(DelayedInitTechnologyTree):
    def initialize(self):
        from isipp50g.components.metal.metal_traces import M1Wire

        self.WIRE = M1Wire()
        self.DEFAULT = self.WIRE
        
TECH.PCELLS.METAL = TechWireTree()

