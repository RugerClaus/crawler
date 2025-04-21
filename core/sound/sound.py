import pygame

class SoundManager:
    def __init__(self, volume=0.5):
        pygame.mixer.init()
        self.music_tracks = {
            "menu": "assets/audio/menu_music.wav",
            "game": "assets/audio/game_music.wav",
            "intro": "assets/audio/intro_music.wav"
        }
        self.sound_effects = {
            "jump": 'assets/audio/jump.mp3',
            "plasma_rifle": 'assets/audio/weird_space_gun.wav',
            "pickup_potion" : 'assets/audio/pickup_potion.wav',
            "mechanical_item": "assets/audio/mechanical_weapon_pickup.wav",
            "magnum": "assets/audio/gunshot.mp3",
            "gold_coin": "assets/audio/coinsound1.wav",
            "silver_coin": "assets/audio/coinsound2.wav",
            "bronze_coin": "assets/audio/coinsound3.wav",
            "player_hurt": "assets/audio/player_hurt.wav",
            "game_over": "assets/audio/game_over.wav",
            "drink_potion": "assets/audio/drink_potion.wav",
            "no_more_item": "assets/audio/no_more_item.wav"
        }
        self.volume = volume
        self.music_active = True
        self.sfx_active = True

    def play_music(self, track_name, loop=True):
        if not self.music_active:
            return
        if track_name in self.music_tracks:
            if pygame.mixer.music.get_busy() and pygame.mixer.music.get_pos() > 0:
                return
            pygame.mixer.music.load(self.music_tracks[track_name])
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1 if loop else 0)

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_track = None

    def toggle_music(self,state):

        if self.music_active:
            pygame.mixer.music.stop()
            print("Music off")
            self.current_track = None
        else:
            if state in self.music_tracks:
                pygame.mixer.music.load(self.music_tracks[state])
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                self.current_track = state
                print(f"Music on: {state}")

        self.music_active = not self.music_active

    def set_volume(self, volume):
        self.volume = max(0, min(volume, 1))  # Ensure volume is between 0 and 1
        pygame.mixer.music.set_volume(self.volume)

    def play_sfx(self, sfx_name):
        if self.sfx_active and sfx_name in self.sound_effects:
            print("playing sound")
            sfx = pygame.mixer.Sound(self.sound_effects[sfx_name])
            sfx.set_volume(self.volume)
            sfx.play()

    def stop_sfx(self):
        pygame.mixer.stop()


    def toggle_sfx(self):
        self.sfx_active = not self.sfx_active
        print(f"SFX {'On' if self.sfx_active else 'Off'}")

    
    def sfx_status(self):
        return "On" if self.sfx_active else "Off"

    def music_status(self):
        if self.music_active == True:
            return "On"
        else:
            return "Off"