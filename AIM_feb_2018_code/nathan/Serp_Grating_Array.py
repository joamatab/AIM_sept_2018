"""
Serpentine grating array

TODOS
remove taper_swg and taper_flyback child cells
replace with taper layoutviews in layout
"""

# --------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------



import technology
import ipkiss3.all as i3
from technology.WgTemplate import StripWgTemplate
from Sidewall_Grating_Wg import SidewallGratingWg
from ipkiss.geometry.vector import vector_match_transform

import numpy as np
import pylab as plt

# import parabolic taper
from bz.tapers.c_parabolic_taper import ParabolicTaper
# from bz.tapers.c_linear_taper import LinearTaper

# import nitride grating
from c_Vertical_Grating_Wg_SiN import NitrideGratingWg




# --------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------

class SerpGratingArray(i3.PCell):
    """Sidewall Grating Waveguide: Waveguide with rectangular sidewall gratings
    """

    _name_prefix = "SerpGrating"

    wg_temp         = i3.WaveguideTemplateProperty(doc="Waveguide template to use for flyback waveguides, bends, and tapers")
    bend_type       = i3.StringProperty(default="manual", doc="String denoting type of bend to use for connecting arcs (options: 'default', 'manual')")
    taper_type      = i3.StringProperty(default="default", doc="String denoting type of taper to use for connecting tapers (options: 'default', 'manual')")
    bend            = i3.ChildCellProperty(doc="Bend cell to use for connecting arc waveguides")
    taper_swg       = i3.ChildCellProperty(doc="Taper cell to use for taper connectors between sidewall grating waveguides and bends")
    taper_flyback   = i3.ChildCellProperty(doc="Taper cell to use for taper connectors between flyback waveguides and bends")
    swg             = i3.ChildCellProperty(doc="Sidewall grating waveguide cell")
    flyback         = i3.ChildCellProperty(doc="Flyback waveguide cell")

    def _default_wg_temp(self):
        return StripWgTemplate(name=f"{self.name}_WgTemplate")

    def _default_bend(self):
        if self.bend_type is "default":
            return i3.Waveguide(name=f"{self.name}_Bend", trace_template=self.wg_temp)
        from Custom_Waveguide import CustomWaveguide
        return CustomWaveguide(name=f"{self.name}_Bend")

    def _default_taper_swg(self):
        if self.taper_type is "default":
            from Linear_Taper import LinearTaper
            return LinearTaper(name=f"{self.name}_SwgTaper")
        else:
            from Custom_Waveguide import CustomWaveguide
            return CustomWaveguide(name=f"{self.name}_SwgTaper")

    def _default_taper_flyback(self):
        if self.taper_type is "default":
            from Linear_Taper import LinearTaper
            return LinearTaper(name=f"{self.name}_FlybackTaper")
        else:
            from Custom_Waveguide import CustomWaveguide
            return CustomWaveguide(name=f"{self.name}_FlybackTaper")

    def _default_swg(self):
        return SidewallGratingWg(name=f"{self.name}_SidewallGratingWg")

    def _default_flyback(self):
        return i3.Waveguide(name=f"{self.name}_FlybackWg", trace_template=self.wg_temp)


    # --------------------------
    # Layout
    # --------------------------
    class Layout(i3.LayoutView):
        """
        List of properties:
        period
        duty_cycle
            absolute length of the grating section, not percentage
        grating_amp
        grat_wg_width
        flyback_wg_width
        pitch
        spacing
        length
        numrows
        taper_length
        taper_path_flyback
        taper_width_flyback
        taper_path_swg
        taper_width_swg
        bend_width
        arc_path
        arc_width

        TO GENERATE CUSTOM BENDS:
            set pitch to either 16.0 or 16.516

        """

        from ipkiss.technology import get_technology
        TECH = get_technology()

        # -----------
        # Properties

        # Sidewall grating waveguide properties
        period          = i3.PositiveNumberProperty(default=.3, doc="Period of sidewall grating")
        duty_cycle      = i3.PositiveNumberProperty(default=.1, doc="Length of grating teeth (along periodic direction)")
        grating_amp     = i3.NumberProperty(default=.01,
                                                doc="Width/amplitude of grating teeth (normal to periodic direction)")
        grat_wg_width   = i3.PositiveNumberProperty(default=1.0,
                                                  doc="Width of sidewall grating waveguide core (if grating_amp=0 width of waveguide)")

        # Flyback waveguide properites
        flyback_wg_width = i3.PositiveNumberProperty(default=0.4, doc="Width of flyback waveguide core")

        # Grating array properties
        pitch       = i3.PositiveNumberProperty(default=16.0,
                                          doc="Sidewall grating pitch (center-to-center distance of sidewall grating waveguides)")
        spacing     = i3.PositiveNumberProperty(doc="Gap between sidewall grating waveguides and flyback waveguides")

        def _default_spacing(self):
            return (self.pitch - self.grat_wg_width - self.flyback_wg_width) / 2

        length  = i3.PositiveNumberProperty(default=800.0, doc="Length of straight (untapered) waveguide sections")
        numrows = i3.PositiveIntProperty(default=32, doc="Number of sidewall grating/flyback waveguide pairs in the array")

        # Taper properties
        # Properties used for taper_type = "default"
        taper_length        = i3.PositiveNumberProperty(default=10.0, doc="Taper length")
        # Properties used for taper_type = "manual"
        taper_path_flyback  = i3.NumpyArrayProperty(doc="List of coordinates denoting the center path of the taper (bend to flyback waveguide)")
        taper_width_flyback = i3.NumpyArrayProperty(doc="List of taper widths normal to each point on the path (bend to flyback waveguide)")
        taper_path_swg      = i3.NumpyArrayProperty(doc="List of coordinates denoting the center path of the taper (bend to sidewall grating waveguide)")
        taper_width_swg     = i3.NumpyArrayProperty(doc="List of taper widths normal to each point on the path (bend to sidewall grating waveguide)")

        # REDEFINING TAPER HERE
        # taper_swg       = i3.ViewProperty( default='', doc='Taper layout that connects grating waveguide to the bends')
        # taper_flyback   = i3.ViewProperty( default='', doc='Taper layout that connects flyback waveguide to the bends')

        # Pick grating type:
        # 'one_sidewall', 'two_sidewalls', 'nitride_vertical_top', 'nitride_vertical_bottom',
        # 'nitride_one_sidewall_top', 'nitride_one_sidewall_bottom',
        grating_type    = i3.StringProperty( default='', doc='Grating type to draw')


        def _default_taper_path_flyback(self):
            return np.array([[0.0, 0.0],[self.taper_length, 0.0]],np.float_)

        def _default_taper_width_flyback(self):
            return np.array([self.bend_width, self.flyback_wg_width],np.float_)

        def _default_taper_path_swg(self):
            return np.array([[0.0, 0.0],[self.taper_length, 0.0]],np.float_)

        def _default_taper_width_swg(self):
            return np.array([self.bend_width, self.grat_wg_width],np.float_)

        # Bend properties
        # Properties used for bend_type = "default"
        bend_width  = i3.PositiveNumberProperty(default=TECH.WG.CORE_WIDTH, doc="Width of waveguides in bend sections")
        # Properties used for bend_type = "manual"
        arc_path    = i3.NumpyArrayProperty(doc="List of coordinates denoting the center path of the arc connectors (going from sidewall grating waveguide to flyback waveguide")
        arc_width   = i3.NumpyArrayProperty(doc="List of arc widths normal to each point on the path (going from sidewall grating waveguide to flyback waveguide")

        def _default_arc_path(self):
            if self.pitch == 16.0:
                #Use pregenerated adiabatic bends (TX)
                pathwidth   = np.loadtxt("../nathan/bend_data/txbend.txt", np.float_)
                arc_path    = pathwidth[:, :2]
            elif self.pitch == 16.516:
                # Use pregenerated adiabatic bends (RX)
                pathwidth   = np.loadtxt("../nathan/bend_data/rxbend.txt", np.float_)
                arc_path    = pathwidth[:, :2]
            else:
            # Default is 180 arc
                arc_path    = np.zeros([181, 2], np.float_)
                bend_rad    = (self.grat_wg_width / 2 + self.spacing + self.flyback_wg_width / 2) / 2
                for ii in range(181):
                    angle = np.pi / 180.0 * ii
                    arc_path[ii, :] = bend_rad * np.array([-np.sin(angle), np.cos(angle)], np.float_)

            return arc_path

        def _default_arc_width(self):
            if self.pitch == 16.0:
                #Use pregenerated adiabatic bends (TX)
                pathwidth = np.loadtxt("../nathan/bend_data/txbend.txt", np.float_)
                arc_width = pathwidth[:, 2]
            elif self.pitch == 16.516:
                #Use pregenerated adiabatic bends (RX)
                pathwidth = np.loadtxt("../nathan/bend_data/rxbend.txt", np.float_)
                arc_width = pathwidth[:, 2]
            else:
                #Default is uniform width with default core_width
                arc_width = np.ones([181], np.float_)
                arc_width = arc_width * self.bend_width
            return arc_width

        def validate_properties(self):
            """Check whether the combination of properties is valid."""
            if (self.grat_wg_width+self.flyback_wg_width+2*self.spacing) != self.pitch:
                raise i3.PropertyValidationError(self, "Array incorrectly overspecified (pitch=/=wg_widths+spacing",
                                                 {"pitch": self.pitch})
            return True

        @i3.cache()
        def _get_components(self):
            # Make waveguides

            # Pick grating type:
        # 'one_sidewall', 'two_sidewalls', 'nitride_vertical_top', 'nitride_vertical_bottom',
        # 'nitride_one_sidewall_top', 'nitride_one_sidewall_bottom',

            if self.grating_type == 'one_sidewall':
                # single sidewall grating
                swg_l = self.cell.swg.get_default_view(i3.LayoutView)
                swg_l.set(period=self.period, duty_cycle=self.duty_cycle, grating_amp=self.grating_amp, wg_width=self.grat_wg_width,
                          length=self.length, both_sides = False )

            elif self.grating_type == 'two_sidewalls':
                # double sidewall grating
                swg_l = self.cell.swg.get_default_view(i3.LayoutView)
                swg_l.set(period=self.period, duty_cycle=self.duty_cycle, grating_amp=self.grating_amp, wg_width=self.grat_wg_width,
                          length=self.length, both_sides = True )

            elif self.grating_type == 'nitride_vertical_top':
                # nitride vertical grating, top layer
                swg_l = NitrideGratingWg().get_default_view(i3.LayoutView)
                swg_l.set(period=self.period, duty_cycle=self.duty_cycle, grating_amp=self.grating_amp, wg_width=self.grat_wg_width,
                          length=self.length, grating_type='vertical', nitride_layer='top')

            elif self.grating_type == 'nitride_vertical_bottom':
                # nitride vertical grating, top layer
                swg_l = NitrideGratingWg().get_default_view(i3.LayoutView)
                swg_l.set(period=self.period, duty_cycle=self.duty_cycle, grating_amp=self.grating_amp, wg_width=self.grat_wg_width,
                          length=self.length, grating_type='vertical', nitride_layer='bottom')

            elif self.grating_type == 'nitride_one_sidewall_top':
                # nitride vertical grating, top layer
                swg_l = NitrideGratingWg().get_default_view(i3.LayoutView)
                swg_l.set(period=self.period, duty_cycle=self.duty_cycle, grating_amp=self.grating_amp, wg_width=self.grat_wg_width,
                          length=self.length, grating_type='one_sidewall', nitride_layer='top')

            elif self.grating_type == 'nitride_one_sidewall_bottom':
                # nitride vertical grating, top layer
                swg_l = NitrideGratingWg().get_default_view(i3.LayoutView)
                swg_l.set(period=self.period, duty_cycle=self.duty_cycle, grating_amp=self.grating_amp, wg_width=self.grat_wg_width,
                          length=self.length, grating_type='one_sidewall', nitride_layer='bottom')

            # end making grating if statement


            # flyback and stuff
            flyback_l       = self.cell.flyback.get_default_view(i3.LayoutView)
            flyback_path    = [(0.0, 0.0),(self.length,0.0)]
            wg_temp_flyback = self.cell.wg_temp.get_default_view(i3.LayoutView)
            wg_temp_flyback.set(core_width=self.flyback_wg_width)
            flyback_l.set(trace_template=wg_temp_flyback, shape=flyback_path)

            # Center-to-center distance between sidewall grating waveguide and flyback waveguide
            flyback_offset = self.grat_wg_width / 2 + self.spacing + self.flyback_wg_width / 2

            # Make bends
            bend_l = self.cell.bend.get_default_view(i3.LayoutView)
            if self.cell.bend_type is "default":
                # Default waveguide 180 arc
                bend_rad        = flyback_offset / 2
                arc             = i3.ShapeArc(center=(0.0,0.0), radius=bend_rad, start_angle=89.0, end_angle=270.0)
                wg_temp_bend    = self.cell.wg_temp.get_default_view(i3.LayoutView)
                wg_temp_bend.set( core_width = self.bend_width )
                bend_l.set( trace_template = wg_temp_bend, shape = arc )
            else:
                # Custom bend pcell
                bend_l.set(wg_path=self.arc_path, wg_width=self.arc_width, start_angle = 180.0, end_angle = 0.0)

            # Make tapers
            taper_flyback_l = self.cell.taper_flyback.get_default_view(i3.LayoutView)
            taper_swg_l     = self.cell.taper_swg.get_default_view(i3.LayoutView)

            if self.cell.taper_type is "default":
                # Linear taper pcell
                if self.cell.bend_type is "default":
                    flyback_bend_width  = self.bend_width
                    swg_bend_width      = self.bend_width
                else:
                    arcsize             = self.arc_width.shape
                    arclength           = arcsize[0]
                    flyback_bend_width  = self.arc_width[arclength-1]
                    swg_bend_width      = self.arc_width[0]

                taper_flyback_l.set(length=self.taper_length,wg_width_in=flyback_bend_width,wg_width_out=self.flyback_wg_width)
                taper_swg_l.set(length=self.taper_length,wg_width_in=swg_bend_width,wg_width_out=self.grat_wg_width)
            else:
                # Custom taper pcell
                taper_flyback_l.set(wg_path=self.taper_path_flyback,wg_width=self.taper_width_flyback, start_angle=0.0, end_angle=0.0)
                taper_swg_l.set(wg_path=self.taper_path_swg,wg_width=self.taper_width_swg, start_angle=0.0, end_angle=0.0)

            return swg_l, flyback_l, bend_l, taper_swg_l, taper_flyback_l

        def _generate_instances(self, insts):
            swg_l, flyback_l, bend_l, taper_swg_l, taper_flyback_l = self._get_components()

            # Hard code the tapers into here: (I hate hardcoding stuff, but no choice here)
            taper_length    = 79.0      # 79 is the best according to deniz' sims
            width_etch      = 4.0
            wg_width        = 0.5
            taper_swg = ParabolicTaper(name=f'{self.name}_TAPER').get_default_view(
                i3.LayoutView
            )

            taper_swg.set(  length      = taper_length,
                            width1      = wg_width,
                            width2      = self.grat_wg_width,
                            width_etch  = width_etch
                            )

            taper_flyback = ParabolicTaper(
                name=f'{self.name}_OTHERTAPER'
            ).get_default_view(i3.LayoutView)

            taper_flyback.set(  length      = taper_length,
                                width1      = wg_width,
                                width2      = self.flyback_wg_width,
                                width_etch  = width_etch
                                 )


            for ii in range(self.numrows):

                # Find component translations (for all numrows)
                t_swg           = i3.Translation((0.0, ii * self.pitch))
                # t_taper_swg_w   = vector_match_transform(taper_swg_l.ports["out"], swg_l.ports['in']) + t_swg
                # t_taper_swg_e   = vector_match_transform(taper_swg_l.ports["out"], swg_l.ports['out'], mirrored=True) + t_swg
                t_taper_swg_w   = vector_match_transform( taper_swg.ports["right"], swg_l.ports['in'] ) + t_swg
                t_taper_swg_e   = vector_match_transform( taper_swg.ports["right"], swg_l.ports['out'], mirrored=True ) + t_swg

                # Add grating rows + grating row tapers
                insts += i3.SRef(
                    reference=swg_l,
                    name=f"SidewallGratWg{str(ii)}",
                    transformation=t_swg,
                )

                # insts += i3.SRef(reference=taper_swg_l, name="SwgTaper_West" + str(ii), transformation=t_taper_swg_w)
                # insts += i3.SRef(reference=taper_swg_l, name="SwgTaper_East" + str(ii), transformation=t_taper_swg_e)
                insts += i3.SRef(
                    reference=taper_swg,
                    name=f"SwgTaper_West{str(ii)}",
                    transformation=t_taper_swg_w,
                )

                insts += i3.SRef(
                    reference=taper_swg,
                    name=f"SwgTaper_East{str(ii)}",
                    transformation=t_taper_swg_e,
                )


                if ii < (self.numrows - 1):

                    # Find component translations (for numrows-1)
                    flyback_offset      = self.grat_wg_width / 2 + self.spacing + self.flyback_wg_width / 2
                    t_flyback           = i3.Translation((0.0, ii * self.pitch + flyback_offset))
                    # t_taper_flyback_w   = vector_match_transform(taper_flyback_l.ports["out"], flyback_l.ports['in']) + t_flyback
                    # t_taper_flyback_e   = vector_match_transform(taper_flyback_l.ports["out"], flyback_l.ports['out'],
                    #                                        mirrored=True) + t_flyback
                    t_taper_flyback_w   = vector_match_transform( taper_flyback.ports["right"],
                                                                  flyback_l.ports['in'] ) \
                                                  + t_flyback
                    t_taper_flyback_e   = vector_match_transform( taper_flyback.ports["right"],
                                                                  flyback_l.ports['out'],
                                                                  mirrored = True ) \
                                                  + t_flyback

                    # t_bend_e = i3.VMirror() + vector_match_transform(bend_l.ports['in'], taper_swg_l.ports["in"],mirrored=True) + t_taper_swg_e
                    t_bend_e = i3.VMirror() \
                                       + vector_match_transform( bend_l.ports['in'],
                                                       taper_swg.ports["left"],
                                                       mirrored = True ) \
                                       + t_taper_swg_e
                    t_bend_w = i3.VMirror() \
                                       + vector_match_transform( bend_l.ports['out'],
                                                         taper_flyback.ports["left"] ) \
                                       + t_taper_flyback_w \
                                       + i3.Translation( (0.0, self.pitch) )

                    # Add instances (for numrows-1)

                    # flyback waveguide
                    insts += i3.SRef(
                        reference=flyback_l,
                        name=f"FlybackWg{str(ii)}",
                        transformation=t_flyback,
                    )


                    # flyback tapers
                    # insts += i3.SRef(   reference       = taper_flyback_l,
                    #                     name            = "FlybackTaper_West" + str(ii),
                    #                     transformation  = t_taper_flyback_w )
                    # insts += i3.SRef(   reference       = taper_flyback_l,
                    #                     name            = "FlybackTaper_East" + str(ii),
                    #                     transformation  = t_taper_flyback_e )
                    insts += i3.SRef(
                        reference=taper_flyback,
                        name=f"FlybackTaper_West{str(ii)}",
                        transformation=t_taper_flyback_w,
                    )

                    insts += i3.SRef(
                        reference=taper_flyback,
                        name=f"FlybackTaper_East{str(ii)}",
                        transformation=t_taper_flyback_e,
                    )


                    # bends
                    insts += i3.SRef(
                        reference=bend_l,
                        name=f"Bend_West{str(ii)}",
                        transformation=t_bend_w,
                    )

                    insts += i3.SRef(
                        reference=bend_l,
                        name=f"Bend_East{str(ii)}",
                        transformation=t_bend_e,
                    )


                    # end if
            # end for loop

            return insts



        def _generate_ports(self, ports):
            """
            THIS NEEDS TO BE UPDATED TO REFLECT INPUT OUTPUT TAPERS
            """
            # ports += self.instances["SidewallGratWg0"].ports["in"]
            # ports += self.instances["SidewallGratWg"+str(self.numrows-1)].ports["out"]

            ports += i3.OpticalPort( name       = 'in',
                                     position   = self.instances["SwgTaper_West0"].ports["left"].position,
                                     angle      = 180.0 )
            ports += i3.OpticalPort(
                name='out',
                position=self.instances[f"SwgTaper_East{str(self.numrows - 1)}"]
                .ports["left"]
                .position,
                angle=0.0,
            )


            return ports


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

if __name__ == '__main__':

    print('stuff')

    # settings
    tx_pitch            = 16.0
    rx_pitch            = 16.516
    grat_wg_width       = 6.0
    flyback_wg_width    = 5.0
    grating_amp         = 0.10
    period              = 0.50
    duty_cycle          = 0.25
    numrows             = 32

    serp_grating_layout = SerpGratingArray().get_default_view(i3.LayoutView)
    serp_grating_layout.set( pitch              = tx_pitch,
                             grat_wg_width      = grat_wg_width,
                             flyback_wg_width   = flyback_wg_width,
                             grating_amp        = grating_amp,
                             duty_cycle         = duty_cycle,
                             period             = period,
                             numrows            = numrows )

    serp_grating_layout.write_gdsii('./gds_files/test_serp_grating.gds')

    print serp_grating_layout.ports