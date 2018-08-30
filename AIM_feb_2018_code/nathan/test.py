import technology
import ipkiss3.all as i3

import numpy as np
import pylab as plt

from Sidewall_Grating_Wg import SidewallGratingWg
from Serp_Grating_Array import SerpGratingArray
from Linear_Taper import LinearTaper
from technology.WgTemplate import StripWgTemplate
from Custom_Waveguide import CustomWaveguide

test = SerpGratingArray()

test_l = test_l.get_default_view(i3.LayoutView)
for port in test_l.ports:
    print port.name
# test_l.visualize()

test_l.write_gdsii("./gds_files/test.gds")