"""
AIM basic taper clip, draws a row of back to back taper pairs connected to edge couples positioned at edges of aim chip
authors: bohan zhang
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


# --------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------

# -------------------------------
# TaperPairRowEdgeCouplers class
# -------------------------------
class TaperPairRowEdgeCouplers(i3.PCell):
    """
        Draws a row of taper pairs

        this is for aim


        doesn't actually add the edge couplers... because that's too painful

        Layout properties/inputs:
            n_pairs
                number of tapers in this row
    """

    # name prefix
    _name_prefix = 'TAPER_PAIR_ROW_AIM'

    # ----------------
    # Layout
    class Layout(i3.LayoutView):


        # Properties -------

        # taper to draw
        # taper_prop_dict = i3.DictProperty( default = {}, doc = 'Dictionary of taper cell properties.' + \
        #                                    'Properties = "length", "width1", "width2", "width_etch" ' )

        # connecting length between tapers
        # connect_length = i3.NumberProperty( default=0.0, doc='distance between tapers' )

        # connecting length between taper PAIRS
        # pair_connect_length = i3.NumberProperty( default=0.0, doc='distance between taper pairs' )

        # number of taper pairs
        n_pairs = i3.IntProperty( default = 1, doc = 'number of taper pairs' )

        # Methods -------


        def _generate_instances(self, insts):
            # Generates taper pairs

            tp_name_list = []


            # temporary? pick taper properties
            taper_prop_dict = {
                'length':       79.0,
                'width1':       0.50,
                'width2':       6.50,
                'width_etch':   2.0
            }

            # generate a huge taper row
            tp_rows_layout = TaperPairRow().Layout(
                                                    taper_prop_dict     = taper_prop_dict,
                                                    connect_length      = 0.0,
                                                    pair_connect_length = 10.0,
                                                    n_pairs             = self.n_pairs )

            # load the aim gds just to get its positions and stuff
            # main chip GDS
            fname               = os.path.dirname(os.path.realpath(__file__)) + '/gds/ap_suny_v20a_chipframe.gds'
            main_chip_gds_cell  = i3.GDSCell( filename=fname )

            # grab layout size info
            main_chip_gds_lay               = main_chip_gds_cell.Layout()
            main_chip_gds_lay_size_info     = main_chip_gds_lay.size_info()

            # grab relevant positions
            chip_edge_east = main_chip_gds_lay_size_info.east
            chip_edge_west = main_chip_gds_lay_size_info.west

            # make edge coupler and add to layout
            # edge coupler
            edge_coupler_gds_lay = EdgeCoupler(name=self.name + 'edge_coupler_si').Layout()

            # add and route input/west edgecoupler
            # position edge coupler on west side of chip
            chip_port_west              = i3.OpticalPort(  position = ( chip_edge_west, 0.0 ), angle_deg = 0.0 )
            edge_coupler_west_port      = edge_coupler_gds_lay.ports['out']
            t                           = i3.vector_match_transform( edge_coupler_west_port, chip_port_west )
            edge_coupler_west_name      = self.name + '_EDGE_COUPLER_WEST'
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
            lin_taper_lay_name = self.name + '_EDGETAPER_WEST'
            insts += i3.SRef( name              = lin_taper_lay_name,
                              reference         = lin_taper_lay,
                              transformation    = t,
                              flatten           = True )

            # add taper rows
            taper_row_name  = self.name + '_TAPERSSSSSSSS'
            t = i3.vector_match_transform( tp_rows_layout.ports['left'],
                                           insts[lin_taper_lay_name].ports['out']
                                            )
            insts += i3.SRef( name              = taper_row_name,
                              reference         = tp_rows_layout,
                              transformation    = t,
                              flatten           = True )

            # add east coupler
            chip_port_east              = i3.OpticalPort(  position = ( chip_edge_east, 0.0 ), angle_deg = 180.0 )
            edge_coupler_east_port      = edge_coupler_gds_lay.ports['out']
            t                           = i3.vector_match_transform( edge_coupler_east_port, chip_port_east, mirrored = True )
            edge_coupler_east_name      = self.name + '_EDGE_COUPLER_EAST'
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
            lin_taper_lay_name = self.name + '_EDGETAPER_EAST'
            insts += i3.SRef( name              = lin_taper_lay_name,
                              reference         = lin_taper_lay,
                              transformation    = t,
                              flatten           = True )

            # route the east coupler to the east edge of the taper pairs
            route_wg_row_taper  = i3.Shape([ insts[taper_row_name].ports['right'].position,
                                             insts[lin_taper_lay_name].ports['out'].position ])
            wg_name     = self.name + '_WG'
            wg_lay      = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name ).get_default_view(i3.LayoutView)
            wg_lay.set( shape = route_wg_row_taper )
            insts           += i3.SRef( name        = wg_name,
                                        reference   = wg_lay,
                                        flatten     = True )


            return insts
        # end _generate_instances()

        def _generate_ports(self, ports):
            # add ports 'left' and 'right'

            # left port
            ports += i3.OpticalPort( name       = 'left',
                                     position   = self.instances[ self.name + '_EDGETAPER_WEST' ].ports['in'].position,
                                     angle      = 180.0 )

            # right port
            ports += i3.OpticalPort(name        = 'right',
                                    position    = self.instances[ self.name + '_EDGETAPER_EAST' ].ports['out'].position,
                                    angle       = 0.0 )

            return ports

        # end _generate_ports()

    # end class Layout()
    # ----------------

# end class TaperPairRowEdgeCouplers()
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
    tp_rows_layout      = TaperPairRowEdgeCouplers().Layout()

    tp_rows_layout.write_gdsii('./gds/test_taper_pair_rows_w_edge_couplers_layout.gds')

    print tp_rows_layout.ports


# end main