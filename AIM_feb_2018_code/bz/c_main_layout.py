"""
Main chip layout
This is where I'll route stuff
authors: bohan zhang
"""

# --------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------

# import my code path
# import sys
# sys.path.append( '../../' )

# import aim tech
import nathan.technology

# import ipkiss
import ipkiss3.all as i3                        # ipkiss

# import edge coupler
from c_edge_coupler import EdgeCoupler

# import serpentine grating
from nathan.Serp_Grating_Array import SerpGratingArray

# import aim waveguide template
from nathan.technology.WgTemplate import StripWgTemplate

# import nathan's linear taper
from nathan.Linear_Taper import LinearTaper

# import taper row
from taper_clips.c_taper_pair_row_w_edge_couplers import TaperPairRowEdgeCouplers

# import bend clip row
from c_bend_clip_w_edge_couplers import BendClipEdgeCouplers

# import time and start
import time

# straight grating test site
from c_straight_grating_test_site import StraightGratingTestSite




# --------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------

# -------------------------------
# MainChip class
# -------------------------------
class MainChip(i3.PCell):
    """
    Puts stuff on the main chip
    """

    _name_prefix = 'MAIN'


    # ----------------
    # Layout
    class Layout(i3.LayoutView):

        def _generate_instances(self, insts):
            """
            So i'm thinking:
            - have a list of edge coupler positions
            - have a list of serpentine grating cells
            """

            # main chip GDS
            fname = '../PDK_Library_Layout_GDS/ap_suny_v20a_chipframe.gds'
            main_chip_gds_cell = i3.GDSCell( filename=fname )

            # grab layout add to insts
            main_chip_gds_lay = main_chip_gds_cell.Layout()

            # add main chip layout
            insts += i3.SRef( name = self.name + '_CHIP',
                              reference = main_chip_gds_lay )

            # chip edge positioning
            chip_left_edge_pos  = main_chip_gds_lay.size_info().west
            chip_right_edge_pos = main_chip_gds_lay.size_info().east

            # edge coupler
            edge_coupler_gds_lay = EdgeCoupler(name='edge_coupler_si').Layout()

            # edge coupler dimensions
            edge_coupler_size_info  = edge_coupler_gds_lay.size_info()
            edge_coupler_height     = edge_coupler_size_info.height

            # v groove array pitch
            # spacing between RX and TX must be integer multiple of pitch
            fiber_array_pitch = 127.0
            n_pitches         = 18


            # -------------------------------
            # place serpentine grating arrays

            # Grating variants:
            # grating amplitudes, dimensions row x column
            grating_amps = [ [ 0.002, 0.01, 0.02, 0.04, 0.08, 0.2,  0.002, 0.005 ],
                             [ 0.01,  0.02, 0.04, 0.00, 0.01, 0.01, 0.05,  0.05 ] ]
            # grating types
            # 'one_sidewall', 'two_sidewalls', 'nitride_vertical_top', 'nitride_vertical_bottom',
            # 'nitride_one_sidewall_top', 'nitride_one_sidewall_bottom',
            grating_types = [ ['one_sidewall',  'one_sidewall',  'one_sidewall',  'one_sidewall',  'one_sidewall',         'one_sidewall',            'two_sidewalls',            'two_sidewalls' ],
                              ['two_sidewalls', 'two_sidewalls', 'two_sidewalls', 'two_sidewalls', 'nitride_vertical_top', 'nitride_vertical_bottom', 'nitride_one_sidewall_top', 'nitride_one_sidewall_bottom'] ]


            # settings
            tx_pitch            = 16.0
            rx_pitch            = 16.516
            grat_wg_width       = 6.5
            flyback_wg_width    = 6.5
            period              = 0.460
            duty_cycle          = period/2.0
            numrows_tx          = 32
            numrows_rx          = 31

            # number of rows and columns per Tx/Rx array of arrays
            n_serp_cell_rows    = 2
            n_serp_cell_cols    = 8

            # starting coordinates
            serp_grating_tx_start_pos = ( 550.0, 150.0 )

            # array coordinates/spacings
            col_spacing         = 600.0                                 # spacing between columns
            row_spacing         = fiber_array_pitch * 9.0               # spacing between rows
            row_offset          = 10.0 # 2.0 * edge_coupler_height             # additional row space for connecting waveguides to edge couplers

            # take a bend before entering/exiting
            bend_radius = 10.0

            # TX GRATING ARRAY
            print('Drawing TX grating array...')
            for i_row in range(n_serp_cell_rows):

                for i_col in range(n_serp_cell_cols):

                    serp_grating_layout = SerpGratingArray().get_default_view(i3.LayoutView)
                    serp_grating_layout.set( pitch              = tx_pitch,
                                             grat_wg_width      = grat_wg_width,
                                             flyback_wg_width   = flyback_wg_width,
                                             grating_amp        = grating_amps[i_row][i_col],
                                             duty_cycle         = duty_cycle,
                                             period             = period,
                                             numrows            = numrows_tx,
                                             grating_type       = grating_types[i_row][i_col] )

                    # place a serpentine grating
                    serp_grating_pos    = ( serp_grating_tx_start_pos[0] + col_spacing * float(i_col),
                                            serp_grating_tx_start_pos[1] + row_spacing * float(i_row) + float(n_serp_cell_cols - 1 - i_col)*row_offset )
                    serp_grating_name   = self.name + '_SERP_TX' + str(i_col) + str(i_row)
                    t                   = i3.Rotation( rotation = 90.0 ) + i3.HMirror()
                    insts += i3.SRef( name      = serp_grating_name,
                                      reference = serp_grating_layout,
                                      position  = serp_grating_pos,
                                      flatten   = True,
                                      transformation = t )



                    # add and route input/west edgecoupler
                    # position edge coupler on west side of chip
                    edge_coupler_west_y_pos     = insts[serp_grating_name].ports['in'].position[1] \
                                                  - float(n_serp_cell_cols - 1 - i_col)*row_offset \
                                                  + float(n_serp_cell_cols - 1 - i_col)*fiber_array_pitch \
                                                  + 2.0*bend_radius
                    chip_port_west              = i3.OpticalPort(  position = ( chip_left_edge_pos, edge_coupler_west_y_pos ), angle_deg = 0.0 )
                    edge_coupler_west_port      = edge_coupler_gds_lay.ports['out']
                    t                           = i3.vector_match_transform( edge_coupler_west_port, chip_port_west )
                    edge_coupler_west_name      = self.name + '_EDGE_COUPLER_WEST_TX' + str(i_col) + str(i_row)
                    insts += i3.SRef( name              = edge_coupler_west_name,
                                      reference         = edge_coupler_gds_lay,
                                      transformation    = t )


                    # add a small linear taper to go from 0.4 to 0.5um wg
                    lin_taper_lay = LinearTaper().get_default_view(i3.LayoutView)
                    lin_taper_lay.set( wg_width_in  = 0.4,
                                       wg_width_out = 0.5,
                                       length       = 10.0 )
                    t = i3.vector_match_transform(  lin_taper_lay.ports['in'],
                                                    insts[edge_coupler_west_name].ports['in'] )
                    lin_taper_lay_name = self.name + '_EDGETAPER_WEST_TX' + str(i_col) + str(i_row)
                    insts += i3.SRef( name              = lin_taper_lay_name,
                                      reference         = lin_taper_lay,
                                      transformation    = t,
                                      flatten           = True )


                    # route taper to first arc
                    start_pos_wg_taper_arc1 = ( insts[lin_taper_lay_name].ports['out'].position )
                    end_pos_wg_taper_arc1   = ( insts[lin_taper_lay_name].ports['out'].position[0] + bend_radius*float(n_serp_cell_cols - 1 - i_col) + 0.5,
                                                insts[lin_taper_lay_name].ports['out'].position[1]  )
                    route_wg_shape_taper_arc1 = i3.Shape([ start_pos_wg_taper_arc1, end_pos_wg_taper_arc1 ])
                    wg_name_taper_arc1       = self.name + '_WG_WEST_TAPER_ARC1_TX' + str(i_col) + str(i_row)
                    wg_lay_taper_arc1        = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_taper_arc1 ).get_default_view(i3.LayoutView)
                    wg_lay_taper_arc1.set( shape = route_wg_shape_taper_arc1 )
                    insts           += i3.SRef( name        = wg_name_taper_arc1,
                                                reference   = wg_lay_taper_arc1,
                                                flatten     = True )


                    # route wg to wg with arc
                    arc_center_1        = ( insts[wg_name_taper_arc1].ports['out'].position[0],
                                            insts[wg_name_taper_arc1].ports['out'].position[1] - bend_radius )
                    route_wg_shape_arc1 = i3.ShapeArc( radius       = bend_radius,
                                                       angle_step   = 1.0,
                                                       center       = arc_center_1,
                                                       start_angle  = 90.5,
                                                       end_angle    = -0.5,
                                                       closed       = False,
                                                       clockwise    = True )
                    wg_name_arc1    = self.name + '_WG_WEST_BEND1_TX' + str(i_col) + str(i_row)
                    wg_lay_arc1     = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc1 ).get_default_view(i3.LayoutView)
                    wg_lay_arc1.set( shape = route_wg_shape_arc1 )
                    insts           += i3.SRef( name        = wg_name_arc1,
                                                reference   = wg_lay_arc1,
                                                flatten     = True )


                    # route arc to arc with straight section
                    start_pos_wg_arc1_arc2  = ( insts[wg_name_arc1].ports['out'].position )
                    end_pos_wg_arc1_arc2    = ( insts[wg_name_arc1].ports['out'].position[0],
                                                insts[serp_grating_name].ports['in'].position[1]  )
                    route_wg_shape_arc1_arc2 = i3.Shape([ start_pos_wg_arc1_arc2, end_pos_wg_arc1_arc2 ])
                    wg_name_arc1_arc2       = self.name + '_WG_WEST_DOWN_TX' + str(i_col) + str(i_row)
                    wg_lay_arc1_arc2        = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc1_arc2 ).get_default_view(i3.LayoutView)
                    wg_lay_arc1_arc2.set( shape = route_wg_shape_arc1_arc2 )
                    insts           += i3.SRef( name        = wg_name_arc1_arc2,
                                                reference   = wg_lay_arc1_arc2,
                                                flatten     = True )


                    # route wg to wg with arc2
                    arc_center_2        = ( insts[wg_name_arc1_arc2].ports['out'].position[0] + bend_radius,
                                            insts[wg_name_arc1_arc2].ports['out'].position[1] )
                    route_wg_shape_arc2 = i3.ShapeArc( radius       = bend_radius,
                                                       angle_step   = 1.0,
                                                       center       = arc_center_2,
                                                       start_angle  = 179.5,
                                                       end_angle    = 270.5,
                                                       closed       = False,
                                                       clockwise    = False )
                    wg_name_arc2    = self.name + '_WG_WEST_BEND2_TX' + str(i_col) + str(i_row)
                    wg_lay_arc2     = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc2 ).get_default_view(i3.LayoutView)
                    wg_lay_arc2.set( shape = route_wg_shape_arc2 )
                    insts           += i3.SRef( name        = wg_name_arc2,
                                                reference   = wg_lay_arc2,
                                                flatten     = True )


                    # route wg to grating with arc3
                    arc_center_3        = ( insts[serp_grating_name].ports['in'].position[0] - bend_radius,
                                            insts[serp_grating_name].ports['in'].position[1] )
                    route_wg_shape_arc3 = i3.ShapeArc( radius       = bend_radius,
                                                       angle_step   = 1.0,
                                                       center       = arc_center_3,
                                                       start_angle  = -90.5,
                                                       end_angle    = 0.5,
                                                       closed       = False,
                                                       clockwise    = False )
                    wg_name_arc3    = self.name + '_WG_WEST_BEND_TX' + str(i_col) + str(i_row)
                    wg_lay_arc3     = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc3 ).get_default_view(i3.LayoutView)
                    wg_lay_arc3.set( shape = route_wg_shape_arc3 )
                    insts           += i3.SRef( name        = wg_name_arc3,
                                                reference   = wg_lay_arc3,
                                                flatten     = True )

                    # finish off arc2 to arc3 with wg
                    route_wg_shape_arc2_arc3      = i3.Shape([  insts[wg_name_arc2].ports['out'].position,
                                                                insts[wg_name_arc3].ports['in'].position ])
                    wg_name_arc2_arc3   = self.name + '_WG_WEST_ARC2_TO_ARC3_TX' + str(i_col) + str(i_row)
                    wg_lay_arc2_arc3    = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc2_arc3 ).get_default_view(i3.LayoutView)
                    wg_lay_arc2_arc3.set( shape = route_wg_shape_arc2_arc3 )
                    insts           += i3.SRef( name        = wg_name_arc2_arc3,
                                                reference   = wg_lay_arc2_arc3,
                                                flatten     = True )


                    # add and route output/east edgecoupler
                    # position edge coupler on east side of chip
                    edge_coupler_east_y_pos     = insts[serp_grating_name].ports['out'].position[1] \
                                                  - float(i_col)*fiber_array_pitch \
                                                  + float(i_col)*row_offset \
                                                  - 2.0 * bend_radius
                    chip_port                   = i3.OpticalPort(  position = ( chip_right_edge_pos, edge_coupler_east_y_pos ), angle_deg = 180.0 )
                    edge_coupler_east_port      = edge_coupler_gds_lay.ports['out']
                    t                           = i3.vector_match_transform( edge_coupler_east_port, chip_port, mirrored = True )
                    edge_coupler_east_name      = self.name + '_EDGE_COUPLER_EAST_TX' + str(i_col) + str(i_row)
                    insts += i3.SRef( name              = edge_coupler_east_name,
                                      reference         = edge_coupler_gds_lay,
                                      transformation    = t )


                    # add a small linear taper to go from 0.4 to 0.5um wg
                    lin_taper_east_lay = LinearTaper().get_default_view(i3.LayoutView)
                    lin_taper_east_lay.set( wg_width_in  = 0.4,
                                       wg_width_out = 0.5,
                                       length       = 10.0 )
                    t = i3.vector_match_transform(  lin_taper_east_lay.ports['in'],
                                                    insts[edge_coupler_east_name].ports['in'],
                                                    mirrored = True )
                    lin_taper_east_lay_name = self.name + '_EDGETAPER_EAST_TX' + str(i_col) + str(i_row)
                    insts += i3.SRef( name              = lin_taper_east_lay_name,
                                      reference         = lin_taper_east_lay,
                                      transformation    = t,
                                      flatten           = True )


                    # route taper to arc6
                    start_pos_wg_taper_arc6 = ( insts[lin_taper_east_lay_name].ports['out'].position )
                    end_pos_wg_taper_arc6   = ( insts[lin_taper_east_lay_name].ports['out'].position[0] - bend_radius*float(i_col) - 0.5,
                                                insts[lin_taper_east_lay_name].ports['out'].position[1]  )
                    route_wg_shape_taper_arc6 = i3.Shape([ start_pos_wg_taper_arc6, end_pos_wg_taper_arc6 ])
                    wg_name_taper_arc6       = self.name + '_WG_EAST_TAPER_ARC6_TX' + str(i_col) + str(i_row)
                    wg_lay_taper_arc6        = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_taper_arc6 ).get_default_view(i3.LayoutView)
                    wg_lay_taper_arc6.set( shape = route_wg_shape_taper_arc6 )
                    insts           += i3.SRef( name        = wg_name_taper_arc6,
                                                reference   = wg_lay_taper_arc6,
                                                flatten     = True )


                    # route arc6
                    arc_center_6        = ( insts[wg_name_taper_arc6].ports['out'].position[0],
                                            insts[wg_name_taper_arc6].ports['out'].position[1] + bend_radius )
                    route_wg_shape_arc6 = i3.ShapeArc( radius       = bend_radius,
                                                       angle_step   = 1.0,
                                                       center       = arc_center_6,
                                                       start_angle  = 270.5,
                                                       end_angle    = 179.5,
                                                       closed       = False,
                                                       clockwise    = True )
                    wg_name_arc6    = self.name + '_WG_EAST_BEND6_TX' + str(i_col) + str(i_row)
                    wg_lay_arc6     = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc6 ).get_default_view(i3.LayoutView)
                    wg_lay_arc6.set( shape = route_wg_shape_arc6 )
                    insts           += i3.SRef( name        = wg_name_arc6,
                                                reference   = wg_lay_arc6,
                                                flatten     = True )

                    # route arc6 to arc5 with straight section
                    start_pos_wg_arc6_arc5  = ( insts[wg_name_arc6].ports['out'].position )
                    end_pos_wg_arc6_arc5    = ( insts[wg_name_arc6].ports['out'].position[0],
                                                insts[serp_grating_name].ports['out'].position[1]  )
                    route_wg_shape_arc6_arc5 = i3.Shape([ start_pos_wg_arc6_arc5, end_pos_wg_arc6_arc5 ])
                    wg_name_arc6_arc5       = self.name + '_WG_EAST_UP_TX' + str(i_col) + str(i_row)
                    wg_lay_arc6_arc5        = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc6_arc5 ).get_default_view(i3.LayoutView)
                    wg_lay_arc6_arc5.set( shape = route_wg_shape_arc6_arc5 )
                    insts           += i3.SRef( name        = wg_name_arc6_arc5,
                                                reference   = wg_lay_arc6_arc5,
                                                flatten     = True )


                    # route wg to wg with arc5
                    arc_center_5        = ( insts[wg_name_arc6_arc5].ports['out'].position[0] - bend_radius,
                                            insts[wg_name_arc6_arc5].ports['out'].position[1] )
                    route_wg_shape_arc5 = i3.ShapeArc( radius       = bend_radius,
                                                       angle_step   = 1.0,
                                                       center       = arc_center_5,
                                                       start_angle  = -0.5,
                                                       end_angle    = 90.5,
                                                       closed       = False,
                                                       clockwise    = False )
                    wg_name_arc5    = self.name + '_WG_EAST_BEND5_TX' + str(i_col) + str(i_row)
                    wg_lay_arc5     = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc5 ).get_default_view(i3.LayoutView)
                    wg_lay_arc5.set( shape = route_wg_shape_arc5 )
                    insts           += i3.SRef( name        = wg_name_arc5,
                                                reference   = wg_lay_arc5,
                                                flatten     = True )


                    # route wg to grating output with arc4
                    arc_center_4        = ( insts[serp_grating_name].ports['out'].position[0] + bend_radius,
                                            insts[serp_grating_name].ports['out'].position[1] )
                    route_wg_shape_arc4 = i3.ShapeArc( radius       = bend_radius,
                                                       angle_step   = 1.0,
                                                       center       = arc_center_4,
                                                       start_angle  = 180.5,
                                                       end_angle    = 89.5,
                                                       closed       = False,
                                                       clockwise    = True )
                    wg_name_arc4    = self.name + '_WG_EAST_BEND4_TX' + str(i_col) + str(i_row)
                    wg_lay_arc4     = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc4 ).get_default_view(i3.LayoutView)
                    wg_lay_arc4.set( shape = route_wg_shape_arc4 )
                    insts           += i3.SRef( name        = wg_name_arc4,
                                                reference   = wg_lay_arc4,
                                                flatten     = True )


                    # finish off arc4 to arc5 with wg
                    route_wg_shape_arc4_arc5      = i3.Shape([  insts[wg_name_arc4].ports['out'].position,
                                                                insts[wg_name_arc5].ports['out'].position ])
                    wg_name_arc4_arc5   = self.name + '_WG_EAST_ARC4_TO_ARC5_TX' + str(i_col) + str(i_row)
                    wg_lay_arc4_arc5    = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc4_arc5 ).get_default_view(i3.LayoutView)
                    wg_lay_arc4_arc5.set( shape = route_wg_shape_arc4_arc5 )
                    insts           += i3.SRef( name        = wg_name_arc4_arc5,
                                                reference   = wg_lay_arc4_arc5,
                                                flatten     = True )

                # end for i col
            # end for i row
            # print('done')


            # -----------------------------------
            # RX GRATING ARRAY

            # starting coordinates
            serp_grating_rx_start_pos = ( serp_grating_tx_start_pos[0],
                                          serp_grating_tx_start_pos[1] + float(n_pitches)*fiber_array_pitch )

            print ''
            print('Drawing RX grating array...')
            for i_row in range(n_serp_cell_rows):

                for i_col in range(n_serp_cell_cols):

                    serp_grating_layout_rx = SerpGratingArray().get_default_view(i3.LayoutView)
                    serp_grating_layout_rx.set( pitch              = rx_pitch,
                                                grat_wg_width      = grat_wg_width,
                                                flyback_wg_width   = flyback_wg_width,
                                                grating_amp        = grating_amps[i_row][i_col],
                                                duty_cycle         = duty_cycle,
                                                period             = period,
                                                numrows            = numrows_rx,
                                                grating_type       = grating_types[i_row][i_col] )

                    # place a serpentine grating
                    serp_grating_pos_rx     = ( serp_grating_rx_start_pos[0] + col_spacing * float(i_col),
                                                serp_grating_rx_start_pos[1] + row_spacing * float(i_row) + float(n_serp_cell_cols - 1 - i_col)*row_offset )
                    serp_grating_name_rx    = self.name + '_SERP_RX' + str(i_col) + str(i_row)
                    t                       = i3.Rotation( rotation = 90.0 ) + i3.HMirror( )
                    insts += i3.SRef( name      = serp_grating_name_rx,
                                      reference = serp_grating_layout_rx,
                                      position  = serp_grating_pos_rx,
                                      flatten   = True,
                                      transformation = t )


                    # add and route input/west edgecoupler
                    # position edge coupler on west side of chip
                    edge_coupler_west_y_pos_rx  = insts[serp_grating_name_rx].ports['in'].position[1] \
                                                  - float(n_serp_cell_cols - 1 - i_col)*row_offset \
                                                  + float(n_serp_cell_cols - 1 - i_col)*fiber_array_pitch \
                                                  + 2.0 * bend_radius
                    chip_port_west_rx           = i3.OpticalPort(  position = ( chip_left_edge_pos, edge_coupler_west_y_pos_rx ), angle_deg = 0.0 )
                    edge_coupler_west_port_rx   = edge_coupler_gds_lay.ports['out']
                    t                           = i3.vector_match_transform( edge_coupler_west_port_rx, chip_port_west_rx )
                    edge_coupler_west_name_rx           = self.name + '_EDGE_COUPLER_WEST_RX' + str(i_col) + str(i_row)
                    insts += i3.SRef( name              = edge_coupler_west_name_rx,
                                      reference         = edge_coupler_gds_lay,
                                      transformation    = t )


                    # add a small linear taper to go from 0.4 to 0.5um wg
                    lin_taper_lay_rx = LinearTaper().get_default_view(i3.LayoutView)
                    lin_taper_lay_rx.set(   wg_width_in  = 0.4,
                                            wg_width_out = 0.5,
                                            length       = 10.0 )
                    t = i3.vector_match_transform(  lin_taper_lay_rx.ports['in'],
                                                    insts[edge_coupler_west_name_rx].ports['in'] )
                    lin_taper_lay_name_rx = self.name + '_EDGETAPER_WEST_RX' + str(i_col) + str(i_row)
                    insts += i3.SRef( name              = lin_taper_lay_name_rx,
                                      reference         = lin_taper_lay_rx,
                                      transformation    = t,
                                      flatten           = True )


                    # route taper to first arc
                    start_pos_wg_taper_arc1_rx = ( insts[lin_taper_lay_name_rx].ports['out'].position )
                    end_pos_wg_taper_arc1_rx   = ( insts[lin_taper_lay_name_rx].ports['out'].position[0] + bend_radius*float(n_serp_cell_cols - 1 - i_col) + 0.5,
                                                insts[lin_taper_lay_name_rx].ports['out'].position[1]  )
                    route_wg_shape_taper_arc1_rx = i3.Shape([ start_pos_wg_taper_arc1_rx, end_pos_wg_taper_arc1_rx ])
                    wg_name_taper_arc1_rx       = self.name + '_WG_WEST_TAPER_ARC1_RX' + str(i_col) + str(i_row)
                    wg_lay_taper_arc1_rx        = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_taper_arc1_rx ).get_default_view(i3.LayoutView)
                    wg_lay_taper_arc1_rx.set( shape = route_wg_shape_taper_arc1_rx )
                    insts           += i3.SRef( name        = wg_name_taper_arc1_rx,
                                                reference   = wg_lay_taper_arc1_rx,
                                                flatten     = True )


                    # route wg to wg with arc
                    arc_center_1_rx     = ( insts[wg_name_taper_arc1_rx].ports['out'].position[0],
                                            insts[wg_name_taper_arc1_rx].ports['out'].position[1] - bend_radius )
                    route_wg_shape_arc1_rx  = i3.ShapeArc(  radius       = bend_radius,
                                                            angle_step   = 1.0,
                                                            center       = arc_center_1_rx,
                                                            start_angle  = 90.5,
                                                            end_angle    = -0.5,
                                                            closed       = False,
                                                            clockwise    = True )
                    wg_name_arc1_rx    = self.name + '_WG_WEST_BEND1_RX' + str(i_col) + str(i_row)
                    wg_lay_arc1_rx     = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc1_rx ).get_default_view(i3.LayoutView)
                    wg_lay_arc1_rx.set( shape = route_wg_shape_arc1_rx )
                    insts           += i3.SRef( name        = wg_name_arc1_rx,
                                                reference   = wg_lay_arc1_rx,
                                                flatten     = True )


                    # route arc to arc with straight section
                    start_pos_wg_arc1_arc2_rx   = ( insts[wg_name_arc1_rx].ports['out'].position )
                    end_pos_wg_arc1_arc2_rx     = ( insts[wg_name_arc1_rx].ports['out'].position[0],
                                                    insts[serp_grating_name_rx].ports['in'].position[1]  )
                    route_wg_shape_arc1_arc2_rx = i3.Shape([ start_pos_wg_arc1_arc2_rx, end_pos_wg_arc1_arc2_rx ])
                    wg_name_arc1_arc2_rx        = self.name + '_WG_WEST_DOWN_RX' + str(i_col) + str(i_row)
                    wg_lay_arc1_arc2_rx         = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc1_arc2_rx ).get_default_view(i3.LayoutView)
                    wg_lay_arc1_arc2_rx.set( shape = route_wg_shape_arc1_arc2_rx )
                    insts           += i3.SRef( name        = wg_name_arc1_arc2_rx,
                                                reference   = wg_lay_arc1_arc2_rx,
                                                flatten     = True )


                    # route wg to wg with arc2
                    arc_center_2_rx         = ( insts[wg_name_arc1_arc2_rx].ports['out'].position[0] + bend_radius,
                                                insts[wg_name_arc1_arc2_rx].ports['out'].position[1] )
                    route_wg_shape_arc2_rx  = i3.ShapeArc( radius       = bend_radius,
                                                           angle_step   = 1.0,
                                                           center       = arc_center_2_rx,
                                                           start_angle  = 179.5,
                                                           end_angle    = 270.5,
                                                           closed       = False,
                                                           clockwise    = False )
                    wg_name_arc2_rx     = self.name + '_WG_WEST_BEND2_RX' + str(i_col) + str(i_row)
                    wg_lay_arc2_rx      = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc2_rx ).get_default_view(i3.LayoutView)
                    wg_lay_arc2_rx.set( shape = route_wg_shape_arc2_rx )
                    insts           += i3.SRef( name        = wg_name_arc2_rx,
                                                reference   = wg_lay_arc2_rx,
                                                flatten     = True )


                    # route wg to grating with arc3
                    arc_center_3_rx        = (  insts[serp_grating_name_rx].ports['in'].position[0] - bend_radius,
                                                insts[serp_grating_name_rx].ports['in'].position[1] )
                    route_wg_shape_arc3_rx = i3.ShapeArc( radius       = bend_radius,
                                                       angle_step   = 1.0,
                                                       center       = arc_center_3_rx,
                                                       start_angle  = -90.5,
                                                       end_angle    = 0.5,
                                                       closed       = False,
                                                       clockwise    = False )
                    wg_name_arc3_rx    = self.name + '_WG_WEST_BEND_RX' + str(i_col) + str(i_row)
                    wg_lay_arc3_rx     = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc3_rx ).get_default_view(i3.LayoutView)
                    wg_lay_arc3_rx.set( shape = route_wg_shape_arc3_rx )
                    insts           += i3.SRef( name        = wg_name_arc3_rx,
                                                reference   = wg_lay_arc3_rx,
                                                flatten     = True )

                    # finish off arc2 to arc3 with wg
                    route_wg_shape_arc2_arc3_rx      = i3.Shape([   insts[wg_name_arc2_rx].ports['out'].position,
                                                                    insts[wg_name_arc3_rx].ports['in'].position ])
                    wg_name_arc2_arc3_rx   = self.name + '_WG_WEST_ARC2_TO_ARC3_RX' + str(i_col) + str(i_row)
                    wg_lay_arc2_arc3_rx    = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc2_arc3_rx ).get_default_view(i3.LayoutView)
                    wg_lay_arc2_arc3_rx.set( shape = route_wg_shape_arc2_arc3_rx )
                    insts           += i3.SRef( name        = wg_name_arc2_arc3_rx,
                                                reference   = wg_lay_arc2_arc3_rx,
                                                flatten     = True )


                    # add and route output/east edgecoupler
                    # position edge coupler on east side of chip
                    edge_coupler_east_y_pos_rx  = insts[serp_grating_name_rx].ports['out'].position[1] \
                                                  - float(i_col)*fiber_array_pitch \
                                                  + float(i_col)*row_offset \
                                                  - 2.0 * bend_radius
                    chip_port                   = i3.OpticalPort(  position = ( chip_right_edge_pos, edge_coupler_east_y_pos_rx ), angle_deg = 180.0 )
                    edge_coupler_east_port_rx   = edge_coupler_gds_lay.ports['out']
                    t                           = i3.vector_match_transform( edge_coupler_east_port_rx, chip_port, mirrored = True )
                    edge_coupler_east_name_rx   = self.name + '_EDGE_COUPLER_EAST_RX' + str(i_col) + str(i_row)
                    insts += i3.SRef( name              = edge_coupler_east_name_rx,
                                      reference         = edge_coupler_gds_lay,
                                      transformation    = t )


                    # add a small linear taper to go from 0.4 to 0.5um wg
                    lin_taper_east_lay_rx = LinearTaper().get_default_view(i3.LayoutView)
                    lin_taper_east_lay_rx.set( wg_width_in  = 0.4,
                                               wg_width_out = 0.5,
                                               length       = 10.0 )
                    t = i3.vector_match_transform(  lin_taper_east_lay_rx.ports['in'],
                                                    insts[edge_coupler_east_name_rx].ports['in'],
                                                    mirrored = True )
                    lin_taper_east_lay_name_rx = self.name + '_EDGETAPER_EAST_RX' + str(i_col) + str(i_row)
                    insts += i3.SRef( name              = lin_taper_east_lay_name_rx,
                                      reference         = lin_taper_east_lay_rx,
                                      transformation    = t,
                                      flatten           = True )


                    # route taper to arc6
                    start_pos_wg_taper_arc6_rx = (  insts[lin_taper_east_lay_name_rx].ports['out'].position )
                    end_pos_wg_taper_arc6_rx   = (  insts[lin_taper_east_lay_name_rx].ports['out'].position[0] - bend_radius*float(i_col) - 0.5,
                                                    insts[lin_taper_east_lay_name_rx].ports['out'].position[1]  )
                    route_wg_shape_taper_arc6_rx = i3.Shape([ start_pos_wg_taper_arc6_rx, end_pos_wg_taper_arc6_rx ])
                    wg_name_taper_arc6_rx       = self.name + '_WG_EAST_TAPER_ARC6_RX' + str(i_col) + str(i_row)
                    wg_lay_taper_arc6_rx        = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_taper_arc6_rx ).get_default_view(i3.LayoutView)
                    wg_lay_taper_arc6_rx.set( shape = route_wg_shape_taper_arc6_rx )
                    insts           += i3.SRef( name        = wg_name_taper_arc6_rx,
                                                reference   = wg_lay_taper_arc6_rx,
                                                flatten     = True )


                    # route arc6
                    arc_center_6_rx     = ( insts[wg_name_taper_arc6_rx].ports['out'].position[0],
                                            insts[wg_name_taper_arc6_rx].ports['out'].position[1] + bend_radius )
                    route_wg_shape_arc6_rx = i3.ShapeArc( radius       = bend_radius,
                                                       angle_step   = 1.0,
                                                       center       = arc_center_6_rx,
                                                       start_angle  = 270.5,
                                                       end_angle    = 179.5,
                                                       closed       = False,
                                                       clockwise    = True )
                    wg_name_arc6_rx     = self.name + '_WG_EAST_BEND6_RX' + str(i_col) + str(i_row)
                    wg_lay_arc6_rx      = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc6_rx ).get_default_view(i3.LayoutView)
                    wg_lay_arc6_rx.set( shape = route_wg_shape_arc6_rx )
                    insts           += i3.SRef( name        = wg_name_arc6_rx,
                                                reference   = wg_lay_arc6_rx,
                                                flatten     = True )

                    # route arc6 to arc5 with straight section
                    start_pos_wg_arc6_arc5_rx  = ( insts[wg_name_arc6_rx].ports['out'].position )
                    end_pos_wg_arc6_arc5_rx    = (  insts[wg_name_arc6_rx].ports['out'].position[0],
                                                    insts[serp_grating_name_rx].ports['out'].position[1]  )
                    route_wg_shape_arc6_arc5_rx = i3.Shape([ start_pos_wg_arc6_arc5_rx, end_pos_wg_arc6_arc5_rx ])
                    wg_name_arc6_arc5_rx       = self.name + '_WG_EAST_UP_RX' + str(i_col) + str(i_row)
                    wg_lay_arc6_arc5_rx        = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc6_arc5_rx ).get_default_view(i3.LayoutView)
                    wg_lay_arc6_arc5_rx.set( shape = route_wg_shape_arc6_arc5_rx )
                    insts           += i3.SRef( name        = wg_name_arc6_arc5_rx,
                                                reference   = wg_lay_arc6_arc5_rx,
                                                flatten     = True )


                    # route wg to wg with arc5
                    arc_center_5_rx     = ( insts[wg_name_arc6_arc5_rx].ports['out'].position[0] - bend_radius,
                                            insts[wg_name_arc6_arc5_rx].ports['out'].position[1] )
                    route_wg_shape_arc5_rx = i3.ShapeArc( radius       = bend_radius,
                                                       angle_step   = 1.0,
                                                       center       = arc_center_5_rx,
                                                       start_angle  = -0.5,
                                                       end_angle    = 90.5,
                                                       closed       = False,
                                                       clockwise    = False )
                    wg_name_arc5_rx    = self.name + '_WG_EAST_BEND5_RX' + str(i_col) + str(i_row)
                    wg_lay_arc5_rx     = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc5_rx ).get_default_view(i3.LayoutView)
                    wg_lay_arc5_rx.set( shape = route_wg_shape_arc5_rx )
                    insts           += i3.SRef( name        = wg_name_arc5_rx,
                                                reference   = wg_lay_arc5_rx,
                                                flatten     = True )


                    # route wg to grating output with arc4
                    arc_center_4_rx     = ( insts[serp_grating_name_rx].ports['out'].position[0] + bend_radius,
                                            insts[serp_grating_name_rx].ports['out'].position[1] )
                    route_wg_shape_arc4_rx = i3.ShapeArc( radius       = bend_radius,
                                                       angle_step   = 1.0,
                                                       center       = arc_center_4_rx,
                                                       start_angle  = 180.5,
                                                       end_angle    = 89.5,
                                                       closed       = False,
                                                       clockwise    = True )
                    wg_name_arc4_rx    = self.name + '_WG_EAST_BEND4_RX' + str(i_col) + str(i_row)
                    wg_lay_arc4_rx     = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc4_rx ).get_default_view(i3.LayoutView)
                    wg_lay_arc4_rx.set( shape = route_wg_shape_arc4_rx )
                    insts           += i3.SRef( name        = wg_name_arc4_rx,
                                                reference   = wg_lay_arc4_rx,
                                                flatten     = True )


                    # finish off arc4 to arc5 with wg
                    route_wg_shape_arc4_arc5_rx      = i3.Shape([  insts[wg_name_arc4_rx].ports['out'].position,
                                                                insts[wg_name_arc5_rx].ports['out'].position ])
                    wg_name_arc4_arc5_rx   = self.name + '_WG_EAST_ARC4_TO_ARC5_RX' + str(i_col) + str(i_row)
                    wg_lay_arc4_arc5_rx    = i3.Waveguide( trace_template = StripWgTemplate(), name = wg_name_arc4_arc5_rx ).get_default_view(i3.LayoutView)
                    wg_lay_arc4_arc5_rx.set( shape = route_wg_shape_arc4_arc5_rx )
                    insts           += i3.SRef( name        = wg_name_arc4_arc5_rx,
                                                reference   = wg_lay_arc4_arc5_rx,
                                                flatten     = True )

                # end for i col
            # end for i row
            # print('done')



            # -----------------------------------------------------
            # Taper clips!!!!@!@!@!

            # taper clip position
            taper_clip_y_pos_list = [ 1120.0, 1150.0, 1180.0 ]

            # taper clip pairs
            taper_clip_pairs_list = [ 10, 20, 30 ]

            for n_pairs, taper_clip_y_pos in zip( taper_clip_pairs_list, taper_clip_y_pos_list ):

                # make taper clip row
                taper_clip_row_30_lay = TaperPairRowEdgeCouplers().get_default_view(i3.LayoutView)
                taper_clip_row_30_lay.set( n_pairs = n_pairs )

                # add and route input/west edgecoupler
                chip_port_west              = i3.OpticalPort(  position = ( chip_left_edge_pos, taper_clip_y_pos ), angle_deg = 0.0 )
                edge_coupler_out_port       = edge_coupler_gds_lay.ports['out']
                t                           = i3.vector_match_transform( edge_coupler_out_port, chip_port_west )
                edge_coupler_west_name      = self.name + '_EDGE_COUPLER_WEST_TC' + str(n_pairs)
                insts += i3.SRef(   name              = edge_coupler_west_name,
                                    reference         = edge_coupler_gds_lay,
                                    transformation    = t,
                                    flatten           = False )

                # add taper clip row
                t       = i3.vector_match_transform( taper_clip_row_30_lay.ports['left'], insts[edge_coupler_west_name].ports['in']  )
                insts   += i3.SRef( name              = self.name + '_TAPER_CLIP' + str(n_pairs),
                                    reference         = taper_clip_row_30_lay,
                                    transformation    = t,
                                    flatten           = True )

                # add and route output/east edgecoupler
                chip_port_east              = i3.OpticalPort(  position = ( chip_right_edge_pos, taper_clip_y_pos ), angle_deg = 180.0 )
                edge_coupler_out_port       = edge_coupler_gds_lay.ports['out']
                t                           = i3.vector_match_transform( edge_coupler_out_port, chip_port_east, mirrored = True )
                edge_coupler_east_name      = self.name + '_EDGE_COUPLER_EAST_TC' + str(n_pairs)
                insts += i3.SRef(   name              = edge_coupler_east_name,
                                    reference         = edge_coupler_gds_lay,
                                    transformation    = t,
                                    flatten           = False )
            # end generating taper clips


            # -----------------------------------------------------
            # Taper clips!!!!@!@!@!

            # taper clip position
            taper_clip_y_pos_list = [ 1120.0, 1150.0, 1180.0 ]

            # taper clip pairs
            taper_clip_pairs_list = [ 10, 20, 30 ]

            for n_pairs, taper_clip_y_pos in zip( taper_clip_pairs_list, taper_clip_y_pos_list ):

                # make taper clip row
                taper_clip_row_lay = TaperPairRowEdgeCouplers().get_default_view(i3.LayoutView)
                taper_clip_row_lay.set( n_pairs = n_pairs )

                # add and route input/west edgecoupler
                chip_port_west              = i3.OpticalPort(  position = ( chip_left_edge_pos, taper_clip_y_pos ), angle_deg = 0.0 )
                edge_coupler_out_port       = edge_coupler_gds_lay.ports['out']
                t                           = i3.vector_match_transform( edge_coupler_out_port, chip_port_west )
                edge_coupler_west_name      = self.name + '_EDGE_COUPLER_WEST_TC_PAIRS' + str(n_pairs)
                insts += i3.SRef(   name              = edge_coupler_west_name,
                                    reference         = edge_coupler_gds_lay,
                                    transformation    = t,
                                    flatten           = False )

                # add taper clip row
                t       = i3.vector_match_transform( taper_clip_row_lay.ports['left'], insts[edge_coupler_west_name].ports['in']  )
                insts   += i3.SRef( name              = self.name + '_TAPER_CLIP_PAIRS' + str(n_pairs),
                                    reference         = taper_clip_row_lay,
                                    transformation    = t,
                                    flatten           = True )

                # add and route output/east edgecoupler
                chip_port_east              = i3.OpticalPort(  position = ( chip_right_edge_pos, taper_clip_y_pos ), angle_deg = 180.0 )
                edge_coupler_out_port       = edge_coupler_gds_lay.ports['out']
                t                           = i3.vector_match_transform( edge_coupler_out_port, chip_port_east, mirrored = True )
                edge_coupler_east_name      = self.name + '_EDGE_COUPLER_EAST_TC_PAIRS' + str(n_pairs)
                insts += i3.SRef(   name              = edge_coupler_east_name,
                                    reference         = edge_coupler_gds_lay,
                                    transformation    = t,
                                    flatten           = False )
            # end generating taper clips

            # -----------------------------------------------------
            # BEND clips!!!!@!@!@!

            # bend clip positions
            bend_clip_y_pos_list = [ 2260.0, 2288.0, 2314.0 ]

            # bend clip pairs
            bend_clip_pairs_list = [ 106, 212, 318 ]

            for n_pairs_bc, bend_clip_y_pos in zip( bend_clip_pairs_list, bend_clip_y_pos_list ):

                # make bend clip row
                bend_clip_row_lay = BendClipEdgeCouplers().get_default_view(i3.LayoutView)
                bend_clip_row_lay.set( n_pairs = n_pairs_bc )

                # add and route input/west edgecoupler
                chip_port_west              = i3.OpticalPort(  position = ( chip_left_edge_pos, bend_clip_y_pos ), angle_deg = 0.0 )
                edge_coupler_out_port       = edge_coupler_gds_lay.ports['out']
                t                           = i3.vector_match_transform( edge_coupler_out_port, chip_port_west )
                edge_coupler_west_name_bc   = self.name + '_EDGE_COUPLER_WEST_BC' + str(n_pairs_bc)
                insts += i3.SRef(   name              = edge_coupler_west_name_bc,
                                    reference         = edge_coupler_gds_lay,
                                    transformation    = t,
                                    flatten           = False )

                # add bend clip row
                bend_clip_name = self.name + '_BEND_CLIP' + str(n_pairs_bc)
                t       = i3.vector_match_transform( bend_clip_row_lay.ports['in'], insts[edge_coupler_west_name_bc].ports['in']  )
                insts   += i3.SRef( name              = bend_clip_name,
                                    reference         = bend_clip_row_lay,
                                    transformation    = t,
                                    flatten           = True )

                # add and route output/east edgecoupler
                chip_port_east              = i3.OpticalPort(  position = ( chip_right_edge_pos, insts[bend_clip_name].ports['out'].position[1] ),
                                                               angle_deg = 180.0 )
                edge_coupler_out_port       = edge_coupler_gds_lay.ports['out']
                t                           = i3.vector_match_transform( edge_coupler_out_port, chip_port_east, mirrored = True )
                edge_coupler_east_name_bc   = self.name + '_EDGE_COUPLER_EAST_BC' + str(n_pairs_bc)
                insts += i3.SRef(   name              = edge_coupler_east_name_bc,
                                    reference         = edge_coupler_gds_lay,
                                    transformation    = t,
                                    flatten           = False )
            # end generating bend clips


            # -----------------------------------------------------
            # Straight gratings + straight wg

            # y pos
            pos_2_list = [ 4555.0 + float(ii)*30.0 for ii in range(13) ]
            straight_grating_y_pos_list = [ 3412.0,
                                            3437.0,
                                            3468.0
                                            ] + pos_2_list

            # DEBUG
            # straight_grating_y_pos_list = [ 4555.0 ]

            # variants?
            straight_grating_type_list  = sum( grating_types, [] )
            straight_grating_amp_list   = sum( grating_amps, [])
            # # DEBUG
            # straight_grating_type_list  = [ 'one_sidewall']
            # straight_grating_amp_list   = [ 0.1 ]
            straight_grating_len        = 5000.0

            print straight_grating_y_pos_list
            print straight_grating_amp_list
            print straight_grating_type_list

            i_sg = 0

            for straight_grating_type, straight_grating_amp, straight_grating_y_pos \
                    in zip( straight_grating_type_list, straight_grating_amp_list, straight_grating_y_pos_list ):

                # make straight grating row
                sg_name = self.name + '_STRAIGHT_GRATING' + str(i_sg)
                straight_grating_layout = StraightGratingTestSite( name = sg_name ).get_default_view(i3.LayoutView)
                straight_grating_layout.set(    grating_type    = straight_grating_type,
                                                period          = period,
                                                duty_cycle      = duty_cycle,
                                                grating_amp     = straight_grating_amp,
                                                grat_wg_width   = 6.5,
                                                length          = straight_grating_len
                                            )

                # add and route input/west edgecoupler
                chip_port_west              = i3.OpticalPort(  position = ( chip_left_edge_pos, straight_grating_y_pos ), angle_deg = 0.0 )
                edge_coupler_out_port       = edge_coupler_gds_lay.ports['out']
                t                           = i3.vector_match_transform( edge_coupler_out_port, chip_port_west )
                edge_coupler_west_name_sg   = self.name + '_EDGE_COUPLER_WEST_SG' + str(i_sg)
                insts += i3.SRef(   name              = edge_coupler_west_name_sg,
                                    reference         = edge_coupler_gds_lay,
                                    transformation    = t,
                                    flatten           = False )

                # add straight grating row
                # sg_name = self.name + '_STRAIGHT_GRATING' + str(i_sg)
                t       = i3.vector_match_transform( straight_grating_layout.ports['in'], insts[edge_coupler_west_name_sg].ports['in']  )
                insts   += i3.SRef( name              = sg_name,
                                    reference         = straight_grating_layout,
                                    transformation    = t,
                                    flatten           = True )

                # add and route output/east edgecoupler
                chip_port_east              = i3.OpticalPort(  position = ( chip_right_edge_pos, insts[sg_name].ports['out'].position[1] ),
                                                               angle_deg = 180.0 )
                edge_coupler_out_port       = edge_coupler_gds_lay.ports['out']
                t                           = i3.vector_match_transform( edge_coupler_out_port, chip_port_east, mirrored = True )
                edge_coupler_east_name_sg   = self.name + '_EDGE_COUPLER_EAST_SG' + str(i_sg)
                insts += i3.SRef(   name              = edge_coupler_east_name_sg,
                                    reference         = edge_coupler_gds_lay,
                                    transformation    = t,
                                    flatten           = False )

                i_sg += 1

            # end generating straight gratings




            return insts

        # end _generate_instances()



    # end layout

# end class MainChip




# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

if __name__ == '__main__':

    print('hi')

    # # test drawing one of nathan's waveguides
    # from layout.nathan.Sidewall_Grating_Wg import SidewallGratingWg
    #
    # test_l = SidewallGratingWg().Layout()
    # for port in test_l.ports:
    #     print port.name
    # # test_l.visualize()
    #
    # test_l.write_gdsii("test_sidewall_grating_wg.gds")

    start = time.time()

    # load and save main chip
    chip = MainChip().Layout()

    # print('debug')

    # print chip.instances[ chip.name + '_test_serp' ].ports

    chip.write_gdsii('./gds/bz_main_chip.gds')

    # print stop time
    print( time.time() - start )