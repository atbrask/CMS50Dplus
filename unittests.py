#!/usr/bin/env python
import unittest, datetime
from cms50dplus import *

class CMS50DplusTests(unittest.TestCase):
    # LIVE DATA

    def test_LiveData_init_length(self):
        t = datetime.datetime.utcnow()
        self.assertRaises(ValueError, LiveDataPoint, t, [0x80,0,0,0])
        LiveDataPoint(t, [0x80,0,0,0,0])

    def test_LiveData_init_syncbit(self):
        t = datetime.datetime.utcnow()
        LiveDataPoint(t, [0x80,0,0,0,0])
        self.assertRaises(ValueError, LiveDataPoint, t, [0,0,0,0,0])
        self.assertRaises(ValueError, LiveDataPoint, t, [0,0x80,0,0,0])
        self.assertRaises(ValueError, LiveDataPoint, t, [0,0,0x80,0,0])
        self.assertRaises(ValueError, LiveDataPoint, t, [0,0,0,0x80,0])
        self.assertRaises(ValueError, LiveDataPoint, t, [0,0,0,0,0x80])

    def test_LiveData_signalStrength(self):
        t = datetime.datetime.utcnow()
        for x in range(16):
            y = LiveDataPoint(t, [0x80 | x, 0, 0, 0, 0])
            self.assertEquals(y.signalStrength, x)
            self.assertEquals(y.getBytes(), [0x80 | x, 0, 0, 0, 0])
            self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())

    def test_LiveData_fingerOut(self):
        t = datetime.datetime.utcnow()
        # false
        y = LiveDataPoint(t, [0x80, 0, 0, 0, 0])
        self.assertFalse(y.fingerOut)
        # true
        y = LiveDataPoint(t, [0x80 | 0x10, 0, 0, 0, 0])
        self.assertTrue(y.fingerOut)
        self.assertEquals(y.getBytes(), [0x80 | 0x10, 0, 0, 0, 0])
        self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())

    def test_LiveData_droppingSpO2(self):
        t = datetime.datetime.utcnow()
        # false
        y = LiveDataPoint(t, [0x80, 0, 0, 0, 0])
        self.assertFalse(y.droppingSpO2)
        # true
        y = LiveDataPoint(t, [0x80 | 0x20, 0, 0, 0, 0])
        self.assertTrue(y.droppingSpO2)
        self.assertEquals(y.getBytes(), [0x80 | 0x20, 0, 0, 0, 0])
        self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())

    def test_LiveData_beep(self):
        t = datetime.datetime.utcnow()
        # false
        y = LiveDataPoint(t, [0x80, 0, 0, 0, 0])
        self.assertFalse(y.beep)
        # true
        y = LiveDataPoint(t, [0x80 | 0x40, 0, 0, 0, 0])
        self.assertTrue(y.beep)
        self.assertEquals(y.getBytes(), [0x80 | 0x40, 0, 0, 0, 0])
        self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())

    def test_LiveData_pulseWaveform(self):
        t = datetime.datetime.utcnow()
        for x in range(128):
            y = LiveDataPoint(t, [0x80, x, 0, 0, 0])
            self.assertEquals(y.pulseWaveform, x)
            self.assertEquals(y.getBytes(), [0x80, x, 0, 0, 0])
            self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())

    def test_LiveData_barGraph(self):
        t = datetime.datetime.utcnow()
        for x in range(16):
            y = LiveDataPoint(t, [0x80, 0, x, 0, 0])
            self.assertEquals(y.barGraph, x)
            self.assertEquals(y.getBytes(), [0x80, 0, x, 0, 0])
            self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())

    def test_LiveData_probeError(self):
        t = datetime.datetime.utcnow()
        # false
        y = LiveDataPoint(t, [0x80, 0, 0, 0, 0])
        self.assertFalse(y.probeError)
        # true
        y = LiveDataPoint(t, [0x80, 0, 0x10, 0, 0])
        self.assertTrue(y.probeError)
        self.assertEquals(y.getBytes(), [0x80, 0, 0x10, 0, 0])
        self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())

    def test_LiveData_searching(self):
        t = datetime.datetime.utcnow()
        # false
        y = LiveDataPoint(t, [0x80, 0, 0, 0, 0])
        self.assertFalse(y.searching)
        # true
        y = LiveDataPoint(t, [0x80, 0, 0x20, 0, 0])
        self.assertTrue(y.searching)
        self.assertEquals(y.getBytes(), [0x80, 0, 0x20, 0, 0])
        self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())

    def test_LiveData_pulseRate(self):
        t = datetime.datetime.utcnow()
        for x in range(256):
            highbit = (x & 0x80) >> 1
            lowbits = x & 0x7f
            y = LiveDataPoint(t, [0x80, 0, highbit, lowbits, 0])
            self.assertEquals(y.pulseRate, x)
            self.assertEquals(y.getBytes(), [0x80, 0, highbit, lowbits, 0])
            self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())

    def test_LiveData_bloodSpO2(self):
        t = datetime.datetime.utcnow()
        for x in range(128):
            y = LiveDataPoint(t, [0x80, 0, 0, 0, x])
            self.assertEquals(y.bloodSpO2, x)
            self.assertEquals(y.getBytes(), [0x80, 0, 0, 0, x])
            self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())

    # RECORDED DATA
    def test_RecordedData_init_length(self):
        self.assertRaises(IndexError, RecordedDataPoint, [0xf0,0x80])
        RecordedDataPoint([0xf0, 0x80, 0])

    def test_RecordedData_init_syncbits(self):
        self.assertRaises(ValueError, RecordedDataPoint, [0,0,0])
        self.assertRaises(ValueError, RecordedDataPoint, [0xf0,0,0])
        self.assertRaises(ValueError, RecordedDataPoint, [0,0x80,0])

    def test_RecordedData_pulseRate(self):
        for x in range(256):
            highbit = (x & 0x80) >> 7
            lowbits = x & 0x7f
            y = RecordedDataPoint([0xf0 | highbit, 0x80 | lowbits, 0])
            self.assertEquals(y.pulseRate, x)
            self.assertEquals(y.getBytes(), [0xf0 | highbit, 0x80 | lowbits, 0])
            self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())

    def test_RecordedData_bloodSpO2(self):
        for x in range(128):
            y = RecordedDataPoint([0xf0, 0x80, x])
            self.assertEquals(y.bloodSpO2, x)
            self.assertEquals(y.getBytes(), [0xf0, 0x80, x])
            self.assertEquals(y.__repr__(), eval(y.__repr__()).__repr__())            

if __name__ == '__main__':
    unittest.main()
