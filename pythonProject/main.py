import pygame
from sys import exit
from random import shuffle
from building import bq
from chasing import cq, options, answers
from team import Team

# STARTING
pygame.init()
screen = pygame.display.set_mode((750, 750))
pygame.display.set_caption("The Amaze Chase")
clock = pygame.time.Clock()

# VARIABLES
build_counter, build_order = 0, [i for i in range(82)]
shuffle(build_order)

transition_slide = 1
chase_counter, cq_slide = 0, 1
phase = 0

paused = ticking = False

start_time = 6000

# SOUNDS
money_sound = pygame.mixer.Sound("money.wav")
reveal_sound = pygame.mixer.Sound("reveal.wav")
chaser_intro = pygame.mixer.Sound("chaser_intro.wav")
question_sound = pygame.mixer.Sound("chase_question.wav")
alarm_sound = pygame.mixer.Sound("alarm.wav")


def play_sound(sound):
    pygame.mixer.stop()
    pygame.mixer.Sound.play(sound)


# IMAGES
right_arrow, left_arrow = pygame.image.load("right_arrow.png"), pygame.image.load("left_arrow.png")

# TEAM OBJECTS
team1, team2, team3, team4, team5, chaser = Team("T1"), Team("T2"), Team("T3"), Team("T4"), Team("T5"), Team("Chaser")
chaser.space = 0
teams = [team1, team2, team3, team4, team5]

# FONTS
text_font = pygame.font.Font(None, 21)
bigger_font = label_font = pygame.font.Font(None, 27)
paused_font = pygame.font.Font(None, 50)

# SURFACES
background_surf = pygame.Surface((750, 1000))
background_surf.fill("darkblue")

plus_surf = bigger_font.render("+", False, "grey")
minus_surf = bigger_font.render("-", False, "grey")
halve_surf = text_font.render("/2", False, "grey")
double_surf = text_font.render("x2", False, "grey")
up_surf = text_font.render("UP", False, "grey")
back_surf = text_font.render("BACK", False, "grey")
next_surf = label_font.render("NEXT", False, "white")
reset_surf = label_font.render("RESET", False, "white")
pause_surf = label_font.render("PAUSE", False, "white")

