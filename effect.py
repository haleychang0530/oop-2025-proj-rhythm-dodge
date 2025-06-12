import pygame
import sprinkle

def hurt(o):
    """Play audio and visual effect when the player gets hurt."""
    ob=o.__class__.__name__
    print(ob)
    if ob=="FollowObstacle":
        sound = pygame.mixer.Sound("assets/music/biu.wav")
        sound.play()

    elif ob=="SinCircleObstacle" or "SinGearObstacle":
        #print("ding")
        sound = pygame.mixer.Sound("assets/music/ding.wav")
        sound.play()

    elif ob=="FollowCircleObstacle":
        sound = pygame.mixer.Sound("assets/music/bomb.wav")
        sound.play()

    elif ob=="LaserCircleObstacle" or "LaserObstacle":
        
        sound = pygame.mixer.Sound("assets/music/biu.wav")
        sound.play()

    elif ob=="GearObstacle" or "FollowGearObstacle" :
        #print("ding")
        sound = pygame.mixer.Sound("assets/music/ding.wav")
        sound.play()

    if ob=="CannonObstacle":
        # print("delarn")
        sound = pygame.mixer.Sound("assets/music/delarn.wav")
        sound.play()  

    elif ob=="Obstacle":
        sound = pygame.mixer.Sound("assets/music/slap.wav")
        sound.play()

def lazer():
    sound = pygame.mixer.Sound("assets\sound_effect\mus_sfx_rainbowbeam_1.wav")
    sound.set_volume(0.25)
    sound.play(maxtime=1000)  # 播放音效，最大音量为0.3


    
    