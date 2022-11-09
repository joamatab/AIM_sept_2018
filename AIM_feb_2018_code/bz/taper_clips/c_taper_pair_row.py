"""
Draws a row of taper pairs
Authors: bohan zhang

AIM
"""


# --------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------

# import my code path
# import sys
# sys.path.append( '../../' )

from nathan import technology                 # TECH
import ipkiss3.all as i3                        # ipkiss
import inspect                                  # for inspecting methods of a class

# linear taper
from bz.tapers.c_linear_taper import LinearTaper

# my taper pair
from bz.taper_clips.c_taper_pair import TaperPair

# import aim waveguide template
from nathan.technology.WgTemplate import StripWgTemplate


# --------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------

# -------------------------------
# TaperPairRow class
# -------------------------------
class TaperPairRow(i3.PCell):
    """
        Draws a row of taper pairs

        this is for aim

        Layout properties/inputs:
            taper_prop_dict
                Dictionary of taper cell properties
                Properties = "length", "width1", "width2", "width_etch"
            connect_length
                connecting length between back to back tapers
            pair_connect_length
                connecting length between taper PAIRS
            n_pairs
                number of tapers in this row
    """

    # name prefix
    _name_prefix = 'TAPER_PAIR_ROW'

    # ----------------
    # Layout
    class Layout(i3.LayoutView):


        # Properties -------

        # taper to draw
        taper_prop_dict = i3.DictProperty( default = {}, doc = 'Dictionary of taper cell properties.' + \
                                           'Properties = "length", "width1", "width2", "width_etch" ' )

        # connecting length between tapers
        connect_length = i3.NumberProperty( default=0.0, doc='distance between tapers' )

        # connecting length between taper PAIRS
        pair_connect_length = i3.NumberProperty( default=0.0, doc='distance between taper pairs' )

        # number of taper pairs
        n_pairs = i3.IntProperty( default = 1, doc = 'number of taper pairs' )

        # Methods -------


        def _generate_instances(self, insts):
            # Generates taper pairs

            tp_name_list = []

            for ii in range(self.n_pairs):
                # for each pair

                # draw taper pair layout
                tp_lay = TaperPair(name=f'{self.name}_tp{str(ii)}').get_default_view(
                    i3.LayoutView
                )

                tp_lay.set(
                            taper_prop_dict = self.taper_prop_dict,
                            connect_length  = self.connect_length )

                # set name
                tp_name = f'tp{str(ii)}'
                tp_name_list.append( tp_name )

                # set transformation
                if ii > 0:

                    # set transform
                    t = i3.vector_match_transform(  tp_lay.ports['left'],
                                                    insts[ tp_name_list[ii - 1] ].ports['right']) \
                                                            + i3.Translation( ( self.pair_connect_length, 0.0 ) )

                    # print t

                    # draw next taper pair
                    insts += i3.SRef(name=tp_name, reference=tp_lay, transformation=t)

                    # route wg
                    route_wg = i3.RouteManhattan(   input_port  = insts[ tp_name_list[ii-1] ].ports['right'],
                                                    output_port = insts[ tp_name_list[ii] ].ports['left'])

                    # # make my OWN custom waveguide trace template
                    # wg_trace = f_MyIMECWaveguideTemplate( core_width = self.taper_prop_dict['width1'],
                    #                                       cladding_width = self.taper_prop_dict['width1'] + 2.0*self.taper_prop_dict['width_etch'] )

                    # make waveguide
                    wg = i3.Waveguide(
                        trace_template=StripWgTemplate(),
                        name=f'{self.name}_WG{str(ii)}',
                    )


                    # add wg
                    insts += i3.SRef(
                        name=f'{self.name}connect_wg{str(ii)}',
                        reference=wg.Layout(shape=route_wg),
                    )


                else:
                    # draw first taper pair
                    insts += i3.SRef(name=tp_name, reference=tp_lay)

                    # DEBUG
                    # print insts

                    # end if else

            return insts
        # end _generate_instances()

        def _generate_ports(self, ports):
            # add ports 'left' and 'right'

            # left port
            ports += i3.OpticalPort( name='left',
                                     position=self.instances[ 'tp0' ].ports['left'].position,
                                     angle= 180.0 )

            # right port
            ports += i3.OpticalPort(
                name='right',
                position=self.instances[f'tp{str(self.n_pairs - 1)}']
                .ports['right']
                .position,
                angle=0.0,
            )


            return ports

        # end _generate_ports()

    # end class Layout()
    # ----------------

# end class TaperPairRow()
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

    # now make taper pair row
    connect_length      = 0.0
    pair_connect_length = 30.0
    n_pairs             = 3
    tp_rows_layout      = TaperPairRow().Layout(
                                                    taper_prop_dict     = taper_prop_dict,
                                                    connect_length      = connect_length,
                                                    pair_connect_length = pair_connect_length,
                                                    n_pairs             = n_pairs )

    tp_rows_layout.write_gdsii('./gds/test_taper_pair_rows_layout.gds')

    print tp_rows_layout.ports


# end main