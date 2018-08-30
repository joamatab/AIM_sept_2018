############################################################################################
# virtual fabrication setting:
# 
# This file contains settings to associate different combinations process layers with material stacks
############################################################################################

from ipkiss.technology import get_technology
from ipkiss.technology.technology import TechnologyTree

TECH = get_technology()

from ipkiss.plugins.vfabrication.process_flow import VFabricationProcessFlow
from pysics.basics.material.material_stack import MaterialStack, MaterialStackFactory
from pysics.basics.material.material import Material, MaterialFactory
from pysics.materials.electromagnetics import *

TECH.MATERIALS = MaterialFactory()

from ipkiss.visualisation.display_style import DisplayStyle
from ipkiss.visualisation import color


# Color scheme
COLOR_BABY_BLUE = Color(name = "Baby blue", red = 0.78, green = 0.84, blue = 0.91)
COLOR_UGLY_PINK = Color(name = "Ugly pink", red = 0.82, green = 0.59, blue = 0.58)
COLOR_DARK_UGLY_PINK = Color(name = "Dark ugly pink", red = 0.63, green = 0.43, blue = 0.43)
COLOR_LIGHT_UGLY_PINK = Color(name = "Ligtht ugly pink", red = 0.90, green = 0.76, blue = 0.76)
COLOR_DIAPER_BLUE = Color(name = "Diaper blue", red = 0.58, green = 0.70, blue = 0.84)
COLOR_SEA_GREEN = Color(name="Seagreen", red=0.4, green=0.8, blue=0.4)
COLOR_LIGHT_BLUE = Color(name="Lightblue", red=0.4, green=0.4, blue=0.9)
COLOR_DARK_BLUE = Color(name="Darkblue", red=0.0, green=0.0, blue=0.4)
COLOR_LIGHT_RED = Color(name="Lightred", red=0.9, green=0.4, blue=0.4)
COLOR_DARK_RED = Color(name="Darkred", red=0.4, green=0.0, blue=0.0)
COLOR_NICKEL = Color(name="Nickel", red=0.7, green=0.7, blue=0.8)
COLOR_TUNGSTEN = Color(name="Tungsten", red=0.47, green=0.49, blue=0.52)

# Material
TECH.MATERIALS.AIR = Material(name="air", display_style=DisplayStyle(color=COLOR_BABY_BLUE), solid=False)
TECH.MATERIALS.SILICON = Material(name="silicon", display_style=DisplayStyle(color=COLOR_UGLY_PINK))
TECH.MATERIALS.SILICON_NITRIDE = Material(name="silicon nitride", display_style=DisplayStyle(color=COLOR_SEA_GREEN))
TECH.MATERIALS.P_SILICON = Material(name="P-silicon", display_style=DisplayStyle(color=COLOR_LIGHT_RED))
TECH.MATERIALS.PB_SILICON = Material(name="PBODY-silicon", display_style=DisplayStyle(color=COLOR_RED))
TECH.MATERIALS.PP_SILICON = Material(name="PPLUS-silicon", display_style=DisplayStyle(color=COLOR_DARK_RED))
TECH.MATERIALS.N_SILICON = Material(name="N-silicon", display_style=DisplayStyle(color=COLOR_LIGHT_BLUE))
TECH.MATERIALS.NB_SILICON = Material(name="NBODY-silicon", display_style=DisplayStyle(color=COLOR_BLUE))
TECH.MATERIALS.NN_SILICON = Material(name="NPLUS-silicon", display_style=DisplayStyle(color=COLOR_DARK_BLUE))
TECH.MATERIALS.SILICON_OXIDE = Material(name="silicon oxide", display_style=DisplayStyle(color=COLOR_DIAPER_BLUE))
TECH.MATERIALS.POLYSILICON = Material(name = "poly", display_style = DisplayStyle(color = color.COLOR_CHERRY))
TECH.MATERIALS.SILICIDE = Material(name="silicide", display_style=DisplayStyle(color=COLOR_NICKEL))
TECH.MATERIALS.TUNGSTEN = Material(name="tungsten", display_style=DisplayStyle(color=COLOR_TUNGSTEN))
TECH.MATERIALS.COPPER = Material(name="copper", display_style=DisplayStyle(color=COLOR_COPPER))

TECH.MATERIALS.SILICON.epsilon = 12
TECH.MATERIALS.POLYSILICON.epsilon = 12.25
TECH.MATERIALS.SILICON_OXIDE.epsilon = 2.3104
TECH.MATERIALS.AIR.epsilon = 1

# Material stacks
TECH.MATERIAL_STACKS = MaterialStackFactory()

# Layer thicknesses
# Nominal thickness is specified, see ISIPP50G technology handbook
MSTACK_BOX_THICKNESS = 0.500
MSTACK_SOI_THICKNESS = 0.214
MSTACK_SOI_FC_THICKNESS = 0.144
MSTACK_SOI_SKT_THICKNESS = 0.061
MSTACK_GATEOX_THICKNESS = 0.005
MSTACK_POLY_THICKNESS = 0.160
MSTACK_SOI_POLY_THICKNESS = MSTACK_SOI_THICKNESS + MSTACK_GATEOX_THICKNESS + MSTACK_POLY_THICKNESS
MSTACK_PMD_THICKNESS = 1.0
MSTACK_SAL_THICKNESS = 0.05
MSTACK_D_LINER = 0.390
MSTACK_LINER_THICKNESS = 0.050
MSTACK_M1_THICKNESS = 0.500
MSTACK_IMD_THICKNESS = 0.500
MSTACK_M2_THICKNESS = 0.700

