import pygame
import random
import button
import csv


# Load player data from CSV file
player_data = []
with open("player_data.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        player_data.append({
            "name": row["Name"],
            "skill": int(row["XP"])
        })

# Shuffle the player data randomly to ensure team assignment is not biased
random.shuffle(player_data)

# Split players into teams (assuming you want two teams)
team1 = []
team2 = []

for player in player_data:
    if len(team1) <= len(team2):
        team1.append(player)
    else:
        team2.append(player)

# Calculate team skill levels
team1_skill = sum(player["skill"] for player in team1)
team2_skill = sum(player["skill"] for player in team2)

# Print the team skill levels (for demonstration)
print("Team 1 Skill:", team1_skill)
print("Team 2 Skill:", team2_skill)


pygame.init()

clock = pygame.time.Clock()
fps = 60

# Game window
screen_width = 1500
screen_height = 800  # Increase the screen height to accommodate the panel

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption('Battle Royale')

# define game variables
current_fighter = 2
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 15
clicked = False
game_over = 0

# define fonts
font = pygame.font.SysFont('Times New Roman', 24)

# define colors
red = (255, 0, 0)
green = (0, 255, 0)

# Load images
# Background image
background_img = pygame.image.load('img/Background/background.jpg').convert_alpha()
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))  # Scale the background image

# Panel image
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()
panel_width = screen_width
panel_height = 250
panel_img = pygame.transform.scale(panel_img, (panel_width, panel_height))

# button image
#potion_img = pygame.image.load('img/Icons/potion.png').convert_alpha()
restart_img = pygame.image.load('img/Icons/restart.png').convert_alpha()

# load victory and defeat images
victory_img = pygame.image.load('img/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('img/Icons/defeat.png').convert_alpha()

# sword icon
sword_img = pygame.image.load('img/Icons/sword.png').convert_alpha()


# create function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Function for drawing background
def draw_bg():
    screen.blit(background_img, (0, 0))


# Function for drawing panel
def draw_panel():
    # draw panel rectangle
    screen.blit(panel_img, (0, 0))  # Place the panel at the top
    # show player stats
    draw_text(f'Player 1 HP: {Character1.hp}', font, red, 260, 60)
    draw_text(f'Player 2 HP: {Character4.hp}', font, red, 260, 120)

    ##for count, i in enumerate()
    draw_text(f'Opponent 1 HP: {Character2.hp}', font, red, 1050, 60)
    draw_text(f'Opponent 2 HP: {Character3.hp}', font, red, 1050, 120)


# Fighter class
class Fighter():
    def __init__(self, x, y, name, max_hp, strength):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0:idle, 1:attack, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()
        # load idle images
        temp_list = []
        for i in range(9):
            img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            # self.animation_list.append(img)
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # load attack images
        temp_list = []
        for i in range(15):
            img = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            # self.animation_list.append(img)
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # load hurt images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            # self.animation_list.append(img)
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # load death images
        temp_list = []
        for i in range(15):
            img = pygame.image.load(f'img/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.25, img.get_height() * 1.25))
            # self.animation_list.append(img)
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 100
        # handle animation
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if animation run out hen reset back to start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        # set variables to attack animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # deal damage to enemy
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        # run enemy hurt animation
        target.hurt()
        # check if target is dead
        if target.hp < 1:
            target.hp = 0
            target.alive = False
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)
        # set variables to attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        # set variables to hurt animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        # set variables to death animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        self.alive = True
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)


class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        # update w new health
        self.hp = hp
        # calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))


class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # move damage text up
        self.rect.y -= 1
        # delete the text after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()


damage_text_group = pygame.sprite.Group()

Character1 = Fighter(340, 570, 'Player', 30, 10)
Character4 = Fighter(390, 570, 'Player', 30, 10)
Character2 = Fighter(700, 580, 'Opponent', 30, 10)
Character3 = Fighter(750, 570, 'Opponent', 30, 10)

opponent_list = []
opponent_list.append(Character2)
opponent_list.append(Character3)

Character1_health_bar = HealthBar(260, 90, Character1.hp, Character1.max_hp)
Character4_health_bar = HealthBar(260, 155, Character4.hp, Character4.max_hp)
Character2_health_bar = HealthBar(1050, 90, Character2.hp, Character2.max_hp)
Character3_health_bar = HealthBar(1050, 155, Character3.hp, Character3.max_hp)

# create buttons
restart_button = button.Button(screen, 650, 200, restart_img, 150, 100)

run = True
while run:
    clock.tick(fps)

    # Draw background
    draw_bg()

    # Draw panel
    draw_panel()
    Character1_health_bar.draw(Character1.hp)
    Character4_health_bar.draw(Character4.hp)
    Character2_health_bar.draw(Character2.hp)
    Character3_health_bar.draw(Character3.hp)

    # Draw fighters
    Character1.draw()
    Character1.update()
    Character4.draw()
    Character4.update()

    for opponent in opponent_list:
        opponent.update()
        opponent.draw()

    # draw the damage text
    damage_text_group.update()
    damage_text_group.draw(screen)

    # control player action
    # reset action variable
    attack = False
    potion = False
    target = None
    # mouse is visible
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, opponent in enumerate(opponent_list):
        if opponent.rect.collidepoint(pos):
            # hide the mouse
            pygame.mouse.set_visible(False)
            # show sword in place of mouse cursor
            screen.blit(sword_img, pos)
            if clicked == True and opponent.alive == True:
                attack = True
                target = opponent_list[count]


    # player action
    if Character1.alive == True:
        if current_fighter == 1:
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                # look for player action
                # attack
                if attack == True and target != None:
                    Character1.attack(target)
                    current_fighter += 1
                    action_cooldown = 0
    if Character4.alive == True:
        if current_fighter == 1:
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                # look for player action
                # attack
                if attack == True and target != None:
                    Character4.attack(target)
                    current_fighter += 1
                    action_cooldown = 0

    # enemy action
    for count, opponent in enumerate(opponent_list):
        if current_fighter == 2 + count:
            if opponent.alive == True:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    # attack
                    opponent.attack(Character1)
                    current_fighter += 1
                    action_cooldown = 0
            else:
                current_fighter += 1

    # if all fighters had a turn, reset
    if current_fighter > total_fighters:
        current_fighter = 1

    # check if all bandits are dead
    alive_opponents = 0
    for opponent in opponent_list:
        if opponent.alive == True:
            alive_opponents += 1
    if alive_opponents == 0:
        game_over = 1

    # check if game is over
    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (250, 50))
        if game_over == -1:
            screen.blit(defeat_img, (290, 50))
        if restart_button.draw():
            Character1.reset()
            for opponent in opponent_list:
                opponent.reset()
            current_fighter = 1
            action_cooldown
            game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()

pygame.quit()
