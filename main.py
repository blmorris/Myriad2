# main.py -- put your code here!
import pyb  # not necessary if declared in boot.py
from pyb import I2C

from pyb import DAC, ADC, Timer, RTC
i2c = I2C(1, I2C.MASTER)


class DSP:
    def __init__(self, i2c):
        sdsp_n_reset = pyb.Pin('A6', pyb.Pin.OUT_OD)
        sdsp_n_reset.high()
        pyb.delay(10)
        sdsp_n_reset.low()
        pyb.delay(10)
        sdsp_n_reset.high()
        pyb.delay(10)
        self.i2c = i2c
        f = open('FullBinary.bin', 'rb')
        self.buf = f.read()
        f.close()
        self.switches = {'Audin_Switch': [0x2A, 0x2B],
                         'EQ_Bypass_SW': [0xFD, 0xFE]}
        self.switch_side = {'DIRECT': 0, 'I2S': 1, 'NO_EQ': 0, 'EQ': 1}
        self.filters = [[[0x00, 0xDF], [0x00, 0xE0], [0x00, 0xE1],
                         [0x00, 0xE2], [0x00, 0xE3]],
                        [[0x00, 0xE4], [0x00, 0xE5], [0x00, 0xE6],
                         [0x00, 0xE7], [0x00, 0xE8]],
                        [[0x00, 0xE9], [0x00, 0xEA], [0x00, 0xEB],
                         [0x00, 0xEC], [0x00, 0xED]],
                        [[0x00, 0xEE], [0x00, 0xEF], [0x00, 0xF0],
                         [0x00, 0xF1], [0x00, 0xF2]],
                        [[0x00, 0xF3], [0x00, 0xF4], [0x00, 0xF5],
                         [0x00, 0xF6], [0x00, 0xF7]],
                        [[0x00, 0xF8], [0x00, 0xF9], [0x00, 0xFA],
                         [0x00, 0xFB], [0x00, 0xFC]]]

    def dsp_send_i2c(self, addr, data):
        self.i2c.send(bytes([addr, data]), 0x34)

    def start_up(self):
        self.i2c.send(bytes(self.buf[0:4]), 0x34)
        self.i2c.send(bytes(self.buf[4:5126]), 0x34)
        self.i2c.send(bytes(self.buf[5126:9224]), 0x34)
        self.i2c.send(bytes(self.buf[9224:9250]), 0x34)
        self.i2c.send(bytes(self.buf[9250:9254]), 0x34)

    def change_switch(self, switch, side_on):
        s_on = [0x00,
                self.switches[switch][self.switch_side[side_on]],
                0x00, 0x80, 0x00, 0x00]
        s_off = [0x00,
                 self.switches[switch][(self.switch_side[side_on]+1) % 2],
                 0x00, 0x00, 0x00, 0x00]
        self.i2c.send(bytes(s_on), 0x34)
        self.i2c.send(bytes(s_off), 0x34)

    def safeload_write(self, data1, data2, data3, data4, data5):
        i2c.send(bytes(data1), 0x34)
        i2c.send(bytes(data2), 0x34)
        i2c.send(bytes(data3), 0x34)
        i2c.send(bytes(data4), 0x34)
        i2c.send(bytes(data5), 0x34)

    def filter_safeload_write(self, filter, data1, data2, data3, data4, data5):
        data1.insert(0, 0x00)
        data1.insert(1, self.filters[filter-1][0][1])
        data2.insert(0, 0x00)
        data2.insert(1, self.filters[filter-1][1][1])
        data3.insert(0, 0x00)
        data3.insert(1, self.filters[filter-1][2][1])
        data4.insert(0, 0x00)
        data4.insert(1, self.filters[filter-1][3][1])
        data5.insert(0, 0x00)
        data5.insert(1, self.filters[filter-1][4][1])
        self.safeload_write(data1, data2, data3, data4, data5)

    def EQ_test(self):
        self.filter_safeload_write(1, [0x00, 0x5A, 0x0F, 0x08],
                                   [0xFF, 0x4D, 0x4E, 0x9F],
                                   [0x00, 0x58, 0xA9, 0x19],
                                   [0x00, 0xFC, 0x5E, 0xC2],
                                   [0xFF, 0x83, 0x83, 0x17])
        self.filter_safeload_write(2, [0x00, 0x7D, 0xD2, 0xA5],
                                   [0xFF, 0x06, 0x8A, 0xB3],
                                   [0x00, 0x7B, 0xCF, 0x1F],
                                   [0x00, 0xF9, 0x75, 0x4D],
                                   [0xFF, 0x86, 0x5E, 0x3B])
        self.filter_safeload_write(3, [0x00, 0x96, 0xF0, 0xE8],
                                   [0xFF, 0x21, 0xAD, 0xDA],
                                   [0x00, 0x53, 0xD6, 0xF3],
                                   [0x00, 0xDE, 0x52, 0x26],
                                   [0xFF, 0x95, 0x38, 0x26])
        self.filter_safeload_write(6, [0x00, 0x7B, 0x30, 0xA6],
                                   [0xFF, 0x0E, 0x96, 0x3F],
                                   [0x00, 0x76, 0xBD, 0xB6],
                                   [0x00, 0xF1, 0x69, 0xC1],
                                   [0xFF, 0x8E, 0x11, 0xA4])

