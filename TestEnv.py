import numpy as np
from matplotlib import pyplot as plt
from dateien.devices import open_device
from testat2 import vi_characteristic, is_strictly_monotonic

"""Init all devices
v_source    -> voltage source
v_meter     -> voltage meter
a_meter     -> current meter"""

v_source = open_device(addr=0x73CC)
v_meter = open_device(addr=0x198A)
a_meter = open_device(addr=0x4D1E)

"""Creating a 1D numpy array with the desired measurement points"""
source_voltage = np.linspace(0, 5, 26)

"""Calling the vi_characteristic function with the parameters"""
res = vi_characteristic(v_source=v_source, v_meter=v_meter, a_meter=a_meter,
                       source_voltage=source_voltage)

"""Showing the result"""
print(res)
"""Plotting the result"""
plt.plot(res[:, 0], res[:, 1])
plt.show()

