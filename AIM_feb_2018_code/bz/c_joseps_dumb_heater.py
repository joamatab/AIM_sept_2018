"""
jhoseps dumb heater
"""

# --------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------

# import my code path
import sys
sys.path.append( '../../' )

# import aim tech
import layout.nathan.technology

# import ipkiss
import ipkiss3.all as i3                        # ipkiss


# --------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------

# -------------------------------
# heater class
# -------------------------------
class heater(i3.PCell):
    """
    heater
    """

    _name_prefix = '_HEAT'


    # ----------------
    # Layout
    class Layout(i3.LayoutView):

        def _generate_instances(self, insts):

            # edge coupler
            fname                   = '../josep/thermo_optic_phase_shifter.gds'
            heater_gds_lay          = i3.GDSCell( filename=fname ).Layout()

            insts += i3.SRef( name = self.name + '_HEAT',
                              reference = heater_gds_lay )

            return insts

        # end _generate_instances()


        # def _generate_ports(self, ports):
        #     # Port 'out' = chip edge
        #     # Port 'in' = connecting waveguide
        #
        #     # generate chip/out port
        #     edge_coupler_size_inf       = self.instances[ self.name + '_EDGE_COUPLER' ].size_info()
        #     edge_coupler_left_edge_pos  = edge_coupler_size_inf.west
        #     edge_coupler_mid_y          = edge_coupler_size_inf.center[1]
        #     ports += i3.OpticalPort( name       = 'out',
        #                              position   = (edge_coupler_left_edge_pos, edge_coupler_mid_y),
        #                              angle      = 180.0 )
        #
        #     # generate waveguide/in port
        #     edge_coupler_right_edge_pos = edge_coupler_size_inf.east
        #     ports += i3.OpticalPort( name       = 'in',
        #                              position   = (edge_coupler_right_edge_pos, edge_coupler_mid_y),
        #                              angle      = 0.0 )
        #
        #     return ports
        #
        # # end _generate_ports

    # end layout

# end class EdgeCoupler


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

if __name__ == '__main__':

    print('hi')


    # load and save main chip
    ec = heater().Layout()

    print ec.ports

    print('debug')
    ec.write_gdsii('lololoolol.gds')