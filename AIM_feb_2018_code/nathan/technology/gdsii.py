############################################################################################
# GDSII settings:
#
# GDSII layer mapping
# - TECH keys defined here is used by IPKISS
############################################################################################

from ipkiss.technology import get_technology
from ipkiss.technology.technology import TechnologyTree
from ipkiss.process.layer_map import GenericGdsiiPPLayerOutputMap, GenericGdsiiPPLayerInputMap
import string

# Layer mapping
TECH = get_technology()

from ipkiss.technology.technology import DelayedInitTechnologyTree
TECH = get_technology()
TECH.GDSII = TechnologyTree()


##################################
# SETTINGS
##################################
TECH.GDSII.STRNAME_CHARACTER_DICT = {" -./": "_"}                                           # Mapping for illegal characters in cell names
TECH.GDSII.STRNAME_ALLOWED_CHARACTERS = string.ascii_letters + string.digits + '_$'         # Allowed characters in cell names

TECH.GDSII.MAX_COORDINATES = 200                                                            # Max number of vertices in a path
TECH.GDSII.MAX_PATH_LENGTH = 100                                                            # Max number of control points in a path
TECH.GDSII.MAX_VERTEX_COUNT = 4000                                                          # Max number of vertices in a polygon
TECH.GDSII.MAX_NAME_LENGTH = 255                                                            # Max length of a cell name

##################################
# LAYER MAP
##################################

TECH.GDSII.LAYERTABLE = {                                     # GDSII layer table - not required as such, but used for defining the maps below
    # (ProcessLayer, PatternPurpose) : (GDSIILayer, GDSIIDatatype)
    #CHANGES FOR AIM BEGIN HERE
    (TECH.PROCESS.WG,  TECH.PURPOSE.CORE   ): ( 709, 727),
    (TECH.PROCESS.WG,  TECH.PURPOSE.CLADDING   ): ( 727, 727),      # SAME AS BSEAMFILL
    (TECH.PROCESS.WG,  TECH.PURPOSE.TRENCH   ): ( 702, 727),
    (TECH.PROCESS.WG,  TECH.PURPOSE.HOLE): ( 702, 727),

    #CHANGES END HERE(MORE LATER)

    (TECH.PROCESS.FC,  TECH.PURPOSE.CORE   ): ( 35, 4),
    (TECH.PROCESS.FC,  TECH.PURPOSE.CLADDING   ): ( 35, 5),
    (TECH.PROCESS.FC,  TECH.PURPOSE.TRENCH   ): ( 35, 6),
    (TECH.PROCESS.FC,  TECH.PURPOSE.HOLE): ( 35, 2),

    (TECH.PROCESS.SKT,  TECH.PURPOSE.CORE   ): ( 43, 4),
    (TECH.PROCESS.SKT,  TECH.PURPOSE.CLADDING   ): ( 43, 5),
    (TECH.PROCESS.SKT,  TECH.PURPOSE.TRENCH   ): ( 43, 6),
    (TECH.PROCESS.SKT,  TECH.PURPOSE.HOLE): ( 43, 2),

    (TECH.PROCESS.NBODY, TECH.PURPOSE.DRAWING ): ( 25, 0),
    (TECH.PROCESS.PBODY, TECH.PURPOSE.DRAWING ): ( 26, 0),

    (TECH.PROCESS.FCW, TECH.PURPOSE.CORE   ): ( 31, 6),
    (TECH.PROCESS.FCW, TECH.PURPOSE.TRENCH   ): ( 31, 4),
    (TECH.PROCESS.FCW, TECH.PURPOSE.INVERSION   ): ( 31, 5),
    (TECH.PROCESS.N1, TECH.PURPOSE.DRAWING    ): (  2, 0),
    (TECH.PROCESS.P1, TECH.PURPOSE.DRAWING    ): (  3, 0),
    (TECH.PROCESS.N2, TECH.PURPOSE.DRAWING    ): (  6, 0),
    (TECH.PROCESS.P2, TECH.PURPOSE.DRAWING    ): (  7, 0),
    (TECH.PROCESS.NPLUS, TECH.PURPOSE.DRAWING ): (  4, 0),
    (TECH.PROCESS.PPLUS, TECH.PURPOSE.DRAWING ): (  5, 0),
    (TECH.PROCESS.SAL, TECH.PURPOSE.DRAWING   ): (  8, 0),
    (TECH.PROCESS.PCON, TECH.PURPOSE.DRAWING  ): ( 10, 0),

    (TECH.PROCESS.M1, TECH.PURPOSE.DRAWING    ): ( 11, 1),
    (TECH.PROCESS.M1, TECH.PURPOSE.NOFILL     ): ( 11, 9),
    (TECH.PROCESS.M1, TECH.PURPOSE.PERF       ): ( 11, 11),
    (TECH.PROCESS.M1, TECH.PURPOSE.NO_PERF       ): ( 11, 12),

    (TECH.PROCESS.VIA12, TECH.PURPOSE.DRAWING  ): ( 12, 0),

    (TECH.PROCESS.M2, TECH.PURPOSE.DRAWING    ): ( 13, 1),
    (TECH.PROCESS.M2, TECH.PURPOSE.NOFILL     ): ( 13, 9),
    (TECH.PROCESS.M2, TECH.PURPOSE.PERF       ): ( 13, 11),
    (TECH.PROCESS.M2, TECH.PURPOSE.NO_PERF    ): ( 13, 12),

    (TECH.PROCESS.PASS1, TECH.PURPOSE.DRAWING  ): ( 16, 0),
    (TECH.PROCESS.METPASS, TECH.PURPOSE.DRAWING): ( 18, 0),

    (TECH.PROCESS.EXPO, TECH.PURPOSE.DRAWING       ): ( 83, 0),
    (TECH.PROCESS.LPASS, TECH.PURPOSE.DRAWING ): ( 91, 0),
    (TECH.PROCESS.PASS2, TECH.PURPOSE.DRAWING ): ( 17, 0),

    (TECH.PROCESS.TRENCH, TECH.PURPOSE.DRAWING    ): ( 88, 0),

    #CHANGES FOR AIM BEGIN AGAIN HERE
    (TECH.PROCESS.NONE, TECH.PURPOSE.BESAMFILL      ): (723, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.BCAAMFILL      ): (724, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.BSEAMFILL      ): (727, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.BFNAMFILL      ): (734, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.BSNAMFILL      ): (736, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.BM1AMFILL      ): (751, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.BM1AMCHE       ): (752, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.BMLAMFILL      ): (782, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.BM2AMFILL      ): (755, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.BM2AMCHE       ): (756, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.BMLAMCHE       ): (784, 727),

    (TECH.PROCESS.NONE, TECH.PURPOSE.WGKOAM         ): (802, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.METKOAM        ): (803, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.ABSTRACTAM     ): (804, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.LOGOAM         ): (806, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.LOGO2AM        ): (807, 727),

    (TECH.PROCESS.NONE, TECH.PURPOSE.ZLAM           ): (701, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.REAM           ): (702, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.SEAM           ): (709, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.ENAM           ): (711, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.FNAM           ): (733, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.SNAM           ): (735, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.NDAM           ): (791, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.NNAM           ): (792, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.NNNAM          ): (793, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.PDAM           ): (794, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.PPAM           ): (795, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.PPPAM          ): (796, 727),

    (TECH.PROCESS.NONE, TECH.PURPOSE.TRAM           ): (718, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.NGAM           ): (776, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.ESAM           ): (720, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.CAAM           ): (721, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.CBAM           ): (722, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.M1AM           ): (710, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.V1AM           ): (715, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.M2AM           ): (725, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.VAAM           ): (771, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.MLAM           ): (780, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.DIAM           ): (726, 727),
    (TECH.PROCESS.NONE, TECH.PURPOSE.PAAM           ): (779, 727),

    # really annoying label layers
    (TECH.PROCESS.NONE, TECH.PURPOSE.LOL709           ): (709, 728),
    (TECH.PROCESS.NONE, TECH.PURPOSE.LOL804           ): (804, 0),
    (TECH.PROCESS.NONE, TECH.PURPOSE.LOL7090           ): (709, 0),
    (TECH.PROCESS.NONE, TECH.PURPOSE.LOL7250           ): (725, 0),

    #CHANGES END HERE

    # required tech keys for Ipkiss compatibility
    # required for Ipkiss.eda compatibility
    (TECH.PROCESS.WG, TECH.PURPOSE.TRACE           ): (37, 8),
    (TECH.PROCESS.FC, TECH.PURPOSE.TRACE           ): (35, 8), 
    (TECH.PROCESS.SKT, TECH.PURPOSE.TRACE          ): (43, 8),         
    # required for Picazzo
    (TECH.PROCESS.NONE, TECH.PURPOSE.ERROR         ): (10154, 0),
    (TECH.PROCESS.NONE, TECH.PURPOSE.BBOX          ): (120, 0)
}

