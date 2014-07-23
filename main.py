# main.py -- put your code here!
# import pyb	# not necessary if declared in boot.py
from pyb import I2C


from pyb import DAC, ADC, Timer, RTC
i2c = I2C(1,I2C.MASTER)
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
        f = open('FullBinary.bin','rb')
        self.buf=f.read()
        f.close()
        self.switches = {'Audin_Switch' : [0x2A, 0x2B], 'EQ_Bypass_SW' : [0xFD, 0xFE]}
        self.switch_side = {'DIRECT': 0, 'I2S': 1, 'NO_EQ' : 0, 'EQ' : 1}
    def dsp_send_i2c(self,addr,data):
        self.i2c.send(bytes([addr, data]), 0x34)
    def start_up(self):
        self.i2c.send( bytes(self.buf[0:4]), 0x34)
        self.i2c.send( bytes(self.buf[4:5126]), 0x34)
        self.i2c.send( bytes(self.buf[5126:9224]), 0x34)
        self.i2c.send( bytes(self.buf[9224:9250]), 0x34)
        self.i2c.send( bytes(self.buf[9250:9254]), 0x34)
    def change_switch(self, switch, side_on):
        s_on = [0x00,self.switches[switch][self.switch_side[side_on]] , 0x00, 0x80, 0x00, 0x00]
        s_off = [0x00,self.switches[switch][(self.switch_side[side_on]+1)%2] , 0x00, 0x00, 0x00, 0x00]
        self.i2c.send(bytes(s_on),0x34)
        self.i2c.send(bytes(s_off),0x34)
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
    def mic_send_i2c(self,addr,data):
        self.i2c.send(bytes([addr, data]), 0x18)
    def start_up(self):
        self.mic_send_i2c(0x00,0x00)
        self.mic_send_i2c(0x01,0x01)
        self.mic_send_i2c(0x04,0x03)
        self.mic_send_i2c(0x05,0x91)
        self.mic_send_i2c(0x06,0x20)


        self.mic_send_i2c(0x12,0x88)
        self.mic_send_i2c(0x13,0x82)


        self.mic_send_i2c(0x1a,0xaa)
        self.mic_send_i2c(0x3b,0x50)
        self.mic_send_i2c(0x3c,0x50)


        self.mic_send_i2c(0x51,0xC0)
        self.mic_send_i2c(0x52,0x00)


        self.mic_send_i2c(0x00,0x01)
        self.mic_send_i2c(0x1a,0x00)
        self.mic_send_i2c(0x33,0x50)
        self.mic_send_i2c(0x34,0xcf)
        self.mic_send_i2c(0x36,0x3F)
        self.mic_send_i2c(0x37,0xcf)
        self.mic_send_i2c(0x39,0x3F)
        self.mic_send_i2c(0x3b,0x40)
        self.mic_send_i2c(0x3c,0x40)
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


# volume control
tim = Timer(1)
tim.init(freq = 20)
dac = DAC(1)
pot = ADC('B0')
tim.callback(lambda t: dac.write(int(pot.read()>>4)))

#GPIO test
gpio = pyb.Pin('A13', pyb.Pin.OUT_PP)
gpio.high()
pyb.delay(10)
gpio.low()
pyb.delay(10)
gpio.high()
pyb.delay(10)

i2c.mem_write(0xF0,0x20,0x00)
i2c.mem_write(0x0F,0x20,0x0A)
i2c.mem_write(0xF0, 0x20,0x02)
i2c.mem_write(0x00, 0x20,0x03 )
#gpio_int = pyb.ExtInt('A14', pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_NONE, lambda f : print('press!'))
def button():
	s = i2c.mem_read(1,0x20,0x09)
	f = s[0]>>4
	f = f^0x0F
	i2c.mem_write(f,0x20,0x0A)

'''
ti = Timer(2)
ti.init(freq = 1)
ti.callback(lambda d: i2c.mem_write((i2c.mem_read(1,0x20,0x09)[0]>>4)^0x0F, 0x20, 0x0A))
'''

def rail_voltage():
    vp = ADC('B1')
    num = (3.3/4096)*(53.22/3.32)
    rv = vp.read()*num
    return rv
'''
def power_stat():
    if ADC('B1').read()>1000:
		pyb.LED(3).off()
		pyb.LED(4).intensity(0)
	else:
		pyb.LED(4).intensity(255)
		pyb.LED(3).toggle()
ti.callback(power_stat())
'''

def mic_rms_dB(i2):
    i2.mem_write(bytes([0x06,0x8E]), 0x34,2074,addr_size=16)
    buf = bytearray(3)
    i2c.mem_read(buf,0x34,2074,addr_size=16)
    val = ((buf[0] <<16)+(buf[1]<<8)+buf[2])/2**19
    if val < 16:
        return val * 10
    else:
        return (val - 32.0) * 10


class Amplifier:
    def __init__(self):
        self.mute_one = pyb.Pin('B8',pyb.Pin.OUT_PP)
        self.mute_two =pyb.Pin('B9',pyb.Pin.OUT_PP)
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
        wds = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        return wd[tim[3]-1]
    def date(self):
        return '%s / %s / %s' % (self.month(), self.day(), self.year())
    def hour(self):
        tim = self.datime.datetime()
        h = tim[4]
        e = 'a.m.'
        if h>=12 and h!=24:
            e = 'p.m.'
        if h>12:
            h -=12
        return '%s %s' % (h,e)
    def minute(self):
        tim = self.datime.datetime()
        return tim[5]
    def second(self):
        tim = self.datime.datetime()
        return tim[6]
    def time(self):
        tim = self.datime.datetime()
        h = tim[4]
        e = 'a.m.'
        if h>=12 and h!=24:
            e = 'p.m.'
        if h>12:
            h -=12
        return '%s : %s : %s %s' % (h, self.minute(), self.second(), e)
    def subseconds(self):
        tim = self.datime.datetime()
        return tim[7]



pyb.LED(2).toggle()
dsp = DSP(i2c)
dsp.start_up()
mic = Microphone(i2c)
mic.start_up()
pyb.LED(2).toggle()