# material stacks FEOL (SOI+poly)
TECH.MATERIAL_STACKS.MSTACK_STI_OX = MaterialStack(name = "374nm STI Oxide", 
                                                   materials_heights = [(TECH.MATERIALS.SILICON_OXIDE, MSTACK_BOX_THICKNESS),
                                                                        (TECH.MATERIALS.SILICON_OXIDE, MSTACK_SOI_THICKNESS)
                                                                        ], 
                                                   display_style = DisplayStyle(color = COLOR_BABY_BLUE))

TECH.MATERIAL_STACKS.MSTACK_SOI_SKT = MaterialStack(name = "61nm SOI", 
                                                    materials_heights = [(TECH.MATERIALS.SILICON_OXIDE, MSTACK_BOX_THICKNESS),
                                                                         (TECH.MATERIALS.SILICON, MSTACK_SOI_SKT_THICKNESS),
                                                                         (TECH.MATERIALS.SILICON_OXIDE, MSTACK_SOI_THICKNESS - MSTACK_SOI_SKT_THICKNESS)
                                                                         ], 
                                                    display_style = DisplayStyle(color = COLOR_LIGHT_UGLY_PINK))

TECH.MATERIAL_STACKS.MSTACK_SOI_FC = MaterialStack(name = "144nm SOI", 
                                                   materials_heights = [(TECH.MATERIALS.SILICON_OXIDE, MSTACK_BOX_THICKNESS),
                                                                        (TECH.MATERIALS.SILICON, MSTACK_SOI_FC_THICKNESS),
                                                                        (TECH.MATERIALS.SILICON_OXIDE, MSTACK_SOI_THICKNESS - MSTACK_SOI_FC_THICKNESS)
                                                                        ], 
                                                   display_style = DisplayStyle(color = COLOR_UGLY_PINK))

TECH.MATERIAL_STACKS.MSTACK_SOI = MaterialStack(name = "214nm SOI", 
                                                materials_heights = [(TECH.MATERIALS.SILICON_OXIDE, MSTACK_BOX_THICKNESS),
                                                                     (TECH.MATERIALS.SILICON, MSTACK_SOI_THICKNESS)
                                                                     ], 
                                                display_style = DisplayStyle(color = COLOR_DARK_UGLY_PINK))

# N-implanted SOI
TECH.MATERIAL_STACKS.MSTACK_SOI_SKT_N = MaterialStack(name = "61nm SOI N", 
                                                       materials_heights = [(TECH.MATERIALS.SILICON_OXIDE, MSTACK_BOX_THICKNESS),
                                                                            (TECH.MATERIALS.N_SILICON, MSTACK_SOI_SKT_THICKNESS),
                                                                            (TECH.MATERIALS.SILICON_OXIDE, MSTACK_SOI_THICKNESS - MSTACK_SOI_SKT_THICKNESS)
                                                                            ], 
                                                       display_style = DisplayStyle(color = COLOR_LIGHT_BLUE))

TECH.MATERIAL_STACKS.MSTACK_SOI_FC_N = MaterialStack(name = "144nm SOI N", 
                                                     materials_heights = [(TECH.MATERIALS.SILICON_OXIDE, MSTACK_BOX_THICKNESS),
                                                                          (TECH.MATERIALS.N_SILICON, MSTACK_SOI_FC_THICKNESS),
                                                                          (TECH.MATERIALS.SILICON_OXIDE, MSTACK_SOI_THICKNESS - MSTACK_SOI_FC_THICKNESS)
                                                                          ], 
                                                     display_style = DisplayStyle(color = COLOR_LIGHT_BLUE))

TECH.MATERIAL_STACKS.MSTACK_SOI_N = MaterialStack(name = "214nm SOI N", 
                                                  materials_heights = [(TECH.MATERIALS.SILICON_OXIDE, MSTACK_BOX_THICKNESS),
                                                                       (TECH.MATERIALS.N_SILICON, MSTACK_SOI_THICKNESS)
                                                                       ], 
                                                  display_style = DisplayStyle(color = COLOR_LIGHT_BLUE))

# P-implanted SOI
TECH.MATERIAL_STACKS.MSTACK_SOI_SKT_P = MaterialStack(name = "61nm SOI P", 
                                                       materials_heights = [(TECH.MATERIALS.SILICON_OXIDE,MSTACK_BOX_THICKNESS),
                                                                            (TECH.MATERIALS.P_SILICON, MSTACK_SOI_SKT_THICKNESS),
                                                                            (TECH.MATERIALS.SILICON_OXIDE, MSTACK_SOI_THICKNESS - MSTACK_SOI_SKT_THICKNESS)
                                                                            ], 
                                                       display_style = DisplayStyle(color = COLOR_LIGHT_RED))

