import pygame
import sys
from manage_db import SuperGameDB

db = SuperGameDB("supergame.db")

user_id = int(sys.argv[1])
clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((800, 450))  # flags=pygame.NOFRAME
pygame.display.set_caption("Running Warrior")
icon = pygame.image.load('images/gameicon.png').convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load('images/bg.png').convert_alpha()
walk_left = [
    pygame.image.load('images/player_left/player_left1.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left2.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left3.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left4.png').convert_alpha(),
]
walk_right = [
    pygame.image.load('images/player_right/player_right1.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right2.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right3.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right4.png').convert_alpha(),
]

ghost = pygame.image.load('images/ghost.png').convert_alpha()
ghost_list_in_game = []

player_anim_count = 0
bg_x = 0

player_speed = 5
player_x = 150
player_y = 315

is_jump = False
jump_count = 8

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)

score_timer = pygame.USEREVENT + 2
pygame.time.set_timer(score_timer, 1000)

label = pygame.font.Font('fonts/Geologica_Auto-Bold.ttf', 40)
lose_label = label.render('Игра окончена!', True, (188, 89, 31))
restart_label = label.render('Играть заново', True, (111, 167, 121))
restart_label_rect = restart_label.get_rect(topleft=(50, 100))
exit_label = label.render('Выход', True, (111, 167, 121))
exit_label_rect = exit_label.get_rect(topleft=(530, 100))

bullets_left = 5
bullet = pygame.image.load('images/bullet.png').convert_alpha()
bullets = []

gameplay = True
score = 0

running = True
while running:
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 800, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if ghost_list_in_game:
            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 10

                if el.x < -10:
                    ghost_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 500:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
                score += 3
        else:
            if jump_count >= - 8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -800:
            bg_x = 0

        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4

                if el.x > 802:
                    bullets.pop(i)

                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)
                            score += 2
    else:
        screen.fill((227, 208, 177))
        screen.blit(lose_label, (255, 20))
        screen.blit(restart_label, restart_label_rect)
        screen.blit(exit_label, exit_label_rect)
        score_text = label.render('Ваш счёт: {}'.format(score), True, (255, 255, 255))
        score_text_rect = score_text.get_rect(center=(400, 200))
        screen.blit(score_text, score_text_rect)

        top_users = db.get_top_users()
        leaderboard_font = pygame.font.Font('fonts/Geologica_Auto-Bold.ttf', 30)
        leaderboard_text = leaderboard_font.render('Таблица лидеров', True, (255, 255, 255))
        screen.blit(leaderboard_text, (280, 250))
        y_offset = 300
        for index, user in enumerate(top_users):
            user_text = leaderboard_font.render(f'{index + 1}. {user[0]} - {user[1]} очков', True, (255, 255, 255))
            screen.blit(user_text, (280, y_offset))
            y_offset += 40

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            ghost_list_in_game.clear()
            bullets.clear()
            bullets_left = 5
            db.insert_game(score, user_id)
            score = 0
        elif exit_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            running = False
            pygame.quit()
            db.insert_game(score, user_id)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(802, 315)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            bullets_left -= 1
        if event.type == score_timer:
            if gameplay:
                score += 1

    clock.tick(30)
