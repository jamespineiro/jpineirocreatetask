# This is a cannon game where you upgrade your cannon's shot distance earns you coins.
# You buy cannon upgrades with these coins, such as a coin multiplier and cannon power upgrade.
# You can also traverse to 2 different environments to shoot your cannon in.
# Once you are first in the game, keep in mind that you can click on the bottom right button
# for infinite coins, for review purposes.

from sys import exit 
import pygame

# This whole game was created with help of the pygame library.
# All art for this game was created by me.
# All sound effects were gathered from online at freesound.org 
# All music was created by Zakiro and is free for all commerical and non-commercial projects.
# Link to Zakiro music page: https://zakiro101.itch.io/free-casual-game-music-pack-vol-2 

# Initiates pygame and the screen display to the computers fullscreen, also sets variables for the screen
# width and height, along with importing the primary font of the game in.
# (Font is free to use for non-commerical purposes only)
pygame.init()
pygame.display.init()
pygame.display.set_caption('Cannon Game')
width = 1440
height = 900
size = (width,height)
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
font = pygame.font.Font('font/Ticketing.ttf',30)
width, height = screen.get_size()
clock = pygame.time.Clock()
keys = pygame.key.get_pressed()

# Sets lists to determine the Ball sprite cost for coin upgrades (That's why they are up so much higher 
# than the rest), and also creates booleans to determine if its the first frame of a cannon shot, or 
# if the ball is already mid air (To determine the velocity and the simulated gravities effect on it)
new_start = False
coin_level = 0
coin_index = [.05,.1,.2,.3,.4,.5,.6,.7,.7]
cost_index = [5,10,50,150,500,1000,10000,10000]
moon_mode = False
new_moon = False

