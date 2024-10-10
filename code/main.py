import pygame
from os.path import join
import random


#classes:

class Player(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images','player.png')).convert_alpha()
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.direction = pygame.math.Vector2()
        self.speed = 300
        self.rotation = 0

        #cooldwon section
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

        #transform test
        


        # mask
        #self.mask = pygame.mask.from_surface(self.image)
        # mask_surf = mask.to_surface()
        # mask_surf.set_colorkey('black')  #all of pxels of one color invisible
       
        


    def update(self):
        self.player_input()
        self.laser_timer()
        
    
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        recent_keys = pygame.key.get_just_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a]) 
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf,self.rect.midtop,(all_sprites,laser_sprites))
            laser_sound.play()
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

class Star(pygame.sprite.Sprite):
    def __init__(self,groups,surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(random.randint(0,WINDOW_WIDTH),random.randint(0,WINDOW_HEIGHT)))
    
class Meteor(pygame.sprite.Sprite):
    def __init__(self,groups,surf):
        super().__init__(groups)
        self.original_image = surf
        self.image = self.original_image
        self.rect = self.image.get_frect(center=(random.randint(0,WINDOW_WIDTH),random.randint(-200,-50)))
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(random.uniform(-0.5,0.5),1)
        self.speed = random.randint(800 - game_speed,1000 - game_speed)
        self.rotation_speed = random.randint(10,100)
        self.rotation = 0

        

    def update(self):
        self.rect.center +=   self.direction * self.speed * dt 
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed* dt
        self.image = pygame.transform.rotozoom(self.original_image,self.rotation,1)
        self.rect = self.image.get_frect(center = self.rect.center)
     
class Laser(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        
        

    def update(self):
        self.rect.y -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.images = [pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]
        self.index = 0
        self.image = self.images[self.index]
        self.image = pygame.transform.rotozoom(self.image,0,1.5)
        self.rect = pos
        self.cooldown_time = 30
        self.explosion_time = 0


    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.explosion_time >= self.cooldown_time:
            if self.index < 20:
                self.index +=1
                self.image = self.images[self.index]
                self.image = pygame.transform.rotozoom(self.image,0,1.5)
                self.explosion_time = pygame.time.get_ticks()
            else: self.kill( )

class Special_item(pygame.sprite.Sprite):
    def __init__(self,groups,surf,pos):
        super().__init__(groups)
        self.image = surf
        #self.rect = pos
        self.image = pygame.transform.rotozoom(special_item_surf,0,0.05)
        self.rect = self.image.get_rect(center= pos)
    def update(self):
        self.rect.bottom += 5 
        

def collisions():
    global running, defeat_screen, meteor_crashed, final_score, current_time
    if pygame.sprite.spritecollide(player,meteor_sprites,True,pygame.sprite.collide_mask): #with added mask
        final_score = pygame.time.get_ticks()/100
        game_over_sound.play()
        running = False
        defeat_screen = True
        
    
    for item in special_item_sprites:
        collided_sprites= pygame.sprite.spritecollide(player,special_item_sprites,True,pygame.sprite.collide_mask)
        if collided_sprites:
            if random.choice(['player_speed','bullet_speed']) == 'player_speed':
                player.speed += 20
                text_surf = font.render('Speed increased!',True,'red',)
                text_rect = text_surf.get_rect(center=item.rect.center)
                display_surface.blit(text_surf,(50,50))
                flying_text(text_surf,text_rect)
            else:
                player.cooldown_duration -= 20
                text_surf = font.render('Shooting speed increased!',True,'red',)
                text_rect = text_surf.get_rect(center=item.rect.center)
                flying_text(text_surf,text_rect)
            

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites,True)
        if collided_sprites:
           laser.kill()
           meteor_crashed += 1
           
           for meteor in collided_sprites:
               Explosion(meteor.rect.center,all_sprites)
               explosion_sound.play()
               Special_item((all_sprites,special_item_sprites),random.choice([special_item_surf,special_item_surf]),meteor.rect.center)
    
    
def display_score():
    global current_time
    current_time = pygame.time.get_ticks()
    text_surf = font.render(str(int((current_time - start_time)/100)),True,(209, 206, 157))
    text_rect = text_surf.get_rect(midbottom=(WINDOW_WIDTH/2,150))
    display_surface.blit(text_surf,text_rect)
    
    pygame.draw.rect(display_surface,(209, 206, 157),text_rect.inflate(20,10).move(0,-8),5,10)

def speeding_game():

    global game_speed, last_speed_up
    curent_time = pygame.time.get_ticks()
    #print(curent_time/100 - last_speed_up/100)
    if game_speed > 100 and (curent_time/100 - last_speed_up/100) > 50:
        last_speed_up = pygame.time.get_ticks()
        game_speed -= 20
        pygame.time.set_timer(meteor_event, game_speed)

