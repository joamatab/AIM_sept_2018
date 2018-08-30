"""
AIM edge coupler (Si, TE, SMF 28) class
authors: bohan zhang
"""

# --------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------

# import my code path
import sys
sys.path.append( '../../' )

# import os so i can get the path to this file
import os


# import aim tech
# import layout.nathan.technology

# import ipkiss
import ipkiss3.all as i3                        # ipkiss


# --------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------

# -------------------------------
# EdgeCoupler class
# -------------------------------
class EdgeCoupler(i3.PCell):
    """
    Edge coupler pcell with layout and ports
    """

    _name_prefix = '_EDGE_COUPLER'


    # ----------------
    # Layout
    class Layout(i3.LayoutView):

        def _generate_instances(self, insts):

            # edge coupler
            fname                   = os.path.dirname(os.path.realpath(__file__)) + '/gds/aim_edge_coupler_si.gds'
            edge_coupler_gds_lay    = i3.GDSCell( filename=fname ).Layout()

            insts += i3.SRef( name = self.name + '_EDGE_COUPLER',
                              reference = edge_coupler_gds_lay,
                              flatten = True )

            return insts

        # end _generate_instances()


        def _generate_ports(self, ports):
            # Port 'out' = chip edge
            # Port 'in' = connecting waveguide

            # generate chip/out port
            edge_coupler_size_inf       = self.instances[ self.name + '_EDGE_COUPLER' ].size_info()
            edge_coupler_left_edge_pos  = edge_coupler_size_inf.west
            edge_coupler_mid_y          = edge_coupler_size_inf.center[1]
            ports += i3.OpticalPort( name       = 'out',
                                     position   = (edge_coupler_left_edge_pos, edge_coupler_mid_y),
                                     angle      = 180.0 )

            # generate waveguide/in port
            edge_coupler_right_edge_pos = edge_coupler_size_inf.east
            ports += i3.OpticalPort( name       = 'in',
                                     position   = (edge_coupler_right_edge_pos, edge_coupler_mid_y),
                                     angle      = 0.0 )

            return ports

        # end _generate_ports

    # end layout

# end class EdgeCoupler


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

if __name__ == '__main__':

    print('hi')


    # load and save main chip
    ec = EdgeCoupler().Layout()

    print ec.ports

    print('debug')
    ec.write_gdsii('./gds/test_edge_coupler.gds')