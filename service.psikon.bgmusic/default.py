import xbmc
import time

def should_play():
	return not xbmc.getCondVisibility("Player.Playing")


def playmusic(media):
	xbmc.executebuiltin("PlayMedia(%s)" % media)
	xbmc.executebuiltin("PlayerControl(RandomOn)")
	bg_active = True

	
RUN = True

	
while RUN: 
	if (should_play()):
		playmusic("special://home/addons/service.psikon.bgmusic/resources/music.mp3")
		
	xbmc.sleep(2000)

