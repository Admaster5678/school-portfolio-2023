from pathlib import Path
assets_dir = Path(Path( __file__ ).parent, 'assets')

import pygame, time
pygame.init()
pygame.mixer.init()

screen_size = (858, 525)
screen = pygame.display.set_mode(screen_size)
FPS = 60

white, black, grey = (255,)*3, (0,)*3, (48,)*3
menu, game, end_scr = True, True, True

big_font = pygame.font.Font(str(Path(assets_dir, 'bit5x3.ttf')), 100)
title_text = big_font.render('PONG', False, white)
tt_rect = ((screen_size[0]-title_text.get_width())//2, screen_size[1]//3-title_text.get_height(), title_text.get_width(), title_text.get_height())

medium_font = pygame.font.Font(str(Path(assets_dir, 'bit5x3.ttf')), 25)
button_text = medium_font.render('PLAY', False, white)
bt_rect = ((screen_size[0]-button_text.get_width())//2, screen_size[1]//2, button_text.get_width(), button_text.get_height())
b_rect = ((screen_size[0]-bt_rect[2]*1.5)//2, screen_size[1]//2-bt_rect[3]//3, bt_rect[2]*1.5, bt_rect[3]*1.5)
h_button_text = medium_font.render('PLAY', False, grey)

num_text_tuple = tuple([big_font.render(str(i), False, white) for i in range(10)])
num_text_size = (num_text_tuple[0].get_width(), num_text_tuple[0].get_height())

hit_sound = pygame.mixer.Sound(str(Path(assets_dir, 'hit.mp3')))
bounce_sound = pygame.mixer.Sound(str(Path(assets_dir, 'bounce.mp3')))
score_sound = pygame.mixer.Sound(str(Path(assets_dir, 'score.mp3')))

prev_time = time.time()
while menu:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game, menu, end_scr = False, False, False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE: game, menu, end_scr = False, False, False
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
    
    screen.fill(black)

    mouse_pos = pygame.mouse.get_pos()
    if b_rect[0] <= mouse_pos[0] and mouse_pos[0] <= b_rect[0]+b_rect[2] and b_rect[1] <= mouse_pos[1] and mouse_pos[1] <= b_rect[1]+b_rect[3]:
        screen.blit(h_button_text, bt_rect[:2])
        pygame.draw.rect(screen, grey, b_rect, 2)
    else:
        screen.blit(button_text, bt_rect[:2])
        pygame.draw.rect(screen, white, b_rect, 2)
    screen.blit(title_text, tt_rect[:2])
    pygame.display.update()

paddle_size = [5, 40]
paddle_v = 5

p1_pos = [50, (screen_size[1]-paddle_size[1])//2]
p2_pos = [screen_size[0]-paddle_size[0]-50, (screen_size[1]-paddle_size[1])//2]

ball_r = 5
ball_pos = [screen_size[0]/2, screen_size[1]/2]
ball_v = [-2., 1.]

hit_count = 0

net_line_size = (5,15)

score = [0,0]

prev_time = time.time()
while game:
    for event in pygame.event.get():

        if event.type == pygame.QUIT: game, end_scr = False, False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE: game, end_scr = False, False

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_w]:
        if p1_pos[1]-paddle_v>=20: p1_pos[1] -= paddle_v
    if pressed_keys[pygame.K_s]:
        if p1_pos[1]+paddle_v<=screen_size[1]-paddle_size[1]-20: p1_pos[1] += paddle_v
    if pressed_keys[pygame.K_UP]:
        if p2_pos[1]-paddle_v>=20: p2_pos[1] -= paddle_v
    if pressed_keys[pygame.K_DOWN]:
        if p2_pos[1]+paddle_v<=screen_size[1]-paddle_size[1]-20: p2_pos[1] += paddle_v

    if ball_pos[0]-ball_r<=p1_pos[0]+paddle_size[0] and ball_pos[0]-ball_r-ball_v[0]>p1_pos[0]+paddle_size[0]:
        if p1_pos[1]<=ball_pos[1]+ball_r and ball_pos[1]-ball_r<=p1_pos[1]+paddle_size[1]:
            ball_v[1] = (ball_v[0]*(2*(ball_pos[1]-p1_pos[1])-paddle_size[1])/paddle_size[1])
            if ball_v[0]<0: ball_v[1]*=-1
            ball_v[0]*=-1
            hit_sound.play()
            hit_count+=1
            if hit_count>4:
                hit_count = 0
                ball_v[0]*=1.25
    if ball_pos[0]+ball_r>=p2_pos[0] and ball_pos[0]+ball_r-ball_v[0]<p2_pos[0]:
        if p2_pos[1]<=ball_pos[1]+ball_r and ball_pos[1]-ball_r<=p2_pos[1]+paddle_size[1]:
            ball_v[1] = (ball_v[0]*(2*(ball_pos[1]-p2_pos[1])-paddle_size[1])/paddle_size[1])
            if ball_v[0]<0: ball_v[1]*=-1
            ball_v[0]*=-1
            hit_sound.play()
            hit_count+=1
            if hit_count>4:
                hit_count = 0
                ball_v[0]*=1.25

    if ball_pos[0]<0:
        ball_pos = [screen_size[0]/2, ball_pos[1]]
        ball_v = [2., ball_v[1]*-1]
        hit_count=0
        score[1]+=1
        score_sound.play()
        if score[1]>10 and score[1]-score[0]>1:
            game = False
        elif score[0]>17 and score[1]>17:
            game = False

    elif ball_pos[0]>screen_size[0]:
        ball_pos = [screen_size[0]/2, ball_pos[1]]
        ball_v = [-2., ball_v[1]*-1]
        hit_count=0
        score[0]+=1
        score_sound.play()
        if score[0]>10 and score[0]-score[1]>1: 
            game = False
        elif score[0]>17 and score[1]>17:
            game = False

    elif ball_pos[1]-ball_r+ball_v[1] < 20 or ball_pos[1]+ball_r+ball_v[1] > screen_size[1]-20-2*ball_r:
        bounce_sound.play()
        ball_v[1]*=-1
    
    ball_pos[0]+=ball_v[0]
    ball_pos[1]+=ball_v[1]

    current_time = time.time()
    dt = current_time-prev_time
    prev_time = current_time
    sleep_time = 1./FPS-dt
    if sleep_time>0: time.sleep(sleep_time)

    screen.fill(black)

    if score[0]>9: screen.blit(num_text_tuple[1], (screen_size[0]//4-num_text_size[0], 40))
    if score[1]>9: screen.blit(num_text_tuple[1], (screen_size[0]*3//4-num_text_size[0], 40))
    screen.blit(num_text_tuple[score[0]%10], (screen_size[0]//4, 40))
    screen.blit(num_text_tuple[score[1]%10], (screen_size[0]*3//4, 40))

    pygame.draw.rect(screen, white, p1_pos+paddle_size)
    pygame.draw.rect(screen, white, p2_pos+paddle_size)
    pygame.draw.circle(screen, white, ball_pos, ball_r)

    net_line_x, net_line_y = (screen_size[0]-net_line_size[0])//2, 20
    while net_line_y <= screen_size[1]-20-net_line_size[1]:
        pygame.draw.rect(screen, white, (net_line_x, net_line_y)+net_line_size)
        net_line_y+=net_line_size[1]+5
        
    pygame.display.update()

end_result_text = big_font.render('Tie!' if score[0] == score[1] else 'Player '+('1' if score[0]>score[1] else '2')+' wins!', False, white)
end_result_text_rect = ((screen_size[0]-end_result_text.get_width())//2, screen_size[1]//3-end_result_text.get_height(), end_result_text.get_width(), end_result_text.get_height())

exit_button_text = medium_font.render('Exit', False, white)
h_exit_button_text = medium_font.render('Exit', False, grey)
exit_button_text_rect = ((screen_size[0]-exit_button_text.get_width())//2, screen_size[1]//2, exit_button_text.get_width(), exit_button_text.get_height())
exit_button_rect = ((screen_size[0]-exit_button_text_rect[2]*1.5)//2, screen_size[1]//2-exit_button_text_rect[3]//3, exit_button_text_rect[2]*1.5, exit_button_text_rect[3]*1.5)

prev_time = time.time()
while end_scr:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            end_scr = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE: end_scr = False

        if event.type == pygame.MOUSEBUTTONUP:
            if exit_button_rect[0] <= event.pos[0] and event.pos[0] <= exit_button_rect[0]+exit_button_rect[2]:
                if exit_button_rect[1] <= event.pos[1] and event.pos[1] <= exit_button_rect[1]+exit_button_rect[3]: end_scr = False

    current_time = time.time()
    dt = current_time-prev_time
    prev_time = current_time
    sleep_time = 1./FPS-dt
    if sleep_time>0: time.sleep(sleep_time)

    screen.fill(black)
    
    mouse_pos = pygame.mouse.get_pos()
    if exit_button_rect[0] <= mouse_pos[0] and mouse_pos[0] <= exit_button_rect[0]+exit_button_rect[2] and exit_button_rect[1] <= mouse_pos[1] and mouse_pos[1] <= exit_button_rect[1]+exit_button_rect[3]:
        screen.blit(h_exit_button_text, exit_button_text_rect[:2])
        pygame.draw.rect(screen, grey, exit_button_rect, 2)
    else:
        screen.blit(exit_button_text, exit_button_text_rect[:2])
        pygame.draw.rect(screen, white, exit_button_rect, 2)

    screen.blit(end_result_text, end_result_text_rect[:2])
    
    pygame.display.update()

pygame.mixer.quit()
pygame.quit()