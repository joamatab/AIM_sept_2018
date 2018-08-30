"""
draws back to back tapers
author: bohan zhang
"""


# --------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------

# # import my code path
# import sys
# sys.path.append( '../../' )

# from isipp50g import technology                 # TECH
from nathan import technology                 # TECH
import ipkiss3.all as i3                        # ipkiss
import inspect                                  # for inspecting methods of a class

# linear taper
from bz.tapers.c_linear_taper import LinearTaper
from bz.tapers.c_parabolic_taper import ParabolicTaper

# MY IMEC waveguide template
# from gratings.waveguide_traces import f_MyIMECWaveguideTemplate

# import aim waveguide template
from nathan.technology.WgTemplate import StripWgTemplate


# --------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------

# -------------------------------
# TaperPair class
# -------------------------------
class TaperPair(i3.PCell):
    """
        Draws back to back tapers

        RIGHT NOW ONLY DRAWS PARABOLIC TAPERS

        this is for aim

        Layout properties/inputs:
            taper_prop_dict
                Dictionary of taper cell properties
                Properties = "length", "width1", "width2", "width_etch"
            connect_length
                connecting length between tapers
    """

    # name prefix
    _name_prefix = 'TAPER_PAIR'

    # ----------------
    # Layout
    class Layout(i3.LayoutView):


        # Properties -------

        # taper to draw
        # taper_layout = i3.ViewProperty( default='', doc='taper cell to draw and stuff' )

        # connecting length between tapers
        connect_length = i3.NumberProperty( default=0.0, doc='distance between tapers' )

        # taper cell
        # taper_cell      = i3.PCellProperty( default=i3.PCell(), doc='taper cell to draw')
        taper_prop_dict = i3.DictProperty( default = {}, doc = 'Dictionary of taper cell properties.' + \
                                           'Properties = "length", "width1", "width2", "width_etch" ' )

        # this is terrible...
        # actually fuck it hard code in the taper

        # Methods -------


        def _generate_instances(self, insts):
            # generates taper pair

            # generate left taper cell
            taper_layout_left = ParabolicTaper( name=self.name + '_TAPER_L').get_default_view(i3.LayoutView)
            taper_layout_left.set( length       = self.taper_prop_dict['length'],
                                   width1       = self.taper_prop_dict['width1'],
                                   width2       = self.taper_prop_dict['width2'],
                                   width_etch   = self.taper_prop_dict['width_etch'] )

            # generate right taper cell
            taper_layout_right = ParabolicTaper( name=self.name + '_TAPER_R').get_default_view(i3.LayoutView)
            taper_layout_right.set( length       = self.taper_prop_dict['length'],
                                    width1       = self.taper_prop_dict['width1'],
                                    width2       = self.taper_prop_dict['width2'],
                                    width_etch   = self.taper_prop_dict['width_etch'] )

            # draw taper pairs
            insts   += i3.SRef(name=self.name + '_taper1', reference = taper_layout_left)
            t       = i3.vector_match_transform( taper_layout_left.ports['right'],
                                                 taper_layout_right.ports['right'],
                                                 mirrored=True ) + i3.Translation( ( self.connect_length, 0.0 ) )
            insts   += i3.SRef(name=self.name + '_taper2', reference = taper_layout_right, transformation=t)

            # route between tapers
            if self.connect_length > 0.0:
                route_tapers = i3.RouteManhattan(   input_port  = insts[self.name + '_taper1'].ports['right'],
                                                    output_port = insts[self.name + '_taper2'].ports['right'])

                # # make my OWN custom waveguide trace template
                # wg_trace = f_MyIMECWaveguideTemplate( core_width = taper_layout_left.width2,
                #                                       cladding_width = taper_layout_right.width2 + 2.0*taper_layout_right.width_etch )
                # wg_lay = i3.Waveguide(trace_template=StripWgTemplate(), name=wg_name).get_default_view(i3.LayoutView)


                # make waveguide
                wg = i3.Waveguide(trace_template=StripWgTemplate(), name = self.name + '_WG' )

                # add wg
                insts += i3.SRef( name=self.name + 'connect_wg', reference = wg.Layout( shape = route_tapers ) )
            # end if self.connect_length > 0.0

            return insts
        # end _generate_instances()

        def _generate_ports(self, ports):
            # add ports 'left' and 'right'

            # left port
            ports += i3.OpticalPort( name='left',
                                     position=self.instances[self.name + '_taper1'].ports['left'].position,
                                     angle= 180.0 )

            # right port
            ports += i3.OpticalPort(name='right',
                                    position=self.instances[self.name + '_taper2'].ports['left'].position,
                                    angle=0.0 )

            return ports

        # end _generate_ports()

    # end class Layout()
    # ----------------

# end class TaperPair()
# -------------------------------


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

if __name__ == '__main__':

    print('hi')

    # first make a linear taper
    taper_prop_dict = {
        'length':       100.0,
        'width1':       0.450,
        'width2':       11.0,
        'width_etch':   2.0
    }
    lin_taper_cell = LinearTaper

    # now make taper pair
    connect_length      = 0.0
    # taper_pair_layout   = TaperPair().Layout( taper_layout =  lin_taper_layout,
    #                                           connect_length = connect_length )
    taper_pair_layout = TaperPair().Layout(
                                            taper_prop_dict = taper_prop_dict,
                                            connect_length  = connect_length )

    taper_pair_layout.write_gdsii('./gds/test_taper_pair_layout.gds')

    print taper_pair_layout.ports


# end main