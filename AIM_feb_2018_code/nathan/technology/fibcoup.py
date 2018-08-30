############################################################################################
# PICAZZO Fiber coupler settings and IoFibcoup
############################################################################################

from ipkiss.technology import get_technology
from ipkiss.technology.technology import TechnologyTree, DelayedInitTechnologyTree
from numpy import floor

TECH = get_technology()
TECH.IO = TechnologyTree()
TECH.IO.DEFAULT_FIBCOUP_SPACING = 30.0 # Default spacing between fibercouplers for IOFibCoup

####################################################
# settings required for using picazzo fiber couplers
####################################################

class TechFibCoupTreeStraight(DelayedInitTechnologyTree):
    
    def initialize(self):
        self.SOCKET = TechnologyTree()
        self.SOCKET.LENGTH = 50.0
        self.SOCKET.WIDTH = 10.0

        from picazzo3.traces.wire_wg import WireWaveguideTemplate
        wide_trace_template = WireWaveguideTemplate()
        wide_trace_template.Layout(core_width=10.0, cladding_width=14.0) 
        
        self.SOCKET.TRACE_TEMPLATE = wide_trace_template # Wide trace template.
        
        #TE Grating
        self.GRATING_TE = TechnologyTree()
        self.GRATING_TE.N_O_LINES = 25 # Default number of lines used.
        self.GRATING_TE.PERIOD = 0.63 # Default period used in the grating.
        self.GRATING_TE.LINE_WIDTH = 0.315 # Default linewidth used in the grating.
        self.GRATING_TE.BOX_WIDTH = 14.0 # Default box width 
        
        #TM Grating
        self.GRATING_TM = TechnologyTree()
        self.GRATING_TM.N_O_LINES = 16 # Default number of lines used.
        self.GRATING_TM.PERIOD = 1.080 # Default period used in the grating.
        self.GRATING_TM.LINE_WIDTH = 0.540 # Default linewidth used in the grating.
        self.GRATING_TM.BOX_WIDTH = 14.0   # Default box width 
        
        
        # default
        self.GRATING = self.GRATING_TE
       
class TechFibcoupTreeCurved(DelayedInitTechnologyTree):
    
    def initialize(self):
        # Socket 
        self.SOCKET=TechnologyTree()
        self.SOCKET.LENGTH = 20.0
        self.SOCKET.STRAIGHT_EXTENSION = (0.0, 0.05) # Default straight extentions used for the socket taper. 
        self.SOCKET.MARGIN_FROM_GRATING = TECH.WG.SHORT_STRAIGHT # Distance between the last grating line and the end of the socket by default
        self.SOCKET.START_TRACE_TEMPLATE = TECH.PCELLS.WG.DEFAULT 
        self.SOCKET.TRANSITION_LENGTH = 5.0
        
        from picazzo3.traces.wire_wg import WireWaveguideTemplate
        wide_trace_template = WireWaveguideTemplate(name="LinearTransitionSocket_WGT")
        wide_trace_template.Layout(core_width=17.0, cladding_width=2 * TECH.WG.TRENCH_WIDTH + 17.0) 
        
        self.SOCKET.WIDE_TRACE_TEMPLATE = wide_trace_template # Wide trace template.
        
        # Grating
        
        self.GRATING = TechnologyTree()
        self.GRATING.PERIOD = 0.63 # Default period used in the grating.
        self.GRATING.FOCAL_DISTANCE = 20.0 # Default focal distance of curved gratings. 
        self.GRATING.BOX_WIDTH = 15.5 # Default box width        
        self.GRATING.N_O_LINES = int(floor(self.GRATING.BOX_WIDTH  / self.GRATING.PERIOD ))
        self.GRATING.START_RADIUS = self.GRATING.FOCAL_DISTANCE  - self.GRATING.BOX_WIDTH / 2.0  # Default first radius of the grating.
       
        self.GRATING.ANGLE_SPAN = 90 # Default angle span of a curved grating when it is not boxed.

    
####################################################
# default fiber couplers
####################################################     

