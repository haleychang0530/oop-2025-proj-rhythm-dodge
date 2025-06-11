import pygame

def hurt(o):
    """Play audio and visual effect when the player gets hurt."""
    ob = o.__class__.__name__
    if ob=="FollowObstacle":
        sound = pygame.mixer.Sound("assets/sound_effect/snd_arrow.wav")
        sound.play()

    elif ob=="SinCircleObstacle" or "SinObstacle" or "SinGearObstacle":
        #print("ding")
        sound = pygame.mixer.Sound("assets/sound_effect/old/ding.wav")
        sound.play()

    elif ob=="FollowCircleObstacle":
        sound = pygame.mixer.Sound("assets/sound_effect/snd_battlefall.wav")
        sound.play()

    if ob=="LaserCircleObstacle" or "LaserObstacle":
        lazer()

    elif ob=="GearObstacle" or "FollowGearObstacle" :
        #print("ding")
        sound = pygame.mixer.Sound("assets/sound_effect/old/ding.wav")
        sound.play()

    if ob=="CannonObstacle":
        # print("delarn")
        sound = pygame.mixer.Sound("assets/sound_effect/snd_buyitem.wav")
        sound.play()  

def lazer():
    sound = pygame.mixer.Sound("assets/sound_effect/mus_sfx_rainbowbeam_1.wav")
    sound.set_volume(0.35)
    sound.play(maxtime=1000)  # 播放音效，最大音量为0.3


    
    