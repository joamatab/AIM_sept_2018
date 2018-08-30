from ipkiss.technology.technology import TechnologyTree
from ipkiss.technology import get_technology

TECH = get_technology()

TECH.METRICS = TechnologyTree()
TECH.METRICS.GRID = 1E-9          # Default manufacturing grid, in nm
TECH.METRICS.UNIT = 1E-6          # Default user unit, in um
TECH.METRICS.ANGLE_STEP = 1.0     # Default angle step used in curve discretisation, in degrees