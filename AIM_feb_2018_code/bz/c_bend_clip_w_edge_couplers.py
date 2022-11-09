"""
Makes bend clip with edge coupler ports, but NO actual edge couplers
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

# bends
from c_bend_clip import BendClip


# --------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------

# -------------------------------
# BendClipEdgeCouplers class
# -------------------------------
class BendClipEdgeCouplers(i3.PCell):
    """
        Draws a row of bends yea
        Draws the TX bends

        this is for aim


        doesn't actually add the edge couplers... because that's too painful

        Layout properties/inputs:
            n_bend_pairs
    """

    # name prefix
    _name_prefix = 'BEND_CLIP_COUPLERS_AIM'

    # ----------------
    # Layout
    class Layout(i3.LayoutView):


        # Properties -------

        # number of taper pairs
        n_pairs = i3.IntProperty( default = 1, doc = 'number of taper pairs' )

        # Methods -------


        def _generate_instances(self, insts):
            # Generates taper pairs w edge couplers

            # load the aim gds just to get its positions and stuff
            # main chip GDS
            fname               = '../PDK_Library_Layout_GDS/ap_suny_v20a_chipframe.gds'
            main_chip_gds_cell  = i3.GDSCell( filename=fname )

            # grab layout size info
            main_chip_gds_lay               = main_chip_gds_cell.Layout()
            main_chip_gds_lay_size_info     = main_chip_gds_lay.size_info()

            # grab relevant positions
            chip_edge_east = main_chip_gds_lay_size_info.east
            chip_edge_west = main_chip_gds_lay_size_info.west

            # make edge coupler
            edge_coupler_gds_lay = EdgeCoupler(
                name=f'{self.name}edge_coupler_sffdfi'
            ).Layout()


            # add and route input/west edgecoupler
            # position edge coupler on west side of chip
            chip_port_west              = i3.OpticalPort(  position = ( chip_edge_west, 0.0 ), angle_deg = 0.0 )
            edge_coupler_west_port      = edge_coupler_gds_lay.ports['out']
            t                           = i3.vector_match_transform( edge_coupler_west_port, chip_port_west )
            edge_coupler_west_name = f'{self.name}_EDGE_COUPLER_WEST'
            west_edge_coupler = i3.SRef( name              = edge_coupler_west_name,
                              reference         = edge_coupler_gds_lay,
                              transformation    = t,
                              flatten           = False )


            # add a small linear taper to go from 0.4 to 0.5um wg
            lin_taper_lay = LinearTaper().get_default_view(i3.LayoutView)
            lin_taper_lay.set( wg_width_in  = 0.4,
                               wg_width_out = 0.5,
                               length       = 10.0 )
            t = i3.vector_match_transform(  lin_taper_lay.ports['in'],
                                            west_edge_coupler.ports['in'] )
            lin_taper_lay_name = f'{self.name}_EDGETAPER_WEST'
            insts += i3.SRef( name              = lin_taper_lay_name,
                              reference         = lin_taper_lay,
                              transformation    = t,
                              flatten           = True )

            # route wg to wg with arc
            bend_radius      = 10.0
            arc_center_1     = (    insts[lin_taper_lay_name].ports['out'].position[0],
                                    insts[lin_taper_lay_name].ports['out'].position[1] + bend_radius )
            route_wg_shape_arc1 = i3.ShapeArc(  radius       = bend_radius,
                                                angle_step   = 1.0,
                                                center       = arc_center_1,
                                                start_angle  = 269.5,
                                                end_angle    = 0.5,
                                                closed       = False,
                                                clockwise    = False )
            wg_name_arc1 = f'{self.name}_ARC1'
            wg_lay_arc1     = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc1 ).get_default_view(i3.LayoutView)
            wg_lay_arc1.set( shape = route_wg_shape_arc1 )
            insts           += i3.SRef( name        = wg_name_arc1,
                                        reference   = wg_lay_arc1,
                                        flatten     = True )

            # add the bends
            bend_clip_lay = BendClip(name=f'{self.name}_BEND_CLIP').get_default_view(
                i3.LayoutView
            )

            bend_clip_lay.set( n_pairs = self.n_pairs )

            # add to insts
            bend_clip_lay_name = f'{self.name}_BEND_CLIP'
            t = i3.vector_match_transform( bend_clip_lay.ports['in'],
                                           insts[wg_name_arc1].ports['out'] )
            insts += i3.SRef( name              = bend_clip_lay_name,
                              reference         = bend_clip_lay,
                              transformation    = t,
                              flatten           = True )


            # add output bend
            arc_center_2     = (    insts[bend_clip_lay_name].ports['out'].position[0] + bend_radius,
                                    insts[bend_clip_lay_name].ports['out'].position[1] )
            route_wg_shape_arc2 = i3.ShapeArc(  radius       = bend_radius,
                                                angle_step   = 1.0,
                                                center       = arc_center_2,
                                                start_angle  = 180.5,
                                                end_angle    = 89.5,
                                                closed       = False,
                                                clockwise    = True )
            wg_name_arc2 = f'{self.name}_ARC2'
            wg_lay_arc2     = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc2 ).get_default_view(i3.LayoutView)
            wg_lay_arc2.set( shape = route_wg_shape_arc2 )
            insts           += i3.SRef( name        = wg_name_arc2,
                                        reference   = wg_lay_arc2,
                                        flatten     = True )


            # add east coupler
            chip_port_east              = i3.OpticalPort(  position = ( chip_edge_east, insts[wg_name_arc2].ports['out'].position[1] ),
                                                           angle_deg = 180.0 )
            edge_coupler_east_port      = edge_coupler_gds_lay.ports['out']
            t                           = i3.vector_match_transform( edge_coupler_east_port, chip_port_east, mirrored = True )
            edge_coupler_east_name = f'{self.name}_EDGE_COUPLER_EAST'
            east_edge_coupler =  i3.SRef( name              = edge_coupler_east_name,
                              reference         = edge_coupler_gds_lay,
                              transformation    = t,
                              flatten           = False )


            # add a small linear taper to go from 0.4 to 0.5um wg
            lin_taper_lay = LinearTaper().get_default_view(i3.LayoutView)
            lin_taper_lay.set( wg_width_in  = 0.4,
                               wg_width_out = 0.5,
                               length       = 10.0 )
            t = i3.vector_match_transform(  lin_taper_lay.ports['in'],
                                            east_edge_coupler.ports['in'], mirrored = True )
            lin_taper_lay_name = f'{self.name}_EDGETAPER_EAST'
            insts += i3.SRef( name              = lin_taper_lay_name,
                              reference         = lin_taper_lay,
                              transformation    = t,
                              flatten           = True )


            # route arc to arc with straight section
            route_wg_shape_out = i3.Shape([ insts[wg_name_arc2].ports['out'].position,
                                            insts[lin_taper_lay_name].ports['out'].position ])
            wg_name_out = f'{self.name}_WG_CON_OUT'
            wg_lay_out         = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_out ).get_default_view(i3.LayoutView)
            wg_lay_out.set( shape = route_wg_shape_out )
            insts           += i3.SRef( name        = wg_name_out,
                                        reference   = wg_lay_out,
                                        flatten     = True )


            return insts
        # end _generate_instances()

        def _generate_ports(self, ports):
            # add ports 'left' and 'right'

            # left port
            ports += i3.OpticalPort(
                name='in',
                position=self.instances[f'{self.name}_EDGETAPER_WEST']
                .ports['in']
                .position,
                angle=180.0,
            )


            # right port
            ports += i3.OpticalPort(
                name='out',
                position=self.instances[f'{self.name}_EDGETAPER_EAST']
                .ports['out']
                .position,
                angle=0.0,
            )


            return ports

        # end _generate_ports()

    # end class Layout()
    # ----------------

# end class BendClipEdgeCouplers()
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
    bend_clip_layout      = BendClipEdgeCouplers().Layout( n_pairs = 300 )

    bend_clip_layout.write_gdsii('./gds/test_bend_clip_edge_couplers.gds')

    print bend_clip_layout.ports


# end main