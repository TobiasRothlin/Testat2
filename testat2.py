import math

import numpy as np
from scipy import interpolate
from scipy.misc import derivative


def vi_characteristic(v_source, v_meter, a_meter, source_voltage):
    """Measures the vi characteristic of a device under test. returns

    Parameters
    ----------
    v_source : object
        The voltage supply used for the experiment.

    v_meter : object
        The voltage meter used for the experiment.

    a_meter : object
        The current meter used for the experiment.

    source_voltage : list
        The Amplitude with which the entire measurement will be done.

    Returns
    -------
    object
        a 2D numpy array with the voltage in the first column and current in
        the second.


    Example
    -------
    source_voltage = np.linspace(0, 5, 26)\n
    res = vi_characteristic(v_source=v_source, v_meter=v_meter,
    a_meter=a_meter, source_voltage=source_voltage)
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

    Parameters
    ----------
    vi : object
        is an 2D numpy array with two rows. The first row contains the
        voltage the second row the corresponding current.

    Returns
    -------
    bool
        a bool if true -> the characteristic curve is strictly monotonic


    Example
    -------
    is_strictly_monotonic(vi=np.c_[[3, 2, 1], [30, 25, 10]])
    """
    return monotonic_direction_detection(
        vi[:, 0]) and monotonic_direction_detection(vi[:, 1])


def monotonic_direction_detection(vi_column):
    """Helper function checks if the first two numbers of vi_column are
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
    points in the vi characteristic curve the function will extrapolate.

    Parameters
    ----------
    vi : object
        is an 2D numpy array with two rows. The first row contains the voltage
        the second row the corresponding current.

    points : dict
        is a dictionary with one or two keys ("V", "I"). Each key has a 1D
        numpy array with the points which have to be interpolated.

    Returns
    -------
    dict
        a dictionary with one or two keys ("V", "I"). Depending on the points
        dictionary. Each key has a 1D numpy array containing the corresponding
        values to the values in the points dict.


    Example
    -------
    vi = np.c_[[1, 2.5, 8], [10, 12, 20]]\n
    res = interpolation(vi, {"V": [1.4, 1.8, 4], "I": [11.1, 18]})
    """
    list_of_interpolated_values = {}
    for line in points:
        if line == "V":
            interpolated_values = []
            for point in points[line]:
                closest_point = find_closest_points_on_x_axis(vi, point)
                res = linear_interpolation_x_axis(closest_point[0],
                                                  closest_point[1], point)
                interpolated_values.append(res)
            list_of_interpolated_values["I"] = np.array(interpolated_values)

        if line == "I":
            interpolated_values = []
            for point in points[line]:
                closest_point = find_closest_points_on_y_axis(vi, point)
                res = linear_interpolation_y_axis(closest_point[0],
                                                  closest_point[1], point)
                interpolated_values.append(res)
            list_of_interpolated_values["V"] = np.array(interpolated_values)
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
        higher_index = 1

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
        higher_index = 1

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
    """Measures the time dependent signals of the DUT.

    Parameters
    ----------
    source : object
        The Signal Generator used for the experiment.

    scope : object
        The Scope used for the experiment.

    f : list
        A list containing the frequencies at which to measure.

    amplitude : float
        The Amplitude with which the entire measurement will be done.


    Returns
    -------
    list
        A list containing 4 numpy array I1, Q1, I2, Q2


    Example
    -------
    f = np.logspace(3, 6, 31)\n
    I1, Q1, I2, Q2 = iq_measurements(source=source, scope=scope, f=f,
    amplitude=1.0)
    """

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


