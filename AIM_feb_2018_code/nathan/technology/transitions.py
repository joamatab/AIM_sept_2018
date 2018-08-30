############################################################################################
# waveguide transition settings:
# 
# Auto-TraceTransition database (Required for autotransitions in IPKISS)
############################################################################################

from picazzo3.traces.wire_wg import WireWaveguideTemplate
from WgTemplate import WGWireWaveguideTemplate, StripWgTemplate
from ipkiss.technology import get_technology
from picazzo3.traces.wire_wg import WireWaveguideTransitionLinear


TECH = get_technology()
db = TECH.PCELLS.TRANSITION.AUTO_TRANSITION_DATABASE
db.treat_trace_template_as(WGWireWaveguideTemplate, WireWaveguideTemplate)
db.treat_trace_template_as(StripWgTemplate, WireWaveguideTemplate)
#Need to add at least one transition apparently
db.add(StripWgTemplate, StripWgTemplate, WireWaveguideTransitionLinear)