TECH.MATERIAL_STACKS.MSTACK_SOI_FC_P = MaterialStack(name = "144nm SOI P", 
                                                     materials_heights = [(TECH.MATERIALS.SILICON_OXIDE, MSTACK_BOX_THICKNESS),
                                                                          (TECH.MATERIALS.P_SILICON, MSTACK_SOI_FC_THICKNESS),
                                                                          (TECH.MATERIALS.SILICON_OXIDE, MSTACK_SOI_THICKNESS - MSTACK_SOI_FC_THICKNESS)
                                                                          ], 
                                                     display_style = DisplayStyle(color = COLOR_LIGHT_RED))

TECH.MATERIAL_STACKS.MSTACK_SOI_P = MaterialStack(name = "214nm SOI P", 
                                                  materials_heights = [(TECH.MATERIALS.SILICON_OXIDE,MSTACK_BOX_THICKNESS),
                                                                       (TECH.MATERIALS.P_SILICON, MSTACK_SOI_THICKNESS)
                                                                       ], 
                                                  display_style = DisplayStyle(color = COLOR_LIGHT_RED))

# NBODY-implanted SOI
TECH.MATERIAL_STACKS.MSTACK_SOI_SKT_NBODY = MaterialStack(name = "61nm SOI NBODY", 
                                                       materials_heights = [(TECH.MATERIALS.SILICON_OXIDE, MSTACK_BOX_THICKNESS),
                                                                            (TECH.MATERIALS.NB_SILICON, MSTACK_SOI_SKT_THICKNESS),
                                                                            (TECH.MATERIALS.SILICON_OXIDE, MSTACK_SOI_THICKNESS - MSTACK_SOI_SKT_THICKNESS)
                                                                            ], 
                                                       display_style = DisplayStyle(color = COLOR_BLUE))

TECH.MATERIAL_STACKS.MSTACK_SOI_FC_NBODY = MaterialStack(name = "144nm SOI NBODY", 
                                                     materials_heights = [(TECH.MATERIALS.SILICON_OXIDE, MSTACK_BOX_THICKNESS),
                                                                          (TECH.MATERIALS.NB_SILICON, MSTACK_SOI_FC_THICKNESS),
                                                                          (TECH.MATERIALS.SILICON_OXIDE, MSTACK_SOI_THICKNESS - MSTACK_SOI_FC_THICKNESS)
                                                                          ], 
                                                     display_style = DisplayStyle(color = COLOR_BLUE))

TECH.MATERIAL_STACKS.MSTACK_SOI_NBODY = MaterialStack(name = "214nm SOI NBODY", 
                                                  materials_heights = [(TECH.MATERIALS.SILICON_OXIDE, MSTACK_BOX_THICKNESS),
                                                                       (TECH.MATERIALS.NB_SILICON, MSTACK_SOI_THICKNESS)
                                                                       ], 
                                                  display_style = DisplayStyle(color = COLOR_BLUE))

# PBODY-implanted SOI
TECH.MATERIAL_STACKS.MSTACK_SOI_SKT_PBODY = MaterialStack(name = "61nm SOI PBODY", 
                                                       materials_heights = [(TECH.MATERIALS.SILICON_OXIDE,MSTACK_BOX_THICKNESS),
                                                                            (TECH.MATERIALS.PB_SILICON, MSTACK_SOI_SKT_THICKNESS),
                                                                            (TECH.MATERIALS.SILICON_OXIDE, MSTACK_SOI_THICKNESS - MSTACK_SOI_SKT_THICKNESS)
                                                                            ], 
                                                       display_style = DisplayStyle(color = COLOR_RED))

TECH.MATERIAL_STACKS.MSTACK_SOI_FC_PBODY = MaterialStack(name = "144nm SOI PBODY", 
                                                     materials_heights = [(TECH.MATERIALS.SILICON_OXIDE, MSTACK_BOX_THICKNESS),
                                                                          (TECH.MATERIALS.PB_SILICON, MSTACK_SOI_FC_THICKNESS),
                                                                          (TECH.MATERIALS.SILICON_OXIDE, MSTACK_SOI_THICKNESS - MSTACK_SOI_FC_THICKNESS)
                                                                          ], 
                                                     display_style = DisplayStyle(color = COLOR_RED))

TECH.MATERIAL_STACKS.MSTACK_SOI_PBODY = MaterialStack(name = "214nm SOI PBODY", 
                                                  materials_heights = [(TECH.MATERIALS.SILICON_OXIDE,MSTACK_BOX_THICKNESS),
                                                                       (TECH.MATERIALS.PB_SILICON, MSTACK_SOI_THICKNESS)
                                                                       ], 
                                                  display_style = DisplayStyle(color = COLOR_RED))
# NPLUS-implanted SOI
TECH.MATERIAL_STACKS.MSTACK_SOI_NPLUS = MaterialStack(name = "214nm SOI NPLUS", 
                                                  materials_heights = [(TECH.MATERIALS.SILICON_OXIDE, MSTACK_BOX_THICKNESS),
                                                                       (TECH.MATERIALS.NB_SILICON, 0.5 * MSTACK_SOI_THICKNESS),
                                                                       (TECH.MATERIALS.NN_SILICON, 0.5 * MSTACK_SOI_THICKNESS)
                                                                       ], 
                                                  display_style = DisplayStyle(color = COLOR_DARK_BLUE))

