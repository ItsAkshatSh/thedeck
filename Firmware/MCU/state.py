from config import(POMO_WORK_SECS, POMO_BREAK_SECS, POMO_SESSIONS_MAX)

#SCREEN
SCREEN_NOW_PLAYING = 0
SCREEN_POMODORO = 1
SCREEN_SETTINGS = 2
SCREEN_COUNT = 3

#POMO PHASE
POMO_IDLE = 0
POMO_WORK = 1
POMO_BREAK = 2

class State:
    def __init__(self):
        #NAV
        self.screen = SCREEN_NOW_PLAYING
        self.prev_screen = SCREEN_NOW_PLAYING
        
        #settings
        self.volume = 70
        self.brightness = 80
        
        #MEDIA
        self.title = "Not Playing"
        self.artist = "Unknown"
        self.progress_sec = 0
        self.duration_Sec = 0
        self.playing = False
        self.media_dirty = False
        
        self.bg_color = 0x000000
        self.dynamic_bg = False
        
        
        #Pomodoro
        self.pomo_phase = POMO_IDLE
        self.pomo_session = 0
        self.pomo_running = False
        self.pomo_secs = POMO_WORK_SECS
        
        self.cmd_queue = []
        
    def pomo_tick(self):
        if not self.pomo_running:
            return
        if self.pomo_secs > 0:
            self.pomo_secs -= 1
            return
        
        #timer expired, switch phase
        if self.pomo_phase == POMO_WORK:
            self.pomo_session = min(self.pomo_session + 1, POMO_SESSIONS_MAX)
            if self.pomo_session == POMO_SESSIONS_MAX:
                self.pomo_running = False
                self.pomo_phase = POMO_IDLE
                self.pomo_secs = POMO_WORK_SECS
                self.pomo_session = 0
            else:
                self.pomo_phase = POMO_BREAK
                self.pomo_secs = POMO_BREAK_SECS
        
        else:
            self.pomo_phase = POMO_WORK
            self.pomo_secs = POMO_WORK_SECS
    
    def pomo_start(self):
        if self.pomo_phase == POMO_IDLE:
            self.pomo_phase = POMO_WORK
        self.pomo_running = True
        
    def pomo_stop(self):
        self.pomo_running = False
        
    def pomo_reset(self):
        self.pomo_phase = POMO_IDLE
        self.pomo_session = 0
        self.pomo_secs = POMO_WORK_SECS
        self.pomo_running = False
        
    def toggle_play(self):
        self.playing = not self.playing
        cmd = "CMD:PLAY" if self.playing else "CMD:PAUSE"
        self.cmd_queue.append(cmd)
        
        
    @property
    def progress_pct(self):
        if self.duration_Sec == 0:
            return 0
        return min(1.0, self.progress_sec / self.duration_Sec)
    
    @property
    def pomo_pct(self):
        total = POMO_BREAK_SECS if self.pomo_phase == POMO_BREAK else POMO_WORK_SECS
        return 1.0 - (self.pomo_secs / total)
    
    @property
    def pomo_time_str(self):
        m = self.pomo_secs // 60
        s = self.pomo_secs % 60
        return f"{m}:{s:02d}"
    
    @property
    def  progress_str(self):
        m,s = divmod(self.progress_sec, 60)
        return f"{m}:{s:02d}"
    
    @property
    def duration_str(self):
        m,s = divmod(self.duration_Sec, 60)
        return f"{m}:{s:02d}"