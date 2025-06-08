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


    
    