__all__ = ['WGWireWaveguideTemplate', 'StripWgTemplate']

from ipkiss.technology import get_technology
from ipkiss.process import ProcessProperty, PurposeProperty
from ipcore.properties.predefined import PositiveNumberProperty, NonNegativeNumberProperty
from ipcore.properties.lock_properties import lock_properties
TECH = get_technology()

from picazzo3.traces.wire_wg import WireWaveguideTemplate

class WGWireWaveguideTemplate(WireWaveguideTemplate):
    _name_prefix = "WGTMPL"

    class Layout(WireWaveguideTemplate.Layout):
        core_process = ProcessProperty(locked=True, default=TECH.PROCESS.WG)
        core_purpose = PurposeProperty(locked=True, default=TECH.PURPOSE.CORE)
        cladding_process = ProcessProperty(locked=True, default=TECH.PROCESS.WG)
        cladding_purpose = PurposeProperty(locked=True, default=TECH.PURPOSE.CLADDING)
        core_width = PositiveNumberProperty(default=TECH.WG.CORE_WIDTH)
        cladding_width = PositiveNumberProperty(default=TECH.WG.CLADDING_WIDTH)


class StripWgTemplate(WGWireWaveguideTemplate):
    """ Single-mode strip waveguide, C-band TE mode"""

    def _default_name(self):
        return "StripWgTemplate"

    class Layout(WGWireWaveguideTemplate.Layout):
        core_width = PositiveNumberProperty(default=0.4)
        cladding_width = PositiveNumberProperty(default=4.0)

from ipkiss3.pcell.photonics.rounded_waveguide import RoundedWaveguide


class WireWaveguide(RoundedWaveguide):
    def _default_trace_template(self):
        return StripWgTemplate()

    class Layout(RoundedWaveguide.Layout):
        def _default_bend_radius(self):
            return TECH.WG.BEND_RADIUS