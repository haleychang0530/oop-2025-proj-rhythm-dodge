import pygame
import sprinkle

def hurt(screen,player,o):
    """Play audio and visual effect when the player gets hurt."""
    ob=o.__class__.__name__
    if ob=="FollowGearObstacle":
        sound = pygame.mixer.Sound("assets/music/biu.wav")
        sound.play()

    elif ob=="SinCircleObstacle":
        sound = pygame.mixer.Sound("assets/music/ding.wav")
        sound.play()
        sound = pygame.mixer.Sound("assets/music/dong.wav")
        sound.play()

    elif ob=="FollowCircleObstacle":
        sound = pygame.mixer.Sound("assets/music/bomb.wav")
        sound.play()

    elif ob=="LaserCircleObstacle":
        sound = pygame.mixer.Sound("assets/music/bomb.wav")
        sound.play()

    elif ob=="GearObstacle":
        #sound = pygame.mixer.Sound("assets/music/slap.wav")
        #sound.play()
        sound = pygame.mixer.Sound("assets/music/bomb.wav")
        sound.play()

    elif ob=="FollowGearObstacle" or "SinGearObstacle":
        sound = pygame.mixer.Sound("assets/music/gun.wav")
        sound.play()   

    elif ob=="Obstacle":
        sound = pygame.mixer.Sound("assets/music/slap.wav")
        sound.play()   


    
    