def game_over(meteor_crashed,final_score):
    global current_time, game_speed
    display_surface.fill((50,50,50))
    background_rect2 = background2_surf.get_rect(topleft=(0,0))
    display_surface.blit(background2_surf,background_rect2)
    text_surf = font_bigger.render("Game Over",True,(209, 206, 157))
    text_rect = text_surf.get_rect(midbottom=(WINDOW_WIDTH/2,200))
    display_surface.blit(text_surf,text_rect)
    text_surf = font.render(f"Meteores crashed: {meteor_crashed}",True,(209, 206, 157))
    text_rect = text_surf.get_rect(midbottom=(WINDOW_WIDTH/2,250))
    display_surface.blit(text_surf,text_rect)
    text_surf = font.render(f"Score: {int((final_score*100 - start_time)/100)}",True,(209, 206, 157))
    text_rect = text_surf.get_rect(midbottom=(WINDOW_WIDTH/2,300))
    display_surface.blit(text_surf,text_rect)
    text_surf = font_bigger.render("Press f to start again",True,(209, 206, 157))
    text_rect = text_surf.get_rect(midbottom=(WINDOW_WIDTH/2,WINDOW_HEIGHT - 200))
    if int(pygame.time.get_ticks()/100) % 8 <4:
        text_surf = font_bigger.render("Press f to start again",True,(135, 85, 95))
    display_surface.blit(text_surf,text_rect)

    player.rect.center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2)
    meteor_sprites.empty()
    menu_music.stop()
    
def menu():
    display_surface.fill((54, 24, 100))
    background_rect = background_surf.get_rect(topleft=(0,0))
    display_surface.blit(background_surf,background_rect)
    #comet_rect = comet_surf.get_rect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT-400))
    #display_surface.blit(comet_surf,comet_rect)
    text_surf = font_bigger.render("Space Shooter",True,(209, 206, 157))
    text_rect = text_surf.get_rect(midbottom=(WINDOW_WIDTH/2,200))
    display_surface.blit(text_surf,text_rect)
    text_surf = font.render("Press f to start",True,(209, 206, 157))
    text_rect = text_surf.get_rect(midbottom=(WINDOW_WIDTH/2,WINDOW_HEIGHT - 60))
    
    if int(pygame.time.get_ticks()/100) % 10 <5:
        display_surface.blit(text_surf,text_rect)

def flying_text(text_surf,text_rect):
    start_y = text_rect.y
    if start_y - 100 < text_rect.y:
        text_rect.y-=5
        display_surface.blit(text_surf,text_rect)
        print("o tak")
    

#general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space shooter')
menu_screen = True
defeat_screen = False
running = False
clock = pygame.time.Clock()
game_speed = 500
last_speed_up = 0
meteor_crashed = 0
final_score = 0
current_time = pygame.time.get_ticks()


#import section
star_surf = pygame.image.load(join('images','star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('images','meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images','laser.png')).convert_alpha()
comet_surf = pygame.image.load(join('images','comet.png')).convert_alpha()
background_surf = pygame.image.load(join('images','background4.jpg')).convert()
background_surf = pygame.transform.scale(background_surf,(WINDOW_WIDTH,WINDOW_HEIGHT))
background2_surf = pygame.image.load(join('images','background3.jpg')).convert()
background2_surf = pygame.transform.scale(background2_surf,(WINDOW_WIDTH,WINDOW_HEIGHT))
special_item_surf = pygame.image.load(join('images','innastar.png')).convert_alpha()


font = pygame.font.Font(join('images','Oxanium-Bold.ttf'),40)
font_bigger = pygame.font.Font(join('images','Oxanium-Bold.ttf'),100)
#music
laser_sound = pygame.mixer.Sound(join('audio','laser.wav'))
laser_sound.set_volume(0.2)
explosion_sound = pygame.mixer.Sound(join('audio','explosion.wav'))
explosion_sound.set_volume(0.2)
game_music = pygame.mixer.Sound(join('audio','game_music.wav'))
game_music.set_volume(0.2)
menu_music = pygame.mixer.Sound(join('audio','menu_music.mp3'))
game_music.play(loops=-1)
game_over_sound = pygame.mixer.Sound(join('audio','game_over.mp3'))
game_over_sound.set_volume(0.6)

#sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for i in range(20):
    Star(all_sprites,star_surf)
special_item_sprites = pygame.sprite.Group()
player = Player(all_sprites)

#custom event (meteor)
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event,game_speed)

while True:
    if running:
        dt = clock.tick(60)/1000 #getting delta time in seconds
        #event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == meteor_event:
                Meteor( (meteor_sprites,all_sprites), meteor_surf)
        #update game
        all_sprites.update()
        collisions()

        #draw game
        display_surface.fill((30, 21, 92))
        all_sprites.draw(display_surface)
        display_score()
        speeding_game()
        pygame.display.update()
        
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                running=False
                menu_screen = False
                defeat_screen=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    running = True
                    menu_screen = False
                    defeat_screen = False
                    final_score = 0  
                    meteor_crashed = 0  
                    current_time = 0  
                    game_speed = 500  
                    pygame.time.set_timer(meteor_event, game_speed)
                    all_sprites.empty()  
                    player = Player(all_sprites)  
                    for i in range(20):
                        Star(all_sprites,star_surf)
                    start_time = pygame.time.get_ticks()
                    menu_music.play(loops=-1)
                    game_music.stop()
        if menu_screen:
            display_surface.fill((120,120,120))
            menu()
            
        elif defeat_screen:
            game_over(meteor_crashed, final_score)
            
        pygame.display.update()

pygame.quit()