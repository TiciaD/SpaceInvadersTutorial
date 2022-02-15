import pygame
import os
import time
import random
pygame.font.init()

# Window Size Settings
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Tutorial")

# Load images
RED_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_blue_small.png"))

# Player ship
YELLOW_SPACE_SHIP = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "blue-ship-small.png")), (100, 100))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

# Laser Methods


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    # method to draw laser to screen
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    # method to move laser downwards
    def move(self, vel):
        self.y += vel

    # method to determine if laser is off-screen based on height of screen
    def off_screen(self, height):
        return self.y <= height and self.y >= 0

    # method to determine if laser has collided with another object
    def collision(self, obj):
        return collide(obj, self)


# Generic Ship methods
class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    # function to draw ship and fill rectangle it's in
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_width()


# Player methods
class Player(Ship):
    def __init__(self, x, y, health=100):
        # take generic ship class's initialization method
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        # set pixel perfect collision detection
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health


# Enemy Ship methods
class Enemy(Ship):
    # Match ship colors to their laser colors
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        # set ship image and laser image to match the color map
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        # set mask for enemy ship
        self.mask = pygame.mask.from_surface(self.ship_img)

    # Move enemy ship downwards
    def move(self, vel):
        self.y += vel

#
# def collide(obj1, obj2):


# Main Game Loop
def main():
    # run program
    run = True
    # lose condition
    lost = False
    # Time in seconds You Lost screen is shown
    lost_count = 0
    # set frames per second
    FPS = 60
    # set level
    level = 0
    # set lives
    lives = 5
    # set font
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    # set enemies list to contain each enemy
    enemies = []
    # set number of enemies in a wave
    wave_length = 5
    # set enemy ship velocity
    enemy_vel = 1

    # set player velocity (pixels)
    player_vel = 5

    # create Ship
    player = Player(300, 650)

    # set game clock
    clock = pygame.time.Clock()

    # Display
    def redraw_window():
        # draw background image to screen
        WIN.blit(BG, (0, 0))
        # draw text for lives and level counter
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        # draw enemy
        for enemy in enemies:
            enemy.draw(WIN)

        # draw ship
        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lose", 1, (255, 255, 255))
            WIN.blit(lost_label, WIDTH/2 - lost_label.get_width()/2, 350)

        # update the display
        pygame.display.update()

    while run:
        # set clock to pace of frames per second
        clock.tick(FPS)
        # draw images to screen
        redraw_window()

        # lose condition
        # check if all lives lost or all health lost
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 5:
                run = False
            else:
                continue

        # when all enemies are defeated
        if len(enemies) == 0:
            # increment level
            level += 1
            # increase number of enemies in wave
            wave_length += 5
            # spawn new enemies
            for i in range(wave_length):
                # set position of enemy to random coordinate offscreen and random color of ship
                enemy = Enemy(random.randrange(
                    50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                # add to enemies list
                enemies.append(enemy)

        # check if user has hit the exit button
        # if so then stop running the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # set keys that are currently being pressed
        keys = pygame.key.get_pressed()
        # if player presses A key go left
        if keys[pygame.K_a] and player.x - player_vel > 0:
            # subtract velocity from current player position on x-axis
            player.x -= player_vel
        # if player presses D key go right
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:
            # add velocity to current player position on x-axis
            player.x += player_vel
        # if player presses W key go up
        if keys[pygame.K_w] and player.y - player_vel > 0:
            # subtract velocity from current player position on y-axis
            player.y -= player_vel
        # if player presses S key go down
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT:
            # add velocity to current player position on y-axis
            player.y += player_vel

        # loop over enemies list
        for enemy in enemies:
            # move each enemy at velocity sent in param
            enemy.move(enemy_vel)

            # check if enemy is off bottom of screen
            if (enemy.y + enemy.get_height() > HEIGHT):
                # if so decrement player's lives
                lives -= 1
                # remove that enemy from the list so it doesn't come back
                enemies.remove(enemy)


main()
