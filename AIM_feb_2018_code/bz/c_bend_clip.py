"""
Makes bend clip
authors: bohan
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

# tapers
from nathan.Linear_Taper import LinearTaper
from bz.tapers.c_parabolic_taper import ParabolicTaper

# my taper pair row
from bz.taper_clips.c_taper_pair_row import TaperPairRow

# import aim waveguide template
from nathan.technology.WgTemplate import StripWgTemplate

# import edge coupler
from bz.c_edge_coupler import EdgeCoupler

# import os so i can get the path to this file
import os

# import numpy
import numpy as np


# --------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------

# -------------------------------
# BendClip class
# -------------------------------
class BendClip(i3.PCell):
    """
        Draws a row of bends yea
        Draws the TX bends

        this is for aim


        doesn't actually add the edge couplers... because that's too painful

        Layout properties/inputs:
            n_bend_pairs
    """

    # name prefix
    _name_prefix = 'BEND_CLIP_AIM'

    # ----------------
    # Layout
    class Layout(i3.LayoutView):


        # Properties -------

        # number of bend pairs
        n_pairs = i3.IntProperty( default = 1, doc = 'number of bend pairs' )

        # Methods -------


        def _generate_instances(self, insts):
            # Generates bend pairs

            tp_name_list = []

            # arc path
            fname       = '../nathan/bend_data/txbend.txt'
            path_width  = np.loadtxt( fname, np.float_ )
            arc_path    = path_width[:, :2]

            # make a bend woo
            bend_wg_lay = i3.Waveguide( name = self.name+"_Bend", trace_template = StripWgTemplate() ).get_default_view(i3.LayoutView)
            bend_wg_lay.set( shape = arc_path )

            # add to insts
            insts += i3.SRef( name = self.name + '_BEND',
                              reference = bend_wg_lay )

            # list of bend names
            bend_name_A_list = []
            bend_name_B_list = []

            # draw a bunch of bends
            for ii in range(self.n_pairs):

                # make bend A
                if ii == 0:
                    # place first bend pair

                    # make a bend woo
                    bend_name_A     = self.name + '_BEND_A' + str(ii)
                    bend_wg_lay_A   = i3.Waveguide( trace_template = StripWgTemplate() ).get_default_view(i3.LayoutView)
                    bend_wg_lay_A.set( shape = arc_path )

                    # add to insts
                    insts += i3.SRef( name          = bend_name_A,
                                      reference     = bend_wg_lay_A,
                                      flatten       = True )

                else:

                    # make a bend woo
                    bend_name_A     = self.name + '_BEND_A' + str(ii)
                    bend_wg_lay_A   = i3.Waveguide( trace_template = StripWgTemplate() ).get_default_view(i3.LayoutView)
                    bend_wg_lay_A.set( shape = arc_path )

                    # add to insts
                    t = i3.vector_match_transform(  bend_wg_lay_A.ports['in'],
                                                    insts[ bend_name_B_list[ii-1] ].ports['out'],
                                                    mirrored = False )
                    insts += i3.SRef( name          = bend_name_A,
                                      reference     = bend_wg_lay_A,
                                      transformation = t,
                                      flatten       = True )

                # make another bend woo
                bend_name_B     = self.name + '_BEND_B' + str(ii)
                bend_wg_lay_B   = i3.Waveguide( trace_template = StripWgTemplate() ).get_default_view(i3.LayoutView)
                bend_wg_lay_B.set( shape = arc_path )

                # add to insts
                t = i3.vector_match_transform( bend_wg_lay_B.ports['in'], insts[bend_name_A].ports['out'],  mirrored = True )
                insts += i3.SRef( name          = bend_name_B,
                                  reference     = bend_wg_lay_B,
                                  transformation = t,
                                  flatten       = True )

                # end if else

                # append bend names
                bend_name_A_list.append(bend_name_A)
                bend_name_B_list.append(bend_name_B)

            # end for loop


            return insts
        # end _generate_instances()

        def _generate_ports(self, ports):
            # add ports 'left' and 'right'

            # left port
            ports += i3.OpticalPort( name       = 'in',
                                     position   = self.instances[ self.name + '_BEND_A0' ].ports['in'].position,
                                     angle      = 0.0 )

            # right port
            ports += i3.OpticalPort(name        = 'out',
                                    position    = self.instances[ self.name + '_BEND_B' + str(self.n_pairs-1) ].ports['out'].position,
                                    angle       = 180.0 )

            return ports

        # end _generate_ports()

    # end class Layout()
    # ----------------

# end class BendClip()
# -------------------------------


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

if __name__ == '__main__':

    print('hi')

    # first make a linear taper
    # taper_prop_dict = {
    #     'length':       100.0,
    #     'width1':       0.450,
    #     'width2':       11.0,
    #     'width_etch':   2.0
    # }
    # lin_taper_cell = LinearTaper
    #
    # # now make taper pair row
    # connect_length      = 0.0
    # pair_connect_length = 30.0
    # n_pairs             = 3
    bend_clip_layout      = BendClip().Layout( n_pairs = 20 )

    bend_clip_layout.write_gdsii('./gds/test_bend_clip.gds')

    print bend_clip_layout.ports


# end main