import xbmc
import xbmcaddon
import xbmcgui
import time

SELF = xbmcaddon.Addon(id='service.psikon.bgmusic')

def should_play():
	media = SELF.getSetting('psikon.media')
	if not media:
		return false
        
	if xbmcgui.Window(10000).getProperty("PseudoTVRunning") in ["True", True]:
		return false
    
	return not xbmc.getCondVisibility("Player.Playing")


def playmusic(media):
	xbmc.executebuiltin("PlayMedia(%s)" % media)
	xbmc.executebuiltin("PlayerControl(RandomOn)")
	xbmc.enableNavSounds(True)

	
while not xbmc.abortRequested: 
	if (should_play()):
		playmusic(SELF.getSetting('psikon.media'))
		
	xbmc.sleep(2000)

