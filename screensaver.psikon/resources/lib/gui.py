import os, sys, urllib
import xbmc, xbmcgui, xbmcaddon
import subprocess

__addon__   = sys.modules[ "__main__" ].__addon__
__addonid__ = sys.modules[ "__main__" ].__addonid__
__cwd__     = sys.modules[ "__main__" ].__cwd__

URL="http://lab.icradle.net/full_screen_clock/"

def log(txt):
    if isinstance (txt,str):
        txt = txt.decode("utf-8")
    message = u'%s: %s' % (__addonid__, txt)
    xbmc.log(msg=message.encode("utf-8"), level=xbmc.LOGDEBUG)

class Screensaver(xbmcgui.WindowXMLDialog):
    def __init__( self, *args, **kwargs ):
        self._addon = xbmcaddon.Addon('screensaver.psikon')

    def getUrl(self):
        url = self._addon.getSetting('url')
        if 'http://' not in url:
            url = 'file://' + os.getcwd() + '/resources/web/' + url
        return url

    def onInit(self):
        log("starting screen saver")
        self.conts()

        browser_cmd = self._addon.getSetting('browser-command')
        browser_args = self._addon.getSetting('browser-args').replace('%url%', self.getUrl()).split(' ')

        cmd = [browser_cmd] + browser_args

        daemon_cmd = ["python", os.getcwd() + "/resources/lib/app.py"]

        self.daemon_process = subprocess.Popen(daemon_cmd)
        self.process = subprocess.Popen(cmd) 

        log("firefox started: %s" % self.process.pid)

        while (not xbmc.abortRequested) and (not self.stop):

            xbmc.sleep(1000)

        log("wait, is the screen saver dying over here?")

        self.process.terminate()
        self.daemon_process.terminate()

    def conts(self):
        self.winid = xbmcgui.getCurrentWindowDialogId()
        self.stop = False
        self.Monitor = MyMonitor(action = self.exit)

    def exit(self):
        self.stop = True
        self.close()
        
class MyMonitor(xbmc.Monitor):
    def __init__( self, *args, **kwargs ):
        self.action = kwargs['action']

    def onScreensaverDeactivated(self):
        log("Stopping screensaver!")
        self.action()
