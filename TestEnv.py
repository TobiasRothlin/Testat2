import numpy as np
from matplotlib import pyplot as plt
from dateien.devices import open_device
from testat2 import vi_characteristic, is_strictly_monotonic, iq_measurements, \
    frequency_response, group_delay, save_data, load_data

"""Init all devices
v_source    -> voltage source
v_meter     -> voltage meter
a_meter     -> current meter"""

# v_source = open_device(addr=0x73CC)
# v_meter = open_device(addr=0x198A)
# a_meter = open_device(addr=0x4D1E)

"""Creating a 1D numpy array with the desired measurement points"""
# source_voltage = np.linspace(0, 5, 26)

"""Calling the vi_characteristic function with the parameters"""
# vi = vi_characteristic(v_source=v_source, v_meter=v_meter, a_meter=a_meter,
#                         source_voltage=source_voltage)

"""Showing the result"""
# print(res)
"""Plotting the result"""
# plt.plot(res[:, 0], res[:, 1])
# plt.show()

# source = open_device(addr=0xC34F)
# scope = open_device(addr=0xDC31)
#
# f = np.logspace(3, 6, 31)
# I1, Q1, I2, Q2 = iq_measurements(source=source, scope=scope, f=f,
#                                   amplitude=1.0)
# # plt.plot(f, I1)
# # plt.plot(f, Q1)
# # plt.plot(f, I2)
# # plt.plot(f, Q2)
# # plt.xscale("log")
# # plt.show()
#
# A, Phi = frequency_response(I1, Q1, I2, Q2)
#
# plt.plot(f, A)
# plt.xscale("log")
# plt.yscale("log")
# plt.show()
#
# plt.plot(f, Phi)
# plt.xscale("log")
# plt.show()

#f = np.logspace(3, 6, 31)
#phi = -np.arctan(f*2*np.pi*3300*1.5e-9)
#tau_g = group_delay(f, phi)
# print(tau_g)
# plt.plot(f, tau_g)
# plt.xscale("log")
# plt.show()

# save_data("iq_data.txt", f, I1, Q1, I2, Q2)
# save_data("save_data.txt", [1, 2, 3], [[4, 7], [5, 8], [6, 9]])
# save_data("vi_characteristic.txt", vi)
# save_data("frequency_response_with_labels.txt", f, I1, Q1,
# labels=["Frequency (Hz)", "Amplitude", "Phase"])

res = load_data("frequency_response_with_labels.txt", True)
print(res)