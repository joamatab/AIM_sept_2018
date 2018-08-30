"""
Parabolic taper cell
"""


# --------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------

# from nathan import technology                 # TECH
import ipkiss3.all as i3                        # ipkiss

# block layers
from nathan.block_layers import layers as block_layers

# --------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------

# -------------------------------
# Parabolic taper class
# -------------------------------
class ParabolicTaper(i3.PCell):
    """
    Draws a single, parabolic taper

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
    _name_prefix = 'PARA_TAPER'

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
            elems += i3.ParabolicWedge( layer        = i3.TECH.PPLAYER.WG.COR,
                                        begin_coord  = ( -self.length, 0.0 ),
                                        end_coord    = ( 0.0, 0.0 ),
                                        begin_width  = self.width1,
                                        end_width    = self.width2 )

            # draw clad etch
            for block_lay in block_layers:
                elems += i3.ParabolicWedge(   layer         = block_lay,
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


#   end class ParabolicTaper()
# -------------------------------


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

if __name__ == '__main__':

    print('hi')

    # DEBUG drawing a parabolic taper
    length      = 79.0
    width1      = 0.5
    width2      = 6.5
    width_etch  = 4.0
    lin_taper_layout = ParabolicTaper().Layout(    length      = length,
                                                width1      = width1,
                                                width2      = width2,
                                                width_etch  = width_etch )
    lin_taper_layout.write_gdsii('./gds/AIM_serpentine_grating_parabolic_taper.gds')

    # # Hard code the tapers into here: (I hate hardcoding stuff, but no choice here)
    # taper_length    = 79.0      # 79 is the best according to deniz' sims
    # width_etch      = 4.0
    # wg_width        = 0.5
    # taper_swg = ParabolicTaper( name = self.name + '_TAPER' ).get_default_view(i3.LayoutView)
    # taper_swg.set(  length      = taper_length,
    #                 width1      = wg_width,
    #                 width2      = self.grat_wg_width,
    #                 width_etch  = width_etch
    #                 )
    #
    # taper_flyback = ParabolicTaper( name = self.name + '_OTHERTAPER' ).get_default_view(i3.LayoutView)
    # taper_flyback.set(  length      = taper_length,
    #                     width1      = wg_width,
    #                     width2      = self.flyback_wg_width,
    #                     width_etch  = width_etch
    #                      )

# end main