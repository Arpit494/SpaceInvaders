import pygame
import random
import math
from pygame import mixer
#import speech_recognition as sr 
#import threading
#from gtts import gTTS
#import os
#from time import sleep

pygame.init()

screen = pygame.display.set_mode((800,600))     # Creating Display for game
pygame.display.set_caption("Space_Inveder")     # Set name for game
icon = pygame.image.load("ufo.png")             # Loading image for game icon  
pygame.display.set_icon(icon)                   # Set game icon
spaceshipImg = pygame.image.load("player.png")  # Load Image for Spaceship
BackgroungImg = pygame.image.load("background.png").convert()    # Load image for Background
BulletImg = pygame.image.load("bullet.png")

# Adding Background Music to our Game
mixer.music.load("background.wav")
mixer.music.play(-1)

# Coordinate Axis for Bullet 
Bullet_X = 0
Bullet_Y = 460
BulletX_change = 0
BulletY_change = 1
Bullet_State = 'ready'


# Coordinate Axis for Spaceships
Spaceship_X = 380
Spaceship_Y = 500
Spaceship_Speed = 0.4

#Coordinate Axis for Enemy and loading image
EnemyImg = []
Enemy_X = []
Enemy_Y = []
Enemy_Speed = []
Change_enemy_Y_coordinate = []
numbers_of_Enemy = 6
count = []

for i in range(numbers_of_Enemy):
    EnemyImg.append(pygame.image.load("enemy1.png"))
    Enemy_X.append(random.randint(0,740))
    Enemy_Y.append(random.randint(0,200))
    Enemy_Speed.append(0.3)
    Change_enemy_Y_coordinate.append(50)
    count.append(0)


'''
command =""
def Get_Audio():
    global command
    r = sr.Recognizer()
    print("Speak Something")
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))

    command = said.upper() '''


# Creating Spaceship along with there movement
def Create_Spaceship():
    global Spaceship_X,Spaceship_Y,Bullet_X
    # Movement of Spaceships
    #print(command)
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] )  and Spaceship_X>0 :
        Spaceship_X -= Spaceship_Speed
    if (keys[pygame.K_RIGHT])and Spaceship_X <740:
        Spaceship_X += Spaceship_Speed 
    if (keys[pygame.K_SPACE]):
        if Bullet_State is "ready":
            Bullet_Sound = mixer.Sound("laser.wav")
            Bullet_Sound.play()
            Bullet_X = Spaceship_X
            Fire_Bullet(Bullet_X, Bullet_Y)   
    screen.blit(spaceshipImg,(Spaceship_X,Spaceship_Y))
    Bullet_Movement() 


def Fire_Bullet(BulletX, BulletY):
    global Bullet_State
    Bullet_State = 'fire'
    screen.blit(BulletImg,(BulletX+16, BulletY+10))
    #screen.blit(BulletImg,(BulletX-5, BulletY+10))


def Bullet_Movement():
    global Bullet_Y,Bullet_State
    if Bullet_Y <= 0:
        Bullet_Y = 460
        Bullet_State = 'ready'
    if Bullet_State is 'fire':
        Fire_Bullet(Bullet_X, Bullet_Y)
        Bullet_Y -= BulletY_change     

# Creating Enemy 
def Create_Enemy():
    global Enemy_X,Enemy_Y,count
    for i in range(numbers_of_Enemy):
        screen.blit(EnemyImg[i],(Enemy_X[i],Enemy_Y[i]))
        if Enemy_Y[i] >= 450:
            for j in range(numbers_of_Enemy):
                Enemy_Y[j] = 2000
            Game_Over()
            break    
        # Movement of Enemy
        #for i in range(numbers_of_Enemy):
        if Enemy_X[i] < 735 and count[i] == 0 : Enemy_X[i] += Enemy_Speed[i]
        elif (Enemy_X[i] >= 735 and count[i] == 0) or Enemy_X[i] <= 0:
            Enemy_Y[i] += Change_enemy_Y_coordinate[i] ;count[i] = 1 
            if Enemy_X[i] <= 0 : count[i] = 0
        elif  count[i] == 1: Enemy_X[i] -= Enemy_Speed[i]
        Kill_Enemy(i)


game_over_text = pygame.font.Font("freesansbold.ttf", 64)
# Game Over Function
def Game_Over():
    gameover = game_over_text.render("GAME OVER", True, (255,255,255))
    screen.blit(gameover,(200, 250))


# Collision Function
def Collision(Enemy_X,Enemy_Y,Bullet_X,Bullet_Y):
    distance = math.sqrt(math.pow(Enemy_X-Bullet_X,2) + math.pow(Enemy_Y-Bullet_Y,2))
    if distance < 30:
        return True
    return False 

Score = 0
font = pygame.font.Font("freesansbold.ttf", 32)

# Display Score Function
def Display_Score():
    score = font.render("Score: " + str(Score), True, (255,255,255))
    screen.blit(score,(10, 10))

# Kill Enemy
def Kill_Enemy(i):
    global Score,Enemy_X,Enemy_Y,Bullet_X,Bullet_Y
    if Collision(Enemy_X[i],Enemy_Y[i],Bullet_X,Bullet_Y):
        Kill_Sound = mixer.Sound("explosion.wav")
        Kill_Sound.play()
        Bullet_Y = 480
        Bullet_State = 'ready'
        Score += 1
        Enemy_X[i] = random.randint(0,740)
        Enemy_Y[i] = random.randint(0,200)

y = 0
# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    
    #screen.fill((0,0,0))                     # Filling Background with balck color 
    # Movement of background
    rel_Y = y % BackgroungImg.get_rect().height
    screen.blit(BackgroungImg, (0, rel_Y - BackgroungImg.get_rect().height))
    if rel_Y < 600:
        screen.blit(BackgroungImg,(0, rel_Y))
    y -= 0.2   
    '''
    t1 = threading.Thread(target=Create_Spaceship, name='t1') 
    t2 = threading.Thread(target=Get_Audio, name='t2')   
  
    # starting threads 
    t1.start() 
    t2.start() 
  
    # wait until all threads finish 
    t1.join() 
    t2.join() '''
    Create_Spaceship()                       # Calling Create_Spaceship function
    Create_Enemy()                           # Calling Create_Enemy function
    Display_Score()
    pygame.display.update()                  # Update screen after donig all changes  