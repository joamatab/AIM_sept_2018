import technology
import ipkiss3.all as i3
from technology.WgTemplate import StripWgTemplate

import numpy as np

class CustomWaveguide(i3.PCell):
    """Custom waveguide: a waveguide pcell which takes a given center path and has variable width along the path

    Note: beginning and end angles of waveguide are set to nearest 90 degree angle unless start_angle, end_angle are specified
    """

    _name_prefix = "CustomWg"

    class Layout(i3.LayoutView):

        wg_path = i3.NumpyArrayProperty(doc="List of coordinates denoting the center path of the waveguide")
        wg_width = i3.NumpyArrayProperty(doc="List of waveguide widths normal to the path, specified for each point on the path")
        wg_angles = i3.NumpyArrayProperty(doc="Internal Property!: list of waveguide pointing angles at each path point (rads)")
        start_angle = i3.NumberProperty(doc="Beginning angle of waveguide for calculating slope (in degrees);"
                                            "Note this angle points *into* the waveguide so start_angle=0.0 is equivalent"
                                            "to the wg going east")
        end_angle = i3.NumberProperty(doc="End angle of waveguide for calculating slope (in degrees);"
                                            "Note this angle points *out of* the waveguide so end_angle=0.0 is equivalent"
                                            "to the waveguide going east")

        def _default_wg_path(self):
            sample_wg_path = np.array([[0.0, 0.0],[5.0, 0.0],[10.0, 0.0],[15.0,0.0]],np.float_)
            return sample_wg_path

        def _default_wg_width(self):
            width = i3.TECH.WG.CORE_WIDTH
            size = self.wg_path.shape
            length = size[0]
            sample_wg_width = width*np.ones([length],np.float_)
            return sample_wg_width

        def _default_wg_angles(self):
            length, numdim = self.wg_path.shape
            angle = np.zeros([length-2],np.float_)
            for ii in range(length - 2):
                dy = self.wg_path[ii + 2,1] - self.wg_path[ii,1]
                dx = self.wg_path[ii + 2,0] - self.wg_path[ii,0]
                angle[ii] = np.arctan2(dy, dx)

            return angle

        def _default_start_angle(self):
            start_angle = int(np.round(self.wg_angles[0]/(np.pi/2)))*90.0
            return start_angle

        def _default_end_angle(self):
            size = self.wg_angles.shape
            length = size[0]
            end_angle = int(np.round(self.wg_angles[length-1]/(np.pi/2)))*90.0
            return end_angle


        def validate_properties(self):
            """Check whether the combination of properties is valid."""
            return True

        def _generate_elements(self, elems):
            # Append start and end angles
            size = self.wg_width.shape
            length = size[0]
            allangles = np.zeros([length],np.float_)
            allangles[0] = self.start_angle*np.pi/180.0
            allangles[1:(length-1)] = self.wg_angles
            allangles[length-1] = self.end_angle*np.pi/180.0

            # Check block fill layer widths
            import block_layers as bl
            block_layers = bl.layers
            block_widths = bl.widths
            max_width = 0.0
            for ii in range(len(block_widths)):
                if block_widths[ii]>max_width:
                    max_width=block_widths[ii]

            # Create coord list for boundaries
            topcoords = np.zeros([length, 2], np.float_)
            botcoords = np.zeros([length, 2], np.float_)
            topbfillcoords = np.zeros([length, 2], np.float_)
            botbfillcoords = np.zeros([length, 2], np.float_)
            for ii in range(length):
                norm = np.array([-np.sin(allangles[ii]),np.cos([allangles[ii]])],np.float_)
                topcoords[ii,:] = self.wg_path[ii,:] + self.wg_width[ii]/2*norm
                botcoords[ii,:] = self.wg_path[ii,:] - self.wg_width[ii]/2*norm
                topbfillcoords[ii, :] = self.wg_path[ii, :] + (self.wg_width[ii]/2+max_width)*norm
                botbfillcoords[ii, :] = self.wg_path[ii, :] - (self.wg_width[ii]/2+max_width)*norm

            allcoords = np.zeros([2*length, 2], np.float_)
            allbfillcoords = np.zeros([2*length, 2], np.float_)
            allcoords[0:length,:] = topcoords
            allbfillcoords[:length, :] = topbfillcoords
            for ii in range(length):
                allcoords[(length+ii),:]=botcoords[length-(ii+1),:]
                allbfillcoords[(length + ii), :] = botbfillcoords[length - (ii + 1), :]

            wg_coords = []
            fill_coords = []
            for ii in range(2*length):
                wg_coords.append((allcoords[ii,0],allcoords[ii,1]))
                fill_coords.append((allbfillcoords[ii,0],allbfillcoords[ii,1]))

            wg_shape = i3.Boundary(shape=wg_coords,layer=i3.TECH.PPLAYER.WG.COR)

            # Add wg shape to core layer
            elems += wg_shape

            # Add block layers
            for ii in range(len(block_layers)):
                fill_shape = i3.Boundary(shape=fill_coords,layer=block_layers[ii])
                elems += fill_shape

            return elems

        def _generate_ports(self, ports):
            size = self.wg_width.shape
            length = size[0]-1
            ports += i3.OpticalPort(name="in", position=(self.wg_path[0,0],self.wg_path[0,1]), angle=self.start_angle+180.0,
                                    trace_template=StripWgTemplate().Layout(core_width=self.wg_width[0]))
            ports += i3.OpticalPort(name="out", position=(self.wg_path[length, 0], self.wg_path[length, 1]),
                                    angle=self.end_angle,
                                    trace_template=StripWgTemplate().Layout(core_width=self.wg_width[length]))
            return ports
