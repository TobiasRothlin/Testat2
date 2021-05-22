import numpy as np


def vi_characteristic(v_source, v_meter, a_meter, source_voltage):
    voltage_current_list = []
    for voltage in source_voltage:
        v_source.voltage = voltage
        new_row_in_array = [v_meter.measure(), a_meter.measure()]
        voltage_current_list.append(new_row_in_array)

    return np.array(voltage_current_list)


def is_strictly_monotonic(vi):
    print("Testing if \n", vi, "\n is strictly monotonic")
    return monotonic_direction_detection(
        vi[:, 0]) and monotonic_direction_detection(vi[:, 1])


def monotonic_direction_detection(vi_column):
    if vi_column[0] > vi_column[1]:
        return is_strictly_monotonic_decreasing(vi_column)
    elif vi_column[0] < vi_column[1]:
        return is_strictly_monotonic_increasing(vi_column)
    else:
        return False


def is_strictly_monotonic_increasing(vi_column):
    print("-----In function is_strictly_monotonic_increasing-----")
    print(vi_column)
    previous_line = vi_column[0]
    for numb in vi_column[1:]:
        print("comparing: previous_line =", previous_line, " >= numb = ", numb)
        if previous_line >= numb:
            return False
        else:
            previous_line = numb
    return True


def is_strictly_monotonic_decreasing(vi_column):
    print("-----In function is_strictly_monotonic_decreasing-----")
    print(vi_column)
    previous_line = vi_column[0]
    for numb in vi_column[1:]:
        print("comparing: previous_line =", previous_line, " >= numb = ", numb)
        if previous_line <= numb:
            return False
        else:
            previous_line = numb
    return True


def interpolation(vi, points):
    for line in points:
        if line == "V":
            for point in points[line]:
                closestPoint = find_closest_points_on_x_axis(vi, point)
    return None


def find_closest_points_on_x_axis(vi, point):
    print("-------- Point ", point, " ---------")
    print(vi[:,0])
    print("-----------------")


def linear_interpolation_x_axis(point_one, point_two, x_value):
    a = (point_one[1] - point_two[1]) / (point_one[0] - point_two[0])
    b = point_one[1] - (a * point_one[0])
    return (a * x_value) + b


def linear_interpolation_y_axis(point_one, point_two, y_value):
    a = (point_one[1] - point_two[1]) / (point_one[0] - point_two[0])
    b = point_one[1] - (a * point_one[0])
    return (y_value - b) / a
