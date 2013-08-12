import xbmc
import time

RUN = True

SELF = xbmc.Addon('service.psikon.bgmusic')

def should_play():
	media = SELF.getSetting('psikon.media')
	if !media:
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