def frequency_response(i1, q1, i2, q2):
    """Calculates the frequency response with the measurements gathered in
    the function iq_measurements. These two arrays can be plotted as
    the Bode plot.

    Parameters
    ----------
    i1 : list
        I1 of the I/Q Values

    q1 : list
        Q1 of the I/Q Values

    i2 : list
        I2 of the I/Q Values

    q2 : list
        Q2 of the I/Q Values


    Returns
    -------
    list
        A list containing two numpy array A & Phi:
        A is a 1D numpy array containing the amplitude at different
        frequencies. Phi is a 1D numpy array containing the phase at different
        frequencies.


    Example
    -------
    A, Phi = frequency_response(I1, Q1, I2, Q2)
    """

    a = []
    phi = []
    for i in range(len(i1)):
        amp = (math.sqrt(math.pow(i2[i], 2) + math.pow(q2[i], 2))) / (
            math.sqrt(math.pow(i1[i], 2) + math.pow(q1[i], 2)))
        phase = math.atan2(q2[i], i2[i]) - math.atan2(q1[i], i1[i])
        a.append(amp)
        phi.append(phase)
    return [np.array(a), np.array(phi)]


def group_delay(f, phi):
    """Calculates the group delay of a given system

        Parameters
        ----------
        f : list
            contains a list or 1D numpy array of frequencies

        phi : list
            contains a list or 1D numpy array of phase responses

        Returns
        -------
        list
            a 1D numpy array containing the group_delay at different
            frequencies.


        Example
        -------
        f = np.logspace(3, 6, 31)\n
        phi = -np.arctan(f*2*np.pi*3300*1.5e-9)\n
        tau_g = group_delay(phi, f)
        """

    list_of_group_delay = []
    interpolated_function = interpolate.interp1d(
        f, phi, fill_value="extrapolate")

    for frequency in f:
        list_of_group_delay.append((-(1 / (2 * math.pi))) * derivative(
            interpolated_function, frequency))
    return np.array(list_of_group_delay)


def save_data(fname, *args, labels=[]):
    """Saves a unspecified number of measurements and saves them into a file.

            Parameters
            ----------
            fname : str
                the file path where the file will be saved

            *args : list
                a list or 1D / 2D numpy array with measurements with
                the same length

            labels : list
                a list of strings which will be the headers for the columns

            Example
            -------
            save_data("iq_data.txt", f, I1, Q1, I2, Q2) # f¨unf 1D Arrays
            """
    file_as_string = ""

    if len(labels) > 0:
        file_as_string += "# "
        for header in labels:
            file_as_string += str(header) + ","
        file_as_string += "\n"

    for i in range(len(args[0])):
        line_in_file = ""
        for line in args:
            array = ""
            try:
                for element in line[i]:
                    array += str('{0:.6f}'.format(element)) + ","
            except TypeError:
                array = str('{0:.6f}'.format(line[i])) + ","
            line_in_file += (str(array))
        file_as_string += (line_in_file[:-1] + "\n")
    print(file_as_string)

    f = open(fname, "w")
    f.write(file_as_string)
    f.close()


def load_data(fname, col_labels=False):
    """Loads the measurement data from the specified file.

        Parameters
        ----------
        fname : str
            the file path where the file is saved

        *col_labels : bool
            specifies if the file contains a Header string

        Returns
        -------
         list
            when col_labels = False a 2D numpy array.
            when col_label = True a 2D numpy array and a list with the headers
            as string.

        Example
        -------
        f, A, phi = load_data("frequency_response.txt")
        """
    f = open(fname, "r")
    text_file_as_string = f.read()
    lines_in_file = text_file_as_string.split("\n")

    parsed_file = []

    for element in lines_in_file[0].split(","):
        parsed_file.append([])

    header_string = ""
    if col_labels:
        header_string = lines_in_file[0]
        if not "#" in header_string:
            raise ValueError("no labels present in the file")
        if not len(lines_in_file[1].split(",")) == len(header_string.split(",")):
            raise ValueError("invalid number of labelse")

        lines_in_file = lines_in_file[1:]

        print("header_string: ",header_string)
    print("lines_in_file: ", lines_in_file)

    if "#" in lines_in_file[0]:
        raise ValueError("labels found in the file")

    for line in lines_in_file:
        elements = line.split(",")
        for i in range(len(elements)):
            try:
                parsed_file[i].append(float(elements[i]))
            except ValueError:
                print("Could not parse : ", element)

    measurement_array = []

    for measurement in parsed_file:
        measurement_array.append(np.array(measurement))

    return np.array(measurement_array, dtype=object)
