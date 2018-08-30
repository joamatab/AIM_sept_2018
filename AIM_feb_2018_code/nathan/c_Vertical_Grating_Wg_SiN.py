"""
DRAWS VERTICALLY ETCHED NITRIDE GRATING
EDITED BY BOHAN
"""

# --------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------

import technology
import ipkiss3.all as i3
from technology.WgTemplate import StripWgTemplate

import numpy as np
import pylab as plt


# --------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------


# -------------------------------
# NitrideGratingWg class
# -------------------------------
class NitrideGratingWg(i3.PCell):
    """
    Nitride grating
    Can draw both sidewall gratings and full width (vertical) gratings

    Layout properties:
        period
        duty_cycle
        grating_amp
        wg_width
        length
        grating_type
            'vertical' for vertical (along entire width) grating
            'one_sidewall' for single sidewall grating
            'two_sidewalls' for double sidewall grating
        nitride_layer
            flag to determine nitride top or bottom ('top' or 'bottom')

    Ports:
        in
        out

    """

    _name_prefix = "NitrideVertGratWg"

    class Layout(i3.LayoutView):

        from ipkiss.technology import get_technology
        TECH = get_technology()

        period      = i3.PositiveNumberProperty(default = .3, doc = "Period of sidewall grating")
        duty_cycle  = i3.PositiveNumberProperty(default=.1, doc="Length of grating teeth (along periodic direction)")
        grating_amp = i3.PositiveNumberProperty(default=.01, doc="Width/amplitude of grating teeth (normal to periodic direction)")
        wg_width    = i3.PositiveNumberProperty(default=TECH.WG.CORE_WIDTH, doc="Width of waveguide core (if grating_amp=0 width of waveguide)")
        length      = i3.PositiveNumberProperty(default = 100.0, doc="Length of waveguide")

        # Flag to determine grating type
        # 'vertical' for vertical (along entire width) grating
        # 'one_sidewall' for single sidewall grating
        # 'two_sidewalls' for double sidewall grating
        grating_type = i3.StringProperty( default='', doc='determines grating type. Set to "vertical", "one_sidewall", or "two_sidewalls"')

        # flag to determine nitride top or bottom ('top' or 'bottom')
        nitride_layer = i3.StringProperty( default='', doc='determines which nitride layer to draw. Set to "top" or "bottom"')

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

            # determine which layer to use
            my_layer = {
                'top':      i3.TECH.PPLAYER.AIM.SNAM,
                'bottom':   i3.TECH.PPLAYER.AIM.FNAM,
            }[self.nitride_layer]

            # Add waveguide core
            elems += i3.Path(layer=i3.TECH.PPLAYER.WG.COR, shape=wg_path, line_width=self.wg_width)
            if self.grating_type != 'vertical':
                elems += i3.Path(layer=my_layer, shape=wg_path, line_width=self.wg_width)

            # Add grating teeth
            ytrans = i3.Translation((0.0,self.wg_width/2+self.grating_amp/2))
            for ii in range(numperiod):
                #Start with gap rather than tooth

                if self.grating_type == 'vertical':
                    # Draw vertically etched tooth
                    xtrans = i3.Translation(((gap_cycle+ii*self.period),0.0))
                    elems += i3.Path(layer=my_layer, shape=gt_path, line_width=self.wg_width,
                                     transformation=(xtrans))

                elif self.grating_type == 'one_sidewall':
                    # Draw single sided sidewall grating
                    xtrans = i3.Translation(((gap_cycle+ii*self.period),0.0))
                    elems += i3.Path(layer=my_layer, shape=gt_path, line_width=self.grating_amp,
                                     transformation=(xtrans + ytrans))

                elif self.grating_type == 'two_sidewalls':
                    # Draw double sided sidewall grating
                    xtrans = i3.Translation(((gap_cycle+ii*self.period),0.0))
                    elems += i3.Path(layer=my_layer, shape=gt_path, line_width=self.grating_amp,
                                     transformation=(xtrans + ytrans))
                    elems += i3.Path(layer=my_layer, shape=gt_path, line_width=self.grating_amp,
                                     transformation=(xtrans - ytrans))

                # # draw bottom grating if desired
                # if self.both_sides == True:
                #     elems += i3.Path(layer=i3.TECH.PPLAYER.WG.COR, shape=gt_path, line_width=self.grating_amp,
                #                      transformation=(xtrans - ytrans))

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

# end NitrideGratingWg class

# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

if __name__ == '__main__':

    print ('hi')

    # values
    period          = 0.5
    duty_cycle      = 0.2
    grating_amp     = 0.1
    wg_width        = 2.0
    length          = 100.0
    grating_type    = 'one_sidewall'
    nitride_layer   = 'top'

    # draw layout
    nitride_grating_layout = NitrideGratingWg().Layout( period          = period,
                                                        duty_cycle      = duty_cycle,
                                                        grating_amp     = grating_amp,
                                                        wg_width        = wg_width,
                                                        length          = length,
                                                        grating_type    = grating_type,
                                                        nitride_layer   = nitride_layer )
    nitride_grating_layout.write_gdsii('./gds_files/test_nitride_grating.gds')