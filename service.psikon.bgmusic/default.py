import xbmc
import xbmcaddon
import time

RUN = True

SELF = xbmcaddon.Addon(id='service.psikon.bgmusic')

def should_play():
	media = SELF.getSetting('psikon.media')
	if not media:
		return false
	return not xbmc.getCondVisibility("Player.Playing")


def playmusic(media):

	
	xbmc.executebuiltin("PlayMedia(%s)" % media)
	xbmc.executebuiltin("PlayerControl(RandomOn)")
	bg_active = True

	

	
while RUN: 
	if (should_play()):
		playmusic(SELF.getSetting('psikon.media'))
		
	xbmc.sleep(2000)