# PPLUS-implanted SOI
TECH.MATERIAL_STACKS.MSTACK_SOI_PPLUS = MaterialStack(name = "214nm SOI PPLUS", 
                                                  materials_heights = [(TECH.MATERIALS.SILICON_OXIDE,MSTACK_BOX_THICKNESS),
                                                                       (TECH.MATERIALS.PB_SILICON, 0.5 * MSTACK_SOI_THICKNESS),
                                                                       (TECH.MATERIALS.PP_SILICON, 0.5 * MSTACK_SOI_THICKNESS)
                                                                       ], 
                                                  display_style = DisplayStyle(color = COLOR_DARK_RED))
# Stacks for passives simulation only
TECH.MATERIAL_STACKS.MSTACK_PSV_STI_OX_POLY = MaterialStack(name = "214nm Oxide + poly", 
                                                        materials_heights = [(TECH.MATERIALS.SILICON_OXIDE, MSTACK_BOX_THICKNESS),
                                                                             (TECH.MATERIALS.SILICON_OXIDE, MSTACK_SOI_THICKNESS + MSTACK_GATEOX_THICKNESS),
                                                                             (TECH.MATERIALS.POLYSILICON, MSTACK_POLY_THICKNESS)], 
                                                        display_style = DisplayStyle(color = color.COLOR_BLUE_VIOLET))
TECH.MATERIAL_STACKS.MSTACK_PSV_STI_OX = MaterialStack(name = "214nm Oxide + 160nm oxide", 
                                                        materials_heights = [(TECH.MATERIALS.SILICON_OXIDE, MSTACK_BOX_THICKNESS),
                                                                             (TECH.MATERIALS.SILICON_OXIDE, MSTACK_SOI_THICKNESS + MSTACK_GATEOX_THICKNESS),
                                                                             (TECH.MATERIALS.SILICON_OXIDE, MSTACK_POLY_THICKNESS)], 
                                                        display_style = DisplayStyle(color = COLOR_BABY_BLUE))

TECH.MATERIAL_STACKS.MSTACK_PSV_SOI_SKT_POLY = MaterialStack(name = "61nm SOI + poly", 
                                                          materials_heights = [(TECH.MATERIALS.SILICON_OXIDE,MSTACK_BOX_THICKNESS),
                                                                               (TECH.MATERIALS.SILICON, MSTACK_SOI_SKT_THICKNESS),
                                                                               (TECH.MATERIALS.SILICON_OXIDE, MSTACK_SOI_THICKNESS - MSTACK_SOI_SKT_THICKNESS + MSTACK_GATEOX_THICKNESS),
                                                                               (TECH.MATERIALS.POLYSILICON, MSTACK_POLY_THICKNESS)], 
                                                          display_style = DisplayStyle(color = color.COLOR_DEEP_GREEN))
TECH.MATERIAL_STACKS.MSTACK_PSV_SOI_SKT = MaterialStack(name = "61nm SOI + oxide", 
                                                        materials_heights = [(TECH.MATERIALS.SILICON_OXIDE,MSTACK_BOX_THICKNESS),
                                                                             (TECH.MATERIALS.SILICON, MSTACK_SOI_SKT_THICKNESS),
                                                                             (TECH.MATERIALS.SILICON_OXIDE, MSTACK_SOI_THICKNESS - MSTACK_SOI_SKT_THICKNESS + MSTACK_GATEOX_THICKNESS),
                                                                             (TECH.MATERIALS.SILICON_OXIDE, MSTACK_POLY_THICKNESS)], 
                                                        display_style = DisplayStyle(color = COLOR_LIGHT_UGLY_PINK))
TECH.MATERIAL_STACKS.MSTACK_PSV_SOI_FC_POLY = MaterialStack(name = "144nm SOI + poly", 
                                                           materials_heights = [(TECH.MATERIALS.SILICON_OXIDE, MSTACK_BOX_THICKNESS),
                                                                                (TECH.MATERIALS.SILICON, MSTACK_SOI_FC_THICKNESS),
                                                                                (TECH.MATERIALS.SILICON_OXIDE, MSTACK_SOI_THICKNESS - MSTACK_SOI_FC_THICKNESS + MSTACK_GATEOX_THICKNESS),
                                                                                (TECH.MATERIALS.POLYSILICON, MSTACK_POLY_THICKNESS)], 
                                                        display_style = DisplayStyle(color = color.COLOR_ORANGE))

TECH.MATERIAL_STACKS.MSTACK_PSV_SOI_FC = MaterialStack(name = "144nm SOI + oxide", 
                                                       materials_heights = [(TECH.MATERIALS.SILICON_OXIDE, MSTACK_BOX_THICKNESS),
                                                                            (TECH.MATERIALS.SILICON, MSTACK_SOI_FC_THICKNESS),
                                                                            (TECH.MATERIALS.SILICON_OXIDE, MSTACK_SOI_THICKNESS - MSTACK_SOI_FC_THICKNESS + MSTACK_GATEOX_THICKNESS),
                                                                            (TECH.MATERIALS.SILICON_OXIDE, MSTACK_POLY_THICKNESS)], 
                                                       display_style = DisplayStyle(color = COLOR_UGLY_PINK))

