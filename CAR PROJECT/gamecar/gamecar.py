import pygame
import time
import random

pygame.init()

gameExit = False

display_width = int(1280 * 1.1)
display_height = int(720 * 1.1)

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
brown = (165, 42, 42)

car_width = 60

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Đua xe 2 người")
clock = pygame.time.Clock()

CarA = pygame.image.load('D:\\CAR PROJECT\\images\\car1.jpg')
CarB = pygame.image.load('D:\\CAR PROJECT\\images\\car2.jpg')

def get_high_score():
    high_score = 0
    try:
        high_score_file = open("high_score.txt", "r")
        high_score = int(high_score_file.read())
        high_score_file.close()
    except IOError:
        print("There is no high score yet!")
    except ValueError:
        print("I'm confused. Starting with no high score.")

    return high_score

def save_high_score(new_high_score):
    try:
        high_score_file = open("high_score.txt", "w")
        high_score_file.write(str(new_high_score))
        high_score_file.close()
    except IOError:
        print("Unable to save the high score.")

def things_dodged(count):
    high_score = get_high_score()
    font = pygame.font.SysFont(None, 40)
    text = font.render("Score: " + str(count), True, black)
    if count > high_score:
        save_high_score(count)
    highScore = font.render("High Score: " + str(high_score), True, black)
    gameDisplay.blit(text, (20, 20))
    gameDisplay.blit(highScore, (20, 50))

def car1(x, y):
    gameDisplay.blit(CarA, (x, y))

def car2(x, y):
    gameDisplay.blit(CarB, (x, y))

def things(thingx, thingy, thingw, thingh, color):
    if color == "green":
        thing_image = pygame.image.load('D:\\CAR PROJECT\\images\\thing_green.png')
    elif color == "red":
        thing_image = pygame.image.load('D:\\CAR PROJECT\\images\\thing_red.png')
    else:
        thing_image = pygame.Surface([thingw, thingh])
        thing_image.fill(color)

    gameDisplay.blit(thing_image, (thingx, thingy))

def check_car_collision(x1, y1, x2, y2, width, height):
    rect1 = pygame.Rect(x1, y1, width, height)
    rect2 = pygame.Rect(x2, y2, width, height)
    return rect1.colliderect(rect2)

def text_objects(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 3))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)

def crash(car):
    message_display('Player ' + car + ' Crashed')
    game_loop()

def crash3():
    message_display('Collision')
    game_loop()

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3:
                    intro = False

        gameDisplay.fill(white)
        message_display('1.Easy 2.Medium 3.Hard')

        pygame.display.update()
        clock.tick(15)

def game_loop():
    global gameExit  # Sử dụng biến toàn cục gameExit
    frame_count = 0
    game_intro()
    thing_speed = 5
    thing_width = 100
    thing_height = 100
    thing_starty = -600
    thing_frequency = 25

    y_change = 0
    y2_change = 0

    x = (display_width * 0.48 / 2)
    y = (display_height * 0.79)

    x2 = (display_width * 0.48 * 1.5)
    y2 = (display_height * 0.79)

    x_change = 0
    x2_change = 0

    dodged = 0

    things_list = []

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x_change = -8
                    y_change = 0
                elif event.key == pygame.K_d:
                    x_change = 8
                    y_change = 0
                elif event.key == pygame.K_w:
                    x_change = 0
                    y_change = -8
                elif event.key == pygame.K_s:
                    x_change = 0
                    y_change = 8
                if event.key == pygame.K_LEFT:
                    x2_change = -8
                    y2_change = 0
                elif event.key == pygame.K_RIGHT:
                    x2_change = 8
                    y2_change = 0
                elif event.key == pygame.K_UP:
                    x2_change = 0
                    y2_change = -8
                elif event.key == pygame.K_DOWN:
                    x2_change = 0
                    y2_change = 8

            if event.type == pygame.KEYUP:
                if (
                    event.key == pygame.K_LEFT
                    or event.key == pygame.K_RIGHT
                    or event.key == pygame.K_UP
                    or event.key == pygame.K_DOWN
                ):
                    x2_change = 0
                    y2_change = 0
                if (
                    event.key == pygame.K_d
                    or event.key == pygame.K_a
                    or event.key == pygame.K_s
                    or event.key == pygame.K_w
                ):
                    x_change = 0
                    y_change = 0

        x += x_change
        if y + y_change >= display_height * 0.79:
            y_change = 0
        elif y + y_change <= 0:
            y_change = 0
        y += y_change

        x2 += x2_change
        if y2 + y2_change >= display_height * 0.79:
            y2_change = 0
        elif y2 + y2_change <= 0:
            y2_change = 0
        y2 += y2_change

        gameDisplay.fill(white)

        # Kiểm tra va chạm giữa car1 và car2
        if check_car_collision(x, y, x2, y2, car_width, car_width):
            gameExit = True

        for thing in things_list:
            if not thing['dodged'] and not thing['crashed']:
                if check_car_collision(x, y, thing['x'], thing['y'], thing_width, thing_height) or \
                        check_car_collision(x2, y2, thing['x'], thing['y'], thing_width, thing_height):
                    gameExit = True

                elif check_car_collision(x, y, thing['x'], thing['y'], thing_width, thing_height):
                    if thing['type'] == 'green':
                        dodged += 1
                    elif thing['type'] == 'red':
                        gameExit = True
                    thing['dodged'] = True

                elif check_car_collision(x2, y2, thing['x'], thing['y'], thing_width, thing_height):
                    if thing['type'] == 'green':
                        dodged += 1
                    elif thing['type'] == 'red':
                        gameExit = True
                    thing['crashed'] = True

                if thing['type'] == 'green':
                    things(thing['x'], thing['y'], thing_width, thing_height, 'green')
                elif thing['type'] == 'red':
                    things(thing['x'], thing['y'], thing_width, thing_height, 'red')

                thing['y'] += thing_speed

        car1(x, y)
        car2(x2, y2)
        things_dodged(dodged)

        pygame.display.update()
        clock.tick(60)

        if frame_count % thing_frequency == 0:
            new_thing = {'x': random.randrange(0, int(display_width)),
                         'y': -thing_height,
                         'dodged': False,
                         'crashed': False,
                         'type': random.choice(['green', 'red'])}
            things_list.append(new_thing)

        frame_count += 1

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, int(display_width))
            dodged += 1
            if thing_speed < 15:
                thing_speed += 1

        pygame.time.delay(thing_frequency)

    if gameExit:
        message_display('Game Over')

game_loop()
pygame.quit()
quit()
