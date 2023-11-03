from os import path


import pygame
pygame.init()


screen = pygame.display.set_mode([858, 525])


white = (255,)*3
menu, game = True, True


big_font = pygame.font.Font(path.realpath('assets')+'\\bit5x3.ttf', 100)
title_text = big_font.render('PONG', False, white)
tt_rect = ((858-title_text.get_width())//2, 525//3-title_text.get_height(), title_text.get_width(), title_text.get_height())

medium_font = pygame.font.Font(path.realpath('assets')+'\\bit5x3.ttf', 25)
button_text = medium_font.render('PLAY', False, white)
bt_rect = ((858-button_text.get_width())//2, 525//2, button_text.get_width(), button_text.get_height())
b_rect = ((858-bt_rect[2]*1.5)//2, 525//2-bt_rect[3]//3, bt_rect[2]*1.5, bt_rect[3]*1.5)

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


while game: break


pygame.quit()
