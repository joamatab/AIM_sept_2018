import technology
import ipkiss3.all as i3
from technology.WgTemplate import StripWgTemplate

import numpy as np

class LinearTaper(i3.PCell):
    """Linear tapered waveguide: a linear taper between waveguide widths
    """

    _name_prefix = "LinTaper"

    class Layout(i3.LayoutView):

        wg_width_in = i3.PositiveNumberProperty(default=i3.TECH.WG.CORE_WIDTH, doc="Width of input waveguide (west side)")
        wg_width_out = i3.PositiveNumberProperty(default=i3.TECH.WG.CORE_WIDTH, doc="Width of output waveguide (east side)")
        length = i3.PositiveNumberProperty(default = 10.0, doc="Length of taper")

        def validate_properties(self):
            """Check whether the combination of properties is valid."""
            return True

        def _generate_elements(self, elems):
            # Waveguide path
            wg_path = [(0.0, 0.0), (self.length, 0.0)]

            taper_boundary = [(0.0, self.wg_width_in/2),(self.length, self.wg_width_out/2),
                           (self.length, -self.wg_width_out/2),(0.0, -self.wg_width_in/2)]

            taper_shape = i3.Boundary(shape=taper_boundary,layer=i3.TECH.PPLAYER.WG.COR)

            # Add taper shape to core layer
            elems += taper_shape

            # Add block layers
            import block_layers as bl
            block_layers = bl.layers
            block_widths = bl.widths
            for ii in range(len(block_layers)):
                fill_boundary = [(0.0, self.wg_width_in / 2+block_widths[ii]), (self.length, self.wg_width_out / 2+block_widths[ii]),
                                 (self.length, -self.wg_width_out / 2-block_widths[ii]), (0.0, -self.wg_width_in / 2-block_widths[ii])]
                fill_shape = i3.Boundary(shape=fill_boundary,layer=block_layers[ii])
                elems += fill_shape

            return elems

        def _generate_ports(self, ports):
            ports += i3.OpticalPort(name="in", position=(0.0, 0.0), angle=180.0,
                                    trace_template=StripWgTemplate().Layout(core_width=self.wg_width_in))
            ports += i3.OpticalPort(name="out", position=(self.length, 0.0), angle=0.0,
                                    trace_template=StripWgTemplate().Layout(core_width=self.wg_width_out))
            return ports
