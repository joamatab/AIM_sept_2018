"""
Linear taper class
authors: bohan zhang
"""

# --------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------

from nathan import technology                 # TECH
import ipkiss3.all as i3                        # ipkiss

# block layers
from nathan.block_layers import layers as block_layers

# --------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------

# -------------------------------
# Linear taper class
# -------------------------------
class LinearTaper(i3.PCell):
    """
    Draws a single, linear taper

    Layout Properties:
        length
            Length of taper (um)
        width1
            Width of left edge of taper
        width2
            Width of right edge of taper
        width_etch
            Width of etch, from edge of waveguide
    """

    # name prefix
    _name_prefix = 'LIN_TAPER'

    # ----------------
    # Layout
    class Layout(i3.LayoutView):

        # Properties -------

        length      = i3.PositiveNumberProperty(default=0.0, doc='length of taper')
        width1      = i3.PositiveNumberProperty(default=0.0, doc='width of left edge of taper')
        width2      = i3.PositiveNumberProperty(default=0.0, doc='width of right edge of taper')
        width_etch  = i3.PositiveNumberProperty(default=0.0, doc='width of taper sidewall etch')

        # Methods -------

        def _generate_elements(self, elems):
            """
            This method generates layout by adding elements to 'elems'
            """

            # draw wg
            elems += i3.Wedge( layer        = i3.TECH.PPLAYER.WG.COR,
                               begin_coord  = ( -self.length, 0.0 ),
                               end_coord    = ( 0.0, 0.0 ),
                               begin_width  = self.width1,
                               end_width    = self.width2 )

            # draw clad etch
            for block_lay in block_layers:
                elems += i3.Wedge(layer         = block_lay,
                                  begin_coord   = (-self.length, 0.0),
                                  end_coord     = (0.0, 0.0),
                                  begin_width   = self.width1 + 2*self.width_etch,
                                  end_width     = self.width2 + 2*self.width_etch)

            # return elems
            return elems
        # end _generate_elements()

        def _generate_ports(self, ports):
            # generate ports
            # the ports are 'right', and 'left'
            ports += i3.OpticalPort( name='right', position=(0.0, 0.0), angle= 0.0 )
            ports += i3.OpticalPort( name='left', position=(-self.length, 0.0), angle= 180.0 )
            return ports
        # end _generate_ports()

    # end Layout
    # ----------------


#   end class LinearTaper()
# -------------------------------


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

if __name__ == '__main__':

    print('hi')

    # DEBUG drawing a linear taper
    length      = 200.0
    width1      = 0.45
    width2      = 8.0
    width_etch  = 4.0
    lin_taper_layout = LinearTaper().Layout(    length      = length,
                                                width1      = width1,
                                                width2      = width2,
                                                width_etch  = width_etch )
    lin_taper_layout.write_gdsii('./gds/test_lin_taper.gds')

# end main