# Creates a new Ball class, details inside
class Ball(pygame.sprite.Sprite):
    # Initiates the balls actual stats and starting location, alongside a list to iterate through
    # levels as the player buys more speed upgrades
    def __init__(self):
        super().__init__()
        global speed_level, moon_mode, new_moon
        
        self.gravity = 0
        
        speed_level = 0
        self.speed_levels = [10,20,30,40,50,60,70,80,80]
        self.original_speed_levels = [10,20,30,40,50,60,70,80,80]
        self.speed = self.speed_levels[speed_level]
        self.start_x = 200
        self.start_y = 635

        self.image = pygame.image.load('ball/ball.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (self.start_x,self.start_y))
        self.height = 32
        
    # Used to set the speed back to level 1 for the first shot once the player gets on the moon. 
    # Had a bug where the player would have max stats for the first shot on the moon, and 
    # this is how I fixed it. 
        self.speed1 = 10

        self.ball = pygame.image.load('ball/ball.png').convert_alpha()
        self.gravity_timer = 0

# Moves the ball every frame depending on the speed level, and sets the speed to 0 once you hit 
# the ground so that the ball doesnt keep falling
    def move(self):
        if new_moon:
            self.rect.x+=self.speed1
            self.rect.y-=self.speed1
            if self.rect.y > 600:
                self.speed1 = 0
        else:
            self.rect.x+=self.speed
            self.rect.y-=self.speed
# Constantly brings the ball down by a set amount per second to imitate gravity. When on the moon, 
# gravity is severely cut
    def apply_gravity(self):
            if not moon_mode:
                self.gravity+=.9
            elif moon_mode:
                self.gravity+=.21
            self.rect.y+=self.gravity
            if self.rect.bottom >= 640 + self.height:
                self.gravity = 0
                self.rect.bottom = 640 + self.height
                self.speed/=7
# Slows the ball down once it hits the ground    
    def apply_friction(self):
        if self.rect.y >= 640 + self.height:
            if self.speed<=0:
                self.speed = 0
            else:
                self.speed -= .9
# Checks for the conditions of the ball, and then applies gravity, moves, and checks for ground 
# friction every frame.
    def update(self):
        global new_start
        if new_start and self.rect.y >=670-self.height:
            self.gravity = 0
            self.speed = self.original_speed_levels[speed_level]
            new_start = False
            self.rect.y = 600
            self.rect.x = 200
        else:
            self.apply_gravity()
            self.apply_friction()
            self.move()

class CameraGroup(pygame.sprite.Group):
    # Initiates the camera and its starting variables, which allow
    # It to focus in the center of the screen, and also import environment surfaces
    def __init__(self):
        global moon_mode, earth_x, earth_y
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        # Camera Offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0]//2
        self.half_h = self.display_surface.get_size()[1]//2
        # Cannon
        self.cannon_surf = cannon1
        self.cannon_rect = self.cannon_surf.get_rect(topleft = (150,535))
        # Moon and sand ground surfaces
        self.moon_ground_surf = moon_ground
        self.moon_ground_rect = self.moon_ground_surf.get_rect(topleft = (-550,660))
        self.ground_surf = ground
        self.ground_rect = self.ground_surf.get_rect(topleft = (-550,660))
        # Applies the orange transitional sky if youre on Earth.
        if not moon_mode:
            self.horizon_surf = horizon
            self.horizon_rect = self.horizon_surf.get_rect(bottomleft = (-550,-4339))
    # Centers the camera
    def center_target_camera(self,target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h
    # Creates offsets for each surface/image in the environment and moves them
    # Depending on the ball's location (Example, if the ball moves right, everything else moves left)
    def custom_draw(self,ball):
        
        self.center_target_camera(ball)

        if not moon_mode:
            horizon_offset = self.horizon_rect.bottomleft - self.offset
            self.display_surface.blit(self.horizon_surf,horizon_offset )

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)
        
        #Cannon
        cannon_offset = self.cannon_rect.topleft - self.offset
        self.display_surface.blit(self.cannon_surf,cannon_offset)

        if not moon_mode:
            ground_offset = self.ground_rect.topleft-self.offset
            self.display_surface.blit(self.ground_surf,ground_offset)
        if moon_mode:
            moon_ground_offset = self.moon_ground_rect.topleft-self.offset
            self.display_surface.blit(self.moon_ground_surf,moon_ground_offset)

# Sets GUI variables for coin balance, distance record, current altitude, and current distance
balance = 0
record = 0
altitude = 0
distance = 0

# Updates and displays balance when in motion
def update_earnings():
    good_balance = (int)(balance)
    if not moon_mode:
        balance_text = coin_font.render(f'{good_balance}',False,("#ead4aa"))
    if moon_mode:
        balance_text = coin_font.render(f'{good_balance}',False,("#Fad6FF"))
    balance_text_rect = balance_text.get_rect(midleft = (width - 230,90))
    screen.blit(balance_text,balance_text_rect)

# Updates and displays distance record if you reach a new highest distance
def update_record():
    if not moon_mode:
        record_text = coin_font.render(f'{record}',False,("#ead4aa"))
    if moon_mode:
        record_text = coin_font.render(f'{record}',False,("#Fad6FF"))
    record_text_rect = record_text.get_rect(midleft = (140,90))
    screen.blit(record_text,record_text_rect)

# Updates and displays current altitude as you get higher and lower
def update_altitude():
    if not moon_mode:
        altitude_text = coin_font.render(f'{altitude}',False,("#ead4aa"))
    if moon_mode:
        altitude_text = coin_font.render(f'{altitude}',False,("#Fad6FF"))
    altitude_text_rect = altitude_text.get_rect(midleft = (140,340))
    screen.blit(altitude_text,altitude_text_rect)

# Updates and displays current distance
def update_distance():
    if not moon_mode:
        distance_text = coin_font.render(f'{distance}',False,("#ead4aa"))
    if moon_mode:
        distance_text = coin_font.render(f'{distance}',False,("#Fad6FF"))
    distance_text_rect = distance_text.get_rect(midleft = (140,210))
    screen.blit(distance_text,distance_text_rect)

# Updates and displays current FPS
def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(f'{fps} FPS',1,pygame.Color("Yellow"))
    screen.blit(fps_text,(10,5))

# Bool conditions and timers

# An infinite while loop that runs the game while it is true
running = True
# True when player is at the title screen, runs title screen components
menu = True
# True when player is at the 'shop' or pregame screen, runs 'shop'/pregame screen components
pregame = False
# True when pregame 'fire' button is pressed, 
game = False
# True when player purchases the "shoot for the stars" upgrade (Wins you the game)
win = False
# Wait before you can fire again after entering shop
wait = 0
# Displayed "Level _ out of 8 for cannon"
display_level = 1
# Displayed "Level _ out of 8 for coin multiplier"
cdisplay_level = 1
# True if hovering over fire button
selected = False
# True if hovering over cannon upgrade button
cannon_upgrade_selected = False
# True if hovering over coin upgrade button
coin_upgrade_selected = False
# True if hovering over "buy moon environment" button
moon_selected = False
# True if hovering over "Shoot for the stars (Win the game)" button
win_button_selected = False
# True if hovering over "AP graders click here for infinite coins" button
max_coins_selected_bool = False
# True if hovering over "auto fire" button, regardless of if its purchased or not
autofire_selected = False
# True if player clicked on "AP graders click here for infinite coins" button
infinite_coins = False
# True if cannon upgrade level < 5
shop_1 = True
# True if cannon upgrade level >= 5 and <8 and coin upgrade level is less than 8
shop_2 = False
# True if cannon and coin levels are both 8
shop_3 = False
# Same conditions as shop 1, but once player is on the moon (Comes after completing shop 3 and 
# purchasing moon)
shop_4 = False
# Same conditions as shop 2, but once player is on the moon (Comes after completing shop 3 and 
# purchasing moon)
shop_5 = False
# Same conditions as shop 3, but once player is on the moon (Comes after completing shop 3 and 
# purchasing moon)
shop_6 = False
# Is true if auto fire mode is on, causes shop to be inaccessible
auto_shop = False
# Is true if player hovers over "quit" button in the victory screen
quit_selected_bool = False
# Is true if auto fire is on (Available after purchase)
auto_fire = False
# Is true once auto fire is purchased for 500 coins
auto_purchased = False
# Creates a cooldown for the auto fire shots, in order to imitate the "wait" timer fire cooldown
# after entering shop stage
auto_fire_wait = 0
# Waits a few frames for after the ball hit the ground to return back to the "shop" stage of the
# game
auto_fire_return_wait = 0
# Makes it so that the earth_shop_music only plays once and loops infinitely, rather than having
# multiple of the same song playing at once.
earth_shop_music_count = 0
# Makes it so that the moon_shop_music only plays once and loops infinitely, rather than having
# multiple of the same song playing at once.
moon_shop_music_count = 0
# Makes it so that the title_music only plays once and loops infinitely, rather than having
# multiple of the same song playing at once.
title_music_count = 0
# Makes it so that the victory_music only plays once and loops infinitely, rather than having
# multiple of the same song playing at once.
victory_music_count = 0
# Makes it so that the cannon fire sound only plays once when the ball fires.
shot_sound_count = 0
# Makes it so that the sand sound only plays once when the ball lands.
sand_count = 0
# Is true when the max_coins, fire, and auto_fire buttons are in "blink" mode
p_blinking = False
# Switches value of p_blinking every 50 frames
p_blink = 0
# Incriments to 50 and then allows the user to return to the shop menu. Count starts 
returnb_count = 0
# Is true when returnb_count >= 50; When returnbool is true, the return button is accessible
# and the icon displays
returnbool = False

# Cannon surface load (Was originally going to add multiple cannons but I scrapped the idea,
# hence the 'cannon1' name)

cannon1 = pygame.image.load('Cannon/Cannon1.png').convert_alpha()

# Environment surface loads (rotozoom makes the moon_ground twice as big and assigns
# title_ground to that)
ground = pygame.image.load('Images/Ground.png').convert_alpha()
horizon = pygame.image.load('Images/2.png').convert_alpha()
moon_ground = pygame.image.load('Images/moon_ground.png').convert_alpha()
title_ground = pygame.transform.rotozoom(moon_ground,0,2)

# Creates a new ball object, called 'ball', and adds ball to that camera group so
# that the camera will follow it
ball = Ball()
camera_group = CameraGroup()
camera_group.add(ball)

# Imports background music
music_volume = .2
title_music = pygame.mixer.Sound('Soundtrack (Credit to Zakiro on itch.io, free for commerical and non-commercial use)/Track 1 (Lets Go).wav')
earth_shop_music = pygame.mixer.Sound('Soundtrack (Credit to Zakiro on itch.io, free for commerical and non-commercial use)/Track 4 (The Cafe).wav')
moon_shop_music = pygame.mixer.Sound('Soundtrack (Credit to Zakiro on itch.io, free for commerical and non-commercial use)/Track 2 (Party Tonight).wav')
victory_music = pygame.mixer.Sound('Soundtrack (Credit to Zakiro on itch.io, free for commerical and non-commercial use)/Track 7 (Panorama).wav')

# Imports sound effects and sets their volume
cannon_and_sand_volume = .3
button_volume = .5
cannon_fire_sound = pygame.mixer.Sound('Sound Effects/cannonfire.wav')
cannon_fire_sound.set_volume(cannon_and_sand_volume)
error_sound = pygame.mixer.Sound('Sound Effects/error.aiff')
error_sound.set_volume(button_volume)
buy_sound = pygame.mixer.Sound('Sound Effects/chaching.wav')
buy_sound.set_volume(button_volume)
press_sound = pygame.mixer.Sound('Sound Effects/press.wav')
press_sound.set_volume(button_volume)
sand_sound = pygame.mixer.Sound('Sound Effects/sand.wav')
sand_sound.set_volume(cannon_and_sand_volume)

# Creates surfaces for sprites and text

# Loads in coin image and font for the balance variable 
coin_icon = pygame.image.load('Images/coinicon.png').convert_alpha()
coin_font = pygame.font.Font('font/Ticketing.ttf',100)

# Loads in the image displaying how upgrades don't show until the round after
# you buy them, along with the moon alternative
warning = pygame.image.load('images/reloadwarning.png').convert_alpha()
warning_rect = warning.get_rect(midtop = (width/2,590))
moon_warning = pygame.image.load('images/moonreloadwarning.png').convert_alpha()
moon_warning_rect = moon_warning.get_rect(midtop = (width/2,590))

# Loads in the texts that display the level and cost of upgrades
slevel_text = pygame.font.Font('font/Ticketing.ttf',40)
level_text = slevel_text.render(f'LEVEL {display_level} OF 8',False,("#000000"))
level_text_rect = level_text.get_rect(midleft = (width/2-100,250))
clevel_text = slevel_text.render(f'LEVEL {display_level} OF 8',False,("#000000"))
clevel_text_rect = clevel_text.get_rect(midleft = (width/2-100,410))
clevel_cost = slevel_text.render(f'LEVEL {cdisplay_level+1} COST:{cost_index[coin_level]}',False,("#000000"))
clevel_cost_rect = clevel_cost.get_rect(midleft = (width/2-100,370))
canlevel_cost = slevel_text.render(f'LEVEL {display_level+1} COST:{cost_index[speed_level]}',False,("#000000"))
canlevel_cost_rect = canlevel_cost.get_rect(midleft = (width/2-100,210))

# Same as above but for the moon environment upgrade
moon_text = slevel_text.render('COST:50000',False,("#000000"))
moon_text_rect = moon_text.get_rect(midleft = (width/2-80,565))
moon_text_name = slevel_text.render('THE MOON',False,("#000000"))
moon_text_name_rect = moon_text.get_rect(midleft = (width/2-80,525))

# Same as above but to win the game
win_text = slevel_text.render('COST:99999',False,("#000000"))
win_text_rect = moon_text.get_rect(midleft = (width/2-80,565))
win_text_name = slevel_text.render('WIN THE GAME',False,("#000000"))
win_text_name_rect = moon_text.get_rect(midleft = (width/2-80,525))

# Loads in the image for the 'fire' button, the blinking alternative, and the
# hovered/selected alternative. Also generates the rects for these
fire_button = pygame.image.load('Images/fireicon.png').convert_alpha()
fb_rect = fire_button.get_rect(midbottom = (width/2,850))
fire_blinking = pygame.image.load('Images/fireblinking.png').convert_alpha()
fbb_rect = fire_blinking.get_rect(midbottom = (width/2,850))
fire_hovered = pygame.image.load('Images/firehighlighted.png').convert_alpha()
fh_rect = fire_hovered.get_rect(midbottom = (width/2,850))
fire_faded = pygame.image.load('Images/firefaded.png').convert_alpha()
fbfade_rect = fire_faded.get_rect(midbottom = (width/2,850))

# Same as above but for once the player is on the moon
moon_fire_button = pygame.image.load('Images/moonfireicon.png').convert_alpha()
moon_fb_rect = moon_fire_button.get_rect(midbottom = (width/2,850))
moon_fire_blinking = pygame.image.load('Images/moonfireblinking.png').convert_alpha()
moon_fbb_rect = moon_fire_blinking.get_rect(midbottom = (width/2,850))
moon_fire_hovered = pygame.image.load('Images/moonfirehighlighted.png').convert_alpha()
moon_fh_rect = moon_fire_hovered.get_rect(midbottom = (width/2,850))

# Loads in the images for the three Earth shop variations, and generates the
# rects for these as well
shop = pygame.image.load('Images/shop.png').convert_alpha()
shop_rect = shop.get_rect(midbottom = (width/2,600))
starter_shop = pygame.image.load('Images/startershop.png').convert_alpha()
starter_shop_rect = starter_shop.get_rect(midbottom = (width/2,600))
mid_shop = pygame.image.load('Images/midshop.png').convert_alpha()
mid_shop_rect = mid_shop.get_rect(midbottom = (width/2,600))
auto_fire_shop = pygame.image.load('Images/autofireshop.png').convert_alpha()

# Loads in the images for the three moon shop variations, and generates the
# rects for these as well
moon_shop = pygame.image.load('Images/moonshop.png').convert_alpha()
moon_shop_rect = moon_shop.get_rect(midbottom = (width/2,600))
moon_starter_shop = pygame.image.load('Images/moonstartershop.png').convert_alpha()
moon_starter_shop_rect = moon_starter_shop.get_rect(midbottom = (width/2,600))
moon_mid_shop = pygame.image.load('Images/moonmidshop.png').convert_alpha()
moon_mid_shop_rect = moon_mid_shop.get_rect(midbottom = (width/2,600))

# Loads in the image for the cannon upgrade button, the blinking alternative, 
# and the hovered/selected alternative. Also generates the rects for these
cannon_upgrade_icon = pygame.image.load('Images/cannonupgradeicon.png').convert_alpha()
cannon_upgrade_icon_rect = cannon_upgrade_icon.get_rect(midbottom = (560,260))
cannon_upgrade_icons = pygame.image.load('Images/cannonupgradeiconselected.png').convert_alpha()
cannon_upgrade_icons_rect = cannon_upgrade_icons.get_rect(midbottom = (560,260))

# Loads in the image for the coin upgrade button, the blinking alternative, 
# and the hovered/selected alternative. Also generates the rects for these
coin_upgrade_icon = pygame.image.load('Images/coinupgradeicon.png').convert_alpha()
coin_upgrade_icon_rect = coin_upgrade_icon.get_rect(midbottom = (560,437))
coin_upgrade_icons = pygame.image.load('Images/coinupgradeiconselected.png').convert_alpha()
coin_upgrade_icons_rect = coin_upgrade_icons.get_rect(midbottom = (560,437))

# Loads in the image for the 'play' button, the blinking alternative,
# and the hovered/selected alternative. Also generates the rects for these
play = pygame.image.load('Images/play.png').convert_alpha()
play_rect = play.get_rect(midbottom = (width/2,850))
playb = pygame.image.load('Images/playblink.png').convert_alpha()
playb_rect = playb.get_rect(midbottom = (width/2,850))
plays = pygame.image.load('Images/playselected.png').convert_alpha()
plays_rect = plays.get_rect(midbottom = (width/2,850))

# Loads in the menu cannon image, which is just a bigger cannon. It also loads in the 
# menu ground, which follows these same rules. It also loads in the menu and win screen text images
menu_cannon = pygame.image.load('Cannon/menu_cannon.png').convert_alpha()
menu_cannon_rect = menu_cannon.get_rect(midbottom = (300,670))
menu_ground = pygame.image.load('Images/menu_ground.png').convert_alpha()
menu_count = 0
menu_title = pygame.image.load('Images/title.png').convert_alpha()
win_title = pygame.image.load('Images/wintitle.png').convert_alpha()


# Loads in the image for the 'return' button, the blinking alternative, the faded/inaccessible 
# alternative, and the hovered/selected alternative. Also generates the rects for these
returnb = pygame.image.load('Images/returnbutton.png').convert_alpha()
returnb_rect = returnb.get_rect(midbottom = (width/2,850))
returnb_fade = pygame.image.load('Images/return_faded.png').convert_alpha()
returnb_fade_rect = returnb_fade.get_rect(midbottom = (width/2,850))
returnb_blink = pygame.image.load('Images/return_blinking.png').convert_alpha()
returnb_blink_rect = returnb_blink.get_rect(midbottom = (width/2,850))
returnb_selected = pygame.image.load('Images/return_selected.png').convert_alpha()
returnb_selected_rect = returnb_selected.get_rect(midbottom = (width/2,850))

# Same as above but for the moon environment
moon_returnb = pygame.image.load('Images/moonreturnbutton.png').convert_alpha()
moon_returnb_rect = moon_returnb.get_rect(midbottom = (width/2,850))
moon_returnb_blink = pygame.image.load('Images/moonreturn_blinking.png').convert_alpha()
moon_returnb_blink_rect = moon_returnb_blink.get_rect(midbottom = (width/2,850))
moon_returnb_selected = pygame.image.load('Images/moonreturn_selected.png').convert_alpha()
moon_returnb_selected_rect = moon_returnb_selected.get_rect(midbottom = (width/2,850))

# These three load in images for each GUI counter (balance,distance,alti)
record_icon = pygame.image.load('Images/recordicon.png').convert_alpha()
altitude_icon = pygame.image.load('Images/altitudeicon.png').convert_alpha()
distance_icon = pygame.image.load('Images/distanceicon.png').convert_alpha()

# These load in images and create rects for the moon purchase and win buttons, in 
# order to create the image and the hitbox for these
moon_environment_icon = pygame.image.load('Images/moonenvironmenticon.png').convert_alpha()
moon_environment_icon_rect = moon_environment_icon.get_rect(midbottom = (570,580))
moon_environment_icons = pygame.image.load('Images/moonenvironmenticonselected.png').convert_alpha()
moon_environment_icons_rect = moon_environment_icons.get_rect(midbottom = (570,580))
win_button = pygame.image.load('Images/winbutton.png').convert_alpha()
win_button_rect = win_button.get_rect(midbottom = (570,580))
win_buttons = pygame.image.load('Images/winbuttonhighlighted.png').convert_alpha()
win_buttons_rect = win_button.get_rect(midbottom = (570,580))

# Loads in the image for the 'max coins' button, the blinking alternative and the 
# hovered/selected alternative. Also generates the rects for these
max_coins = pygame.image.load('Images/maxcoins.png').convert_alpha()
max_coins_rect = max_coins.get_rect(midbottom = (1300,880))
max_coins_selected = pygame.image.load('Images/maxcoinsselected.png').convert_alpha()
max_coins_selected_rect = max_coins_selected.get_rect(midbottom = (1300,880))
max_coins_blink = pygame.image.load('Images/maxcoinsblink.png').convert_alpha()

# Same as above but for the moon environment
moon_max_coins = pygame.image.load('Images/moonmaxcoins.png').convert_alpha()
moon_max_coins_rect = moon_max_coins.get_rect(midbottom = (1300,880))
moon_max_coins_selected = pygame.image.load('Images/moonmaxcoinsselected.png').convert_alpha()
moon_max_coins_selected_rect = moon_max_coins_selected.get_rect(midbottom = (1300,880))
moon_max_coins_blink = pygame.image.load('Images/moonmaxcoinsblink.png').convert_alpha()
max_coins_faded = pygame.image.load('Images/maxcoinsfaded.png').convert_alpha()

# Creates the selected and unselected button for the 'quit' button that appears 
# when you win the game. Also generates the rect/hitbox for these
quit_button = pygame.image.load('Images/quit.png').convert_alpha()
quit_selected = pygame.image.load('Images/quitselected.png').convert_alpha()
quit_rect = quit_button.get_rect(midbottom = (width/2,850))

# Loads in the image for the 'auto fire' button, the blinking alternative, the on/off 
# alternatives, and the hovered/selected alternative. Also generates the rect for these
auto_button = pygame.image.load('Images/autofirebutton.png').convert_alpha()
auto_buttons = pygame.image.load('Images/autofireselected.png').convert_alpha()
auto_buttonb = pygame.image.load('Images/autofireblink.png').convert_alpha()
auto_button_on = pygame.image.load('Images/autofireon.png').convert_alpha()
auto_button_off = pygame.image.load('Images/autofireoff.png').convert_alpha()
autofire_rect = auto_button.get_rect(midbottom = (142,880))
auto_ons = pygame.image.load('Images/autofireons.png').convert_alpha()
auto_offs = pygame.image.load('Images/autofireoffs.png').convert_alpha()

# Same as above but for the moon environment
moon_auto_button = pygame.image.load('Images/moonautofirebutton.png').convert_alpha()
moon_auto_buttons = pygame.image.load('Images/moonautofireselected.png').convert_alpha()
moon_auto_buttonb = pygame.image.load('Images/moonautofireblink.png').convert_alpha()

# While the program is running
while running:
    while menu:
        # This loop checks for user input every single frame
        for event in pygame.event.get():
            # If the user hits the exit button at the top of the window, 
            # close the game
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                exit()
            # Creates a new variable 'pos' that returns the current cursor
            # location as a tuple (Ex: (0,0))
            pos = pygame.mouse.get_pos()
            # If the cursor is over the play button, the play button is 
            # selected (Displays the selected play button image)
            if play_rect.collidepoint(pos) or playb_rect.collidepoint(pos):
                selected = True
            else:
                selected = False
            # If the play button is selected and the user clicks, 
            # exit the menu/title screen and move onto the pregame/shop screen
            if selected and event.type == pygame.MOUSEBUTTONDOWN:
                        pregame = True
                        menu = False
                        selected = False
                        press_sound.play()

        # Fill the background in a sunsetish color, place an ombre transitional 
        # image known as 'horizon' on top, and then add the menu_ground, menu_cannon, 
        # and menu_title (At their respected tuples) in that order.
        screen.fill("#FF9506")
        screen.blit(horizon,(0,-4339))
        screen.blit(menu_ground,(0,660))
        screen.blit(menu_cannon, menu_cannon_rect)
        screen.blit(menu_title,(522,20))

        # Increments the menu_count by 1 every frame
        menu_count+=1
        
        # If the menu music hasn't already begun, start it now and infinitely
        # loop it. Make sure it doesn't start again or layer on top of 
        # another already playing song
        if title_music_count == 0:
            title_music.play(loops=-1)
            title_music.set_volume(.2)
            title_music_count+=1
        
        # If the play button isn't selected, make it blink every 50 frames
        if not selected:
            if menu_count < 50:
                screen.blit(play,play_rect)
            elif menu_count >= 50 and menu_count < 100:
                screen.blit(playb,playb_rect)
            else:
                screen.blit(playb,playb_rect)
                menu_count = 0
        else:
            screen.blit(plays,plays_rect)
        
        # Update the fps counter, and refresh the screen 60 times per second
        update_fps()
        pygame.display.update()
        clock.tick(60)  

    while pregame:
        # This loop checks for user input every single frame
        for event in pygame.event.get():
            # If the user hits the exit button at the top of the window, 
            # close the game
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                exit()
            # Creates a new variable 'pos' that returns the current cursor
            # location as a tuple (Ex: (0,0))
            pos = pygame.mouse.get_pos()
            # If the cursor is hovering over the fire button or its blinking
            # alternative, set selected to true
            if fb_rect.collidepoint(pos) or fbb_rect.collidepoint(pos):
                selected = True
            else:
                selected = False
            # If auto fire isn't turned on and the cursor hovers over any
            # upgrade buttons, display their respective 'selected' versions 
            # (Usually just turns the text and outline to a bright yellow)
            if not auto_fire:
                if cannon_upgrade_icon_rect.collidepoint(pos) or cannon_upgrade_icons_rect.collidepoint(pos):
                    cannon_upgrade_selected = True
                else:
                    cannon_upgrade_selected = False
                if (coin_upgrade_icon_rect.collidepoint(pos) or coin_upgrade_icons_rect.collidepoint(pos)) and (shop_2 or shop_3 or shop_5 or shop_6):
                    coin_upgrade_selected = True
                else:
                    coin_upgrade_selected = False
                if (moon_environment_icon_rect.collidepoint(pos) or moon_environment_icons_rect.collidepoint(pos)) and shop_3:
                    moon_selected = True
                else:
                    moon_selected = False
                if (win_button_rect.collidepoint(pos) or win_buttons_rect.collidepoint(pos)) and shop_6:
                    win_button_selected = True
                else:
                    win_button_selected = False
                if max_coins_rect.collidepoint(pos) or max_coins_selected_rect.collidepoint(pos):
                    max_coins_selected_bool = True
                else:
                    max_coins_selected_bool = False
            # If the cursor is hovering over the auto fire button, replace 
            # the auto fire button image with the selected auto fire button image
            if autofire_rect.collidepoint(pos):
                autofire_selected = True
            else:
                autofire_selected = False
            # If the auto fire button is being hovered over and the user clicks 
            # on it and their balance is 500 or more, auto fire is now purchased, 
            # the user loses 500 coins, and 'buy_sound' plays.
            # If the user's balance is less than 500, play the 'error_sound'
            if autofire_selected and not auto_purchased and event.type == pygame.MOUSEBUTTONDOWN:
                if balance>=500:
                    auto_purchased = True
                    balance-=500
                    buy_sound.play()
                else:
                    error_sound.play()
            # If auto fire is purchased and the user clicks on it, auto fire 
            # is activated, and the 'press_sound' (Sounds like a button press) is played
            # If auto fire is already off for this, auto fire is deactivated, 
            # and the same sound plays
            if auto_purchased:
                if event.type == pygame.MOUSEBUTTONDOWN and autofire_selected and not auto_fire:
                    auto_fire = True
                    press_sound.play()
                elif event.type == pygame.MOUSEBUTTONDOWN and autofire_selected and auto_fire:
                    auto_fire = False
                    press_sound.play()
            # If the user clicks on the moon environment upgrade and their balance
            # is 50000 or more, the balance becomes 0, the environment switches to the
            # moon, and the stats are all reset to how they were when the game began. 
            # If the user balance is less than 50000, play the 'error' sound (It sounds kind of like "errr")
            if moon_selected and event.type == pygame.MOUSEBUTTONDOWN and not moon_mode:
                if balance >= 50000:
                    balance = 0
                    moon_mode = True
                    coin_level = 0
                    speed_level = 0
                    display_level = 1
                    cdisplay_level = 1
                    new_moon = True
                    earth_shop_music.set_volume(0)
                    level_text = slevel_text.render(f'LEVEL {display_level} OF 8',False,("#000000"))
                    level_text_rect = level_text.get_rect(midleft = (width/2-100,250))
                    clevel_text = slevel_text.render(f'LEVEL {display_level} OF 8',False,("#000000"))
                    clevel_text_rect = clevel_text.get_rect(midleft = (width/2-100,410))
                    clevel_cost = slevel_text.render(f'LEVEL {cdisplay_level+1} COST:{cost_index[coin_level]}',False,("#000000"))
                    clevel_cost_rect = clevel_cost.get_rect(midleft = (width/2-100,370))
                    canlevel_cost = slevel_text.render(f'LEVEL {display_level+1} COST:{cost_index[speed_level]}',False,("#000000"))
                    canlevel_cost_rect = canlevel_cost.get_rect(midleft = (width/2-100,210))
                else:
                    error_sound.play()
            # If it's moon mode and the user clicks on the win button and they 
            # have the max amount of coins, they switch to the win screen. 
            # If they don't have enough, the error sound plays
            elif win_button_selected and event.type == pygame.MOUSEBUTTONDOWN and moon_mode and balance == 99999:
                win = True
                pregame = False
            elif win_button_selected and event.type == pygame.MOUSEBUTTONDOWN and moon_mode and balance != 99999:
                error_sound.play()
            # If the user wants to see the features of the game without waiting 
            # (It's an idle game so there is a lot of waiting), 
            # clicking on the max coins button at the bottom right gives them
            # infinite coins. The press sound plays after this, 
            # and it sounds like a click/button press
            if max_coins_selected_bool and event.type == pygame.MOUSEBUTTONDOWN:
                infinite_coins = True
                press_sound.play()
            # If auto fire isn't on and the user clicks on an upgrade, 
            # the game will make sure that they have enough coins for said upgrade.
            # If they do, they gain the upgrade, and
            # lose the coins. If they do not, then the error sound will play
            if not auto_fire:
                if cannon_upgrade_selected and event.type == pygame.MOUSEBUTTONDOWN:
                    if balance>=cost_index[speed_level]:
                        buy_sound.play()
                        if display_level < 8:
                            display_level+=1
                            level_text = slevel_text.render(f'LEVEL {display_level} OF 8',False,("#000000"))
                            level_text_rect = level_text.get_rect(midleft = (width/2-100,250))
                            canlevel_cost = slevel_text.render(f'LEVEL {display_level+1} COST:{cost_index[speed_level+1]}',False,("#000000"))
                            canlevel_cost_rect = canlevel_cost.get_rect(midleft = (width/2-100,210))
                        if speed_level < 7:
                            balance-= cost_index[speed_level]
                            speed_level+=1
                        if speed_level == 7:
                            canlevel_cost = slevel_text.render(f'MAX LEVEL',False,("#000000"))
                            canlevel_cost_rect = canlevel_cost.get_rect(midleft = (width/2-100,210))
                    else:
                        error_sound.play()
                if coin_upgrade_selected and event.type == pygame.MOUSEBUTTONDOWN:
                    if balance>=cost_index[coin_level]:
                        buy_sound.play()
                        if cdisplay_level < 8:
                            cdisplay_level+=1
                            clevel_text = slevel_text.render(f'LEVEL {cdisplay_level} OF 8',False,("#000000"))
                            clevel_text_rect = clevel_text.get_rect(midleft = (width/2-100,410))
                            clevel_cost = slevel_text.render(f'LEVEL {cdisplay_level+1} COST:{cost_index[coin_level+1]}',False,("#000000"))
                            clevel_cost_rect = clevel_text.get_rect(midleft = (width/2-100,370))
                        if coin_level < 7:
                            balance-= cost_index[coin_level]
                            coin_level+=1
                        if coin_level == 7:
                            clevel_cost = slevel_text.render(f'MAX LEVEL',False,("#000000"))
                            clevel_cost_rect = clevel_text.get_rect(midleft = (width/2-100,370))
                    else:
                        error_sound.play()

            # If the fire button is selected, the cooldown period has passed,
            # and the user clicks it, the press sound will play. 
            # The game will also switch modes and reset all 
            # user-input-related conditionals. All sound counters will reset as well,
            # so that the cannon fire and sand sound effects will be able to play again
            if selected and event.type == pygame.MOUSEBUTTONDOWN and wait > 50:
                press_sound.play()
                pregame = False
                game = True
                p_blinking = False
                wait = 0
                selected = False
                shot_sound_count = 0
                sand_count = 0
        
        # If it's moon mode, the screen will fill with a dark purplish color, 
        # the moon environment's music will begin, and it will loop. Otherwise,
        # the screen will fill with a sunset color, the Earth environment's music 
        # will begin, and that will loop instead. After one of these two occur, 
        # the cannon is displayed on the screen, and the respective moon/Earth ground is placed
        # under the cannon.
        if moon_mode:
            screen.fill("#2b274e")
            if moon_shop_music_count == 0:
                moon_shop_music.play(loops = -1)
                moon_shop_music.set_volume(.2)
                moon_shop_music_count+=1
        else:
            screen.fill("#FF9506")
            screen.blit(horizon,(-550,-4339))
            if earth_shop_music_count == 0:
                title_music.set_volume(0)
                earth_shop_music.play(loops = -1)
                earth_shop_music.set_volume(.2)
                earth_shop_music_count+=1
        screen.blit(cannon1,(150,535))
        if moon_mode:
            screen.blit(moon_ground,(0,660))
        else:
            screen.blit(ground,(0,660))
        # The coin and record images are displayed, and their respective
        # numbers are placed to their rights
        screen.blit(coin_icon,(width-300,65))
        screen.blit(record_icon,(30,30))
        update_earnings()
        update_record()
        
        # If it isn't moon mode and the fire button isn't selected, the 
        # Earth fire button will be displayed, and it will blink every 50 frames. 
        # Otherwise, the moon version (purple instead of brown) will display,
        # and blink every 50 frames.
        if not moon_mode:
            if not selected:
                if p_blinking and p_blink <= 50:
                    p_blink+=1
                    screen.blit(fire_button,fb_rect)
                elif p_blinking and p_blink>50 and p_blink <=100:
                    p_blink+=1
                    screen.blit(fire_blinking,fbb_rect)
                    screen.blit(max_coins_blink,max_coins_rect)
                else:
                    screen.blit(fire_blinking,fbb_rect)
                    screen.blit(max_coins_blink,max_coins_rect)
                    p_blink = 0
            else:
                screen.blit(fire_hovered,fh_rect)
        else:
            if not selected:
                if p_blinking and p_blink <= 50:
                    p_blink+=1
                    screen.blit(moon_fire_button,moon_fb_rect)
                elif p_blinking and p_blink>50 and p_blink <=100:
                    p_blink+=1
                    screen.blit(moon_fire_blinking,moon_fbb_rect)
                else:
                    screen.blit(moon_fire_blinking,moon_fbb_rect)
                    p_blink = 0
            else:
                screen.blit(moon_fire_hovered,fh_rect)
        
        # The exact same thing as the fire button, but for the auto fire button. 
        # The only difference is that the auto fire buttons are gold/mint green,
        # rather than brown/purple like the fire button.
        # Also, these auto fire buttons are only displayed when auto 
        # fire hasn't been purchased yet
        if not moon_mode:
            if not auto_purchased: 
                if autofire_selected:
                    screen.blit(auto_buttons,autofire_rect)
                elif p_blinking and p_blink <= 50:
                    screen.blit(auto_button,autofire_rect)
                elif p_blinking and p_blink > 50 and p_blink <= 100:
                    screen.blit(auto_buttonb,autofire_rect)
                else:
                    screen.blit(auto_buttonb,autofire_rect)
        if moon_mode:
            if not auto_purchased: 
                if autofire_selected:
                    screen.blit(moon_auto_buttons,autofire_rect)
                elif p_blinking and p_blink <= 50:
                    screen.blit(moon_auto_button,autofire_rect)
                elif p_blinking and p_blink > 50 and p_blink <= 100:
                    screen.blit(moon_auto_buttonb,autofire_rect)
                else:
                    screen.blit(moon_auto_buttonb,autofire_rect)
            
        # If auto fire is purchased and on, the screen will display the 
        # auto fire on button. If it isn't on, it will display
        # the auto fire off button
        if auto_purchased:
            if not auto_fire and not autofire_selected:
                screen.blit(auto_button_off,autofire_rect)
            if auto_fire and not autofire_selected:
                screen.blit(auto_button_on,autofire_rect)
            if auto_fire and autofire_selected:
                screen.blit(auto_ons,autofire_rect)
            elif not auto_fire and autofire_selected:
                screen.blit(auto_offs,autofire_rect)

        # If auto fire isn't on, the fire button will display if it isn't 
        # blinking (p_blinking is true when blinking). If the fire buttons 
        # cooldown isn't over, it will display a faded gray version instead
        if not auto_fire:
            if wait > 50 and not p_blinking and not moon_mode:
                screen.blit(fire_button,fb_rect)
                p_blinking = True
            elif wait>50 and not p_blinking and moon_mode:
                screen.blit(moon_fire_button,moon_fb_rect)
                p_blinking = True
            elif wait <= 50 and not p_blinking:
                screen.blit(fire_faded,fbfade_rect)
        else:
        # If auto fire is on, just display the faded fire button, as there won't
        # be a player clicking/selecting it. Wait twice as long as you
        # would manually, and then automatically fire
            screen.blit(fire_faded,fbfade_rect)
            if wait>50 and auto_fire_wait>110:
                pregame = False
                game = True
                p_blinking = False
                wait = 0
                selected = False
                shot_sound_count = 0
        
        # Reset the auto fire waittime if it's above 110
        if auto_fire_wait>111:
            auto_fire_wait = 0
                
        # If it isn't auto fire mode, display a normal shop with upgrades
        if not auto_fire:
            # If both speed and coin multiplier levels are maxed out,
            # allow the user to be able to purchase the moon environment. 
            # If the player is already on the moon, allow
            # them to be able to purchase the win screen/win the game
            if speed_level >= 7 and coin_level >= 7:
                if not moon_mode:
                    screen.blit(shop,shop_rect)
                    shop_2 = False
                    shop_3 = True
                else:
                    screen.blit(moon_shop,moon_shop_rect)
                    shop_5 = False
                    shop_6 = True
                # If the cannon upgrade is being hovered over, display
                # the selected upgrade button image. If it's not, display 
                # the normal upgrade button image
                if cannon_upgrade_selected:
                    screen.blit(cannon_upgrade_icons,cannon_upgrade_icons_rect)
                else:
                    screen.blit(cannon_upgrade_icon,cannon_upgrade_icon_rect)
                # Same as above but for the coin upgrade instead
                if coin_upgrade_selected:
                    screen.blit(coin_upgrade_icons,coin_upgrade_icons_rect)
                else:
                    screen.blit(coin_upgrade_icon,coin_upgrade_icon_rect)
                # Same as above but for the moon environment upgrade 
                # instead. Also, display the moon cost and title in text
                if not moon_mode:
                    if moon_selected:
                        screen.blit(moon_environment_icons,moon_environment_icons_rect)
                    else:
                        screen.blit(moon_environment_icon,moon_environment_icon_rect)
                    screen.blit(moon_text,moon_text_rect)
                    screen.blit(moon_text_name,moon_text_name_rect)
                else:
                # Same as above but for the win upgrade, and display
                # the win cost and title in text
                    if win_button_selected:
                        screen.blit(win_buttons,win_buttons_rect)
                    else:
                        screen.blit(win_button,win_button_rect)
                    screen.blit(win_text,win_text_rect)
                    screen.blit(win_text_name,win_text_name_rect)
                # Display the coin level and cost in text
                screen.blit(clevel_text,clevel_text_rect)
                screen.blit(clevel_cost,clevel_cost_rect)
            elif speed_level >= 4 and coin_level<=7 and speed_level <7 or speed_level>=4 and coin_level<7 and speed_level<=7:
                # If the speed level is above 5 and both upgrades aren't maxed out yet,
                # display the shop with only the speed and coin upgrade (No moon or win upgrade yet)
                # Shop color varies based on environment (Brown/Gold = Earth, Purple/Mint = Moon)
                if not moon_mode:
                    screen.blit(mid_shop,mid_shop_rect)
                    shop_1 = False
                    shop_2 = True
                else:
                    screen.blit(moon_mid_shop,moon_mid_shop_rect)
                    shop_4 = False
                    shop_5 = True
                # If the cannon upgrade is being hovered over, display the selected 
                # upgrade button image. If it's not, display the normal upgrade button image
                if cannon_upgrade_selected:
                    screen.blit(cannon_upgrade_icons,cannon_upgrade_icons_rect)
                else:
                    screen.blit(cannon_upgrade_icon,cannon_upgrade_icon_rect)
                # Same as above but for coin upgrade
                if coin_upgrade_selected:
                    screen.blit(coin_upgrade_icons,coin_upgrade_icons_rect)
                else:
                    screen.blit(coin_upgrade_icon,coin_upgrade_icon_rect)
                # Display the coin level and cost in text
                screen.blit(clevel_text,clevel_text_rect)
                screen.blit(clevel_cost,clevel_cost_rect)
            else:
                # If the speed level is under 5 display the shop with only 
                # the speed upgrade available
                if not moon_mode:
                    screen.blit(starter_shop,starter_shop_rect)
                    shop_1 = True
                else:
                    screen.blit(moon_starter_shop,moon_starter_shop_rect)
                    shop_3 = False
                    shop_4 = True
                # If the cannon upgrade is being hovered over, display the 
                # selected upgrade button image. If it's not, display the normal
                # upgrade button image
                if cannon_upgrade_selected:
                    screen.blit(cannon_upgrade_icons,cannon_upgrade_icons_rect)
                else:
                    screen.blit(cannon_upgrade_icon,cannon_upgrade_icon_rect)
            # Display the speed level and cost in text
            screen.blit(level_text,level_text_rect)
            screen.blit(canlevel_cost,canlevel_cost_rect)
            
            # Display the 'upgrades from this round will appear next round'
            # warning (colors vary based on environment)
            if not moon_mode:
                screen.blit(warning,warning_rect)
            else:
                screen.blit(moon_warning,moon_warning_rect)
        # If auto fire is on, display a gray shop that can't be accessed
        # until auto fire is off
        else:
            screen.blit(auto_fire_shop,shop_rect)
            auto_shop = True

        # If it isn't moon mode make the gold max coins 
        # button blink every 50 frames
        if not moon_mode:
            if max_coins_selected_bool:
                screen.blit(max_coins_selected,max_coins_selected_rect)
            else:
                if p_blinking and p_blink <= 50:
                        screen.blit(max_coins,max_coins_rect)
                elif p_blinking and p_blink>50 and p_blink <=100:
                    screen.blit(max_coins_blink,max_coins_rect)
                else:
                    screen.blit(max_coins_blink,max_coins_rect)
        # If it is moon mode make the mint green max coins 
        # button blink every 50 frames
        else:
            if max_coins_selected_bool:
                screen.blit(moon_max_coins_selected,moon_max_coins_selected_rect)
            else:
                if p_blinking and p_blink <= 50:
                        screen.blit(moon_max_coins,moon_max_coins_rect)
                elif p_blinking and p_blink>50 and p_blink <=100:
                    screen.blit(moon_max_coins_blink,moon_max_coins_rect)
                else:
                    screen.blit(moon_max_coins_blink,moon_max_coins_rect)
        
        # If you clicked the max coins button (Infinite coins is true)
        # and you dip below 99999 coins, coins will be set back to 99999
        if infinite_coins:
            if balance!=99999:
                balance = 99999
                
        # If auto fire is on, fade out the max coins button until auto fire is off
        if auto_fire:
            screen.blit(max_coins_faded,max_coins_rect)
        
        # Increment the fire cooldowns by 1
        auto_fire_wait+=1
        wait+=1
        
        # Update the FPS on the screen and refresh the screen 60 times per second
        update_fps()
        pygame.display.update()
        clock.tick(60)

    while game:
        # This loop checks for user input every single frame
        for event in pygame.event.get():
            # If the user hits the exit button at the top of the window, close the game
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                exit()
            # Creates a new variable 'pos' that returns the current cursor location 
            # as a tuple (Ex: (0,0))
            pos = pygame.mouse.get_pos()
            # If the player cursor hovers over the return button, selected is true
            if returnb_rect.collidepoint(pos) or returnb_blink_rect.collidepoint(pos):
                selected = True
            else:
                selected = False
            # If the return button is selected and the player clicks and the ball is 
            # on the ground, play the press sound, switch the game back to shop mode, and 
            # set all conditionals to default values
            if selected and event.type == pygame.MOUSEBUTTONDOWN and ball.rect.y >= 660 - 32:
                press_sound.play()
                pregame = True
                game = False
                new_start = True
                returnbool = False
                selected = False
                if new_moon:
                    new_moon = False       
        
        # Coins go up every single pixel the ball moves forwards
        coin_count = 0
        
        # When the cannon fires/this gamemode starts, play the cannon firing sound once
        if shot_sound_count == 0 and not moon_mode:
            cannon_fire_sound.play()
            shot_sound_count+=1

        # If the ball is off the ground, add the coin index (coin multiplier amount) 
        # to the player balance. To avoid an unreasonably high balance, this 
        # only happens every 50 frames
        if ball.rect.y < 635 and coin_count % 50 == 0:
            balance+=coin_index[coin_level]
            if balance >= 99999:
                balance = 99999

        # Incrementing coin count by 1
        coin_count+=1
        
        # If you're on the moon, make the sky look purplish. Otherwise, the sky will 
        # be filled with a sunset color
        if moon_mode:
            screen.fill("#2b274e")
        else:
            screen.fill("#FF9506")
        
        # Move the camera, move and load the new ball instance, display the coin icon, 
        # balance, record icon, altitude icon, distance record, current altitude, 
        # current distance, and distance icon in that order
        camera_group.update()
        camera_group.custom_draw(ball)
        screen.blit(coin_icon,(width-300,65))
        update_earnings()
        screen.blit(record_icon,(30,30))
        screen.blit(altitude_icon,(15,280))
        update_record()
        update_altitude()
        update_distance()
        screen.blit(distance_icon,(5,150))
        
        # Altitude and distance are divided by 10 to avoid ridiculously high number values
        altitude = (int)((((ball.rect.topleft[1] - 660)*-1)-20)/10)
        distance = (int)(((ball.rect.topleft[0]-200))/100)
        
        # Making sure you can't immediately return once the ball hits the ground,
        # because of possible bounces
        auto_fire_return_wait+=1
        
        # Play the sand impact sound once the ball hits the sand, and never again. 
        # Only plays when the player is on Earth
        if ball.rect.bottom >= 660 and sand_count == 0 and not moon_mode:
            sand_sound.play()
            sand_count+=1;
        
        # If auto fire is active, return to shop mode once the necessary ball conditions
        # are met, rather than waiting for player input. Takes twice as long as manual 
        # input would for balancing reasons
        if auto_fire:
            if ball.rect.y>=660-32 and auto_fire_return_wait>111:
                    pregame = True
                    game = False
                    new_start = True
                    returnbool = False
                    selected = False
                    if new_moon:
                        new_moon = False
                        
        # Sets auto_fire_return_wait to 0 once it's hit its max
        if auto_fire_return_wait>111:
            auto_fire_return_wait = 0
            
        # Records when the player hits a new record
        if distance >= record:
            record = distance

        # If the ball is on the ground and the cooldown isn't over, display a faded return button
        if (ball.rect.y<635 and not returnbool and not selected):
            screen.blit(returnb_fade,returnb_fade_rect)
        elif ball.rect.y>=635 and not returnbool:
            returnbool = True
            screen.blit(returnb,returnb_rect)
        
        # If the return button isn't selected, makes it blink every 50 frames. Color 
        # variation based on environment
        if not selected:
            if returnbool:
                returnb_count+=1
                if returnb_count <=50 and not moon_mode:
                    screen.blit(returnb,returnb_rect)
                elif returnb_count <=50 and moon_mode:
                    screen.blit(moon_returnb,moon_returnb_rect)
                elif returnb_count > 50 and returnb_count <=100 and not moon_mode:
                    screen.blit(returnb_blink,returnb_blink_rect)
                elif returnb_count > 50 and returnb_count <=100 and moon_mode:
                    screen.blit(moon_returnb_blink,moon_returnb_blink_rect)
                else:
                    if not moon_mode:
                        screen.blit(returnb_blink,returnb_blink_rect)
                    else:
                        screen.blit(moon_returnb_blink,moon_returnb_blink_rect)
                    returnb_count = 0
        # Displays the selected version based on the environment. If ball is up too 
        # high, displays a faded version of the return button instead
        elif selected and ball.rect.y>=635 and not moon_mode:
            screen.blit(returnb_selected,returnb_selected_rect)
        elif selected and ball.rect.y>=635 and moon_mode:
            screen.blit(moon_returnb_selected,moon_returnb_selected_rect)
        else:
            screen.blit(returnb_fade,returnb_fade_rect)
        
        # If auto fire is on, keeps the return button faded, as it won't be 
        # pressed by any user
        if auto_fire:
            screen.blit(returnb_fade,returnb_fade_rect)

        # Update the FPS on the screen and refresh the screen 60 times per second
        update_fps()
        pygame.display.update()
        clock.tick(60)

    while win:
        # This loop checks for user input every single frame
        for event in pygame.event.get():
            # Creates a new variable 'pos' that returns the current 
            # cursor location as a tuple (Ex: (0,0))
            pos = pygame.mouse.get_pos()
            # If the user hits the exit button at the top of the window, close the game
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                exit()
            # If the cursor hovers over the 'quit' button, make it being selected true
            if quit_rect.collidepoint(pos):
                quit_selected_bool = True
            else:
                quit_selected_bool = False
            # If the quit button is selected and the player clicks it, end the game
            if quit_selected_bool and event.type == pygame.MOUSEBUTTONDOWN:
                press_sound.play()
                pygame.display.quit()
                pygame.quit()
                exit()

        # Make the sky a goldish color, and display the moon ground, menu cannon, 
        # and win message on the screen in that order.
        screen.fill("#d6a851")
        screen.blit(title_ground,(0,650))
        screen.blit(menu_cannon, (menu_cannon_rect.x,menu_cannon_rect.y-10))
        screen.blit(win_title,(522,20))
        
        # If the 'quit' button is selected, make it look selected 
        # (highlighted borders and yellow text)
        if quit_selected_bool:
            screen.blit(quit_selected,quit_rect)
        else:
            screen.blit(quit_button,quit_rect)
        
        # Begin playing and infinitely looping the victory music, with no overlap
        if victory_music_count == 0:
            moon_shop_music.set_volume(0)
            victory_music.play(loops=-1)
            victory_music.set_volume(.2)
            victory_music_count+=1
        
        # Update the FPS on the screen and refresh the screen 60 times per second
        update_fps()
        pygame.display.update()
        clock.tick(60)

# Quits the game
pygame.display.quit()
pygame.quit()