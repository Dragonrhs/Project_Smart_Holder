import time

class HX711:
    def __init__(self, pd_sck, dout, gain=128):
        self.CLOCK = pd_sck
        self.DATA = dout
        self.CLOCK.value(False)

        self.OFFSET = 0

        self.set_gain(gain);

    def set_gain(self, gain):
        if gain is 128:
            self.GAIN = 1
        elif gain is 64:
            self.GAIN = 3
        elif gain is 32:
            self.GAIN = 2

    def read(self):
        # wait for the device being ready
        for _ in range(500):
            if self.DATA() == 0:
                break
            time.sleep_ms(1)
        else:
            raise OSError("Sensor does not respond")

        # shift in data, and gain & channel info
        result = 0
        for j in range(24 + self.GAIN):
            self.CLOCK(True)
            self.CLOCK(False)
            result = (result << 1) | self.DATA()

        # shift back the extra bits
        result >>= self.GAIN

        # check sign
        if result > 0x7fffff:
            result -= 0x1000000

        return result - self.OFFSET

    def read_average(self, times=3):
        sum = 0
        for i in range(times):
            sum += self.read()
        return sum / times

    def tare(self, times=15):
        self.set_offset(self.read_average(times))

    def set_offset(self, offset):
        self.OFFSET = offset