TECH.GDSII.EXPORT_LAYER_MAP = GenericGdsiiPPLayerOutputMap(pplayer_map=TECH.GDSII.LAYERTABLE,       # GDSII export map - required
                                                           ignore_undefined_mappings=True)
TECH.GDSII.IMPORT_LAYER_MAP = GenericGdsiiPPLayerInputMap(pplayer_map=TECH.GDSII.LAYERTABLE,
                                                          ignore_undefined_mappings=True)        # GDSII import map - required


##################################
# FILTERS
##################################

from ipkiss.primitives.filters.path_cut_filter import PathCutFilter
from ipkiss.primitives.filters.empty_filter import EmptyFilter
from ipkiss.primitives.filters.path_to_boundary_filter import PathToBoundaryFilter
from ipkiss.primitives.filters.boundary_cut_filter import BoundaryCutFilter
from ipkiss.primitives.filters.name_scramble_filter import NameScrambleFilter
from ipkiss.primitives.filters.name_error_filter import PCellNameErrorFilter
from ipkiss.primitives.filter import ToggledCompoundFilter

f = ToggledCompoundFilter()
f += PathCutFilter(name="cut_path",
                   max_path_length=TECH.GDSII.MAX_COORDINATES,
                   grids_per_unit=int(TECH.METRICS.UNIT / TECH.METRICS.GRID),
                   overlap=1)
f += PathToBoundaryFilter(name="path_to_boundary",
                          exclude_layers=[TECH.PPLAYER.NONE.DICING])
f += BoundaryCutFilter(name="cut_boundary", max_vertex_count=TECH.GDSII.MAX_VERTEX_COUNT)
f += EmptyFilter(name="write_empty")
f += PCellNameErrorFilter(name="name_error_filter", allowed_characters=TECH.GDSII.STRNAME_ALLOWED_CHARACTERS)
f["cut_path"] = True
f["path_to_boundary"] = True
f["cut_boundary"] = True
f["write_empty"] = True
f["name_error_filter"] = False
TECH.GDSII.FILTER = f                             # GDSII export filters (several filter which can be toggled on or off) - required

TECH.GDSII.NAME_FILTER = NameScrambleFilter(allowed_characters=TECH.GDSII.STRNAME_ALLOWED_CHARACTERS,   # GDSII cell name filter - required
                                            replace_characters=TECH.GDSII.STRNAME_CHARACTER_DICT,
                                            default_replacement="",
                                            max_name_length=TECH.GDSII.MAX_NAME_LENGTH,
                                            scramble_all=False)