class TechFibcoupStraightCellsTree(DelayedInitTechnologyTree):
    def initialize(self):
        ## standard gratings 1550nm
        def STANDARD_GRATING_1550_TE():
            # The imec PDK has no straight grating couplers, so we define one here one
            from picazzo3.fibcoup.uniform import UniformLineGrating as _ULG
            from picazzo3.traces.wire_wg import WireWaveguideTemplate
            t_tree = TECH.IO.FIBCOUP.STRAIGHT
            wg_t = WireWaveguideTemplate(name="STD_FIBCOUP_SOCKET_WG_TE_T")
            G = _ULG(name="std_grating_1550",
                     trace_template=t_tree.SOCKET.TRACE_TEMPLATE, 
                     library=TECH.PCELLS.LIB
                     )
            G.Layout(origin=(0.0,0.0),
                     period=t_tree.GRATING.PERIOD, 
                     line_width=t_tree.GRATING_TE.LINE_WIDTH,
                     line_length=t_tree.GRATING_TE.BOX_WIDTH,
                     n_o_periods=t_tree.GRATING_TE.N_O_LINES)   
            TECH.PCELLS.LIB.add(G.dependencies()) #make sure that the child cells are also added to this lib
            return G

        ### standard gratings 1550nm TM polarization
        def STANDARD_GRATING_1550_TM():
            from picazzo3.fibcoup.uniform import UniformLineGrating as _ULG
            from picazzo3.traces.wire_wg import WireWaveguideTemplate
            std1550_grating_trench = 0.540
            std1550_grating_period = 1.080
            std1550_grating_n_o_periods = 16
            wg_t = WireWaveguideTemplate(name="STD_FIBCOUP_SOCKET_WG_TM_T")
            wg_t.Layout(core_width=10.0,
                        cladding_width=14.0)
            G = _ULG(name="std_grating_1550_tm",
                     trace_template=wg_t, 
                     library=TECH.PCELLS.LIB
                     )
            G.Layout(origin=(0.0,0.0),
                     period=std1550_grating_period, 
                     line_width=std1550_grating_trench, 
                     n_o_periods=std1550_grating_n_o_periods)   
            TECH.PCELLS.LIB.add(G.dependencies()) #make sure that the child cells are also added to this lib
            return G

        
        self.DEFAULT_GRATING_TE = STANDARD_GRATING_1550_TE()
        self.DEFAULT_GRATING_TM = STANDARD_GRATING_1550_TM()
        self.DEFAULT_GRATING = self.DEFAULT_GRATING_TE
        
        
class TechFibcoupCurvedCellsTree(DelayedInitTechnologyTree):
    
    def initialize(self):
        # load the C-band coupler from the library as default
        from isipp50g.components.grating_couplers.grating_couplers import FGCCTE_FCWFC1DC_630_378
        fc_cell = FGCCTE_FCWFC1DC_630_378()
        TECH.PCELLS.LIB.add(fc_cell.dependencies()) #make sure that the child cells are also added to this lib        
        self.DEFAULT_GRATING = fc_cell




TECH.IO.FIBCOUP = TechnologyTree()
TECH.IO.FIBCOUP.CURVED = TechFibcoupTreeCurved()
TECH.IO.FIBCOUP.CURVED.PCELLS = TechFibcoupCurvedCellsTree()
TECH.IO.FIBCOUP.STRAIGHT = TechFibCoupTreeStraight()
TECH.IO.FIBCOUP.STRAIGHT.PCELLS = TechFibcoupStraightCellsTree()
TECH.IO.FIBCOUP.DEFAULT = TECH.IO.FIBCOUP.CURVED


####################################################
# Settings for IOFibcoup
####################################################    

class TechAdapterTree(DelayedInitTechnologyTree):
    def initialize(self):
        self.IOFIBCOUP = TechnologyTree()
        self.IOFIBCOUP.FANOUT_LENGTH = 40.0
        self.IOFIBCOUP.S_BEND_ANGLE = 60.0
        self.IOFIBCOUP.CONNECT_TRANSITION_LENGTH = None # automatic
        self.IOFIBCOUP.FIBER_COUPLER_TRANSITION_LENGTH = None # automatic
        
        self.DEFAULT_ADAPTER = self.IOFIBCOUP

class TechIoFibcoupAdapterPCellTree(DelayedInitTechnologyTree):
    def initialize(self):
        from picazzo3.container.iofibcoup import IoFibcoup
        self.ADAPTER = IoFibcoup

TECH.IO.ADAPTER = TechAdapterTree()
TECH.IO.ADAPTER.IOFIBCOUP.PCELLS = TechIoFibcoupAdapterPCellTree()
