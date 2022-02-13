import pygame
import random
import time

# initialize pygame
pygame.init()

# setting up variables
start = False
game_over = False
score = 0
high_score = 0

# pygame variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUEGREEN = (0,255,170)
FPS = 240
HEIGHT = 600
WIDTH = 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font('freesansbold.ttf', 25)
play_again_button = None
start_button = None
exit_button = None

red = 69
direction = "U"
pygame.display.set_caption("Vexation")
timer = 3


class Blocks:
    # list of all blocks [[x, y, w, h]]
    block_coord = [[0, 0, 600, 600]]

    # generates a sequence of blocks
    @classmethod
    def generate_block(cls, block_coord):
        block = []
        # set the min and max values for the x_coord of the new block
        x_min = block_coord[-1][0] - block_coord[-1][2]
        x_max = block_coord[-1][0] + block_coord[-1][2]
        if x_min <= 50:
            x_min = 50
        if x_max >= 600:
            x_max = 550

        block.append(random.randrange(x_min, x_max, 50))
        block.append(block_coord[-1][1] - 200)
        min_width = abs(block[0] - (block_coord[-1][0] + 25))
        if min_width <= 0:
            min_width = 25
        block.append(random.randrange(min_width, min_width + 200, 25))
        block.append(250)

        block_coord.append(block)

    # removes blocks that are no longer visible
    @classmethod
    def remove_block(cls, block_coord):
        global score
        if block_coord[0][1] > 700:
            block_coord.pop(0)
            score += 10

    # draw all blocks in block_coord
    @classmethod
    def draw_blocks(cls, block_coord):
        WINDOW.fill(WHITE)
        for block in block_coord:
            pygame.draw.rect(WINDOW, (red, 105, 255),
                             (block[0], int(block[1]), block[2], block[3]))

    # detects if your mouse is touching the white
    @classmethod
    def collision(cls, block_coord, mouse_pos):
        # print(mouse_pos)
        mouseX = mouse_pos[0]
        mouseY = mouse_pos[1]
        collision = True

        for block in block_coord:
            if block[0] < mouseX < block[0] + block[2] and block[
                    1] < mouseY < block[1] + block[3]:
                collision = False
                break
        return collision


class Button:
    def __init__(self, x, y, width, height, colour, text=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.text = text

    # draw the button
    def draw(self):
        pygame.draw.rect(WINDOW, self.colour, (self.x, self.y, self.width, self.height))
        if self.text != "":
            button_font = pygame.font.Font('freesansbold.ttf', 15)
            button_text = button_font.render(self.text, True, BLACK)
            WINDOW.blit(button_text, (self.x + (self.width/2 - button_text.get_width()/2), self.y + (self.height/2 - button_text.get_height()/2)))

    # check if the button is clicked
    # returns True if it is clicked, return False if it's not clicked
    def is_clicked(self, mouse_pos):
        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            return True
        else:
            return False


class Image:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        WINDOW.blit(self.image, (self.rect.x, self.rect.y))

        return action


# main function
def main():
    global FPS, WINDOW, FONT, BLACK, RED, start, score, high_score, game_over, red, direction, play_again_button, start_button, exit_button, timer
    running = True
    while running:
        # clock = pygame.time.Clock()
        for event in pygame.event.get():
            # clock.tick(FPS)
            if event.type == pygame.QUIT:
                running = False
            # if mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    # if the play_again button is clicked
                    if play_again_button.is_clicked(pygame.mouse.get_pos()):
                        # reset game variables
                        game_over = False
                        score = 0
                        Blocks.block_coord = [[0, 0, 600, 600]]
                        timer = 3
                        red = 69
                        direction = "U"
                if not start:
                    if start_button.draw():
                        start = True
                    if exit_button.draw():
                        running = False
        if start:
            if not game_over:
                if len(Blocks.block_coord) < 5:
                    Blocks.generate_block(Blocks.block_coord)
                WINDOW.fill(WHITE)
                Blocks.draw_blocks(Blocks.block_coord)
                # countdown timer shown at the start of a new game
                if timer >= 0:
                    # display the countdown timer
                    timer_font = pygame.font.Font('freesansbold.ttf', 55)
                    text = timer_font.render(str(timer), True, (255, 255, 0))
                    center = text.get_rect(center=(WIDTH/2, HEIGHT/2))
                    WINDOW.blit(text, center)
                    time.sleep(1)
                    timer -= 1
                    pygame.display.update()
                else:
                    # draw the blocks on the users screen
                    Blocks.remove_block(Blocks.block_coord)
                    game_over = Blocks.collision(Blocks.block_coord,
                                                 pygame.mouse.get_pos())

                    time.sleep(0.001)
                    text = FONT.render(f"Score: {score}", True, BLACK)
                    WINDOW.blit(text, (10, 5))
                    text = FONT.render(f"High Score: {high_score}", True, BLACK)
                    WINDOW.blit(text, (400, 5))

                    pygame.display.update()

                    # increment the y coordinate of every block (makes blocks move down)
                    for i in range(0, len(Blocks.block_coord)):
                        increment = 0.5 + (0.1 * score / 100)
                        if increment > 1.25:
                            increment = 1.25
                        Blocks.block_coord[i][1] += increment

                        # changes the colour of the block
                        if red >= 255:
                            direction = "D"
                        elif red <= 0:
                            direction = "U"

                        if direction == "U":
                            red += 0.01
                        else:
                            red -= 0.01
            else:
                # update the users high score
                if score > high_score:
                    high_score = score
                # displays the game over screen
                WINDOW.fill(BLACK)
                font = pygame.font.Font('freesansbold.ttf', 55)
                text = font.render(f"YOU LOSE", True, WHITE)
                center = text.get_rect(center=(WIDTH/2, HEIGHT/2))
                WINDOW.blit(text, center)
                text = FONT.render(f"Score: {score}", True, WHITE)
                center = text.get_rect(center=(WIDTH/2, HEIGHT/2 + 75))
                WINDOW.blit(text, center)
                center = text.get_rect(center=(WIDTH/2, HEIGHT/2 + 125))
                play_again_button = Button(center[0], center[1], 100, 25, WHITE, "Play Again")
                play_again_button.draw()
                pygame.display.update()
        else:
            # visuals
            Title = pygame.font.SysFont('Ariel', 50)
            description = pygame.font.SysFont('Ariel', 20)

            # changes background colour
            WINDOW.fill(BLACK)

            textsurface = Title.render('Instructions', False, WHITE)
            WINDOW.blit(textsurface, (200, 20))

            instructions = description.render('Like suffering? Good. The goal is to survive for as long as possible, ',
                                              False, WHITE)
            instructions2 = description.render(
                'using your cursor to navigate through the maze without touching the walls. Do not die :)', False,
                WHITE)
            instructions3 = description.render('NO ONE HAS EVER GONE PAST 1000', False, RED)
            WINDOW.blit(instructions, (70, 80))
            WINDOW.blit(instructions2, (20, 100))
            WINDOW.blit(instructions3,(180, 130))

            # load button images
            start_img = pygame.image.load('startbutton.png').convert_alpha()
            exit_img = pygame.image.load('exit.png').convert_alpha()

            # start button
            start_button = Image(120, 150, start_img, 0.475)
            exit_button = Image(120, 325, exit_img, 1)
            start_button.draw()
            exit_button.draw()
            pygame.display.update()

    pygame.quit()


main()
