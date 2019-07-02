# uncompyle6 version 3.3.2
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.15 (v2.7.15:ca079a3ea3, Apr 30 2018, 16:30:26) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: toontown.launcher.DownloadForceAcknowledge
from pandac.PandaModules import *
from toontown.toontowngui import TTDialog
from toontown.toonbase import TTLocalizer

class DownloadForceAcknowledge:
    __module__ = __name__

    def __init__(self, doneEvent):
        self.doneEvent = doneEvent
        self.dialog = None
        return

    def enter(self, phase):
        doneStatus = {}
        if launcher.getPhaseComplete(phase):
            doneStatus['mode'] = 'complete'
            messenger.send(self.doneEvent, [doneStatus])
        try:
            base.localAvatar.b_setAnimState('neutral', 1)
        except:
            pass
        else:
            doneStatus['mode'] = 'incomplete'
            self.doneStatus = doneStatus
            percentComplete = base.launcher.getPercentPhaseComplete(phase)
            phaseName = TTLocalizer.LauncherPhaseNames[phase]
            msg = TTLocalizer.DownloadForceAcknowledgeMsg % {'phase': phaseName, 'percent': percentComplete}
            self.dialog = TTDialog.TTDialog(text=msg, command=self.handleOk, style=TTDialog.Acknowledge)
            self.dialog.show()

    def exit(self):
        if self.dialog:
            self.dialog.hide()
            self.dialog.cleanup()
            self.dialog = None
        return

    def handleOk(self, value):
        messenger.send(self.doneEvent, [self.doneStatus])