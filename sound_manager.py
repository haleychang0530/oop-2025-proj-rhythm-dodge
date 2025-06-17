import pygame

class SoundManager:
    def __init__(self):
        self.sfx = {
            "level1_playing": pygame.mixer.Sound("assets/music/level1.mp3"),
            "level2_playing": pygame.mixer.Sound("assets/music/level2.mp3"),

            "level1_menu": pygame.mixer.Sound("assets/music/level1.mp3"),
            "level2_menu": pygame.mixer.Sound("assets/music/level2.mp3"),

            "triangle": pygame.mixer.Sound("assets/sound_effect/mus_sfx_eyeflash.wav"),
            "hurt": pygame.mixer.Sound("assets/sound_effect/snd_break1.wav"),
            "dead": pygame.mixer.Sound("assets/sound_effect/mus_sfx_a_lithit.wav"),
            "lazer": pygame.mixer.Sound("assets/sound_effect/mus_sfx_rainbowbeam_1.wav"),

            "choose_option": pygame.mixer.Sound("assets/sound_effect/snd_block2.wav"),
            "confirm_option": pygame.mixer.Sound("assets/sound_effect/snd_select.wav"),
        }
        self.music_loaded = False

    def play_sfx(self, name):
        if name in self.sfx:
            self.sfx[name].play()

    def play_music(self, path, start_time=0.0, loop=-1, fade_ms=0):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loops=loop, start=start_time, fade_ms=fade_ms)

    def get_music_time(self):
        return pygame.mixer.music.get_pos() if self.music_loaded else 0

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)
        for s in self.sfx.values():
            s.set_volume(volume)
