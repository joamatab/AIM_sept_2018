"""
Draws a long, straight grating for testing
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

# import numpy
import numpy as np

# bends
from c_bend_clip import BendClip

# nitride grating
from nathan.c_Vertical_Grating_Wg_SiN import NitrideGratingWg

# silicon grating
from nathan.Sidewall_Grating_Wg import SidewallGratingWg


# --------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------

# -------------------------------
# StraightGratingTestSite class
# -------------------------------
class StraightGratingTestSite(i3.PCell):
    """
        Draws a long, straight grating for testing

        this is for aim


        doesn't actually add the edge couplers... because that's too painful

        Layout properties/inputs:
            n_bend_pairs
    """

    # name prefix
    _name_prefix = 'STRAIGHT_GRATING_AIM'

    # ----------------
    # Layout
    class Layout(i3.LayoutView):


        # Properties -------

        # number of taper pairs
        # n_pairs = i3.IntProperty( default = 1, doc = 'number of taper pairs' )


        # grating types
        # 'one_sidewall', 'two_sidewalls', 'nitride_vertical_top', 'nitride_vertical_bottom',
        # 'nitride_one_sidewall_top', 'nitride_one_sidewall_bottom',
        grating_type = i3.StringProperty( default='', doc = 'flag for grating type')

        # inputs
        period      = i3.DefinitionProperty( default = 0.0, doc = 'period')
        duty_cycle  = i3.DefinitionProperty( default = 0.0, doc = 'duty cycle')
        grating_amp = i3.DefinitionProperty( default = 0.0, doc = 'grating amp')
        grat_wg_width    = i3.DefinitionProperty( default = 0.0, doc = 'waveguide width')
        length      = i3.DefinitionProperty( default = 0.0, doc = 'length')

        # Methods -------


        def _generate_instances(self, insts):
            # Generates a long ass row of gratings

            # serp_grating_layout = SerpGratingArray().get_default_view(i3.LayoutView)
            # serp_grating_layout.set( pitch              = 0.5,
            #                          grat_wg_width      = 6.5,
            #                          flyback_wg_width   = 6.5,
            #                          grating_amp        = grating_amps[i_row][i_col],
            #                          duty_cycle         = duty_cycle,
            #                          period             = period,
            #                          numrows            = numrows_tx,
            #                          grating_type       = grating_types[i_row][i_col],
            #                          length             = 100.0 )

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
                name=f'{self.name}edge_coupler_mmmmffff'
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

            # Hard code the tapers into here: (I hate hardcoding stuff, but no choice here)
            taper_length    = 79.0      # 79 is the best according to deniz' sims
            width_etch      = 4.0
            wg_width        = 0.5
            taper_swg_lay_1 = ParabolicTaper(
                name=f'{self.name}_TAPER_1'
            ).get_default_view(i3.LayoutView)

            taper_swg_lay_1.set(    length      = taper_length,
                                    width1      = wg_width,
                                    width2      = self.grat_wg_width,
                                    width_etch  = width_etch
                                )
            taper_swg_name_1 = f'{self.name}_TAPER_1'
            t = i3.vector_match_transform( taper_swg_lay_1.ports['left'],
                                           insts[ lin_taper_lay_name ].ports['out'] )
            insts += i3.SRef( name              = taper_swg_name_1,
                              reference         = taper_swg_lay_1,
                              transformation    = t,
                              flatten           = True )


            # add grating array
            # make grating layout
            swg_l_name = f'{self.name}_SWG'
            if self.grating_type == 'one_sidewall':
                # single sidewall grating
                swg_l = SidewallGratingWg( name = swg_l_name ).get_default_view(i3.LayoutView)
                swg_l.set(period=self.period, duty_cycle=self.duty_cycle, grating_amp=self.grating_amp, wg_width=self.grat_wg_width,
                          length=self.length, both_sides = False )

            elif self.grating_type == 'two_sidewalls':
                # double sidewall grating
                swg_l = SidewallGratingWg( name = swg_l_name ).get_default_view(i3.LayoutView)
                swg_l.set(period=self.period, duty_cycle=self.duty_cycle, grating_amp=self.grating_amp, wg_width=self.grat_wg_width,
                          length=self.length, both_sides = True )

            elif self.grating_type == 'nitride_vertical_top':
                # nitride vertical grating, top layer
                swg_l = NitrideGratingWg( name = swg_l_name ).get_default_view(i3.LayoutView)
                swg_l.set(period=self.period, duty_cycle=self.duty_cycle, grating_amp=self.grating_amp, wg_width=self.grat_wg_width,
                          length=self.length, grating_type='vertical', nitride_layer='top')

            elif self.grating_type == 'nitride_vertical_bottom':
                # nitride vertical grating, top layer
                swg_l = NitrideGratingWg( name = swg_l_name ).get_default_view(i3.LayoutView)
                swg_l.set(period=self.period, duty_cycle=self.duty_cycle, grating_amp=self.grating_amp, wg_width=self.grat_wg_width,
                          length=self.length, grating_type='vertical', nitride_layer='bottom')

            elif self.grating_type == 'nitride_one_sidewall_top':
                # nitride vertical grating, top layer
                swg_l = NitrideGratingWg( name = swg_l_name ).get_default_view(i3.LayoutView)
                swg_l.set(period=self.period, duty_cycle=self.duty_cycle, grating_amp=self.grating_amp, wg_width=self.grat_wg_width,
                          length=self.length, grating_type='one_sidewall', nitride_layer='top')

            elif self.grating_type == 'nitride_one_sidewall_bottom':
                # nitride vertical grating, top layer
                swg_l = NitrideGratingWg( name = swg_l_name ).get_default_view(i3.LayoutView)
                swg_l.set(period=self.period, duty_cycle=self.duty_cycle, grating_amp=self.grating_amp, wg_width=self.grat_wg_width,
                          length=self.length, grating_type='one_sidewall', nitride_layer='bottom')

            # end getting grating layout

            # add waveguide instance

            t = i3.vector_match_transform( swg_l.ports['in'],
                                           insts[taper_swg_name_1].ports['right'] )
            insts += i3.SRef( name              = swg_l_name,
                              reference         = swg_l,
                              transformation    = t,
                              flatten           = True )

            # add east coupler
            chip_port_east              = i3.OpticalPort(  position = ( chip_edge_east, 0.0 ),
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
            lin_taper_lay_name_east = f'{self.name}_EDGETAPER_EAST'
            insts += i3.SRef( name              = lin_taper_lay_name_east,
                              reference         = lin_taper_lay,
                              transformation    = t,
                              flatten           = True )


            # east taper
            taper_swg_lay_2 = ParabolicTaper(
                name=f'{self.name}_TAPER_2'
            ).get_default_view(i3.LayoutView)

            taper_swg_lay_2.set(    length      = taper_length,
                                    width1      = wg_width,
                                    width2      = self.grat_wg_width,
                                    width_etch  = width_etch
                                    )
            taper_swg_name_2 = f'{self.name}_TAPER_2'
            t = i3.vector_match_transform( taper_swg_lay_2.ports['left'],
                                           insts[ lin_taper_lay_name_east ].ports['out'],
                                           mirrored = True )
            insts += i3.SRef( name              = taper_swg_name_2,
                              reference         = taper_swg_lay_2,
                              transformation    = t,
                              flatten           = True )


            # connect with fat waveguide, which is just a sidewall grating with no amp
            connect_len     = insts[taper_swg_name_2].ports['right'].position[0] - insts[swg_l_name].ports['out'].position[0]
            fat_wg_l        = SidewallGratingWg().get_default_view(i3.LayoutView)
            fat_wg_l_name = f'{self.name}_FAT_WG_CON'
            fat_wg_l.set(period=self.period, duty_cycle=self.duty_cycle, grating_amp=0.0, wg_width=self.grat_wg_width,
                        length=connect_len, both_sides = False )
            t = i3.vector_match_transform( fat_wg_l.ports['in'],
                                           insts[swg_l_name].ports['out'] )
            insts += i3.SRef( name              = fat_wg_l_name,
                              reference         = fat_wg_l,
                              transformation    = t,
                              flatten           = True )



            return insts



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
                .ports['in']
                .position,
                angle=0.0,
            )


            return ports

        # end _generate_ports()

    # end class Layout()
    # ----------------

# end class StraightGratingTestSite()
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

    grating_type = 'nitride_one_sidewall_bottom'

    # inputs
    period          = 0.460
    duty_cycle      = period/2.0
    grating_amp     = 0.1
    grat_wg_width   = 6.5
    length          = 2000.0

    straight_grating_layout      = StraightGratingTestSite().Layout(    grating_type    = grating_type,
                                                                        period          = period,
                                                                        duty_cycle      = duty_cycle,
                                                                        grating_amp     = grating_amp,
                                                                        grat_wg_width   = grat_wg_width,
                                                                        length          = length
                                                                        )

    straight_grating_layout.write_gdsii('./gds/test_straight_grating_test_site.gds')

    print straight_grating_layout.ports


# end main