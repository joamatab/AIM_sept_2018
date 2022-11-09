"""
Taper clip pcell
author: bohan zhang
"""


# --------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------

# import my code path
# import sys
# sys.path.append( '../../' )

# from isipp50g import technology                 # TECH
from nathan import technology
import ipkiss3.all as i3                        # ipkiss
import inspect                                  # for inspecting methods of a class

# vector match transform
from ipkiss.geometry.vector import vector_match_transform

# taper
from bz.tapers.c_linear_taper import LinearTaper

# # IMEC PDK grating couplers
# from isipp50g.all import FGCCTE_FC1DC_625_313, \
#                             FGCCTE_FCWFC1DC_630_378, \
#                             FGCCTM_FC1DC_984_492

# taper pair row
from bz.taper_clips.c_taper_pair_row import TaperPairRow


# import interpolate frfom scipy
from scipy.interpolate import interp1d

# import numpy
import numpy as np

# import bezier
from hayk.bezier_curve import BezierCurve

# import aim waveguide template
from nathan.technology.WgTemplate import StripWgTemplate

# --------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------

# -------------------------------
# TaperClip class
# -------------------------------
class TaperClip(i3.PCell):
    """
        Draws a taper clip
        All units are in um (for now)

        AIM

        Layout properties/inputs:
            n_rows
            n_taper_pairs_per_row
            row_spacing
            connect_length
            pair_connect_length
            bot_gc_connect_length
            top_gc_connect_length
            bend_radius
            taper_prop_dict
                Dictionary of taper cell properties
                Properties = "length", "width1", "width2", "width_etch"

    """

    # name prefix
    _name_prefix = 'TAPER_CLIP'

    # ----------------
    # Layout
    class Layout(i3.LayoutView):


        # Properties -------

        # taper to draw
        taper_prop_dict = i3.DictProperty( default = {}, doc = 'Dictionary of taper cell properties.' + \
                                           'Properties = "length", "width1", "width2", "width_etch" ' )

        # number of rows
        n_rows                  = i3.IntProperty(default=3, doc='number of taper clip rows')

        # number of taper pairs per row
        n_taper_pairs_per_row   = i3.IntProperty(default=2, doc='number of taper clip pairs per row')

        # spacing between rows
        row_spacing             = i3.PositiveNumberProperty( default=0.0, doc='spacing between rows (midpoint to midpoint)' )

        # Taper pair properties
        connect_length          = i3.NumberProperty( default=0.0, doc='distance between tapers' )
        pair_connect_length     = i3.NumberProperty( default=0.0, doc='distance between taper pairs' )

        # input/output connection length
        bot_gc_connect_length   = i3.NumberProperty( default=0.0, doc='distance between grating and bottom taper' )
        top_gc_connect_length   = i3.NumberProperty( default=0.0, doc='distance between grating and top taper' )

        # radius of each arc
        bend_radius             = i3.PositiveNumberProperty( default=5.0, doc='spacing between rows (midpoint to midpoint)' )


        # Methods -------


        def _generate_instances(self, insts):
            # Generates taper clip

            # make my OWN custom waveguide trace template
            # wg_trace = f_MyIMECWaveguideTemplate(core_width=self.taper_prop_dict['width1'],
            #                                      cladding_width=self.taper_prop_dict['width1'] + 2.0 * self.taper_prop_dict['width_etch'])

            # make waveguide
            wg = i3.Waveguide(trace_template=StripWgTemplate(), name=f'{self.name}_WG')
            wg_round = i3.RoundedWaveguide(
                trace_template=StripWgTemplate(), name=f'{self.name}_WG_ROUND'
            )


            # how much to translate bends left/right
            # t_left = i3.Translation((self.bend_radius + (float(self.n_rows)/2.0) ))
            t_left  = i3.Translation((-2.5*self.bend_radius, 0.0))
            t_right = i3.Translation((2.5*self.bend_radius, 0.0))

            # draw taper pair rows
            for ii in range(self.n_rows):

                # add rows
                tp_rows_layout = TaperPairRow(
                    name=f'{self.name}_TProw{str(ii)}'
                ).get_default_view(i3.LayoutView)

                tp_rows_layout.set(
                                    taper_prop_dict     = self.taper_prop_dict,
                                    connect_length      = self.connect_length,
                                    pair_connect_length = self.pair_connect_length,
                                    n_pairs             = self.n_taper_pairs_per_row )

                # set translation
                t = i3.Translation( ( 0.0, float(ii) * self.row_spacing ) )

                # place taper pair row
                tp_row_name = f'{self.name}_TP_ROW{str(ii)}'
                insts       += i3.SRef( name=tp_row_name,
                                        reference=tp_rows_layout,
                                        transformation=t )

                # draw connecting arcs
                if ii > 0:

                        # bend on the right
                        # make shape bend
                    row_name = f'{self.name}_TP_ROW{str(ii - 1)}'
                    if (ii % 2) == 1:
                        shape_bend = i3.ShapeBend( start_point  = insts[ row_name ].ports['right'].position,
                                                   radius       = self.bend_radius,
                                                   start_angle  = -90.05,
                                                   end_angle    = 90.05,
                                                   angle_step   = 0.1 )

                        # add 180 deg bend
                        wg_copy = i3.Waveguide(
                            trace_template=StripWgTemplate(),
                            name=f'{self.name}_arc_r{str(ii)}',
                        )

                        arc_name = f'{self.name}_arc{str(ii)}'
                        insts += i3.SRef( name              = arc_name,
                                          reference         = wg_copy.Layout(shape=shape_bend),
                                          transformation    = t_right )

                        # connect bottom wgs

                        # get coords
                        in_port_coords = insts[arc_name].ports['in'].position
                        out_port_coords = insts[row_name].ports['right'].position

                        # draw bezier curve
                        bez = BezierCurve(N=100,
                                          P0=(in_port_coords[0] + 0.01, in_port_coords[1]),
                                          P1=(in_port_coords[0] - self.bend_radius / 2.0, in_port_coords[1]),
                                          P2=(out_port_coords[0] + self.bend_radius / 2.0, out_port_coords[1]),
                                          P3=(out_port_coords[0] - 0.01, out_port_coords[1]),
                                          R=(-self.bend_radius, +self.bend_radius),
                                          dy_dx=(0.0, -0.0))
                        bez_coords = bez.bezier_coords()

                        # make ipkiss shape
                        s = i3.Shape(bez_coords)

                        # add bottom wg connector
                        wg_copy = i3.Waveguide(
                            trace_template=StripWgTemplate(),
                            name=f'{self.name}_arc_r_con{str(ii)}',
                        )

                        insts += i3.SRef(
                            name=f'{self.name}_con_wg_r_b_{str(ii)}',
                            reference=wg_copy.Layout(shape=s),
                        )



                        # connect top wgs
                        next_row_name = f'{self.name}_TP_ROW{str(ii)}'
                        in_port_coords  = insts[arc_name].ports['out'].position
                        out_port_coords = insts[next_row_name].ports['right'].position

                        # draw bezier curve
                        bez = BezierCurve(   N = 500,
                                             P0 = (in_port_coords[0] + 0.01, in_port_coords[1]),
                                             P1 = (in_port_coords[0] - self.bend_radius/2.0, in_port_coords[1]),
                                             P2 = (out_port_coords[0] + self.bend_radius/2.0, out_port_coords[1]),
                                             P3 = (out_port_coords[0] - 0.01, out_port_coords[1]),
                                             R = (self.bend_radius, -self.bend_radius),
                                             dy_dx = (0.0, -0.0) )
                        bez_coords = bez.bezier_coords()

                        # make ipkiss shape
                        s = i3.Shape(bez_coords)

                        # add wg bend
                        wg_copy = i3.Waveguide(
                            trace_template=StripWgTemplate(),
                            name=f'{self.name}_bez_r{str(ii)}',
                        )

                        insts += i3.SRef(
                            name=f'{self.name}_con_wg_r_t_{str(ii)}',
                            reference=wg_copy.Layout(shape=s),
                        )



                    else:
                        shape_bend = i3.ShapeBend(
                            start_point     = (insts[row_name].ports['left'].position),
                            radius          = self.bend_radius,
                            start_angle     = 90.05,
                            end_angle       = -90.05,
                            angle_step      = 0.1,
                            clockwise       = False )

                        # add 180 deg bend
                        wg_copy = i3.Waveguide(
                            trace_template=StripWgTemplate(),
                            name=f'{self.name}_arc_l{str(ii)}',
                        )

                        arc_name = f'{self.name}_arc{str(ii)}'
                        insts += i3.SRef( name      = arc_name,
                                          reference = wg_copy.Layout(shape=shape_bend),
                                          transformation = t_left )

                        # connect bottom wgs

                        # get coords
                        in_port_coords = insts[arc_name].ports['out'].position
                        out_port_coords = insts[row_name].ports['left'].position

                        # draw bezier curve
                        bez = BezierCurve(N=100,
                                          P0=(in_port_coords[0] - 0.01, in_port_coords[1]),
                                          P1=(in_port_coords[0] + self.bend_radius / 2.0, in_port_coords[1]),
                                          P2=(out_port_coords[0] - self.bend_radius / 2.0, out_port_coords[1]),
                                          P3=(out_port_coords[0] + 0.01, out_port_coords[1]),
                                          R=(-self.bend_radius, +self.bend_radius),
                                          dy_dx=(0.0, -0.0))
                        bez_coords = bez.bezier_coords()

                        # make ipkiss shape
                        s = i3.Shape(bez_coords)

                        # add bottom wg connector
                        wg_copy = i3.Waveguide(
                            trace_template=StripWgTemplate(),
                            name=f'{self.name}_arc_l_con{str(ii)}',
                        )

                        insts += i3.SRef(
                            name=f'{self.name}_con_wg_l_b_{str(ii)}',
                            reference=wg_copy.Layout(shape=s),
                        )



                        # connect top wgs
                        next_row_name = f'{self.name}_TP_ROW{str(ii)}'
                        in_port_coords  = insts[arc_name].ports['in'].position
                        out_port_coords = insts[next_row_name].ports['left'].position

                        # draw bezier curve
                        bez = BezierCurve(   N = 500,
                                             P0 = (in_port_coords[0] - 0.01, in_port_coords[1]),
                                             P1 = (in_port_coords[0] + self.bend_radius/2.0, in_port_coords[1]),
                                             P2 = (out_port_coords[0] - self.bend_radius/2.0, out_port_coords[1]),
                                             P3 = (out_port_coords[0] + 0.01, out_port_coords[1]),
                                             R = (-self.bend_radius, +self.bend_radius),
                                             dy_dx = (0.0, -0.0) )
                        bez_coords = bez.bezier_coords()

                        # make ipkiss shape
                        s = i3.Shape(bez_coords)

                        # add wg bend
                        wg_copy = i3.Waveguide(
                            trace_template=StripWgTemplate(),
                            name=f'{self.name}_bez_l{str(ii)}',
                        )

                        insts += i3.SRef(
                            name=f'{self.name}_con_wg_l_t_{str(ii)}',
                            reference=wg_copy.Layout(shape=s),
                        )


                            # end if bend

                    # end drawing connecting arcs

            # end for ii in range(self.rows)



            # # connect the input grating
            # # pick grating layout to return
            # grating_layout = {
            #     'FGCCTE_FC1DC_625_313':     FGCCTE_FC1DC_625_313().Layout(),
            #     'FGCCTE_FCWFC1DC_630_378':  FGCCTE_FCWFC1DC_630_378().Layout(),
            #     'FGCCTM_FC1DC_984_492':     FGCCTM_FC1DC_984_492().Layout(),
            # }[self.grating_name]
            #
            #
            #
            # # place bottom grating
            # # always assuming bottom grating starts on the left
            # bot_grating_name = self.name+'_bot_grating'
            # t = i3.vector_match_transform( grating_layout.ports['waveguide'],
            #                                insts[self.name + '_TP_ROW0'].ports['left'] ) + \
            #     i3.Translation( ( -self.bot_gc_connect_length, 0.0 ) )
            #
            # insts += i3.SRef(   name            = bot_grating_name,
            #                     reference       = grating_layout,
            #                     transformation  = t )
            #
            # # connect bottom grating to taper
            # route_wg_bot = i3.RouteManhattan( input_port  = insts[bot_grating_name].ports['waveguide'],
            #                                   output_port = insts[self.name + '_TP_ROW0'].ports['left'] )
            #
            # # add wg
            # wg_bot = i3.Waveguide( trace_template = StripWgTemplate(), name = self.name + '_WG_BOT')
            # insts += i3.SRef(name=self.name + '_connect_wg_bot', reference=wg_bot.Layout(shape=route_wg_bot))
            #
            #
            #
            # # place top grating
            # top_grating_name = self.name + '_top_grating'
            # if (self.n_rows % 2) == 1:
            #     # even # of rows, output is to the right
            #     t = i3.vector_match_transform(  grating_layout.ports['waveguide'],
            #                                     insts[self.name + '_TP_ROW' + str(self.n_rows-1)].ports['right'],
            #                                     mirrored = True ) + \
            #         i3.Translation((self.top_gc_connect_length, 0.0))
            #
            #     insts += i3.SRef( name              = top_grating_name,
            #                       reference         = grating_layout,
            #                       transformation    = t)
            #
            #     # connect top grating to taper
            #     route_wg_top = i3.RouteManhattan(   input_port  = insts[top_grating_name].ports['waveguide'],
            #                                         output_port = insts[self.name + '_TP_ROW' + str(self.n_rows-1)].ports['right'])
            #
            #     # add wg
            #     wg_top = i3.Waveguide( trace_template = StripWgTemplate(), name = self.name + '_WG_TOP')
            #     insts += i3.SRef(name=self.name + '_connect_wg_top', reference=wg_top.Layout(shape=route_wg_top))
            #
            # else:
            #     # odd # of rows, output is to the left
            #     t = i3.vector_match_transform(  grating_layout.ports['waveguide'],
            #                                     insts[self.name + '_TP_ROW' + str(self.n_rows-1)].ports['left'],
            #                                     mirrored = False ) + \
            #         i3.Translation((-self.top_gc_connect_length, 0.0))
            #
            #     insts += i3.SRef( name              = top_grating_name,
            #                       reference         = grating_layout,
            #                       transformation    = t)
            #
            #     # connect top grating to taper
            #     route_wg_top = i3.RouteManhattan(   input_port  = insts[top_grating_name].ports['waveguide'],
            #                                         output_port = insts[self.name + '_TP_ROW' + str(self.n_rows-1)].ports['left'])
            #
            #     # add wg
            #     wg_top = i3.Waveguide( trace_template = StripWgTemplate(), name = self.name + '_WG_TOP')
            #     insts += i3.SRef(name=self.name + '_connect_wg_top', reference=wg_top.Layout(shape=route_wg_top))



            return insts
        # end _generate_instances()

    # end class Layout()
    # ----------------

# end class GratingCouplerRectUniformTaper()
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
    # lin_taper_layout = LinearTaper().Layout( length     = length,
    #                                          width1     = width1,
    #                                          width2     = width2,
    #                                          width_etch = width_etch)


    n_rows                  = 1
    n_taper_pairs_per_row   = 3
    row_spacing             = 14.0
    connect_length          = 0.0
    pair_connect_length     = 40.0
    bot_gc_connect_length   = 25.0
    top_gc_connect_length   = 25.0
    bend_radius             = 10.0

    taper_clip_layout = TaperClip().Layout(
                                            taper_prop_dict         = taper_prop_dict,
                                            n_rows                  = n_rows,
                                            n_taper_pairs_per_row   = n_taper_pairs_per_row,
                                            row_spacing             = row_spacing,
                                            connect_length          = connect_length,
                                            pair_connect_length     = pair_connect_length,
                                            bot_gc_connect_length   = bot_gc_connect_length,
                                            top_gc_connect_length   = top_gc_connect_length,
                                            bend_radius             = bend_radius )

    taper_clip_layout.write_gdsii('./gds/test_taper_clip.gds')


# end main