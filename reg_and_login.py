import pygame
import pygame_gui
from manage_db import SuperGameDB
import subprocess


pygame.init()

window_surface = pygame.display.set_mode((800, 600))

manager = pygame_gui.UIManager((800, 600))

username_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((340, 200), (150, 50)),
                                                          manager=manager)
password_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((340, 250), (150, 50)),
                                                          manager=manager)

login_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((340, 330), (150, 50)), text='Вход',
                                            manager=manager)
register_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((340, 380), (150, 50)), text='Регистрация',
                                               manager=manager)

db = SuperGameDB("supergame.db")
db.create_databases()


def check_credentials(username, password):
    user = db.get_user_by_login(username, password)
    if user and user[2] == password:
        return True
    else:
        return False


def register_user(username, password):
    user = db.get_user_by_login(username, password)
    if not user:
        db.insert_user(username, password)
        return True
    else:
        return False


clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                username = username_text_entry.get_text()
                password = password_text_entry.get_text()
                user_id = db.get_user_id_by_login(username, password)
                if event.ui_element == login_button:
                    if check_credentials(username, password):
                        if check_credentials(username, password):
                            print('Успешный вход в систему!')
                            subprocess.call(["python", "main.py", str(user_id)])
                        else:
                            print('Неверное имя пользователя или пароль')
                elif event.ui_element == register_button:
                    if register_user(username, password):
                        if check_credentials(username, password):
                            print('Успешная регистрация!')
                            subprocess.call(["python", "main.py", str(user_id)])
                        else:
                            print('Пользователь уже существует')


        manager.process_events(event)

    manager.update(time_delta)

    window_surface.fill(pygame.Color('#dac7b2'))

    manager.draw_ui(window_surface)

    pygame.display.update()

db.close_connection()
