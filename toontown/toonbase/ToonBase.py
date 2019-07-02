# uncompyle6 version 3.3.2
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.15 (v2.7.15:ca079a3ea3, Apr 30 2018, 16:30:26) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: toontown.toonbase.ToonBase
from otp.otpbase import OTPBase
from otp.otpbase import OTPLauncherGlobals
from direct.showbase.PythonUtil import *
import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from otp.launcher import DownloadWatcher
import ToontownLoader
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from pandac.PandaModules import *
import sys, os
from toontown.toonbase import TTLocalizer

class ToonBase(OTPBase.OTPBase):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('ToonBase')

    def __init__(self):
        OTPBase.OTPBase.__init__(self)
        if self.isMainWindowOpen():
            try:
                launcher.setPandaErrorCode(7)
            except:
                pass
            else:
                sys.exit(1)
        self.disableShowbaseMouse()
        self.wantDynamicShadows = 0
        self.exitErrorCode = 0
        camera.setPosHpr(0, 0, 0, 0, 0, 0)
        self.camLens.setFov(ToontownGlobals.DefaultCameraFov)
        self.camLens.setNearFar(ToontownGlobals.DefaultCameraNear, ToontownGlobals.DefaultCameraFar)
        self.musicManager.setVolume(0.65)
        self.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)
        tpm = TextPropertiesManager.getGlobalPtr()
        candidateActive = TextProperties()
        candidateActive.setTextColor(0, 0, 1, 1)
        tpm.setProperties('candidate_active', candidateActive)
        candidateInactive = TextProperties()
        candidateInactive.setTextColor(0.3, 0.3, 0.7, 1)
        tpm.setProperties('candidate_inactive', candidateInactive)
        self.transitions.IrisModelName = 'phase_3/models/misc/iris'
        self.transitions.FadeModelName = 'phase_3/models/misc/fade'
        self.exitFunc = self.userExit
        if __builtins__.has_key('launcher'):
            if launcher:
                launcher.setPandaErrorCode(11)
            globalClock.setMaxDt(0.2)
            if self.config.GetBool('want-particles', 1) == 1:
                self.notify.debug('Enabling particles')
                self.enableParticles()
            self.accept(ToontownGlobals.ScreenshotHotkey, self.takeScreenShot)
            self.accept('panda3d-render-error', self.panda3dRenderError)
            oldLoader = self.loader
            self.loader = ToontownLoader.ToontownLoader(self)
            __builtins__['loader'] = self.loader
            oldLoader.destroy()
            self.accept('PandaPaused', self.disableAllAudio)
            self.accept('PandaRestarted', self.enableAllAudio)
            self.friendMode = self.config.GetBool('switchboard-friends', 0)
            self.wantPets = self.config.GetBool('want-pets', 1)
            self.wantBingo = self.config.GetBool('want-fish-bingo', 1)
            self.wantKarts = self.config.GetBool('want-karts', 1)
            self.wantNewSpecies = self.config.GetBool('want-new-species', 0)
            self.inactivityTimeout = self.config.GetFloat('inactivity-timeout', ToontownGlobals.KeyboardTimeout)
            if self.inactivityTimeout:
                self.notify.debug('Enabling Panda timeout: %s' % self.inactivityTimeout)
                self.mouseWatcherNode.setInactivityTimeout(self.inactivityTimeout)
            self.randomMinigameAbort = self.config.GetBool('random-minigame-abort', 0)
            self.randomMinigameDisconnect = self.config.GetBool('random-minigame-disconnect', 0)
            self.randomMinigameNetworkPlugPull = self.config.GetBool('random-minigame-netplugpull', 0)
            self.autoPlayAgain = self.config.GetBool('auto-play-again', 0)
            self.skipMinigameReward = self.config.GetBool('skip-minigame-reward', 0)
            self.wantMinigameDifficulty = self.config.GetBool('want-minigame-difficulty', 0)
            self.minigameDifficulty = self.config.GetFloat('minigame-difficulty', -1.0)
            if self.minigameDifficulty == -1.0:
                del self.minigameDifficulty
            self.minigameSafezoneId = self.config.GetInt('minigame-safezone-id', -1)
            if self.minigameSafezoneId == -1:
                del self.minigameSafezoneId
            self.creditCardUpFront = self.config.GetInt('credit-card-up-front', -1)
            del self.creditCardUpFront == -1 and self.creditCardUpFront
        else:
            self.creditCardUpFront = self.creditCardUpFront != 0
        self.housingEnabled = self.config.GetBool('want-housing', 1)
        self.cannonsEnabled = self.config.GetBool('estate-cannons', 0)
        self.fireworksEnabled = self.config.GetBool('estate-fireworks', 0)
        self.dayNightEnabled = self.config.GetBool('estate-day-night', 0)
        self.cloudPlatformsEnabled = self.config.GetBool('estate-clouds', 0)
        self.greySpacing = self.config.GetBool('allow-greyspacing', 0)
        self.goonsEnabled = self.config.GetBool('estate-goon', 0)
        self.restrictTrialers = self.config.GetBool('restrict-trialers', 1)
        self.slowQuietZone = self.config.GetBool('slow-quiet-zone', 0)
        self.slowQuietZoneDelay = self.config.GetFloat('slow-quiet-zone-delay', 5)
        self.killInterestResponse = self.config.GetBool('kill-interest-response', 0)
        self.lastScreenShotTime = globalClock.getRealTime()
        self.accept('InputState-forward', self.__walking)
        self.canScreenShot = 1
        self.glitchCount = 0
        self.walking = 0

    def disableShowbaseMouse(self):
        self.useDrive()
        self.disableMouse()
        if self.mouseInterface:
            self.mouseInterface.reparentTo(self.dataUnused)
        if base.mouse2cam:
            self.mouse2cam.reparentTo(self.dataUnused)

    def __walking(self, pressed):
        self.walking = pressed

    def takeScreenShot(self):
        namePrefix = 'screenshot'
        namePrefix = launcher.logPrefix + namePrefix
        timedif = globalClock.getRealTime() - self.lastScreenShotTime
        if self.glitchCount > 10 and self.walking:
            return
        if timedif < 1.0 and self.walking:
            self.glitchCount += 1
            return
        if hasattr(self, 'localAvatar'):
            self.screenshot(namePrefix=namePrefix)
            self.lastScreenShotTime = globalClock.getRealTime()
            return
        coordOnScreen = self.config.GetBool('screenshot-coords', 0)
        self.localAvatar.stopThisFrame = 1
        ctext = self.localAvatar.getAvPosStr()
        self.screenshotStr = ''
        messenger.send('takingScreenshot')
        if coordOnScreen:
            coordTextLabel = DirectLabel(pos=(-0.81, 0.001, -0.87), text=ctext, text_scale=0.05, text_fg=VBase4(1.0, 1.0, 1.0, 1.0), text_bg=(0,
                                                                                                                                              0,
                                                                                                                                              0,
                                                                                                                                              0), text_shadow=(0,
                                                                                                                                                               0,
                                                                                                                                                               0,
                                                                                                                                                               1), relief=None)
            coordTextLabel.setBin('gui-popup', 0)
            strTextLabel = None
            if len(self.screenshotStr):
                strTextLabel = DirectLabel(pos=(0.0, 0.001, 0.9), text=self.screenshotStr, text_scale=0.05, text_fg=VBase4(1.0, 1.0, 1.0, 1.0), text_bg=(0,
                                                                                                                                                         0,
                                                                                                                                                         0,
                                                                                                                                                         0), text_shadow=(0,
                                                                                                                                                                          0,
                                                                                                                                                                          0,
                                                                                                                                                                          1), relief=None)
                strTextLabel.setBin('gui-popup', 0)
        self.graphicsEngine.renderFrame()
        self.screenshot(namePrefix=namePrefix, imageComment=ctext + ' ' + self.screenshotStr)
        self.lastScreenShotTime = globalClock.getRealTime()
        if coordOnScreen:
            if strTextLabel is not None:
                strTextLabel.destroy()
            coordTextLabel.destroy()
        return

    def addScreenshotString(self, str):
        if len(self.screenshotStr):
            self.screenshotStr += '\n'
        self.screenshotStr += str

    def initNametagGlobals(self):
        arrow = loader.loadModel('phase_3/models/props/arrow')
        card = loader.loadModel('phase_3/models/props/panel')
        speech3d = ChatBalloon(loader.loadModelNode('phase_3/models/props/chatbox'))
        thought3d = ChatBalloon(loader.loadModelNode('phase_3/models/props/chatbox_thought_cutout'))
        speech2d = ChatBalloon(loader.loadModelNode('phase_3/models/props/chatbox_noarrow'))
        chatButtonGui = loader.loadModelOnce('phase_3/models/gui/chat_button_gui')
        NametagGlobals.setCamera(self.cam)
        NametagGlobals.setArrowModel(arrow)
        NametagGlobals.setNametagCard(card, VBase4(-0.5, 0.5, -0.5, 0.5))
        if self.mouseWatcherNode:
            NametagGlobals.setMouseWatcher(self.mouseWatcherNode)
        NametagGlobals.setSpeechBalloon3d(speech3d)
        NametagGlobals.setThoughtBalloon3d(thought3d)
        NametagGlobals.setSpeechBalloon2d(speech2d)
        NametagGlobals.setThoughtBalloon2d(thought3d)
        NametagGlobals.setPageButton(PGButton.SReady, chatButtonGui.find('**/Horiz_Arrow_UP'))
        NametagGlobals.setPageButton(PGButton.SDepressed, chatButtonGui.find('**/Horiz_Arrow_DN'))
        NametagGlobals.setPageButton(PGButton.SRollover, chatButtonGui.find('**/Horiz_Arrow_Rllvr'))
        NametagGlobals.setQuitButton(PGButton.SReady, chatButtonGui.find('**/CloseBtn_UP'))
        NametagGlobals.setQuitButton(PGButton.SDepressed, chatButtonGui.find('**/CloseBtn_DN'))
        NametagGlobals.setQuitButton(PGButton.SRollover, chatButtonGui.find('**/CloseBtn_Rllvr'))
        rolloverSound = DirectGuiGlobals.getDefaultRolloverSound()
        if rolloverSound:
            NametagGlobals.setRolloverSound(rolloverSound)
        clickSound = DirectGuiGlobals.getDefaultClickSound()
        if clickSound:
            NametagGlobals.setClickSound(clickSound)
        NametagGlobals.setToon(self.cam)
        self.marginManager = MarginManager()
        self.margins = self.aspect2d.attachNewNode(self.marginManager, DirectGuiGlobals.MIDGROUND_SORT_INDEX + 1)
        mm = self.marginManager
        self.leftCells = [mm.addGridCell(0, 1, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop), mm.addGridCell(0, 2, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop), mm.addGridCell(0, 3, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop)]
        self.bottomCells = [
         mm.addGridCell(0.5, 0, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop), mm.addGridCell(1.5, 0, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop), mm.addGridCell(2.5, 0, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop), mm.addGridCell(3.5, 0, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop), mm.addGridCell(4.5, 0, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop)]
        self.rightCells = [
         mm.addGridCell(5, 2, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop), mm.addGridCell(5, 1, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop)]

    def setCellsAvailable(self, cell_list, available):
        for cell in cell_list:
            self.marginManager.setCellAvailable(cell, available)

    def cleanupDownloadWatcher(self):
        self.downloadWatcher.cleanup()
        self.downloadWatcher = None
        return

    def startShow(self, cr, launcherServer=None):
        self.cr = cr
        base.graphicsEngine.renderFrame()
        self.downloadWatcher = DownloadWatcher.DownloadWatcher(TTLocalizer.LauncherPhaseNames)
        if launcher.isDownloadComplete():
            self.cleanupDownloadWatcher()
        else:
            self.acceptOnce('launcherAllPhasesComplete', self.cleanupDownloadWatcher)
        gameServer = base.config.GetString('game-server', '')
        if gameServer:
            self.notify.info('Using game-server from Configrc: %s ' % gameServer)
        else:
            if launcherServer:
                gameServer = launcherServer
                self.notify.info('Using gameServer from launcher: %s ' % gameServer)
            else:
                gameServer = 'localhost'
        serverPort = base.config.GetInt('server-port', 6667)
        serverList = []
        for name in gameServer.split(';'):
            url = URLSpec(name, 1)
            url.setScheme('s')
            if url.hasPort():
                url.setPort(serverPort)
            serverList.append(url)

        if len(serverList) == 1:
            failover = base.config.GetString('server-failover', '')
            serverURL = serverList[0]
            for arg in failover.split():
                try:
                    port = int(arg)
                    url = URLSpec(serverURL)
                    url.setPort(port)
                except:
                    url = URLSpec(arg, 1)
                else:
                    if url != serverURL:
                        serverList.append(url)

        cr.loginFSM.request('connect', [serverList])

    def removeGlitchMessage(self):
        self.ignore('InputState-forward')
        print 'ignoring InputState-forward'

    def exitShow(self, errorCode=None):
        self.notify.info('Exiting Toontown: errorCode = %s' % errorCode)
        if errorCode:
            launcher.setPandaErrorCode(errorCode)
        else:
            launcher.setPandaErrorCode(0)
        sys.exit()

    def setExitErrorCode(self, code):
        self.exitErrorCode = code
        if os.name == 'nt':
            exitCode2exitPage = {OTPLauncherGlobals.ExitEnableChat: 'chat', OTPLauncherGlobals.ExitSetParentPassword: 'setparentpassword', OTPLauncherGlobals.ExitPurchase: 'purchase'}
            if code in exitCode2exitPage:
                launcher.setRegistry('EXIT_PAGE', exitCode2exitPage[code])

    def getExitErrorCode(self):
        return self.exitErrorCode

    def userExit(self):
        try:
            self.localAvatar.d_setAnimState('TeleportOut', 1)
        except:
            pass
        else:
            if self.cr.timeManager:
                self.cr.timeManager.setDisconnectReason(ToontownGlobals.DisconnectCloseWindow)

        self.cr.loginFSM.request('shutdown')
        self.notify.warning('Could not request shutdown; exiting anyway.')
        self.exitShow()

    def panda3dRenderError(self):
        launcher.setPandaErrorCode(14)
        if self.cr.timeManager:
            self.cr.timeManager.setDisconnectReason(ToontownGlobals.DisconnectGraphicsError)
        self.cr.sendDisconnect()
        sys.exit()

    def getShardPopLimits(self):
        if self.cr.productName == 'NTT-DMC':
            return (config.GetInt('shard-low-pop', ToontownGlobals.LOW_POP_NTT), config.GetInt('shard-mid-pop', ToontownGlobals.MID_POP_NTT), config.GetInt('shard-high-pop', ToontownGlobals.HIGH_POP_NTT))
        else:
            return (
             config.GetInt('shard-low-pop', ToontownGlobals.LOW_POP), config.GetInt('shard-mid-pop', ToontownGlobals.MID_POP), config.GetInt('shard-high-pop', ToontownGlobals.HIGH_POP))