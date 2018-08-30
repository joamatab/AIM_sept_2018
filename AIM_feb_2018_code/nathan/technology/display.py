############################################################################################
# Display setting:
# 
# This file contains color settings for layer visualization in IPKISS 
############################################################################################

from ipkiss.technology import get_technology
from ipkiss.technology.technology import TechnologyTree, DelayedInitTechnologyTree

TECH = get_technology()

from ipkiss.visualisation.display_style import DisplayStyle, DisplayStyleSet
from ipkiss.visualisation import color
from ipkiss.visualisation import stipple
from ipkiss.process import PPLayer


COLOR_DARK_RED = color.Color(name = "darkred", red = 0.75, green = 0, blue = 0)
COLOR_DARK_BLUE = color.Color(name = "darkblue", red = 0, green = 0, blue = 0.75)
COLOR_DARK_GREEN = color.Color(name = "darkgreen", red = 0.5, green = 0.31, blue = 0)

DISPLAY_BLACK = DisplayStyle(color=color.COLOR_BLACK, stipple=stipple.STIPPLE_FILLED, edgewidth=0.0)
DISPLAY_BLACK_SPARSE = DisplayStyle(color=color.COLOR_BLACK, stipple=stipple.STIPPLE_LINES_DIAGONAL_L, alpha=0.5, edgewidth=1.0)
DISPLAY_BLACK_EMPTY = DisplayStyle(color=color.COLOR_BLACK, stipple=stipple.STIPPLE_NONE, alpha=0.5, edgewidth=1.0)
DISPLAY_BLACK_DOTS = DisplayStyle(color=color.COLOR_BLACK, stipple=stipple.STIPPLE_DOTS, edgewidth=0.0)
DISPLAY_WHITE = DisplayStyle(color=color.COLOR_WHITE, stipple=stipple.STIPPLE_FILLED, edgewidth=0.0)
DISPLAY_BLUE = DisplayStyle(color=color.COLOR_BLUE, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_BLUE_DRSPARSE = DisplayStyle(color=color.COLOR_BLUE, stipple=stipple.STIPPLE_LINES_DIAGONAL_R, alpha=0.5, edgewidth=1.0)
DISPLAY_BLUE_DLSPARSE = DisplayStyle(color=color.COLOR_BLUE, stipple=stipple.STIPPLE_LINES_DIAGONAL_L, alpha=0.5, edgewidth=1.0)
DISPLAY_DARK_BLUE = DisplayStyle(color=COLOR_DARK_BLUE, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
#DISPLAY_BLUECRAYOLA = DisplayStyle(color=color.COLOR_BLUE_CRAYOLA, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_GREEN = DisplayStyle(color=color.COLOR_GREEN, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_DARKGREEN = DisplayStyle(color=COLOR_DARK_GREEN, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_DARKGREEN_HDENSE = DisplayStyle(color=COLOR_DARK_GREEN, stipple=stipple.STIPPLE_LINES_H_DENSE, alpha=0.5, edgewidth=1.0)
#DISPLAY_DEEPGREEN = DisplayStyle(color=color.COLOR_DEEP_GREEN, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_YELLOW = DisplayStyle(color=color.COLOR_YELLOW, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_MAGENTA = DisplayStyle(color=color.COLOR_MAGENTA, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_MAGENTA_SPARSE = DisplayStyle(color=color.COLOR_MAGENTA, stipple=stipple.STIPPLE_LINES_DIAGONAL_L, alpha=0.5, edgewidth=1.0)
DISPLAY_SCARLET = DisplayStyle(color=color.COLOR_SCARLET, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_RED = DisplayStyle(color=color.COLOR_RED, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_RED_EMPTY = DisplayStyle(color=color.COLOR_RED, stipple=stipple.STIPPLE_NONE, alpha=0.5, edgewidth=1.0)
DISPLAY_RED_DRSPARSE = DisplayStyle(color=color.COLOR_RED, stipple=stipple.STIPPLE_LINES_DIAGONAL_R, alpha=0.5, edgewidth=1.0)
DISPLAY_RED_DLSPARSE = DisplayStyle(color=color.COLOR_RED, stipple=stipple.STIPPLE_LINES_DIAGONAL_L, alpha=0.5, edgewidth=1.0)
DISPLAY_DARK_RED = DisplayStyle(color=COLOR_DARK_RED, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_CYAN = DisplayStyle(color=color.COLOR_CYAN, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_SANGRIA = DisplayStyle(color=color.COLOR_SANGRIA, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_PURPLE = DisplayStyle(color=color.COLOR_PURPLE, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_PURPLE_SPARSE = DisplayStyle(color=color.COLOR_PURPLE, stipple=stipple.STIPPLE_LINES_DIAGONAL_L, alpha=0.5, edgewidth=1.0)
DISPLAY_TITANIUM_YELLOW = DisplayStyle(color=color.COLOR_TITANIUM_YELLOW, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_COPPER = DisplayStyle(color=color.COLOR_COPPER, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_COPPER_DOTS = DisplayStyle(color=color.COLOR_COPPER, stipple=stipple.STIPPLE_DOTS, alpha=0.5, edgewidth=1.0)
DISPLAY_COPPER_EMPTY = DisplayStyle(color=color.COLOR_COPPER, stipple=stipple.STIPPLE_NONE, alpha=0.5, edgewidth=1.0)
DISPLAY_CHAMPAGNE = DisplayStyle(color=color.COLOR_CHAMPAGNE, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_CHAMPAGNE_DOTS = DisplayStyle(color=color.COLOR_CHAMPAGNE, stipple=stipple.STIPPLE_DOTS, alpha=0.5, edgewidth=1.0)
DISPLAY_SILVER = DisplayStyle(color=color.COLOR_SILVER, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_SILVER_DOTS = DisplayStyle(color=color.COLOR_SILVER, stipple=stipple.STIPPLE_DOTS, alpha=0.5, edgewidth=1.0)
DISPLAY_SILVER_EMPTY = DisplayStyle(color=color.COLOR_SILVER, stipple=stipple.STIPPLE_NONE, alpha=0.5, edgewidth=1.0)
DISPLAY_GRAY = DisplayStyle(color=color.COLOR_GRAY, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_GRAY_DOTS = DisplayStyle(color=color.COLOR_GRAY, stipple=stipple.STIPPLE_DOTS, alpha=0.5, edgewidth=1.0)
DISPLAY_GRAY_SPARSE = DisplayStyle(color=color.COLOR_GRAY, stipple=stipple.STIPPLE_LINES_DIAGONAL_L, alpha=0.5, edgewidth=1.0)
DISPLAY_CHERRY = DisplayStyle(color=color.COLOR_CHERRY, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_VIOLET = DisplayStyle(color=color.COLOR_BLUE_VIOLET, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_ORANGE = DisplayStyle(color=color.COLOR_ORANGE, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_ORANGE_DOTS = DisplayStyle(color=color.COLOR_ORANGE, stipple=stipple.STIPPLE_DOTS, alpha=0.5, edgewidth=1.0)
DISPLAY_ORANGE_SPARSE = DisplayStyle(color=color.COLOR_ORANGE, stipple=stipple.STIPPLE_LINES_DIAGONAL_L, alpha=0.5, edgewidth=1.0)
DISPLAY_GREEN_SPARSE = DisplayStyle(color=color.COLOR_GREEN, stipple=stipple.STIPPLE_LINES_DIAGONAL_L, alpha=0.5, edgewidth=1.0)
DISPLAY_DARKSEY_GREEN = DisplayStyle(color=color.COLOR_DARKSEA_GREEN, stipple=stipple.STIPPLE_FILLED, alpha=0.5, edgewidth=1.0)
DISPLAY_DARKSEY_GREEN_SPARSE = DisplayStyle(color=color.COLOR_DARKSEA_GREEN, stipple=stipple.STIPPLE_LINES_DIAGONAL_L, alpha=0.5, edgewidth=1.0)

TECH.DISPLAY = TechnologyTree()

style_set = DisplayStyleSet()
style_set.background = DISPLAY_WHITE

process_display_order = [
        TECH.PROCESS.WG,
        TECH.PROCESS.FC,
        TECH.PROCESS.SKT,
        TECH.PROCESS.FCW,
        TECH.PROCESS.PBODY,
        TECH.PROCESS.NBODY,
        TECH.PROCESS.P1,
        TECH.PROCESS.N1,
        TECH.PROCESS.P2,
        TECH.PROCESS.N2,
        TECH.PROCESS.PPLUS,
        TECH.PROCESS.NPLUS,
        TECH.PROCESS.SAL,
        TECH.PROCESS.PCON,
        TECH.PROCESS.M1,
        TECH.PROCESS.VIA12,
        TECH.PROCESS.M2,
        TECH.PROCESS.PASS1,
        TECH.PROCESS.METPASS,
        TECH.PROCESS.EXPO,
        TECH.PROCESS.LPASS,
        TECH.PROCESS.PASS2,
        TECH.PROCESS.TRENCH,
        TECH.PROCESS.NONE
]

style_set += [(PPLayer(TECH.PROCESS.WG, TECH.PURPOSE.CLADDING), DISPLAY_CYAN),
              (PPLayer(TECH.PROCESS.WG, TECH.PURPOSE.CORE), DISPLAY_VIOLET),
              (PPLayer(TECH.PROCESS.WG, TECH.PURPOSE.TRENCH), DISPLAY_COPPER),
              (PPLayer(TECH.PROCESS.WG, TECH.PURPOSE.HOLE), DISPLAY_BLUE),
              (PPLayer(TECH.PROCESS.WG, TECH.PURPOSE.TRACE), DISPLAY_RED),

              (PPLayer(TECH.PROCESS.FC, TECH.PURPOSE.CLADDING), DISPLAY_YELLOW),
              (PPLayer(TECH.PROCESS.FC, TECH.PURPOSE.CORE), DISPLAY_ORANGE),
              (PPLayer(TECH.PROCESS.FC, TECH.PURPOSE.TRENCH), DISPLAY_SANGRIA),
              (PPLayer(TECH.PROCESS.FC, TECH.PURPOSE.HOLE), DISPLAY_SANGRIA),
              (PPLayer(TECH.PROCESS.FC, TECH.PURPOSE.TRACE), DISPLAY_RED),
                            
              (PPLayer(TECH.PROCESS.SKT, TECH.PURPOSE.CLADDING), DISPLAY_GREEN),
              (PPLayer(TECH.PROCESS.SKT, TECH.PURPOSE.CORE), DISPLAY_DARKSEY_GREEN),
              (PPLayer(TECH.PROCESS.SKT, TECH.PURPOSE.TRENCH), DISPLAY_DARKGREEN),
              (PPLayer(TECH.PROCESS.SKT, TECH.PURPOSE.HOLE), DISPLAY_DARKGREEN_HDENSE),
              (PPLayer(TECH.PROCESS.SKT, TECH.PURPOSE.TRACE), DISPLAY_RED),

              (PPLayer(TECH.PROCESS.FCW, TECH.PURPOSE.CORE), DISPLAY_PURPLE),
              (PPLayer(TECH.PROCESS.FCW, TECH.PURPOSE.TRENCH), DISPLAY_TITANIUM_YELLOW),
              (PPLayer(TECH.PROCESS.FCW, TECH.PURPOSE.INVERSION), DISPLAY_PURPLE),

              (PPLayer(TECH.PROCESS.NBODY, TECH.PURPOSE.DRAWING), DISPLAY_BLUE),
              (PPLayer(TECH.PROCESS.N1, TECH.PURPOSE.DRAWING), DISPLAY_BLUE_DLSPARSE),
              (PPLayer(TECH.PROCESS.N2, TECH.PURPOSE.DRAWING), DISPLAY_BLUE_DLSPARSE),
              (PPLayer(TECH.PROCESS.NPLUS, TECH.PURPOSE.DRAWING), DISPLAY_DARK_BLUE),

              (PPLayer(TECH.PROCESS.PBODY, TECH.PURPOSE.DRAWING), DISPLAY_RED),
              (PPLayer(TECH.PROCESS.P1, TECH.PURPOSE.DRAWING), DISPLAY_RED_DLSPARSE),
              (PPLayer(TECH.PROCESS.P2, TECH.PURPOSE.DRAWING), DISPLAY_RED_DLSPARSE),
              (PPLayer(TECH.PROCESS.PPLUS, TECH.PURPOSE.DRAWING), DISPLAY_DARK_RED),

              (PPLayer(TECH.PROCESS.SAL, TECH.PURPOSE.DRAWING), DISPLAY_SILVER),
              (PPLayer(TECH.PROCESS.PCON, TECH.PURPOSE.DRAWING), DISPLAY_BLACK),

              (PPLayer(TECH.PROCESS.M1, TECH.PURPOSE.DRAWING), DISPLAY_COPPER),
              (PPLayer(TECH.PROCESS.M1, TECH.PURPOSE.NOFILL), DISPLAY_COPPER_DOTS),
              (PPLayer(TECH.PROCESS.M1, TECH.PURPOSE.PERF), DISPLAY_CHAMPAGNE),
              (PPLayer(TECH.PROCESS.M1, TECH.PURPOSE.NO_PERF), DISPLAY_CHAMPAGNE_DOTS),

              (PPLayer(TECH.PROCESS.VIA12, TECH.PURPOSE.DRAWING), DISPLAY_ORANGE),

              (PPLayer(TECH.PROCESS.M2, TECH.PURPOSE.DRAWING), DISPLAY_SILVER),
              (PPLayer(TECH.PROCESS.M2, TECH.PURPOSE.NOFILL), DISPLAY_SILVER_DOTS),
              (PPLayer(TECH.PROCESS.M2, TECH.PURPOSE.PERF), DISPLAY_GRAY),
              (PPLayer(TECH.PROCESS.M2, TECH.PURPOSE.NO_PERF), DISPLAY_GRAY_DOTS),

              (PPLayer(TECH.PROCESS.PASS1, TECH.PURPOSE.DRAWING), DISPLAY_PURPLE),
              (PPLayer(TECH.PROCESS.METPASS, TECH.PURPOSE.DRAWING), DISPLAY_CHERRY),
              (PPLayer(TECH.PROCESS.EXPO, TECH.PURPOSE.DRAWING), DISPLAY_BLUE),
              (PPLayer(TECH.PROCESS.LPASS, TECH.PURPOSE.DRAWING), DISPLAY_GREEN_SPARSE),
              (PPLayer(TECH.PROCESS.PASS2, TECH.PURPOSE.DRAWING), DISPLAY_PURPLE_SPARSE),
              
              (PPLayer(TECH.PROCESS.TRENCH, TECH.PURPOSE.DRAWING), DISPLAY_BLUE),
              
              (PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.OPT_DUM), DISPLAY_SCARLET),
              (PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.LOGOTXT), DISPLAY_COPPER),
              (PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.NOMET), DISPLAY_DARKSEY_GREEN_SPARSE),
              (PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.NOFILL), DISPLAY_ORANGE_SPARSE),
              (PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.VERTBX), DISPLAY_MAGENTA_SPARSE),
              (PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.DICING), DISPLAY_COPPER_EMPTY),
              (PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.DOC), DISPLAY_BLACK_DOTS),
              (PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.IP), DISPLAY_RED_EMPTY),
              (PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.LABEL), DISPLAY_BLACK),
              (PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.PIN), DISPLAY_ORANGE),
              (PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.PAYLOAD), DISPLAY_SILVER_EMPTY),
              (PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.ERROR), DISPLAY_RED),
              (PPLayer(TECH.PROCESS.NONE, TECH.PURPOSE.BBOX), DISPLAY_BLACK_EMPTY)
              ]

from ipkiss.visualisation.color import Color
from numpy import linspace
style_set += [(i, DisplayStyle(color=Color(name="gray_" + str(i),      # Visualization for simple Layers which may be present
                                           red=c_val,
                                           green=c_val,
                                           blue=c_val),
                               alpha=.5))
              for i, c_val in enumerate(linspace(.9, 0.0, num=256))]

TECH.DISPLAY.DEFAULT_DISPLAY_STYLE_SET = style_set   # required