# GAME LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # IF GAME ISN'T PAUSED
        if not paused:
            # TITLE SCREEN
            if phase == 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # NEXT BUTTON
                    if 6 <= mouse_pos[0] <= 63 and 722 <= mouse_pos[1] <= 745:
                        phase = 1
                        ticking = True
                        pygame.mixer.Sound.play(question_sound)
            # BUILDING PHASE
            elif phase == 1:
                if event.type == pygame.KEYDOWN:
                    # RIGHT ARROW KEY
                    if keys[pygame.K_RIGHT] and build_counter != 81:
                        build_counter += 1
                    # LEFT ARROW KEY
                    elif keys[pygame.K_LEFT] and build_counter != 0:
                        build_counter -= 1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 32 <= mouse_pos[1] <= 47:
                        # + BUTTONS
                        if 8 <= mouse_pos[0] % 150 <= 23:
                            pygame.mixer.Sound.play(money_sound)
                            teams[mouse_pos[0] // 150].add()
                        # - BUTTONS
                        elif 31 <= mouse_pos[0] % 150 <= 43:
                            teams[mouse_pos[0] // 150].sub()
                    # NEXT BUTTON
                    elif 6 <= mouse_pos[0] <= 63 and 722 <= mouse_pos[1] <= 745:
                        phase = 2
                        for team in teams:
                            team.move_space(team.score // 500)
                        play_sound(chaser_intro)
            # TRANSITION PHASE
            elif phase == 2:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 32 <= mouse_pos[1] <= 45:
                        # HALVE BUTTON
                        if 51 <= mouse_pos[0] % 150 <= 69:
                            teams[mouse_pos[0] // 150].halve()
                            teams[mouse_pos[0] // 150].move_space(1)
                        # DOUBLE BUTTON
                        elif 77 <= mouse_pos[0] % 150 <= 100:
                            pygame.mixer.Sound.play(money_sound)
                            teams[mouse_pos[0] // 150].double()
                            teams[mouse_pos[0] // 150].move_space(-1)
                    # NEXT BUTTON
                    elif 6 <= mouse_pos[0] <= 63 and 722 <= mouse_pos[1] <= 745:
                        play_sound(question_sound)
                        phase = 3
                elif event.type == pygame.KEYDOWN:
                    # RIGHT ARROW KEY
                    if keys[pygame.K_RIGHT]:
                        transition_slide = 2
                    # LEFT ARROW KEY
                    elif keys[pygame.K_LEFT] and transition_slide == 2:
                        play_sound(chaser_intro)
                        transition_slide = 1
            # CHASE PHASE
            else:
                if event.type == pygame.KEYDOWN:
                    # RIGHT ARROW KEY
                    if keys[pygame.K_RIGHT] and not (chase_counter == 13 and cq_slide == 3):
                        if cq_slide == 3:
                            cq_slide = 1
                            chase_counter += 1
                            pygame.mixer.Sound.play(question_sound)
                        else:
                            cq_slide += 1
                            if cq_slide == 3:
                                play_sound(reveal_sound)
                    # LEFT ARROW KEY
                    elif keys[pygame.K_LEFT] and not (chase_counter == 0 and cq_slide == 1):
                        if cq_slide == 1:
                            cq_slide = 3
                            chase_counter -= 1
                            play_sound(reveal_sound)
                        else:
                            cq_slide -= 1
                            if cq_slide == 2:
                                pygame.mixer.Sound.play(question_sound)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 53 <= mouse_pos[1] <= 69:
                        # UP BUTTON
                        if 6 <= mouse_pos[0] % 150 <= 34 and teams[mouse_pos[0] // 150].space < 8:
                            teams[mouse_pos[0] // 150].move_space(1)
                        # DOWN BUTTON
                        elif 51 <= mouse_pos[0] % 150 <= 100 and teams[mouse_pos[0] // 150].space > 1:
                            teams[mouse_pos[0] // 150].move_space(-1)
                    elif 117 <= mouse_pos[1] <= 138:
                        # CHASER UP BUTTON
                        if 5 <= mouse_pos[0] <= 35 and chaser.space < 7:
                            chaser.move_space(1)
                        # CHASER DOWN BUTTON
                        elif 52 <= mouse_pos[0] <= 99 and chaser.space > 0:
                            chaser.move_space(-1)

        if event.type == pygame.MOUSEBUTTONDOWN and phase:
            if 722 <= mouse_pos[1] <= 745:
                # PAUSE BUTTON
                if 335 <= mouse_pos[0] <= 403:
                    paused = not paused
                    if not paused:
                        if phase == 1 or (phase == 3 and cq_slide != 3):
                            pygame.mixer.Sound.play(question_sound)
                            if phase == 1:
                                ticking = True
                # RESET BUTTON
                elif 677 <= mouse_pos[0] <= 744:
                    phase = build_counter = chase_counter = paused = False
                    cq_slide = 1
                    pygame.mixer.stop()
                    for team in teams:
                        team.reset()
                    start_time = 6000
                    shuffle(build_order)

    for team in teams:
        if team.eliminated:
            team.text = f"{team.name}: 2pts / ELIM"
        elif team.victorious:
            team.text = f"{team.name}: {team.score // 50}pts / HOME"
        else:
            team.text = f"{team.name}: ${team.score}"
            if phase >= 2:
                team.text += f" / {team.space}sp"

    team1_surf = text_font.render(team1.text, False, "white")
    team2_surf = text_font.render(team2.text, False, "white")
    team3_surf = text_font.render(team3.text, False, "white")
    team4_surf = text_font.render(team4.text, False, "white")
    team5_surf = text_font.render(team5.text, False, "white")
    chaser_surf = text_font.render(f"{chaser.name}: {chaser.space}sp", False, "white")

    # Display blue background
    screen.blit(background_surf, (0, 0))

    if paused:
        question_surf = paused_font.render("PAUSED", False, "white")
        ticking = False
        pygame.mixer.stop()
    else:
        if phase == 0:
            question_surf = bigger_font.render("THE AMAZE CHASE", False, "white")
        elif phase == 1:
            question_surf = bigger_font.render(f"{bq[build_order[build_counter]]}", False, "white")
        elif phase == 2:
            if transition_slide == 1:
                question_surf = bigger_font.render("Introducing our Chaser!", False, "white")
            else:
                question_surf = bigger_font.render("Preparing for the Chase Phase...", False, "white")
        else:
            question_surf = bigger_font.render(f"{cq[chase_counter]}", False, "white")
            for team in teams:
                if team.space == 8:
                    team.victorious = True
                else:
                    team.victorious = False

                if team.space <= chaser.space:
                    team.eliminated = True
                else:
                    team.eliminated = False

    question_rect = question_surf.get_rect(center=(375, 375))
    screen.blit(question_surf, question_rect)

    option1_surf = bigger_font.render(f"A) {options[chase_counter][0]}", False, "white")
    option1_rect = option1_surf.get_rect(center=(375, 425))
    option2_surf = bigger_font.render(f"B) {options[chase_counter][1]}", False, "white")
    option2_rect = option2_surf.get_rect(center=(375, 475))
    option3_surf = bigger_font.render(f"C) {options[chase_counter][2]}", False, "white")
    option3_rect = option3_surf.get_rect(center=(375, 525))
    option_rects = [option1_rect, option2_rect, option3_rect]

    if not paused:
        if cq_slide >= 2:
            screen.blit(option1_surf, option1_rect)
            screen.blit(option2_surf, option2_rect)
            screen.blit(option3_surf, option3_rect)
        if cq_slide == 3:
            row = answers[chase_counter]
            left_arrow_rect = left_arrow.get_rect(midleft=option_rects[row].midright)
            right_arrow_rect = right_arrow.get_rect(midright=option_rects[row].midleft)

            screen.blit(left_arrow, left_arrow_rect)
            screen.blit(right_arrow, right_arrow_rect)

    if phase:
        for i in range(10, 611, 150):
            screen.blit(plus_surf, (i, 30))
        for i in range(35, 636, 150):
            screen.blit(minus_surf, (i, 30))
        for i in range(55, 656, 150):
            screen.blit(halve_surf, (i, 34))
        for i in range(80, 681, 150):
            screen.blit(double_surf, (i, 34))
        for i in range(10, 611, 150):
            screen.blit(up_surf, (i, 55))
        for i in range(55, 656, 150):
            screen.blit(back_surf, (i, 55))

        screen.blit(team1_surf, (10, 10))
        screen.blit(team2_surf, (160, 10))
        screen.blit(team3_surf, (310, 10))
        screen.blit(team4_surf, (460, 10))
        screen.blit(team5_surf, (610, 10))

        screen.blit(pause_surf, (340, 725))
        screen.blit(reset_surf, (680, 725))

        if phase == 3:
            screen.blit(chaser_surf, (10, 100))
            screen.blit(up_surf, (10, 120))
            screen.blit(back_surf, (55, 120))

        time_surf = bigger_font.render(f"{(start_time / 100):.2f}", False, "white")
        if phase == 1:
            screen.blit(time_surf, (355, 270))
            if ticking:
                start_time -= 1

        if start_time < 0 and not paused:
            play_sound(alarm_sound)
            pygame.time.delay(2000)
            ticking = False
            if build_counter != 81:
                build_counter += 1
            paused = True
            start_time = 6000

    # Display chase, pause, reset buttons
    screen.blit(next_surf, (10, 725))

    pygame.display.update()
    clock.tick(100)
