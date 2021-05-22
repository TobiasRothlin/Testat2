import unittest
import numpy as np
from matplotlib import pyplot as plt
from dateien.devices import open_device
from testat2 import vi_characteristic, is_strictly_monotonic, interpolation, \
    linear_interpolation_x_axis, linear_interpolation_y_axis


class TestDatenAuswetrung(unittest.TestCase):

    def test_is_strictly_monotonic1(self):
        self.assertTrue(
            is_strictly_monotonic(vi=np.c_[[1, 2, 3], [30, 25, 10]]))

    def test_is_strictly_monotonic2(self):
        self.assertTrue(
            is_strictly_monotonic(vi=np.c_[[3, 2, 1], [30, 25, 10]]))

    def test_is_strictly_monotonic3(self):
        self.assertFalse(
            is_strictly_monotonic(vi=np.c_[[1, 3, 2], [10, 25, 30]]))

    def test_is_strictly_monotonic4(self):
        self.assertFalse(
            is_strictly_monotonic(vi=np.c_[[1, 2, 2], [10, 30, 25]]))

    def test_interpolation1(self):
        vi = np.c_[[1, 2.5, 8], [10, 12, 20]]
        self.assertEqual(interpolation(vi, {"V": [1.4, 1.8, 4]}),
                         {"I": [10.53333333, 11.06666667, 14.18181818]})

    def test_interpolation1(self):
        vi = np.c_[[1, 2.5, 8], [10, 12, 20]]
        self.assertEqual(
            interpolation(vi, {"V": [1.4, 1.8, 4], "I": [11.1, 18]}),
            {"I": [10.53333333, 11.06666667, 14.18181818],
             "V": [1.825, 6.625]})

    def test_LinInterpolationXAxis(self):
        vi = np.c_[[-0.6, 0], [0, 3]]
        print(vi)
        res = linear_interpolation_x_axis(vi[0], vi[1], 1)
        print(res)
        self.assertEqual(res, 8)

    def test_LinInterpolationYAxis(self):
        vi = np.c_[[-0.6, 0], [0, 3]]
        print(vi)
        res = linear_interpolation_y_axis(vi[0], vi[1], 8)
        print(res)
        self.assertEqual(res, 1)
