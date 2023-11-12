from pathlib import Path
assets_dir = str(Path( __file__ ).parent.absolute()) + r'\assets'


import pygame, time
pygame.init()

screen_size = (858, 525)
screen = pygame.display.set_mode(screen_size)
FPS = 60


white = (255,)*3
menu, game = True, True


big_font = pygame.font.Font(assets_dir+r'\bit5x3.ttf', 100)
title_text = big_font.render('PONG', False, white)
tt_rect = ((screen_size[0]-title_text.get_width())//2, screen_size[1]//3-title_text.get_height(), title_text.get_width(), title_text.get_height())

medium_font = pygame.font.Font(assets_dir + r'\bit5x3.ttf', 25)
button_text = medium_font.render('PLAY', False, white)
bt_rect = ((screen_size[0]-button_text.get_width())//2, screen_size[1]//2, button_text.get_width(), button_text.get_height())
b_rect = ((screen_size[0]-bt_rect[2]*1.5)//2, screen_size[1]//2-bt_rect[3]//3, bt_rect[2]*1.5, bt_rect[3]*1.5)

prev_time = time.time()
while menu:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game, menu = False, False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE: game, menu = False, False
            elif event.key == pygame.K_RETURN: menu = False

        if event.type == pygame.MOUSEBUTTONUP:
            if b_rect[0] <= event.pos[0] and event.pos[0] <= b_rect[0]+b_rect[2]:
                if b_rect[1] <= event.pos[1] and event.pos[1] <= b_rect[1]+b_rect[3]:
                    menu = False

    
    current_time = time.time()
    dt = current_time-prev_time
    prev_time = current_time
    sleep_time = 1./FPS-dt
    if sleep_time>0: time.sleep(sleep_time)

    screen.blit(button_text, bt_rect[:2])
    pygame.draw.rect(screen, white, pygame.Rect(b_rect), 2)
    screen.blit(title_text, tt_rect[:2])
    pygame.display.update()

paddle_size = [5, 40]
paddle_v = 1

p1_pos = [5,5]
p2_pos = [screen_size[0]-paddle_size[0]-5,5]

ball_pos = []
ball_v = []

prev_time = time.time()
while game:
    for event in pygame.event.get():

        if event.type == pygame.QUIT: game = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE: game = False

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_w]:
        if p1_pos[1]-paddle_v>=5: p1_pos[1] -= paddle_v
    if pressed_keys[pygame.K_s]:
        if p1_pos[1]+paddle_v<=screen_size[1]-paddle_size[1]-5: p1_pos[1] += paddle_v
    if pressed_keys[pygame.K_UP]:
        if p2_pos[1]-paddle_v>=5: p2_pos[1] -= paddle_v
    if pressed_keys[pygame.K_DOWN]:
        if p2_pos[1]+paddle_v<=screen_size[1]-paddle_size[1]-5: p2_pos[1] += paddle_v

    current_time = time.time()
    dt = current_time-prev_time
    prev_time = current_time
    sleep_time = 1./FPS-dt
    if sleep_time>0:
        time.sleep(sleep_time)

    screen.fill((0,0,0))
    pygame.draw.ellipse(screen, white, p1_pos+paddle_size)
    pygame.draw.ellipse(screen, white, p2_pos+paddle_size)
    pygame.display.update()

    


pygame.quit()
