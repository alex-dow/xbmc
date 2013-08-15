import xbmc
import xbmcaddon
import xbmcgui

def psikon_log(msg):
	xbmc.log("[%s] %s" % ("service.psikon.bgmusic", msg))

	
class PsikonBgMusicPlayer(xbmc.Player):

	def __init__(self, *args, **kwargs):
		self.playing2 = False
		super(PsikonBgMusicPlayer, self).__init__(args, kwargs)

		
	def play(self, media):
		self.playing2 = True
		super(PsikonBgMusicPlayer, self).play(media)

		
	def stop(self):
		self.playing2 = False
		super(PsikonBgMusicPlayer, self).stop()

		
	def isPlaying(self):
		return self.playing2

		
class PsikonBgMusicMonitor(xbmc.Monitor):
	def __init__(self, service):
		self.service = service
		
	def onAbortRequested(self):
		self.service.stop()
	
	def onScreensaverActivated(self):
		self.service.stop()
		
	def onScreensaverDeactivated(self):
		self.service.loop()


class PsikonBgMusic(object):

	def __init__(self):
		self.delay   = 2000
		self.WINDOW  = xbmcgui.Window(10000)
		self.ADDON   = xbmcaddon.Addon(id='service.psikon.bgmusic')
		self.RUN     = False
		self.PLAYER  = PsikonBgMusicPlayer()
		self.FLAG_PLAY = 0
		self.FLAG_NO_MEDIA = 1
		self.FLAG_SELF_PLAYER_ON = 2
		self.FLAG_OTHER_PLAYER_ON = 4
		self.FLAG_PSEUDOTV_ON = 8
		

	def should_play(self):
		
		if xbmcgui.Window(10000).getProperty("PseudoTVRunning") == "True":
			return self.FLAG_PSEUDOTV_ON
		
		media = self.ADDON.getSetting('psikon.media')

		if self.PLAYER.isPlaying():
			return self.FLAG_SELF_PLAYER_ON				
			
		if xbmc.getCondVisibility("Player.Playing"):
			return self.FLAG_OTHER_PLAYER_ON			
			
		if not media:
			return self.FLAG_NO_MEDIA


		return self.FLAG_PLAY
		
	def loop(self):
		while self.RUN:
			flag = self.should_play()
			
			if flag == self.FLAG_PLAY:
				self.play_music(self.ADDON.getSetting('psikon.media'))
			elif flag == self.FLAG_OTHER_PLAYER_ON:
				pass
			elif flag == self.FLAG_PSEUDOTV_ON:
				if self.PLAYER.isPlaying():
					self.PLAYER.stop()
			
			xbmc.sleep(self.delay)
	
	def start(self):
		self.RUN = True
		self.loop()
	
	def stop(self):
		self.RUN = False
		self.stop_music()
		
	def play_music(self, media):
		xbmc.enableNavSounds(False)
		self.PLAYER.play(media)
		xbmc.sleep(100)
		xbmc.enableNavSounds(True)
		self.delay = 2000
	
	def stop_music(self):
		self.PLAYER.stop()


psikon_bg_music = PsikonBgMusic()
psikon_bg_music_monitor = PsikonBgMusicMonitor(psikon_bg_music)

psikon_bg_music.start()