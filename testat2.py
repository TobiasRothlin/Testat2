import numpy as np

def vi_chracteristic(v_source, v_meter, a_meter, source_voltage):
    voltage_current_list = []
    for voltage in source_voltage:
        v_source.voltage = voltage
        new_row_in_array = [v_meter.measure(), a_meter.measure()]
        voltage_current_list.append(new_row_in_array)

    return np.array(voltage_current_list)