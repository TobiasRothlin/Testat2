# -*- coding: utf-8 -*-

import numpy as np
from scipy.optimize import brentq


class Device:
    def __init__(self, description):
        self._description = description

    def __str__(self):
        return f'{self._description}'


# --- first measurement setup -------------------------------------------------
class VoltageSource(Device):
    def __init__(self):
        super().__init__(description='Voltage Source')
        self._voltage = 0.0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, value):
        self._voltage = float(value)

    def __str__(self):
        return super().__str__() + f': voltage={self.voltage:g}'


class Diode:
    def __init__(self, source):
        if not isinstance(source, VoltageSource):
            raise TypeError('the source is not a voltage source')
        self._input = source
        self._R = 23.0

    def _i_diode(self, v):
        return 1e-3*(np.exp(v*3) - 1)

    @property
    def _input_current(self):
        return self._i_diode(self._output_voltage)

    @property
    def _output_voltage(self):
        return brentq(lambda v: self._i_diode(v)
                      - (self._input.voltage - v)/self._R,
                      0,
                      self._input.voltage)


class AmpereMeter(Device):
    def __init__(self, load):
        super().__init__(description='Ampere Meter')
        if not isinstance(load, Diode):
            raise TypeError('the load is not a diode')
        self._load = load

    def measure(self):
        return self._load._input_current


class VoltMeter(Device):
    def __init__(self, load):
        super().__init__(description='Volt Meter')
        if not isinstance(load, Diode):
            raise TypeError('the load is not a diode')
        self._load = load

    def measure(self):
        return self._load._output_voltage


# create all devices for the first measurement setup
voltage_source = VoltageSource()
_diode = Diode(source=voltage_source)
ampere_meter = AmpereMeter(load=_diode)
volt_meter = VoltMeter(load=_diode)


# --- second measurement setup ------------------------------------------------
class SineSource(Device):
    def __init__(self):
        super().__init__(description='Sine Source')
        self._amplitude = 0.0
        self._frequency = 0.0

    @property
    def amplitude(self):
        return self._amplitude

    @amplitude.setter
    def amplitude(self, value):
        self._amplitude = float(value)

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        self._frequency = float(value)

    def _output(self, t, gain=1.0):
        return self.amplitude*np.abs(gain) \
            * np.cos(2*np.pi*self.frequency*np.asarray(t) + np.angle(gain))

    def __str__(self):
        return super().__str__() \
            + f': amplitude={self.amplitude}' \
            + f' frequency={self.frequency}'


class Filter:
    def __init__(self):
        self._R = 3.3e3
        self._C = 1.5e-9

    def _tf(self, f):
        ZC = 1/(2j*np.pi*f*self._C)
        return ZC/(ZC + self._R)


class Oscilloscope(Device):
    def __init__(self, source, filt):
        super().__init__(description='Oscilloscope')
        if not isinstance(source, SineSource):
            raise TypeError('the source is not a sine source')
        self._source = source
        if not isinstance(filt, Filter):
            raise TypeError('is not a filter')
        self._filt = filt
        self._fs = 2.5e6
        self._nsamples = 100000

    @property
    def sample_rate(self):
        return self._fs

    @property
    def nsamples(self):
        return self._nsamples

    def waveforms(self):
        t = np.arange(self.nsamples)/self._fs - (self.nsamples - 1)/2/self._fs
        gain = self._filt._tf(self._source.frequency)
        cable = np.exp(2j*np.pi*self._source.frequency*15.0/3e8)
        ch1 = self._source._output(t, gain=1.0*cable)
        ch2 = self._source._output(t, gain=gain*cable)
        return t, ch1, ch2

    def __str__(self):
        return super().__str__() \
            + f': sample_rate={self.sample_rate:g}' \
            + f' nsamples={self.nsamples:g}'


# create all devices for the second measurement setup
sine_source = SineSource()
oscilloscope = Oscilloscope(source=sine_source, filt=Filter())


def open_device(addr):
    devices = {0x73CC: voltage_source,
               0x4D1E: ampere_meter,
               0x198A: volt_meter,
               0xC34F: sine_source,
               0xDC31: oscilloscope,
               }
    if not isinstance(addr, int):
        raise TypeError(f'addr is not an integer')
    if addr not in devices:
        raise ValueError(f'no device with address 0x{addr:04X} found')
    return devices[addr]
