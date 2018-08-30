"""
Waveguide templates for AIM

The one you want to use is StripWgTemplate

authors: nathan, bohan
"""

__all__ = ['WGWireWaveguideTemplate', 'StripWgTemplate']

from ipkiss.technology import get_technology
from ipkiss.process import ProcessProperty, PurposeProperty
from ipcore.properties.predefined import PositiveNumberProperty, NonNegativeNumberProperty
from ipcore.properties.lock_properties import lock_properties
TECH = get_technology()

from picazzo3.traces.wire_wg import WireWaveguideTemplate

# Waveguide templates needed for our new wavegudes
from ipkiss3.pcell.photonics.waveguide import WindowWaveguideTemplate, TemplatedWindowWaveguide
from picazzo3.traces.twoshape import CoreCladdingShapeWaveguide
from ipkiss3.pcell.trace.window.window import PathTraceWindow
from ipkiss.process.layer import PPLayer
from ipcore.exceptions.exc import PropertyValidationError

# UNUSED
class WGWireWaveguideTemplate(WireWaveguideTemplate):
    _name_prefix = "WGTMPL"

    class Layout(WireWaveguideTemplate.Layout):
        core_process = ProcessProperty(locked=True, default=TECH.PROCESS.WG)
        core_purpose = PurposeProperty(locked=True, default=TECH.PURPOSE.CORE)
        cladding_process = ProcessProperty(locked=True, default=TECH.PROCESS.WG)
        cladding_purpose = PurposeProperty(locked=True, default=TECH.PURPOSE.CLADDING)
        core_width = PositiveNumberProperty(default=TECH.WG.CORE_WIDTH)
        cladding_width = PositiveNumberProperty(default=TECH.WG.CLADDING_WIDTH)
# end WGWireWaveguideTemplate


# ---------------------------
# NEW WIRE WAVEGUIDE TEMPLATE
# ---------------------------
class AIMWGWireWaveguideTemplate(WindowWaveguideTemplate):
    """ Base class for window waveguide templates using a separate shape for the exclusion zone or trench around
        the waveguide.
    """
    _templated_class = CoreCladdingShapeWaveguide

    class Layout(WindowWaveguideTemplate.Layout):

        core_process        = ProcessProperty(default=TECH.PROCESS.WG, doc="process for the waveguide core")
        core_purpose        = PurposeProperty(default=TECH.PURPOSE.LF.LINE, doc="drawing purpose for the waveguide core")
        cladding_process    = ProcessProperty(doc="process for the waveguide cladding, defaults to the core process")
        cladding_purpose    = PurposeProperty(default=TECH.PURPOSE.LF_AREA, doc="drawing purpose layer for the cladding")
        # core_width          = PositiveNumberProperty(default=TECH.WG.CORE_WIDTH)
        cladding_width      = PositiveNumberProperty(default=TECH.WG.CLADDING_WIDTH,
                                                doc="total width of the waveguide with cladding")

        def _default_cladding_process(self):
            return self.core_process

        def _default_cover_layers(self):
            # Layer for Manhattan rectangles
            return [PPLayer(self.cladding_process, self.cladding_purpose)]

        def validate_properties(self):
            if self.cladding_width < self.core_width:
                raise PropertyValidationError(
                    "The waveguide cladding should be at least of as wide as the core. core={:f}, cladding={:f}".format(
                        self.core_width, self.cladding_width))
            return True

        def _default_width(self):
            return self.cladding_width

        def _default_windows(self):

            # populate the cladding PPlayers
            clad_pp_layers_list = [
                TECH.PPLAYER.AIM.BESAMFILL,
                TECH.PPLAYER.AIM.BCAAMFILL,
                TECH.PPLAYER.AIM.BSEAMFILL,
                TECH.PPLAYER.AIM.BFNAMFILL,
                TECH.PPLAYER.AIM.BSNAMFILL,
                TECH.PPLAYER.AIM.BM1AMFILL,
                TECH.PPLAYER.AIM.BMLAMFILL,
                TECH.PPLAYER.AIM.BM2AMFILL,
                    ]

            windows = []

            # add cladding windows
            for pplayer in clad_pp_layers_list:
                windows.append(PathTraceWindow(layer=pplayer,
                                               start_offset=-0.5 * self.cladding_width,
                                               end_offset=+0.5 * self.cladding_width,
                                               shape_property_name="cladding_shape"))

            # add core layer
            windows.append(PathTraceWindow( layer           = TECH.PPLAYER.WG.COR,
                                            start_offset    = -0.5 * self.core_width,
                                            end_offset      = +0.5 * self.core_width))

            return windows

# end AIMWGWireWaveguideTemplate



class StripWgTemplate(AIMWGWireWaveguideTemplate):
    """ Single-mode strip waveguide, C-band TE mode"""

    def _default_name(self):
        return "StripWgTemplate"

    class Layout(AIMWGWireWaveguideTemplate.Layout):
        core_width      = PositiveNumberProperty(default=0.4)
        cladding_width  = PositiveNumberProperty(default=8.0)



from ipkiss3.pcell.photonics.rounded_waveguide import RoundedWaveguide

class WireWaveguide(RoundedWaveguide):
    def _default_trace_template(self):
        return StripWgTemplate()

    class Layout(RoundedWaveguide.Layout):
        def _default_bend_radius(self):
            return TECH.WG.BEND_RADIUS