'''
    def Audin_Switch(self):
        self.i2c.send(bytes([0x00, 0x2A, 0x00, 0x80, 0x00, 0x00]),0x34)
        self.i2c.send(bytes([0x00, 0x2B, 0x00, 0x00, 0x00, 0x00]),0x34)
    def Audin_Switch_I2S(self):
        self.i2c.send(bytes([0x00, 0x2A, 0x00, 0x00, 0x00, 0x00]),0x34)
        self.i2c.send(bytes([0x00, 0x2B, 0x00, 0x80, 0x00, 0x00]),0x34)
'''

# pyb.gpio_out('B3',pyb.PUSH_PULL)
# pyb.gpio('B3',1)
# pyb.delay(100)
# pyb.gpio('B3',0)
# pyb.delay(100)
# pyb.gpio('B3',1)
# pyb.delay(100)
'''
def mute_right():
    i2c.send(bytes([0x01, 0x26, 0x00, 0x00, 0x00, 0x00]), 0x34)
    i2c.send(bytes([0x01, 0x27, 0x00, 0x00, 0x20, 0x00]), 0x34)
def unmute_right():
    i2c.send(bytes([0x01, 0x26, 0x00, 0x80, 0x00, 0x00]), 0x34)
    i2c.send(bytes([0x01, 0x27, 0x00, 0x00, 0x20, 0x00]), 0x34)
'''
# pyb.I2C(1).mem_write(0x60,0x01,0xC0)
# pyb.I2C(1).mem_write(0x60,0x02,0x3F)
# pyb.I2C(1).mem_read(0x60,0x01,4)


class Microphone:
    def __init__(self, i2c):
        mic_n_reset = pyb.Pin('A7', pyb.Pin.OUT_OD)
        mic_n_reset.high()
        pyb.delay(10)
        mic_n_reset.low()
        pyb.delay(10)
        mic_n_reset.high()
        pyb.delay(10)
        self.i2c = i2c

    def mic_send_i2c(self, addr, data):
        self.i2c.send(bytes([addr, data]), 0x18)

    def start_up(self):
        self.mic_send_i2c(0x00, 0x00)
        self.mic_send_i2c(0x01, 0x01)
        self.mic_send_i2c(0x04, 0x03)
        self.mic_send_i2c(0x05, 0x91)
        self.mic_send_i2c(0x06, 0x20)
        self.mic_send_i2c(0x12, 0x88)
        self.mic_send_i2c(0x13, 0x82)
        self.mic_send_i2c(0x1a, 0xaa)
        self.mic_send_i2c(0x3b, 0x50)
        self.mic_send_i2c(0x3c, 0x50)
        self.mic_send_i2c(0x51, 0xC0)
        self.mic_send_i2c(0x52, 0x00)
        self.mic_send_i2c(0x00, 0x01)
        self.mic_send_i2c(0x1a, 0x00)
        self.mic_send_i2c(0x33, 0x50)
        self.mic_send_i2c(0x34, 0xcf)
        self.mic_send_i2c(0x36, 0x3F)
        self.mic_send_i2c(0x37, 0xcf)
        self.mic_send_i2c(0x39, 0x3F)
        self.mic_send_i2c(0x3b, 0x40)
        self.mic_send_i2c(0x3c, 0x40)

'''
class GPIO:
    def __init__(self, i2c):
        g = pyb.Pin('A13', pyb.Pin.OUT_PP)
        g.high()
        pyb.delay(10)
        g.low()
        pyb.delay(10)
        g.high()
        pyb.delay(10)
        self.i2c = i2c
'''

sensor = ADC('A0')


def sensor_distance(unit):
    if unit == 'm':
        return ((sensor.read()/2552.3)**(1/-1.045))*.3048
    elif unit == 'in':
        return ((sensor.read()/2552.3)**(1/-1.045))*12
    elif unit == 'cm':
        return ((sensor.read()/2552.3)**(1/-1.045))*30.48
    else:
        return (sensor.read()/2552.3)**(1/-1.045)


# decrease volume as object gets closer
def v_change_dis():
    return 255-int((sensor.read()) >> 4)
    # you can get rid of "255-" to make it do the opposite
# volume control

tim = Timer(1)
tim.init(freq=20)
dac = DAC(1)
pot = ADC('B0')
# tim.callback(lambda t: dac.write(int(pot.read()>>4)))
tim.callback(lambda t: dac.write(v_change_dis()))
# GPIO test

