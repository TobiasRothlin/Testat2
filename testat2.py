import math

import numpy as np


def vi_characteristic(v_source, v_meter, a_meter, source_voltage):
    """Measures the vi characteristic of a device under test returns a 2D
    numpy array with the voltage in the first column and current in the
    second.
    """

    # Initialise an array
    voltage_current_list = []

    # Do all the measurements with the specified source_voltage
    for voltage in source_voltage:
        v_source.voltage = voltage
        new_row_in_array = [v_meter.measure(), a_meter.measure()]
        voltage_current_list.append(new_row_in_array)

    # Convert the array to an 2D numpy array
    return np.array(voltage_current_list)


def is_strictly_monotonic(vi):
    """Checks if the characteristic curve stored in the  2D numpy array is
    strictly monotonic.
    """
    return monotonic_direction_detection(
        vi[:, 0]) and monotonic_direction_detection(vi[:, 1])


def monotonic_direction_detection(vi_column):
    """Helper function checks if the fitst two numbers of vi_column are
    either ascending or descending. Depending on this, calls the correct
    function to check the rest of the column. """
    if vi_column[0] > vi_column[1]:
        return is_strictly_monotonic_decreasing(vi_column)
    elif vi_column[0] < vi_column[1]:
        return is_strictly_monotonic_increasing(vi_column)
    else:
        return False


def is_strictly_monotonic_increasing(vi_column):
    """Helper function to check if a 1D numpy array is strictly monotonic
    increasing """
    previous_line = vi_column[0]
    for numb in vi_column[1:]:
        if previous_line >= numb:
            return False
        else:
            previous_line = numb
    return True


def is_strictly_monotonic_decreasing(vi_column):
    """Helper function to check if a 1D numpy array is strictly monotonic
        decreasing """
    previous_line = vi_column[0]
    for numb in vi_column[1:]:
        if previous_line <= numb:
            return False
        else:
            previous_line = numb
    return True


def interpolation(vi, points):
    """On an given 2D vi characteristic curve this function can interpolate
    between the closest two points. If the desired point is outside the
    points in the vi characteristic curve the function will extrapolate. """
    list_of_interpolated_values = {}
    for line in points:
        if line == "V":
            interpolated_values = []
            for point in points[line]:
                closest_point = find_closest_points_on_x_axis(vi, point)
                res = linear_interpolation_x_axis(closest_point[0],
                                                  closest_point[1], point)
                interpolated_values.append(res)
            list_of_interpolated_values["I"] = interpolated_values

        if line == "I":
            interpolated_values = []
            for point in points[line]:
                closest_point = find_closest_points_on_y_axis(vi, point)
                res = linear_interpolation_y_axis(closest_point[0],
                                                  closest_point[1], point)
                interpolated_values.append(res)
            list_of_interpolated_values["V"] = interpolated_values
    return list_of_interpolated_values


def find_closest_points_on_x_axis(vi, point):
    """Helper function finds the closest two points in vi (characteristic
    curve) on the X axis (Voltage) to the desired voltage."""
    higher_index = 0
    while vi[:, 0][higher_index] < point and higher_index < len(vi[:, 0]):
        higher_index += 1

    # if the point is outside the values given in the vi array this function
    # will return the two closes numbers (Extrapolating)
    if higher_index == 0:
        print("Extrapolating!")
        higher_index = 1;

    closest_points = [vi[higher_index - 1], vi[higher_index]]
    return np.array(closest_points)


def find_closest_points_on_y_axis(vi, point):
    """Helper function finds the closest two points in vi (characteristic
       curve) on the Y axis (Current) to the desired current."""
    higher_index = 0
    while vi[:, 1][higher_index] < point and higher_index < len(vi[:, 1]):
        higher_index += 1

    # if the point is outside the values given in the vi array this function
    # will return the two closes numbers (Extrapolating)
    if higher_index == 0:
        print("Extrapolating!")
        higher_index = 1;

    closest_points = [vi[higher_index - 1], vi[higher_index]]
    return np.array(closest_points)


def linear_interpolation_x_axis(point_one, point_two, x_value):
    """Helper function does the linear interpolation along the X Axis
    returns the corresponding Y value."""
    a = (point_one[1] - point_two[1]) / (point_one[0] - point_two[0])
    b = point_one[1] - (a * point_one[0])
    return (a * x_value) + b


def linear_interpolation_y_axis(point_one, point_two, y_value):
    """Helper function does the linear interpolation along the Y Axis
    returns the corresponding X value."""
    a = (point_one[1] - point_two[1]) / (point_one[0] - point_two[0])
    b = point_one[1] - (a * point_one[0])
    return (y_value - b) / a


def iq_measurements(source, scope, f, amplitude):
    """Measures the time dependent signals of the DUT. Returns the In-phase
    and quadrature components (I1, Q1, I2, Q2)."""

    # setting the source amplitude
    source.amplitude = amplitude

    # initialise the arrays
    list_of_i1 = []
    list_of_q1 = []
    list_of_i2 = []
    list_of_q2 = []

    # loop through all frequency in the f array
    for frequency in f:

        # Could be removed, but due to the rather long time this function is
        # running, it is nice to see some console logging.
        print("Measuring at frequency = ", frequency)

        # sets the current frequency
        source.frequency = frequency

        # reads the samples measured in the following measurement
        n = scope.nsamples

        # does the measurement
        t, c1, c2 = scope.waveforms()

        # calculates the hanning window
        h = np.hanning(n)

        sum_i1 = 0
        sum_q1 = 0
        sum_i2 = 0
        sum_q2 = 0

        # calculates i1 q1 i2 q2
        for i in range(len(t)):
            sum_i1 += c1[i] * h[i] * math.cos(2 * math.pi * frequency * t[i])
            sum_q1 += c1[i] * h[i] * math.sin(-2 * math.pi * frequency * t[i])
            sum_i2 += c2[i] * h[i] * math.cos(2 * math.pi * frequency * t[i])
            sum_q2 += c2[i] * h[i] * math.sin(-2 * math.pi * frequency * t[i])
        i1 = (4 / (n - 1)) * sum_i1
        q1 = (4 / (n - 1)) * sum_q1
        i2 = (4 / (n - 1)) * sum_i2
        q2 = (4 / (n - 1)) * sum_q2
        list_of_i1.append(i1)
        list_of_q1.append(q1)
        list_of_i2.append(i2)
        list_of_q2.append(q2)

    # returns the lists as numpy arrays
    return [np.array(list_of_i1), np.array(list_of_q1), np.array(list_of_i2),
            np.array(list_of_q2)]
