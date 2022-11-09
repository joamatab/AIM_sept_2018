"""
Makes an array of taper clips

Maybe hard code to draw 3, 6, 9 pairs?

"""


# --------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------

# import my code path
# import sys
# sys.path.append( '../../' )

from isipp50g import technology                 # TECH
import ipkiss3.all as i3                        # ipkiss
import inspect                                  # for inspecting methods of a class

# vector match transform
from ipkiss.geometry.vector import vector_match_transform

# taper
from tapers.c_linear_taper import LinearTaper
from tapers.c_parabolic_taper import ParabolicTaper

# IMEC PDK grating couplers
from isipp50g.all import FGCCTE_FC1DC_625_313, \
                            FGCCTE_FCWFC1DC_630_378, \
                            FGCCTM_FC1DC_984_492

# taper pair row
from taper_clips.c_taper_pair_row import TaperPairRow

# MY IMEC waveguide template
from gratings.waveguide_traces import f_MyIMECWaveguideTemplate

# import interpolate frfom scipy
from scipy.interpolate import interp1d

# import numpy
import numpy as np

# import bezier
from hayk.bezier_curve import BezierCurve

# import taper clip
from c_taper_clip import TaperClip

# --------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------

# -------------------------------
# TaperClipArray class
# -------------------------------
class TaperClipArray(i3.PCell):
    """
        Draws a taper clip array
        All units are in um

        Layout properties/inputs:

    """

    # name prefix
    _name_prefix = 'TAPER_CLIP'

    # ----------------
    # Layout
    class Layout(i3.LayoutView):


        # Properties -------

        taper_prop_dict = i3.DictProperty( default = {}, doc = 'Dictionary of taper cell properties.' + \
                                           'Properties = "length", "width1", "width2", "width_etch" ' )

        # Methods -------


        def _generate_instances(self, insts):
            # Generates taper clip


            # taper clip defaults
            n_rows                  = 3
            n_taper_pairs_per_row   = [ 1, 3, 5 ]
            row_spacing             = 15.0
            grating_name            = 'FGCCTE_FCWFC1DC_630_378'
            connect_length          = 5.0
            pair_connect_length     = 5.0
            bot_gc_connect_length   = 15.0
            top_gc_connect_length   = 15.0
            bend_radius             = 10.0

            # taper properties
            # taper_prop_dict = {
            #     'length':       100.0,
            #     'width1':       0.450,
            #     'width2':       11.0,
            #     'width_etch':   2.0
            # }


            # add first taper clip
            tc1_name = f'{self.name}_tc1'
            taper_clip_layout   = TaperClip( tc1_name ).get_default_view(i3.LayoutView)
            taper_clip_layout.set(  n_rows                  = n_rows,
                                    n_taper_pairs_per_row   = n_taper_pairs_per_row[0],
                                    row_spacing             = row_spacing,
                                    grating_name            = grating_name,
                                    connect_length          = connect_length,
                                    pair_connect_length     = pair_connect_length,
                                    bot_gc_connect_length   = bot_gc_connect_length,
                                    top_gc_connect_length   = top_gc_connect_length,
                                    bend_radius             = bend_radius,
                                    taper_prop_dict         = self.taper_prop_dict )

            # plop it down
            insts += i3.SRef( name      = tc1_name,
                              reference = taper_clip_layout )


            # add second taper clip
            tc2_name = f'{self.name}_tc2'
            taper_clip_layout   = TaperClip( tc2_name ).get_default_view(i3.LayoutView)
            taper_clip_layout.set(  n_rows                  = n_rows,
                                    n_taper_pairs_per_row   = n_taper_pairs_per_row[1],
                                    row_spacing             = row_spacing,
                                    grating_name            = grating_name,
                                    connect_length          = connect_length,
                                    pair_connect_length     = pair_connect_length,
                                    bot_gc_connect_length   = bot_gc_connect_length,
                                    top_gc_connect_length   = top_gc_connect_length,
                                    bend_radius             = bend_radius,
                                    taper_prop_dict         = self.taper_prop_dict )

            # plop it down
            tc1_size_info = insts[tc1_name].size_info()
            tc2_size_info = taper_clip_layout.size_info()

            t = i3.vector_match_transform(
                    i3.OpticalPort(name='temp1', position=(tc2_size_info.west, 0.0), angle=180.0),
                    i3.OpticalPort(name='temp2', position=(tc1_size_info.east, 0.0), angle=0.0)
                                        )
            t += i3.Translation( (-25.0, 0.0) )
            insts += i3.SRef( name      = tc2_name,
                              reference = taper_clip_layout,
                              transformation = t )


            # add third taper clip
            tc3_name = f'{self.name}_tc3'
            taper_clip_layout   = TaperClip( tc3_name ).get_default_view(i3.LayoutView)
            taper_clip_layout.set(  n_rows                  = n_rows,
                                    n_taper_pairs_per_row   = n_taper_pairs_per_row[2],
                                    row_spacing             = row_spacing,
                                    grating_name            = grating_name,
                                    connect_length          = connect_length,
                                    pair_connect_length     = pair_connect_length,
                                    bot_gc_connect_length   = bot_gc_connect_length,
                                    top_gc_connect_length   = top_gc_connect_length,
                                    bend_radius             = bend_radius,
                                    taper_prop_dict         = taper_prop_dict )

            # plop it down
            tc2_size_info = insts[tc2_name].size_info()
            tc3_size_info = taper_clip_layout.size_info()

            pos = ( 0.0, 60.0 )

            insts += i3.SRef( name      = tc3_name,
                              reference = taper_clip_layout,
                              position  = pos )

            # t = i3.vector_match_transform(
            #         i3.OpticalPort(name='temp1', position=(tc3_size_info.west, 0.0), angle=180.0),
            #         i3.OpticalPort(name='temp2', position=(tc2_size_info.east, 0.0), angle=0.0) )
            # t += i3.Translation( (-25.0, 0.0) )
            # insts += i3.SRef( name      = tc3_name,
            #                   reference = taper_clip_layout,
            #                   transformation = t )



            return insts
        # end _generate_instances()

    # end class Layout()
    # ----------------

# end class TaperClipArray()
# -------------------------------


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

if __name__ == '__main__':

    print('hi')

    taper_prop_dict = {
                'length':       127.0,
                'width1':       0.450,
                'width2':       13.0,
                'width_etch':   2.0
            }

    taper_clip_array_layout = TaperClipArray().Layout( taper_prop_dict= taper_prop_dict )

    taper_clip_array_layout.write_gdsii('./gds/bz_taper_clip_array.gds')


# end main