TECH.MATERIAL_STACKS.MSTACK_PSV_SOI_POLY = MaterialStack(name = "214nm SOI + poly", 
                                                           materials_heights = [(TECH.MATERIALS.SILICON_OXIDE, MSTACK_BOX_THICKNESS),
                                                                                (TECH.MATERIALS.SILICON, MSTACK_SOI_THICKNESS),
                                                                                (TECH.MATERIALS.SILICON_OXIDE, MSTACK_GATEOX_THICKNESS),
                                                                                (TECH.MATERIALS.POLYSILICON, MSTACK_POLY_THICKNESS)], 
                                                     display_style = DisplayStyle(color = color.COLOR_PURPLE))

TECH.MATERIAL_STACKS.MSTACK_PSV_SOI = MaterialStack(name = "214nm SOI + oxide", 
                                                materials_heights = [(TECH.MATERIALS.SILICON_OXIDE, MSTACK_BOX_THICKNESS),
                                                                     (TECH.MATERIALS.SILICON, MSTACK_SOI_THICKNESS),
                                                                     (TECH.MATERIALS.SILICON_OXIDE, MSTACK_GATEOX_THICKNESS),
                                                                     (TECH.MATERIALS.SILICON_OXIDE, MSTACK_POLY_THICKNESS)], 
                                                display_style = DisplayStyle(color = COLOR_DARK_UGLY_PINK))
# Material stacks MOL
TECH.MATERIAL_STACKS.MSTACK_PMD = MaterialStack(name = "PMD Oxide", 
                                                materials_heights = [(TECH.MATERIALS.SILICON_OXIDE, MSTACK_D_LINER),
                                                                     (TECH.MATERIALS.SILICON_NITRIDE, MSTACK_LINER_THICKNESS),
                                                                     (TECH.MATERIALS.SILICON_OXIDE, MSTACK_PMD_THICKNESS - MSTACK_D_LINER - MSTACK_LINER_THICKNESS)
                                                                     ], 
                                                display_style = DisplayStyle(color = COLOR_BABY_BLUE))
TECH.MATERIAL_STACKS.MSTACK_POLY = MaterialStack(name = "POLY + PMD", 
                                                materials_heights = [(TECH.MATERIALS.POLYSILICON, MSTACK_POLY_THICKNESS),
                                                                     (TECH.MATERIALS.SILICON_OXIDE, MSTACK_D_LINER - MSTACK_POLY_THICKNESS),
                                                                     (TECH.MATERIALS.SILICON_NITRIDE, MSTACK_LINER_THICKNESS),
                                                                     (TECH.MATERIALS.SILICON_OXIDE, MSTACK_PMD_THICKNESS - MSTACK_D_LINER - MSTACK_LINER_THICKNESS),
                                                                     ], 
                                                display_style = DisplayStyle(color = COLOR_BLUE_CRAYOLA))
TECH.MATERIAL_STACKS.MSTACK_SAL_PMD = MaterialStack(name = "SAL + PMD Oxide", 
                                                materials_heights = [(TECH.MATERIALS.SILICIDE, MSTACK_SAL_THICKNESS),
                                                                     (TECH.MATERIALS.SILICON_OXIDE, MSTACK_D_LINER - MSTACK_SAL_THICKNESS),
                                                                     (TECH.MATERIALS.SILICON_NITRIDE, MSTACK_LINER_THICKNESS),
                                                                     (TECH.MATERIALS.SILICON_OXIDE, MSTACK_PMD_THICKNESS - MSTACK_D_LINER - MSTACK_LINER_THICKNESS),
                                                                     ], 
                                                display_style = DisplayStyle(color = COLOR_DARKSEA_GREEN))
TECH.MATERIAL_STACKS.MSTACK_PCON = MaterialStack(name = "PCON without SAL", 
                                                materials_heights = [(TECH.MATERIALS.TUNGSTEN, MSTACK_PMD_THICKNESS),
                                                                     ], 
                                                display_style = DisplayStyle(color = COLOR_RED))

TECH.MATERIAL_STACKS.MSTACK_SAL_PCON = MaterialStack(name = "PCON", 
                                                materials_heights = [(TECH.MATERIALS.SILICIDE, MSTACK_SAL_THICKNESS),
                                                                     (TECH.MATERIALS.TUNGSTEN, MSTACK_PMD_THICKNESS - MSTACK_SAL_THICKNESS),
                                                                     ], 
                                                display_style = DisplayStyle(color = COLOR_GRAY))

TECH.MATERIAL_STACKS.MSTACK_METAL_OX = MaterialStack(name= "IMD",
                                                     materials_heights=[(TECH.MATERIALS.SILICON_OXIDE, MSTACK_M1_THICKNESS),
                                                                        (TECH.MATERIALS.SILICON_OXIDE, MSTACK_IMD_THICKNESS),
                                                                        (TECH.MATERIALS.SILICON_OXIDE, MSTACK_M2_THICKNESS)],
                                                     display_style=DisplayStyle(color=COLOR_YELLOW))
TECH.MATERIAL_STACKS.MSTACK_METAL_M1 = MaterialStack(name= "M1",
                                                     materials_heights=[(TECH.MATERIALS.COPPER, MSTACK_M1_THICKNESS),
                                                                        (TECH.MATERIALS.SILICON_OXIDE, MSTACK_IMD_THICKNESS),
                                                                        (TECH.MATERIALS.SILICON_OXIDE, MSTACK_M2_THICKNESS)],
                                                     display_style=DisplayStyle(color=color.COLOR_COPPER))
