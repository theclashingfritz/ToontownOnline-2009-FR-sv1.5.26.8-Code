# uncompyle6 version 3.3.2
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.15 (v2.7.15:ca079a3ea3, Apr 30 2018, 16:30:26) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: toontown.toonbase.ToontownTimer
from otp.otpbase import OTPTimer
from pandac.PandaModules import *
from ToontownGlobals import *
from direct.task import Task

class ToontownTimer(OTPTimer.OTPTimer):
    __module__ = __name__

    def __init__(self):
        OTPTimer.OTPTimer.__init__(self)
        self.initialiseoptions(ToontownTimer)

    def getImage(self):
        if ToontownTimer.ClockImage == None:
            model = loader.loadModel('phase_3.5/models/gui/clock_gui')
            ToontownTimer.ClockImage = model.find('**/alarm_clock')
            model.removeNode()
        return ToontownTimer.ClockImage