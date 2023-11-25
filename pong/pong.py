from pathlib import Path
assets_dir = Path(Path( __file__ ).parent, 'assets') # PATH TO ASSETS DIRECTORY

import pygame
pygame.init()
pygame.mixer.init()

screen_size = (858, 525)
screen = pygame.display.set_mode(screen_size) # CREATING THE WINDOW
pygame.display.set_caption('PONG') # SETTING THE WINDOW TITLE

# GENERAL VARIABLES
FPS = 60 # NO OF TIMES OBJECT POSITIONS ARE UPDATED BY THEIR VELOCITY EACH SECOND
         # USED TO LIMIT THE ACTUAL FPS FOR THE MENU AND END SCREENS
white, black, grey = (255,)*3, (0,)*3, (48,)*3 # RGB CODES

paddle_size = [5, 55]
paddle_v = 10

p1_pos = [50, (screen_size[1]-paddle_size[1])//2]
p2_pos = [screen_size[0]-paddle_size[0]-50, (screen_size[1]-paddle_size[1])//2]

ball_r = 6
ball_pos = [screen_size[0]/2, screen_size[1]/2]
ball_v = [-4., 2.]

hit_count = 0

net_line_size = (5,15) # SIZE OF EACH DASH THAT THE NET IS MADE OF

score = [0,0]

menu, game, end_scr = True, True, True # LOOP CONTROL VARIABLES

# FUNCTION THAT RETURNS WHETHER THE MOUSE IS HOVERING OVER A RECT(REGION OF SCREEN)
def mouseover(rect, mouse_pos):
     return rect[0] <= mouse_pos[0] <=rect[0] + rect[2] and \
            rect[1] <= mouse_pos[1] <= rect[1] + rect[3]

# FUNCTION THAT RETURNS WHETHER A COLLISION HAS TAKEN PLACE B/W THE PADDLE AND BALL
# FIRST PARAM -> TRUE IF THE DEALING WITH THE LEFT PADDLE; ELSE FALSE
def paddle_hit(left_paddle, paddle_pos, paddle_size, ball_pos, ball_r):
    if left_paddle:  return ball_pos[0]-ball_r<=paddle_pos[0]+paddle_size[0] and \
                            ball_pos[0]-ball_r-ball_v[0]>paddle_pos[0]+paddle_size[0] and \
                            p1_pos[1]<=ball_pos[1] and \
                            ball_pos[1]<=p1_pos[1]+paddle_size[1]
    
    return  ball_pos[0]+ball_r>=p2_pos[0] and ball_pos[0]+ball_r-ball_v[0]<p2_pos[0] and \
            p2_pos[1]<=ball_pos[1] and ball_pos[1]<=p2_pos[1]+paddle_size[1]

# FUNCTION TO UPDATE VARIABLES WHEN 
def hit_update(paddle_pos, paddle_size, ball_pos, ball_v, hit_count):
    # ANGLE AT WHICH BALL IS SHOT DEPENDS ON HOW FAR IT HIT THE PADDLE FROM THE CENTRE
    ball_v[1] = (ball_v[0]*(2*(ball_pos[1]-paddle_pos[1])-paddle_size[1])/paddle_size[1])
    if ball_v[0]<0: ball_v[1]*=-1
    ball_v[0]*=-1
    hit_sound.play()
    hit_count+=1
    if hit_count>4:
        hit_count = 0
        ball_v[0]*=1.25
    return ball_v, hit_count

# RESOURCE DEFINITIONS

# FONTS
big_font = pygame.font.Font(str(Path(assets_dir, 'bit5x3.ttf')), 100)
medium_font = pygame.font.Font(str(Path(assets_dir, 'bit5x3.ttf')), 25)

# TITLE TEXT
title_text = big_font.render('PONG', False, white)
tt_rect = ((screen_size[0]-title_text.get_width())//2,
            screen_size[1]//3-title_text.get_height(),
            title_text.get_width(),
            title_text.get_height()
          )

# PLAY BUTTON
play_button_text = medium_font.render('PLAY', False, white)
h_play_button_text = medium_font.render('PLAY', False, grey) # BUTTON CHANGES TO GREY ON CURSOR HOVER
play_bt_rect = ((screen_size[0]-play_button_text.get_width())//2, screen_size[1]//2,
            play_button_text.get_width(), play_button_text.get_height()
          )
play_b_rect = (( screen_size[0]-play_bt_rect[2]*1.5)//2, screen_size[1]//2-play_bt_rect[3]//3,
            play_bt_rect[2]*1.5, play_bt_rect[3]*1.5
         ) # RECT FOR THE FRAME AROUND THE BUTTON

# DIGITS FOR SCORE DISPLAY
num_text_tuple = tuple([big_font.render(str(i), False, white) for i in range(10)])
num_text_size = (num_text_tuple[0].get_width(), num_text_tuple[0].get_height())

# EXIT BUTTON FOR THE END SCREEN
exit_button_text = medium_font.render('Exit', False, white)
h_exit_button_text = medium_font.render('Exit', False, grey)
exit_bt_rect = (   (screen_size[0]-exit_button_text.get_width())//2,
                            screen_size[1]//2,
                            exit_button_text.get_width(),
                            exit_button_text.get_height()
                        )
exit_b_rect = ((screen_size[0]-exit_bt_rect[2]*1.5)//2,
                    screen_size[1]//2-exit_bt_rect[3]//3,
                    exit_bt_rect[2]*1.5,
                    exit_bt_rect[3]*1.5
                   )

# SOUND EFFECTS
hit_sound = pygame.mixer.Sound(str(Path(assets_dir, 'hit.mp3')))
bounce_sound = pygame.mixer.Sound(str(Path(assets_dir, 'bounce.mp3')))
score_sound = pygame.mixer.Sound(str(Path(assets_dir, 'score.mp3')))

prev_time = pygame.time.get_ticks()
while menu:

    mouse_over_play_b = mouseover(play_b_rect, pygame.mouse.get_pos())

    for event in pygame.event.get():

        if event.type == pygame.QUIT: # CLOSING THE WINDOW
            game, menu, end_scr = (False,)*3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE: game, menu, end_scr = (False,)*3
            elif event.key == pygame.K_RETURN: menu = False

        if event.type == pygame.MOUSEBUTTONUP and mouse_over_play_b: menu = False

    # FIXED MAX FPS
    current_time = pygame.time.get_ticks()
    dt = current_time-prev_time
    prev_time = current_time
    sleep_time = 1000./FPS - dt
    if sleep_time>0: pygame.time.delay(int(sleep_time))
    
    screen.fill(black)

    if mouse_over_play_b:
        screen.blit(h_play_button_text, play_bt_rect[:2])
        pygame.draw.rect(screen, grey, play_b_rect, 2)
    else:
        screen.blit(play_button_text, play_bt_rect[:2])
        pygame.draw.rect(screen, white, play_b_rect, 2)

    screen.blit(title_text, tt_rect[:2])
    pygame.display.update()

prev_time = pygame.time.get_ticks()
while game:
    #FPS OF THE WINDOW IS UNLOCKED BUT THE POSITIONS WILL STILL
    # BE UPDATED BY V*FPS(CONST) EVERY SECOND; SO THE VELOCITY IS FIXED
    current_time = pygame.time.get_ticks()
    dt = current_time-prev_time
    prev_time = current_time
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT: game, end_scr = (False,)*2

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE: game, end_scr = (False,)*2

    # PADDLE KEYS MUST BE HANDLED LIKE THIS SINCE IF HANDLED LIKE ABOVE, THEY WOULD ONLY
    # REGISTER THE FIRST FRAME THE KEY IS HELD
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_w]:
        # PREVENTS BREACH OF TOP PADDING
        if p1_pos[1]-paddle_v>=20: p1_pos[1] -= paddle_v*dt*FPS/1000
    if pressed_keys[pygame.K_s]:
        if p1_pos[1]+paddle_size[1]+paddle_v<=screen_size[1]-20: # SAME FOR THE BOTTOM
            p1_pos[1] += paddle_v*dt*FPS/1000
    if pressed_keys[pygame.K_UP]:
        if p2_pos[1]-paddle_v>=20: p2_pos[1] -= paddle_v*dt*FPS/1000
    if pressed_keys[pygame.K_DOWN]:
        if p2_pos[1]+paddle_size[1]+paddle_v<=screen_size[1]-20:
            p2_pos[1] += paddle_v*dt*FPS/1000

    # CHECKS IF PADDLE-BALL COLLISION OCCURED AND UPDATES VALUES
    if paddle_hit(True, p1_pos, paddle_size, ball_pos, ball_r):
        ball_v, hit_count = hit_update(p1_pos, paddle_size, ball_pos, ball_v, hit_count)

    if paddle_hit(False, p2_pos, paddle_size, ball_pos, ball_r):
        ball_v, hit_count = hit_update(p2_pos, paddle_size, ball_pos, ball_v, hit_count)

    # CHECKS IF BALL LEFT SCREEN AND UPDATES SCORES AND GAME STATUS
    if ball_pos[0]<0 or ball_pos[0]>screen_size[0]:
        ball_v = [4. * (1 if ball_pos[0]<0 else -1), ball_v[1]*4./ball_v[0]*-1]
        ball_pos = [screen_size[0]/2, ball_pos[1]]
        score_sound.play()
        hit_count=0
        if  score[0]>10 and score[0]-score[1]>1 or score[1]>10 and score[1]-score[0]>1 \
        or  score[0]>17 and score[1]>17: game = False
        score[int(ball_pos[0]<0)]+=1
    # OTHERWISE, CHECKS IF BALL WILL COLLIDE WITH VERTICAL BOUNDARIES
    elif ball_pos[1]-ball_r+ball_v[1] < 20 or ball_pos[1]+ball_r+ball_v[1] > screen_size[1]-20:
        bounce_sound.play()
        ball_v[1]*=-1
    
    # REGULAR BALL UPDATION
    ball_pos[0]+=ball_v[0]*dt*FPS/1000
    ball_pos[1]+=ball_v[1]*dt*FPS/1000

    screen.fill(black)

    # RENDERS FIRST DIGIT OF SCORE IF THE SCORE IS IN 2 DIGITS
    if score[0]>9: screen.blit(num_text_tuple[1], (screen_size[0]//4-num_text_size[0], 40))
    if score[1]>9: screen.blit(num_text_tuple[1], (screen_size[0]*3//4-num_text_size[0], 40))
    # RENDERS UNIT DIGIT
    screen.blit(num_text_tuple[score[0]%10], (screen_size[0]//4, 40))
    screen.blit(num_text_tuple[score[1]%10], (screen_size[0]*3//4, 40))

    pygame.draw.rect(screen, white, p1_pos+paddle_size)
    pygame.draw.rect(screen, white, p2_pos+paddle_size)
    pygame.draw.circle(screen, white, ball_pos, ball_r)

    # RENDERS DASHED NET LINE
    net_line_x, net_line_y = (screen_size[0]-net_line_size[0])//2, 20
    while net_line_y <= screen_size[1]-20-net_line_size[1]:
        pygame.draw.rect(screen, white, (net_line_x, net_line_y)+net_line_size)
        net_line_y+=net_line_size[1]+5
        
    pygame.display.update()

# DONE HERE SO THAT ONLY 1 SURFACE NEEDS TO BE CREATED DEPENDING ON THE OUTCOME
end_result_text = big_font.render (
        'Tie!' if score[0] == score[1] else
        ('Player '+('1' if score[0]>score[1] else '2')+' wins!'),
        False, white)
end_result_text_rect = (   (screen_size[0]-end_result_text.get_width())//2,
                            screen_size[1]//3-end_result_text.get_height(),
                            end_result_text.get_width(),
                            end_result_text.get_height()
                       )

prev_time = pygame.time.get_ticks()
while end_scr:

    mouse_over_exit_b = mouseover(exit_b_rect, pygame.mouse.get_pos())

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            end_scr = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE: end_scr = False

        if event.type == pygame.MOUSEBUTTONUP and mouse_over_exit_b: end_scr = False

    # FIXED MAX FPS
    current_time = pygame.time.get_ticks()
    dt = current_time-prev_time
    prev_time = current_time
    sleep_time = 1000./FPS-dt
    if sleep_time>0: pygame.time.delay(int(sleep_time))

    screen.fill(black)

    if mouse_over_exit_b:
        screen.blit(h_exit_button_text, exit_bt_rect[:2])
        pygame.draw.rect(screen, grey, exit_b_rect, 2)
    else:
        screen.blit(exit_button_text, exit_bt_rect[:2])
        pygame.draw.rect(screen, white, exit_b_rect, 2)

    screen.blit(end_result_text, end_result_text_rect[:2])
    
    pygame.display.update()

pygame.mixer.quit()
pygame.quit()