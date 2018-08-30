"""
DRAWS WAVEGUIDE WITH SIDEWALL GRATING
EDITED BY BOHAN
"""

import technology
import ipkiss3.all as i3
from technology.WgTemplate import StripWgTemplate

import numpy as np
import pylab as plt

class SidewallGratingWg(i3.PCell):
    """Sidewall Grating Waveguide: Waveguide with rectangular sidewall gratings

    Layout properties:
        period
        duty_cycle
        grating_amp
        wg_width
        length

    Ports:
        in
        out

    """

    _name_prefix = "SwGratWg"

    class Layout(i3.LayoutView):

        from ipkiss.technology import get_technology
        TECH = get_technology()

        period      = i3.PositiveNumberProperty(default = .3, doc = "Period of sidewall grating")
        duty_cycle  = i3.PositiveNumberProperty(default=.1, doc="Length of grating teeth (along periodic direction)")
        grating_amp = i3.NumberProperty(default=.01, doc="Width/amplitude of grating teeth (normal to periodic direction)")
        wg_width    = i3.PositiveNumberProperty(default=TECH.WG.CORE_WIDTH, doc="Width of waveguide core (if grating_amp=0 width of waveguide)")
        length      = i3.PositiveNumberProperty(default = 100.0, doc="Length of waveguide")

        # Flag, set to True to draw grating on both sides of wg.
        both_sides = i3.BoolProperty( default=False, doc='set to true to draw grating on both sides')

        def validate_properties(self):
            """Check whether the combination of properties is valid."""
            if self.duty_cycle>=self.period:
                raise i3.PropertyValidationError(self, "Duty cycle is larger than/equal to the grating period",
                                                 {"duty_cyle": self.duty_cycle})

            return True

        def _generate_elements(self, elems):
            # Waveguide path
            wg_path = [(0.0, 0.0), (self.length, 0.0)]

            # Grating tooth path
            gt_path = [(0.0, 0.0), (self.duty_cycle, 0.0)]

            gap_cycle = self.period-self.duty_cycle
            numperiod = int(np.floor(self.length/self.period))

            # Add waveguide core
            elems += i3.Path(layer=i3.TECH.PPLAYER.WG.COR, shape=wg_path, line_width=self.wg_width)

            # Add grating teeth
            if self.grating_amp > 0.0:
                # grating amplitude has to be non-zero

                ytrans = i3.Translation((0.0,self.wg_width/2+self.grating_amp/2))
                for ii in range(numperiod):
                    #Start with gap rather than tooth
                    xtrans = i3.Translation(((gap_cycle+ii*self.period),0.0))
                    elems += i3.Path(layer=i3.TECH.PPLAYER.WG.COR, shape=gt_path, line_width=self.grating_amp,
                                     transformation=(xtrans + ytrans))

                    # draw bottom grating if desired
                    if self.both_sides == True:
                        elems += i3.Path(layer=i3.TECH.PPLAYER.WG.COR, shape=gt_path, line_width=self.grating_amp,
                                         transformation=(xtrans - ytrans))

            # Add block layers
            import block_layers as bl
            block_layers = bl.layers
            block_widths = bl.widths
            for ii in range(len(block_layers)):
                elems += i3.Path(layer=block_layers[ii], shape=wg_path, line_width=self.wg_width+2*self.grating_amp+2*block_widths[ii])

            return elems

        def _generate_ports(self, ports):
            # ports += i3.OpticalPort(name="in", position=(0.0, 0.0), angle=180.0,
            #                         trace_template=StripWgTemplate().Layout(core_width=self.wg_width))
            # ports += i3.OpticalPort(name="out", position=(self.length, 0.0), angle=0.0,
            #                         trace_template=StripWgTemplate().Layout(core_width=self.wg_width))

            ports += i3.OpticalPort(name="in", position=(0.0, 0.0), angle=180.0)
            ports += i3.OpticalPort(name="out", position=(self.length, 0.0), angle=0.0)

            return ports