TECH.MATERIAL_STACKS.MSTACK_METAL_M2 = MaterialStack(name= "M2",
                                                     materials_heights=[(TECH.MATERIALS.SILICON_OXIDE, MSTACK_M1_THICKNESS),
                                                                        (TECH.MATERIALS.SILICON_OXIDE, MSTACK_IMD_THICKNESS),
                                                                        (TECH.MATERIALS.COPPER, MSTACK_M2_THICKNESS)],
                                                     display_style=DisplayStyle(color=color.COLOR_SILVER))
TECH.MATERIAL_STACKS.MSTACK_METAL_M1_M2 = MaterialStack(name= "M1+M2",
                                                        materials_heights=[(TECH.MATERIALS.COPPER, MSTACK_M1_THICKNESS),
                                                                           (TECH.MATERIALS.SILICON_OXIDE, MSTACK_IMD_THICKNESS),
                                                                           (TECH.MATERIALS.COPPER, MSTACK_M2_THICKNESS)],
                                                        display_style=DisplayStyle(color=color.COLOR_CHAMPAGNE))
TECH.MATERIAL_STACKS.MSTACK_METAL_M1_V12_M2 = MaterialStack(name= "M1+VIA12+M2",
                                                            materials_heights=[(TECH.MATERIALS.COPPER, MSTACK_M1_THICKNESS),
                                                                               (TECH.MATERIALS.TUNGSTEN, MSTACK_IMD_THICKNESS),
                                                                               (TECH.MATERIALS.COPPER, MSTACK_M2_THICKNESS)],
                                                            display_style=DisplayStyle(color=color.COLOR_GRAY))
# effective index

TECH.MATERIAL_STACKS.MSTACK_STI_OX.effective_index_epsilon = 2.3104
TECH.MATERIAL_STACKS.MSTACK_SOI_SKT.effective_index_epsilon = 1.823**2
TECH.MATERIAL_STACKS.MSTACK_SOI_FC.effective_index_epsilon = 2.531**2
TECH.MATERIAL_STACKS.MSTACK_SOI.effective_index_epsilon = 2.8255**2

# Booleans

TECH.PPLAYER.WG.ALL = (TECH.PPLAYER.WG.COR ^ TECH.PPLAYER.WG.CLD ) & TECH.PPLAYER.WG.CLD  | TECH.PPLAYER.WG.HOL | TECH.PPLAYER.WG.TRE
TECH.PPLAYER.FC.ALL = (TECH.PPLAYER.FC.COR ^ TECH.PPLAYER.FC.CLD ) & TECH.PPLAYER.FC.CLD  | TECH.PPLAYER.FC.HOL | TECH.PPLAYER.FC.TRE
TECH.PPLAYER.SKT.ALL = (TECH.PPLAYER.SKT.COR ^ TECH.PPLAYER.SKT.CLD ) & TECH.PPLAYER.SKT.CLD  | TECH.PPLAYER.SKT.HOL | TECH.PPLAYER.SKT.TRE
TECH.PPLAYER.FCW.ALL = TECH.PPLAYER.FCW.COR | (TECH.PPLAYER.FCW.TRE ^ TECH.PPLAYER.FCW.INV)
TECH.PPLAYER.N1.ALL = TECH.PPLAYER.N1.DRAWING
TECH.PPLAYER.N2.ALL = TECH.PPLAYER.N2.DRAWING
TECH.PPLAYER.P1.ALL = TECH.PPLAYER.P1.DRAWING
TECH.PPLAYER.P2.ALL = TECH.PPLAYER.P2.DRAWING
TECH.PPLAYER.PBODY.ALL = TECH.PPLAYER.PBODY.DRAWING
TECH.PPLAYER.NBODY.ALL = TECH.PPLAYER.NBODY.DRAWING
TECH.PPLAYER.PPLUS.ALL = TECH.PPLAYER.PPLUS.DRAWING
TECH.PPLAYER.NPLUS.ALL = TECH.PPLAYER.NPLUS.DRAWING
TECH.PPLAYER.SAL.ALL = TECH.PPLAYER.SAL.DRAWING
TECH.PPLAYER.PCON.ALL = TECH.PPLAYER.PCON.DRAWING
TECH.PPLAYER.M1.ALL = (TECH.PPLAYER.M1.PERF ^ TECH.PPLAYER.M1.DRAWING) & TECH.PPLAYER.M1.DRAWING
TECH.PPLAYER.M2.ALL = (TECH.PPLAYER.M2.PERF ^ TECH.PPLAYER.M2.DRAWING) & TECH.PPLAYER.M2.DRAWING
TECH.PPLAYER.VIA12.ALL = TECH.PPLAYER.VIA12.DRAWING

