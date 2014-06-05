import os, sys, urllib
import xbmc, xbmcgui, xbmcaddon
import subprocess
import signal

__addon__   = sys.modules[ "__main__" ].__addon__
__addonid__ = sys.modules[ "__main__" ].__addonid__
__cwd__     = sys.modules[ "__main__" ].__cwd__

def log(msg):
    msg = "%s: %s" % ("screensaver.psistats", msg)
    xbmc.log(msg)

class Screensaver(xbmcgui.WindowXMLDialog):
    def __init__( self, *args, **kwargs ):
        self._addon = xbmcaddon.Addon('screensaver.psistats')

    def run_http_server(self):

        log("starting up http server")

        http_port = self._addon.getSetting('http-port')
        http_server_cmd = ["python", os.getcwd() + "/resources/lib/httpserver.py", "--listen-port", http_port]

        http_server_process = subprocess.Popen(http_server_cmd)

        if (http_server_process.returncode != None):
            log("http server failed to start")
            return False
        else:
            self.http_server_process = http_server_process
            log("http server started")
            return True

    def run_ws_server(self):
        log("starting websockets server")

        ws_port = self._addon.getSetting("wsserver-port")
        
        psistats_ip = self._addon.getSetting('psistats-ip')
        psistats_port = self._addon.getSetting('psistats-port')

        ws_server_cmd = ["python", os.getcwd() + "/resources/lib/wsserver.py", "--listen-port", ws_port, '--psistats-ip', psistats_ip, '--psistats-port', psistats_port]
        
        ws_server_process = subprocess.Popen(ws_server_cmd)
        if (ws_server_process.returncode != None):
            log("websockets server failed to start")
            return False
        else:
            log("websockets server started")
            self.ws_server_process = ws_server_process
            return True

    def run_browser(self):
        log("starting browser")
        http_server_port = self._addon.getSetting("http-port")
        browser_cmd = self._addon.getSetting("browser-command")
        browser_args = self._addon.getSetting("browser-args").replace('%url%', 'http://127.0.0.1:%s/index.html' % http_server_port).split(' ')
        
        cmd = [browser_cmd] + browser_args

        self.browser_process = subprocess.Popen(cmd)
        if (self.browser_process.returncode != None):
            log("browser failed to start")
            return False
        else:
            log("browser started")
            return True

    def stop_all(self):
        self.browser_process.terminate()
        self.http_server_process.terminate()
        self.ws_server_process.terminate()

    def onInit(self):
        log("starting screen saver")
        log("current working directory: %s" % os.getcwd())

        self.conts()

        if self.run_ws_server() == False:
            return

        if self.run_http_server() == False:
            return

        if self.run_browser() == False:
            return 

        while (not xbmc.abortRequested) and (not self.stop):
            xbmc.sleep(1000)

        log("wait, is the screen saver dying over here?")

        self.stop_all()

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
