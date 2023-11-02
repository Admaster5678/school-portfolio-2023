from os import path


import pygame
pygame.init()


screen = pygame.display.set_mode([858, 525])


white = (255,)*3
menu, game = True, True


big_font = pygame.font.Font(path.realpath('assets')+'\\bit5x3.ttf', 100)
title_text = big_font.render('PONG', False, white)

medium_font = pygame.font.Font(path.realpath('assets')+'\\bit5x3.ttf', 25)
button_text = medium_font.render('PLAY', False, white)

while menu:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game, menu = False, False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE: game, menu = False, False
            elif event.key == pygame.K_RETURN: menu = False

        if event.type == pygame.MOUSEBUTTONUP:
            if (858-button_text.get_width()*1.5)//2 <= event.pos[0] and event.pos[0] <= 858//2+button_text.get_width()*1.5//2: 
                if 525//2-button_text.get_height()//3 <= event.pos[1] and event.pos[1] <= 525//2+button_text.get_height()*7//6:
                    menu = False
    
    screen.blit(button_text, ((858-button_text.get_width())//2, 525//2))
    pygame.draw.rect(screen, white, pygame.Rect((858-button_text.get_width()*1.5)//2, 525//2-button_text.get_height()//3,
                                                button_text.get_width()*1.5, button_text.get_height()*1.5), 2)
    screen.blit(title_text, ((858-title_text.get_width())//2,525//3-title_text.get_height()))
    pygame.display.update()


while game: break


pygame.quit()