gpio = pyb.Pin('A13', pyb.Pin.OUT_PP)
gpio.high()
pyb.delay(10)
gpio.low()
pyb.delay(10)
gpio.high()
pyb.delay(10)
'''
class stat:
    def __init__(self):
        self.s = 0
    def num(self):
        self.s = 14
    def renum(self):
        return self.s
    def n(self):
        self.s = 0
num = stat()
'''


def call(line):
    # num.num()
    print(line)
i2c.mem_write(0xF0, 0x20, 0x00)
i2c.mem_write(0x0F, 0x20, 0x0A)
i2c.mem_write(0xF0, 0x20, 0x02)
i2c.mem_write(0x00, 0x20, 0x03)
i2c.mem_write(0x00, 0x20, 0x04)
i2c.mem_write(0x02, 0x20, 0x05)


def button():
    s = i2c.mem_read(1, 0x20, 0x09)
    f = s[0] >> 4
    f = f ^ 0x0F
    i2c.mem_write(f, 0x20, 0x0A)
gpio_int = pyb.ExtInt('A14', pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_NONE, call)

# timer_a = Timer(2)
# timer_a.init(freq = 1)
# timer_a.callback(button())
vp = ADC('B1')


def rail_voltage():
    return vp.read()*((3.3/4096)*(53.22/3.32))


def power_stat():
    pyb.LED(4).intensity(245-int(vp.read() >> 3))
    pyb.LED(3).intensity(245-int(vp.read() >> 3))

power_stat()


def mic_rms_dB(i2):
    i2.mem_write(bytes([0x06, 0x8E]), 0x34, 2074, addr_size=16)
    buf = bytearray(3)
    i2c.mem_read(buf, 0x34, 2074, addr_size=16)
    val = ((buf[0] << 16)+(buf[1] << 8)+buf[2])/2**19
    if val < 16:
        return val * 10
    else:
        return (val - 32.0) * 10


class Amplifier:
    def __init__(self):
        self.mute_one = pyb.Pin('B8', pyb.Pin.OUT_PP)
        self.mute_two = pyb.Pin('B9', pyb.Pin.OUT_PP)

    def mute1(self):
        self.mute_one.high()

    def mute2(self):
        self.mute_two.high()

    def unmute1(self):
        self.mute_one.low()

    def unmute2(self):
        self.mute_two.low()

    def mute(self):
        self.mute_one.high()
        self.mute_two.high()

    def unmute(self):
        self.mute_one.low()
        self.mute_two.low()


class date_time:
    def __init__(self):
        self.datime = RTC()

    def year(self):
        tim = self.datime.datetime()
        return tim[0]

    def month(self):
        tim = self.datime.datetime()
        return tim[1]

    def day(self):
        tim = self.datime.datetime()
        return tim[2]

    def weekday(self):
        tim = self.datime.datetime()
        wds = ['monday', 'tuesday', 'wednesday', 'thursday',
               'friday', 'saturday', 'sunday']
        return wd[tim[3]-1]

    def date(self):
        return '%s/%s/%s' % (self.month(), self.day(), self.year())

    def hour(self):
        tim = self.datime.datetime()
        h = tim[4]
        e = 'a.m'
        if h >= 12 and h != 24:
            e = 'p.m'
        if h > 12:
            h -= 12
        return '%s %s' % (h, e)

    def minute(self):
        tim = self.datime.datetime()
        return tim[5]

    def second(self):
        tim = self.datime.datetime()
        return tim[6]

    def time(self):
        tim = self.datime.datetime()
        h = tim[4]
        e = 'a.m'
        if h >= 12 and h != 24:
            e = 'p.m'
        if h > 12:
            h -= 12
        return '%s:%s:%s %s' % (h, self.minute(), self.second(), e)

    def subseconds(self):
        tim = self.datime.datetime()
        return tim[7]

datetime = date_time()


class logger:
    def __init__(self):
        txt = open('1:/logfile.txt', 'a')
        txt.close()
        selfdatetime = date_time()

    def write(self, text):
        txt = open('1:/logfile.txt', 'a')
        txt.write('%s %s: %s \t' % (datetime.date(), datetime.time(), text))
        txt.close()


pyb.LED(2).toggle()
dsp = DSP(i2c)
dsp.start_up()
mic = Microphone(i2c)
mic.start_up()
pyb.LED(2).toggle()


def lights_feet():
    if sensor_distance('') < 2:
        i2c.mem_write(0x00, 0x20, 0x0A)
    elif sensor_distance('') < 3:
        i2c.mem_write(0b00001000, 0x20, 0x0A)
    elif sensor_distance('') < 4:
        i2c.mem_write(0b00001100, 0x20, 0x0A)
    elif sensor_distance('') < 5:
        i2c.mem_write(0b00001110, 0x20, 0x0A)
    else:
        i2c.mem_write(0x0F, 0x20, 0x0A)
'''
for i in range(1,500):
    #lights_feet()
    button()
   # if num.renum()!=0:
    #    button()
     #   num.n()
    pyb.delay(100)
'''
