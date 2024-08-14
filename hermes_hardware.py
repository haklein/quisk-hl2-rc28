from __future__ import print_function

from hermes.quisk_hardware import Hardware as BaseHardware
import _quisk as QS

import hid

class Hardware(BaseHardware):
  def __init__(self, app, conf):
    BaseHardware.__init__(self, app, conf)
    # Keep track of the current tune frequency and VFO
    self.tune_freq = 0
    self.vfo_freq = 0
    self.h = hid.device()
    self.product_id=30
    self.vendor_id=3110
    self.f1_status = False
    self.f2_status = False
  def open(self):	# Called once to open the Hardware
    self.h.open(self.vendor_id, self.product_id)
    self.h.set_nonblocking(1)
    self.SetLED(link=1)
    BaseHardware.open(self)
  def close(self):	# Called once to close the Hardware
    #self.h.close()
    self.SetLED(link=0)
    BaseHardware.close(self)
  def ChangeFrequency(self, tune, vfo, source='', band='', event=None):
    # When Quisk changes the frequency, record the new frequency
    self.tune_freq = tune
    self.vfo_freq = vfo
    BaseHardware.ChangeFrequency(self, tune, vfo, source, band, event)
    return self.tune_freq, self.vfo_freq	# JSMOD
  def ReturnFrequency(self):
    d = self.h.read(64)
    val = 0
    while len(d)>0:
        if len(d)==32:
            if d[0]==1: # valid frame
                if d[3]>0: # encoder movement
                    val = d[1]
                    val = val * val // 2 + 1
                    if d[3]==2:
                        val *= -1
                    self.tune_freq += val
                elif d[5] & 1 == 0:
                    # ptt
                    self.SetLED(transmit=1,f1=self.f1_status, f2=self.f2_status)
                    QS.set_PTT(1)
                elif d[5] & 2 == 0:
                    # f2 pressed
                    self.f2_status = not self.f2_status
                    self.SetLED(f1=self.f1_status, f2=self.f2_status);
                elif d[5] & 4 == 0:
                    # f1 pressed
                    self.f1_status = not self.f1_status
                    self.SetLED(f1=self.f1_status, f2=self.f2_status);
                else:
                    #  no ptt
                    QS.set_PTT(0)
                    self.SetLED(transmit=0,f1=self.f1_status, f2=self.f2_status)
        d = self.h.read(64)
    if self.tune_freq: 
      return self.tune_freq, self.vfo_freq 
    else: 
      return None, None
  def SetLED(self, transmit=0, f1=0, f2=0, link=1):
    ledstatus = 0xf
    ledstatus &= ~(transmit)
    ledstatus &= ~(f2<<1)
    ledstatus &= ~(f1<<2)
    ledstatus &= ~(link<<3)
    self.h.write([0x0, 0x1, ledstatus])