PROCESS_FLOW_SOI_POLY = VFabricationProcessFlow(
    active_processes = [TECH.PROCESS.FC, TECH.PROCESS.SKT, TECH.PROCESS.WG, TECH.PROCESS.FCW
                        ], # DO NOT CHANGE THE SEQUENCE OF THE ELEMENTS ! IT MUST MATCH THE SEQUENCE OF THE COLUMNS IN VFABRICATION PROPERTY process_to_material_stack_map
    process_to_material_stack_map = 
    #FC, SKT, WG, FCW
    [
        ((0, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_PSV_SOI_POLY), 
        ((0, 0, 1, 0), TECH.MATERIAL_STACKS.MSTACK_PSV_STI_OX_POLY),
        ((0, 1, 0, 0), TECH.MATERIAL_STACKS.MSTACK_PSV_SOI_SKT_POLY), 
        ((1, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_PSV_SOI_FC_POLY),
        ((0, 1, 1, 0), TECH.MATERIAL_STACKS.MSTACK_PSV_STI_OX_POLY),
        ((1, 1, 0, 0), TECH.MATERIAL_STACKS.MSTACK_PSV_STI_OX_POLY),
        ((1, 0, 1, 0), TECH.MATERIAL_STACKS.MSTACK_PSV_STI_OX_POLY),
        ((1, 1, 1, 0), TECH.MATERIAL_STACKS.MSTACK_PSV_STI_OX_POLY),                            

        ((0, 0, 0, 1), TECH.MATERIAL_STACKS.MSTACK_PSV_SOI), 
        ((0, 0, 1, 1), TECH.MATERIAL_STACKS.MSTACK_PSV_STI_OX),
        ((0, 1, 0, 1), TECH.MATERIAL_STACKS.MSTACK_PSV_SOI_SKT), 
        ((1, 0, 0, 1), TECH.MATERIAL_STACKS.MSTACK_PSV_SOI_FC),
        ((0, 1, 1, 1), TECH.MATERIAL_STACKS.MSTACK_PSV_STI_OX),
        ((1, 1, 0, 1), TECH.MATERIAL_STACKS.MSTACK_PSV_STI_OX),
        ((1, 0, 1, 1), TECH.MATERIAL_STACKS.MSTACK_PSV_STI_OX),
        ((1, 1, 1, 1), TECH.MATERIAL_STACKS.MSTACK_PSV_STI_OX),
        ],   
    is_lf_fabrication = {TECH.PROCESS.WG   : False, 
                         TECH.PROCESS.FC   : False,
                         TECH.PROCESS.SKT  : False,
                         TECH.PROCESS.FCW  : True
                         }
)

PROCESS_FLOW_SOI_IMPL = VFabricationProcessFlow(
    active_processes = [TECH.PROCESS.FC, TECH.PROCESS.SKT, TECH.PROCESS.WG, 
                        TECH.PROCESS.PPLUS, TECH.PROCESS.PBODY, TECH.PROCESS.P1, TECH.PROCESS.NPLUS, TECH.PROCESS.NBODY, TECH.PROCESS.N1
                        ], # DO NOT CHANGE THE SEQUENCE OF THE ELEMENTS ! IT MUST MATCH THE SEQUENCE OF THE COLUMNS IN VFABRICATION PROPERTY process_to_material_stack_map
    process_to_material_stack_map = 
    #FC, SKT, WG, PPLUS, PBODY, P1, NPLUS, NBODY, N1
    [
        # no implants
        ((0, 0, 0, 0, 0, 0, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_SOI), 
        ((1, 0, 0, 0, 0, 0, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_SOI_FC),
        ((0, 1, 0, 0, 0, 0, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_SOI_SKT), 
        ((0, 0, 1, 0, 0, 0, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_STI_OX),
        ((0, 1, 1, 0, 0, 0, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_STI_OX),
        ((1, 1, 0, 0, 0, 0, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_STI_OX),
        ((1, 0, 1, 0, 0, 0, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_STI_OX),
        ((1, 1, 1, 0, 0, 0, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_STI_OX),

        # N or P in SOI
        ((0, 0, 0, 0, 0, 1, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_SOI_P), 
        ((0, 1, 0, 0, 0, 1, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_SOI_SKT_P), 
        ((1, 0, 0, 0, 0, 1, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_SOI_FC_P),
        ((0, 0, 0, 0, 0, 0, 0, 0, 1), TECH.MATERIAL_STACKS.MSTACK_SOI_N), 
        ((0, 1, 0, 0, 0, 0, 0, 0, 1), TECH.MATERIAL_STACKS.MSTACK_SOI_SKT_N), 
        ((1, 0, 0, 0, 0, 0, 0, 0, 1), TECH.MATERIAL_STACKS.MSTACK_SOI_FC_N),

        # NBODY or PBODY in SOI - N+NBODY=>NBODY, P+PBODY =>PBODY
        ((0, 0, 0, 0, 1, 0, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_SOI_PBODY), 
        ((0, 0, 0, 0, 1, 1, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_SOI_PBODY), 
        ((0, 1, 0, 0, 1, 0, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_SOI_SKT_PBODY),
        ((0, 1, 0, 0, 1, 1, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_SOI_SKT_PBODY),
        ((0, 1, 0, 1, 1, 1, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_SOI_SKT_PBODY),
        ((1, 0, 0, 0, 1, 0, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_SOI_FC_PBODY),
        ((1, 0, 0, 0, 1, 1, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_SOI_FC_PBODY),
        
        ((0, 0, 0, 0, 0, 0, 0, 1, 0), TECH.MATERIAL_STACKS.MSTACK_SOI_NBODY), 
        ((0, 0, 0, 0, 0, 0, 0, 1, 1), TECH.MATERIAL_STACKS.MSTACK_SOI_NBODY), 
        ((0, 1, 0, 0, 0, 0, 0, 1, 0), TECH.MATERIAL_STACKS.MSTACK_SOI_SKT_NBODY), 
        ((0, 1, 0, 0, 0, 0, 0, 1, 1), TECH.MATERIAL_STACKS.MSTACK_SOI_SKT_NBODY), 
        ((0, 1, 0, 0, 0, 0, 1, 1, 1), TECH.MATERIAL_STACKS.MSTACK_SOI_SKT_NBODY), 
        ((1, 0, 0, 0, 0, 0, 0, 1, 0), TECH.MATERIAL_STACKS.MSTACK_SOI_FC_NBODY),
        ((1, 0, 0, 0, 0, 0, 0, 1, 1), TECH.MATERIAL_STACKS.MSTACK_SOI_FC_NBODY),

        # NPLUS or PPLUS in SOI
        ((0, 0, 0, 1, 0, 0, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_SOI_PPLUS), 
        ((0, 0, 0, 1, 1, 0, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_SOI_PPLUS), 
        ((0, 0, 0, 1, 1, 1, 0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_SOI_PPLUS), 
        ((0, 0, 0, 0, 0, 0, 1, 0, 0), TECH.MATERIAL_STACKS.MSTACK_SOI_NPLUS), 
        ((0, 0, 0, 0, 0, 0, 1, 1, 0), TECH.MATERIAL_STACKS.MSTACK_SOI_NPLUS), 
        ((0, 0, 0, 0, 0, 0, 1, 1, 1), TECH.MATERIAL_STACKS.MSTACK_SOI_NPLUS), 
        ],   
    is_lf_fabrication = {TECH.PROCESS.WG   : False, 
                         TECH.PROCESS.FC   : False,
                         TECH.PROCESS.SKT  : False,
                         TECH.PROCESS.NBODY: False,
                         TECH.PROCESS.NPLUS: False,
                         TECH.PROCESS.N1: False,
                         TECH.PROCESS.PBODY: False,
                         TECH.PROCESS.PPLUS: False,
                         TECH.PROCESS.P1: False,
                         }
)

PROCESS_FLOW_MOL = VFabricationProcessFlow(
    active_processes = [TECH.PROCESS.FCW, TECH.PROCESS.SAL, TECH.PROCESS.PCON
                        ], # DO NOT CHANGE THE SEQUENCE OF THE ELEMENTS ! IT MUST MATCH THE SEQUENCE OF THE COLUMNS IN VFABRICATION PROPERTY process_to_material_stack_map
    process_to_material_stack_map = 
    #FCW,SAL, PCON
    [ 
        # with poly
        ((0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_POLY),
        # without poly
        ((1, 0, 0), TECH.MATERIAL_STACKS.MSTACK_PMD), 
        ((1, 0, 1), TECH.MATERIAL_STACKS.MSTACK_PCON),
        ((1, 1, 0), TECH.MATERIAL_STACKS.MSTACK_SAL_PMD), 
        ((1, 1, 1), TECH.MATERIAL_STACKS.MSTACK_SAL_PCON),
        ],   
    is_lf_fabrication = {TECH.PROCESS.SAL   : False, 
                         TECH.PROCESS.PCON  : False,
                         TECH.PROCESS.FCW   : True
                         }
)

PROCESS_FLOW_METAL = VFabricationProcessFlow(
    active_processes = [TECH.PROCESS.M1, TECH.PROCESS.VIA12, TECH.PROCESS.M2],
    process_to_material_stack_map = 
    # M1,VIA12, M2
    [ 
        ((0, 0, 0), TECH.MATERIAL_STACKS.MSTACK_METAL_OX),
        ((1, 0, 0), TECH.MATERIAL_STACKS.MSTACK_METAL_M1), 
        ((0, 0, 1), TECH.MATERIAL_STACKS.MSTACK_METAL_M2), 
        ((1, 0, 1), TECH.MATERIAL_STACKS.MSTACK_METAL_M1_M2),
        ((1, 1, 1), TECH.MATERIAL_STACKS.MSTACK_METAL_M1_V12_M2),
        ],   
    is_lf_fabrication = {TECH.PROCESS.M1   : False, 
                         TECH.PROCESS.VIA12  : False,
                         TECH.PROCESS.M2   : False
                         }    
)

TECH.VFABRICATION = TechnologyTree()

# individual flow parts
TECH.VFABRICATION.PROCESS_FLOW_SOI_POLY = PROCESS_FLOW_SOI_POLY
TECH.VFABRICATION.PROCESS_FLOW_SOI_IMPL = PROCESS_FLOW_SOI_IMPL
TECH.VFABRICATION.PROCESS_FLOW_METAL = PROCESS_FLOW_METAL

# groups of flows
TECH.VFABRICATION.PROCESS_FLOW_FEOL_MOL = PROCESS_FLOW_SOI_IMPL + PROCESS_FLOW_MOL
TECH.VFABRICATION.PROCESS_FLOW_BEOL = PROCESS_FLOW_METAL

# full flow
TECH.VFABRICATION.PROCESS_FLOW = TECH.VFABRICATION.PROCESS_FLOW_FEOL_MOL + PROCESS_FLOW_METAL