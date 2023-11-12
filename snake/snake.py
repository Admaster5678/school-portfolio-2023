from pathlib import Path
assets_dir = str(Path( __file__ ).parent.absolute()) + r'\assets'


import pygame
pygame.init()

screen_size = (858, 525)
screen = pygame.display.set_mode(screen_size)


white = (255,)*3
menu, game = True, True


big_font = pygame.font.Font(assets_dir+r'\bit5x3.ttf', 100)
title_text = big_font.render('PONG', False, white)
tt_rect = ((screen_size[0]-title_text.get_width())//2, screen_size[1]//3-title_text.get_height(), title_text.get_width(), title_text.get_height())

medium_font = pygame.font.Font(assets_dir + r'\bit5x3.ttf', 25)
button_text = medium_font.render('PLAY', False, white)
bt_rect = ((screen_size[0]-button_text.get_width())//2, screen_size[1]//2, button_text.get_width(), button_text.get_height())
b_rect = ((screen_size[0]-bt_rect[2]*1.5)//2, screen_size[1]//2-bt_rect[3]//3, bt_rect[2]*1.5, bt_rect[3]*1.5)

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

    

    screen.blit(button_text, bt_rect[:2])
    pygame.draw.rect(screen, white, pygame.Rect(b_rect), 2)
    screen.blit(title_text, tt_rect[:2])
    pygame.display.update()

p1_pos = ()
p1_v = 1

p2_pos = ()
p2_v = 1

ball_pos = ()
ball_v = ()
while game:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE: game = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: p1_pos -= p1_v
            elif event.key == pygame.K_DOWN: p1_pos += p1_v
            elif event.key == pygame.K_w: p2_pos -= p2_v
            elif event.key == pygame.K_s: p2_pos += p2_v

    
    screen.fill((0,0,0))

    pygame.display.update()

    


pygame.quit()
