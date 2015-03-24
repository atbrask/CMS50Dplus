#!/usr/bin/env python
import unittest
from cms50dplus import *

class CMS50DplusTests(unittest.TestCase):
    # LIVE DATA

    def test_LiveData_init_length(self):
        self.assertRaises(ValueError, LiveDataPoint, [0x80,0,0,0])
        LiveDataPoint([0x80,0,0,0,0])

    def test_LiveData_init_syncbit(self):
        LiveDataPoint([0x80,0,0,0,0])
        self.assertRaises(ValueError, LiveDataPoint, [0,0,0,0,0])
        self.assertRaises(ValueError, LiveDataPoint, [0,0x80,0,0,0])
        self.assertRaises(ValueError, LiveDataPoint, [0,0,0x80,0,0])
        self.assertRaises(ValueError, LiveDataPoint, [0,0,0,0x80,0])
        self.assertRaises(ValueError, LiveDataPoint, [0,0,0,0,0x80])

    def test_LiveData_signalStrength(self):
        for x in range(16):
            y = LiveDataPoint([0x80 | x, 0, 0, 0, 0])
            self.assertEquals(y.signalStrength, x)
            self.assertEquals(y.getBytes(), [0x80 | x, 0, 0, 0, 0])
            self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())

    def test_LiveData_fingerOut(self):
        # false
        y = LiveDataPoint([0x80, 0, 0, 0, 0])
        self.assertFalse(y.fingerOut)
        # true
        y = LiveDataPoint([0x80 | 0x10, 0, 0, 0, 0])
        self.assertTrue(y.fingerOut)
        self.assertEquals(y.getBytes(), [0x80 | 0x10, 0, 0, 0, 0])
        self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())

    def test_LiveData_droppingSpO2(self):
        # false
        y = LiveDataPoint([0x80, 0, 0, 0, 0])
        self.assertFalse(y.droppingSpO2)
        # true
        y = LiveDataPoint([0x80 | 0x20, 0, 0, 0, 0])
        self.assertTrue(y.droppingSpO2)
        self.assertEquals(y.getBytes(), [0x80 | 0x20, 0, 0, 0, 0])
        self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())

    def test_LiveData_beep(self):
        # false
        y = LiveDataPoint([0x80, 0, 0, 0, 0])
        self.assertFalse(y.beep)
        # true
        y = LiveDataPoint([0x80 | 0x40, 0, 0, 0, 0])
        self.assertTrue(y.beep)
        self.assertEquals(y.getBytes(), [0x80 | 0x40, 0, 0, 0, 0])
        self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())

    def test_LiveData_pulseWaveform(self):
        for x in range(128):
            y = LiveDataPoint([0x80, x, 0, 0, 0])
            self.assertEquals(y.pulseWaveform, x)
            self.assertEquals(y.getBytes(), [0x80, x, 0, 0, 0])
            self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())

    def test_LiveData_barGraph(self):
        for x in range(16):
            y = LiveDataPoint([0x80, 0, x, 0, 0])
            self.assertEquals(y.barGraph, x)
            self.assertEquals(y.getBytes(), [0x80, 0, x, 0, 0])
            self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())

    def test_LiveData_probeError(self):
        # false
        y = LiveDataPoint([0x80, 0, 0, 0, 0])
        self.assertFalse(y.probeError)
        # true
        y = LiveDataPoint([0x80, 0, 0x10, 0, 0])
        self.assertTrue(y.probeError)
        self.assertEquals(y.getBytes(), [0x80, 0, 0x10, 0, 0])
        self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())

    def test_LiveData_searching(self):
        # false
        y = LiveDataPoint([0x80, 0, 0, 0, 0])
        self.assertFalse(y.searching)
        # true
        y = LiveDataPoint([0x80, 0, 0x20, 0, 0])
        self.assertTrue(y.searching)
        self.assertEquals(y.getBytes(), [0x80, 0, 0x20, 0, 0])
        self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())

    def test_LiveData_pulseRate(self):
        for x in range(256):
            highbit = (x & 0x80) >> 1
            lowbits = x & 0x7f
            y = LiveDataPoint([0x80, 0, highbit, lowbits, 0])
            self.assertEquals(y.pulseRate, x)
            self.assertEquals(y.getBytes(), [0x80, 0, highbit, lowbits, 0])
            self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())

    def test_LiveData_bloodSpO2(self):
        for x in range(128):
            y = LiveDataPoint([0x80, 0, 0, 0, x])
            self.assertEquals(y.bloodSpO2, x)
            self.assertEquals(y.getBytes(), [0x80, 0, 0, 0, x])
            self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())


if __name__ == '__main__':
    unittest.main()
