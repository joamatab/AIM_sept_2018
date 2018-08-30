import technology
import ipkiss3.all as i3

from Serp_Grating_Array import SerpGratingArray

txarray = SerpGratingArray()
rxarray = SerpGratingArray()

txarray_l = txarray.get_default_view(i3.LayoutView)
rxarray_l = rxarray.get_default_view(i3.LayoutView)
txarray_l.set(pitch = 16.0, numrows=32)
rxarray_l.set(pitch = 16.516, numrows=31)

txarray_l.write_gdsii("./gds_files/txarray.gds")
rxarray_l.write_gdsii("./gds_files/rxarray.gds")