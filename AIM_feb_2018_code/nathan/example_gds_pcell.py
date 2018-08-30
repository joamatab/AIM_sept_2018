import os

from ipkiss3 import all as i3
from ipkiss3.pcell.gdscell import GDSCell
from aim_cell import AIMCell
from os.path import normpath

@i3.lock_properties()
class ComponentName(AIMCell):
    """Component description
    """

    def _default_filename(self):
        gds_path = 'sub_folder_with_gds_files/gds_name.gds'
        return normpath(gds_path)

    def _default_name(self):
        return "ComponentName"

    class Layout(AIMCell.Layout):

        def _generate_ports(self, ports):
            from technology.WgTemplate import StripWgTemplate
            ports += i3.OpticalPort(name="port_name0", position=(xloc0, yloc0), angle=angle0, trace_template=StripWgTemplate())
            ports += i3.OpticalPort(name="port_name1", position=(xloc1, yloc1), angle=angle1, trace_template=StripWgTemplate())
            return ports
        
