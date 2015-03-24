#!/usr/bin/env python
import sys, serial, argparse, csv, time

class LiveDataPoint(object):
    def __init__(self, data): 
        if [d & 0x80 != 0 for d in data] != [True, False, False, False, False]:
           raise ValueError("Invalid data packet.")

        # 1st byte
        self.signalStrength = data[0] & 0x0f
        self.fingerOut = bool(data[0] & 0x10)
        self.droppingSpO2 = bool(data[0] & 0x20)
        self.beep = bool(data[0] & 0x40)

        # 2nd byte
        self.pulseWaveform = data[1]

        # 3rd byte
        self.barGraph = data[2] & 0x0f
        self.probeError = bool(data[2] & 0x10)
        self.searching = bool(data[2] & 0x20)
        self.pulseRate = (data[2] & 0x40) << 1

        # 4th byte
        self.pulseRate |= data[3] & 0x7f

        # 5th byte
        self.bloodSpO2 = data[4] & 0x7f

    def getBytes(self):
        result = [0]*5

        # 1st byte
        result[0] = self.signalStrength & 0x0f
        if self.fingerOut:
            result[0] |= 0x10
        if self.droppingSpO2:
            result[0] |= 0x20
        if self.beep:
            result[0] |= 0x40
        result[0] |= 0x80 # sync bit

        # 2nd byte
        result[1] = self.pulseWaveform & 0x7f

        # 3rd byte
        result[2] = self.barGraph & 0x0f
        if self.probeError:
            result[2] |= 0x10
        if self.searching:
            result[2] |= 0x20
        result[2] |= (self.pulseRate & 0x80) >> 1

        # 4th byte
        result[3] = self.pulseRate & 0x7f

        # 5th byte
        result[4] = self.bloodSpO2 & 0x7f

        return result

    def __repr__(self):
        hexBytes = ['0x{0:02X}'.format(byte) for byte in self.getBytes()]
        return "LiveDataPoint([{0}])".format(', '.join(hexBytes))

    def __str__(self):
        return ", ".join(["Signal Strength = {0}",
                          "Finger Out = {1}",
                          "Dropping SpO2 = {2}",
                          "Beep = {3}",
                          "Pulse waveform = {4}",
                          "Bar Graph = {5}",
                          "Probe Error = {6}",
                          "Searching = {7}",
                          "Pulse Rate = {8} bpm",
                          "SpO2 = {9}%"]).format(self.signalStrength,
                                                 self.fingerOut,
                                                 self.droppingSpO2,
                                                 self.beep,
                                                 self.pulseWaveform,
                                                 self.barGraph,
                                                 self.probeError,
                                                 self.searching,
                                                 self.pulseRate,
                                                 self.bloodSpO2)

    @staticmethod
    def getCsvColumns():
        return ["PulseRate", "SpO2", "PulseWaveform", "BarGraph", 
                "SignalStrength", "Beep", "FingerOut", "Searching",
                "DroppingSpO2", "ProbeError"]

    def getCsvData(self):
        return [self.pulseRate, self.bloodSpO2, self.pulseWaveform,
                self.barGraph, self.signalStrength, self.beep,
                self.fingerOut, self.searching, self.droppingSpO2,
                self.probeError]

class CMS50Dplus(object):
    def __init__(self, port):
        self.port = port
        self.conn = None

    def isConnected(self):
        return type(self.conn) is serial.Serial and self.conn.isOpen()

    def connect(self):
        if self.conn is None:
            self.conn = serial.Serial(port = self.port,
                                      baudrate = 19200,
                                      parity = serial.PARITY_ODD,
                                      stopbits = serial.STOPBITS_ONE,
                                      bytesize = serial.EIGHTBITS,
                                      timeout = 1)
        elif not self.isConnected():
            self.conn.open()

    def disconnect(self):
        if self.isConnected():
            self.conn.close()

    def getByte(self):
        return ord(self.conn.read())

    def getLiveData(self):
        try:
            self.connect()
            packet = [0]*5
            idx = 0
            while True:
                byte = self.getByte()
            
                if byte & 0x80:
                    if idx == 5 and packet[0] & 0x80:
                        yield LiveDataPoint(packet)
                    packet = [0]*5
                    idx = 0
            
                if idx < 5:
                    packet[idx] = byte
                    idx+=1
        except:
            self.disconnect()

def dumpLiveData(port, filename):
    print "Saving live data..."
    print "Press CTRL-C or disconnect the device to terminate data collection."
    oximeter = CMS50Dplus(port)
    measurements = 0
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(LiveDataPoint.getCsvColumns())
        for liveData in oximeter.getLiveData():
            writer.writerow(liveData.getCsvData())
            
            measurements+=1
            sys.stdout.write("\rGot {0} measurements...".format(measurements))
            sys.stdout.flush()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="cms50dplus.py v1.0 - Contec CMS50D+ Data Downloader (c) 2015 atbrask")

    # Required fields
    parser.add_argument("serialport", help="The device's virtual serial port.")
    parser.add_argument("output", help="Output CSV file.")

    args = parser.parse_args()

    dumpLiveData(args.serialport, args.output)

    print ""
    print "Done."