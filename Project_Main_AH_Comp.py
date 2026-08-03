#This Function that checks for input validation on name,email and age_input     
def input_validation():
    while True:
        name = input("Enter your name: ")
        name.strip()
        if len(name)> 20 :
            print("Name must be less than or equal 20 characters")
            continue
        if name == "":
            print("Name cannot be blank")
            continue

        email = input("Enter your email: ")
        email.strip()
        if "@" not in email or "." not in email.split("@")[-1]:
            print("Please enter a valid email address")
            continue

        age_input = input("Enter your age: ")
        age_input.strip()
        if not age_input.isdigit():
            print("Age must be a valid number")
            continue

        age = int(age_input)
        if age < 8 or age > 120:
            print("Age must be at greater than or equal to 8 but less than or equal to 120")
            continue

        return name, age,email

#Function that sorts the score 
def Partial_BubbleSort(scores_array):
    swapped = True
    n = len(scores_array)
    while swapped: 
        swapped = False
        for i in range(n-1):
            if scores_array[i] < scores_array[i+1]:
                scores_array[i],scores_array[i+1] = scores_array [i+1],scores_array[i]
        return scores_array

name,age,email = input_validation()

import pygame
import mysql.connector
import random
from sys import exit #Allows the program to exit properly

#This function establishes a connection to the local database server and creates a database if it doesnt exist    
def create_connection():
    global mydatabase,mycursor
    mydatabase = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""  
    )
    mycursor = mydatabase.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS Playerdatabase")
    mydatabase.database = "Playerdatabase"
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS playerdetails (
            player_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            age INT,
            highscore INT,
            level INT,
            retries INT
        )
    """)
    
create_connection()

#This function Updates or inserts player data everytime the player dies        
def update_or_inserts_records(name, age, email,highscore,level,retries):
    query = "SELECT player_id,highscore FROM playerdetails WHERE name = %s AND age = %s AND email = %s"
    mycursor.execute(query,(name,age,email))
    result = mycursor.fetchone()
    if result:
        player_id = result[0]
        previous_highscore = result[1]
        if highscore > previous_highscore:
            update_query = "UPDATE playerdetails SET highscore = %s,level = %s,retries = %s WHERE player_id = %s"
            mycursor.execute(update_query,(highscore,level,retries,player_id))
    else :
        insert_query = "INSERT INTO playerdetails(name,age,email,highscore,level,retries) VALUES (%s,%s,%s,%s,%s,%s)"
        mycursor.execute(insert_query,(name,age,email,highscore,level,retries))
    mydatabase.commit()

"""The Bird class represents the player so it handles the appearance,movement and collision mechanics of the player.
The bird or the player character can be controlled using this class."""   
class Bird(pygame.sprite.Sprite):
    def __init__(self):   #Constructor for Bird class  
        super().__init__()
        self.bird_frame_1 = pygame.image.load('Bird/Bird_frame_1.png').convert_alpha()  # Flapping image
        self.bird_frame_2 = pygame.image.load('Bird/Bird_frame_2.png').convert_alpha()  # Normal image
        self.image = self.bird_frame_2
        self.rect = self.image.get_rect(midbottom=(50, 100))
        self.gravity = 0

    """This function implements gravity on the bird and checks for collision with the ground 
    if a collision is detected true is returned else false"""
    def handleGravityAndCollision(self):  
        if game_active:
            self.gravity += 0.35
            self.rect.y += self.gravity
        if self.rect.bottom >= 420:
            self.rect.bottom = 420
            return True
        return False

    def flap(self):   #This function contains code to allow the bird to flap    
        if game_active:
            self.gravity = -5.75
            self.image = self.bird_frame_1

    def stop_flap(self):   #This function contains code to reset flap image 
        self.image = self.bird_frame_2

"""Pole class is responsible for npc (non-player controlled) characters which are the poles 
that the bird has to escape in order to survive.This class is responsible for movement,collision and appearance"""
class Pole(pygame.sprite.Sprite):
    def __init__(self, x, y, is_top):  #Constructor for Pole class                     
        super().__init__()
        self.image = pygame.image.load('Vertical pole/Pole_Bottom.png').convert_alpha()  #Sets image for bottom pole    
        if is_top:
            self.image = pygame.image.load('Vertical pole/Pole_Top.png').convert_alpha()   #Sets image for top pole  
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    # This function updates the position of the pole and removes it from the game if it moves off-screen.
    def update(self):
        if game_active: #As the game progresses the speed multiplier and speed is increased             
            self.rect.x -= self.speed * speed_multiplier
            if self.rect.right < 0:
                self.kill()   #Pole is removed if it goes out of the screen 


pygame.init()
screen = pygame.display.set_mode((900, 450)) #900 pixels horizontal and 450 pixels vertical 
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

water_surf = pygame.image.load('Water/water.png').convert_alpha()  #Water image  

#The single bird group is used for player character   
bird = pygame.sprite.GroupSingle()
bird.add(Bird())

#This list contains pole objects to spawn infinite instances.Because using a "Group" wouldn't meet project requirements.
obstacle_list = []
scores = [] #The scores array captures the player's score upon death         

GAP_SIZE = 600 #This constant determines the gap size between the top and bottom poles 
POLE_X_START = 950 #This constant determines where the pole starts from in the screen   
POLE_Y_MIN = 75 #This constant determines the minimum offset from the centre of the screen where the pole can go 
POLE_Y_MAX = 300 #This constant determines the maximum offset from the centre of the screen where the pole can go           

# Game state
game_active = False #This variable defines the game active state
game_over = False #This variable defines the game over state	       
score_reset_time = 0  # Tracks the start time of the score calculation
level = 1  #This variable keeps track of player level and updates it     
retries = 0   #This variable counts the number of retries the player makes     
speed_multiplier = 1 #This variable keeps track of the pole speed                                                           
next_level_score = 10  #This variable keeps count of the next score needed to increase the level and speed_multiplier
score_recorded = False #This variable ensures that score is recorded once each time the player plays the game
sorted = False #This variable ensures score is sorted once
highscore = 0  #This variable stores the highscore


#This function creates top and bottom poles with a random gap, adjusts their positions, and adds them to the obstacle list.   
def create_poles():
    gap_y = random.randint(POLE_Y_MIN, POLE_Y_MAX)
    top_pole = Pole(POLE_X_START, gap_y - GAP_SIZE / 2 - 330, True) 
    bottom_pole = Pole(POLE_X_START, gap_y + GAP_SIZE / 2, False)
    obstacle_list.append(top_pole)
    obstacle_list.append(bottom_pole)

#This function dynamically updates the scores with intended logic and displays it       
def update_and_display_score():
    """"pygame.ticks gives the time since the game started in ms so the score is 
    reset using score_reset_time,set when the game starts"""     
    score = int(pygame.time.get_ticks() / 1000) - score_reset_time
    score_surf = font.render(f'Score: {score}', False, 'Black')
    score_rect = score_surf.get_rect(center=(450, 20))
    screen.blit(score_surf, score_rect)
    return score

#This function displays the level and speed_multplier during the game     
def display_level_and_speed():
    level_surf = font.render(f'Level: {level}', False, 'Black')
    level_rect = level_surf.get_rect(center=(150, 20))
    screen.blit(level_surf, level_rect)
    speed_surf = font.render(f'Speed: {speed_multiplier:.1f}x', False, 'Black')
    speed_rect = speed_surf.get_rect(center=(750, 20))
    screen.blit(speed_surf, speed_rect)

font_large = pygame.font.Font(None, 50)
font = pygame.font.Font(None, 35)

# Creation of the start button 
start_button_rect = pygame.Rect(350, 200, 200, 80)
button_text = font_large.render("Start", False, (0, 0, 0))


# Creation of the retry button
retry_button_rect = pygame.Rect(390,300, 120, 60)
button2_text = font_large.render("Retry", False, (0, 0, 0))

# Main loop
while True:
    screen.fill('White')
    bird.draw(screen)
    for event in pygame.event.get(): #loops through all events in pygame
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if not game_active and not game_over:
        #The game can be started either by mousebutton press on start button or by pressing spacebar
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if start_button_rect.collidepoint(event.pos): 
                    game_active = True
                    #score_reset_time resets the score at the start of the game    
                    score_reset_time = int(pygame.time.get_ticks() / 1000) 
                    #The timer below is for the pole obstacle which is defined later
                    #change 1200 below if you want to control the poles spawn rate
                    pygame.time.set_timer(pygame.USEREVENT + 1, 1200) 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: #The same comments above apply here for keyboard press
                    game_active = True
                    score_reset_time = int(pygame.time.get_ticks() / 1000)  # Start the score timer
                    pygame.time.set_timer(pygame.USEREVENT + 1, 1200)

        #The bird can be flapped by either spacebar or mousebutton press  
        if game_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.sprite.flap()

        if game_active and event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                bird.sprite.stop_flap( )

        if game_active and event.type == pygame.MOUSEBUTTONDOWN:
            bird.sprite.flap()

        if game_active and event.type == pygame.MOUSEBUTTONUP:
            bird.sprite.stop_flap()

        if game_over:
            #The game can be restarted either by mousebutton press on retry button or by pressing spacebar.    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button_rect.collidepoint(event.pos):
                    game_active = True
                    game_over = False
                    bird.sprite.rect.midbottom = (50, 100)
                    bird.sprite.gravity = 0
                    score_recorded = False
                    obstacle_list.clear()
                    #Score time is reset for the next instance of score to be recorded accurately
                    score_reset_time = int(pygame.time.get_ticks() / 1000)
                    pygame.time.set_timer(pygame.USEREVENT + 1, 1200)
                    level = 1
                    speed_multiplier = 1
                    retries += 1 
                    #Next level score is reset to update speed and level accurately   
                    next_level_score = 10

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    game_over = False
                    bird.sprite.rect.midbottom = (50, 100)
                    bird.sprite.gravity = 0
                    score_recorded = False
                    obstacle_list.clear()
                    score_reset_time = int(pygame.time.get_ticks() / 1000)  # Reset the score timer
                    pygame.time.set_timer(pygame.USEREVENT + 1, 1200)
                    retries += 1 
                    level = 1
                    speed_multiplier = 1
                    next_level_score = 10

        if game_active and event.type == pygame.USEREVENT + 1:
            create_poles()  #To add poles when the game is active  

    if not game_active and not game_over:  #Display for game menu  
        pygame.draw.rect(screen,(0,255,0), start_button_rect)
        screen.blit(button_text, (start_button_rect.x + 50, start_button_rect.y + 20))
        start_text = font.render("Press SPACEBAR or Click the button to Start",False , 'Black')
        start_rect = start_text.get_rect(center=(450, 150))
        screen.blit(start_text, start_rect)

    if game_active:    
        #The for loop updates each pole, draws it on screen, and ends the game if collision with the bird occurs.
        for pole in obstacle_list:
            pole.update()
            screen.blit(pole.image, pole.rect)
            if pygame.sprite.collide_rect(bird.sprite, pole): #Collision Mechanics between the bird and pole       
                game_active = False  
                game_over = True
                break

        score = update_and_display_score()

        #Whenever the score is greater than the next_level_score the level and speed_multiplier is increased 	
        if score >= next_level_score:
            level += 1
            next_level_score += 10
            speed_multiplier += 0.1

        display_level_and_speed()
        
        #handleGravityAndCollision method takes care of bird gravity and returns true if the bird collides with the ground 
        if bird.sprite.handleGravityAndCollision():
            game_active = False
            game_over = True


    if game_over:
        #score should be recorded only once and to do that score_recorded exists 
        if not score_recorded:
            scores.append(score)
            score_recorded = True
        #score should be sorted only once and to do that score_recorded exists 
        if not sorted :
            scores = Partial_BubbleSort(scores)
        if scores:
            highscore = scores[0]
            
        #Next few lines of code is focused on the UI of the game    
        pygame.draw.rect(screen, (0, 255, 0), retry_button_rect)
        screen.blit(button2_text, (retry_button_rect.x + 15, retry_button_rect.y + 15))
        game_over_text = font.render("Game Over!           Highscore: " + str(highscore) , True, 'Black')
        game_over_rect = game_over_text.get_rect(center=(450, 150))
        screen.blit(game_over_text, game_over_rect)
        retry_info_text = font.render("Press SPACEBAR or click the button to retry", True, 'Black')
        retry_info_rect = retry_info_text.get_rect(center=(450, 200))
        screen.blit(retry_info_text, retry_info_rect)
        #The method below updates the records in the database or inserts the data like highscore,level and retries
        update_or_inserts_records(name, age, email,highscore,level,retries)
        #The next few lines of code is focused on UI again     
        database_updation_text = font.render("Player details and the highscore are updated to the database", True, 'Black')
        database_updation_rect = database_updation_text.get_rect(center=(450, 250))
        screen.blit(database_updation_text,database_updation_rect)


    screen.blit(water_surf, (0, 420))   #water image  
    pygame.display.update()
    clock.tick(60)  
