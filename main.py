import os
import sys
import json
import time
import string
import socket
import platform
import subprocess
from random import randint, choice
from other import *
import pygame

print("[INFO]App launched")
pygame.init()


def is_connected() -> bool:
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        return False


def send_email(email_login: str, email_password: str, subject: str, text: str) -> None:
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from smtplib import SMTP_SSL
    msg: MIMEMultipart = MIMEMultipart()
    msg["From"] = email_login
    msg["To"] = email_login
    msg["Subject"] = subject
    msg.attach(MIMEText(text, "plain"))
    server: SMTP_SSL = SMTP_SSL("smtp.yandex.ru", 465)
    server.ehlo(email_login)
    server.login(email_login, email_password)
    server.auth_plain()
    server.send_message(msg)
    server.quit()


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def checking_file():
    print("[INFO]File existence check")
    try:
        with open("data.json", 'r') as data_file:
            data_file.read()
    except FileNotFoundError:
        with open("data.json", 'w') as data_file:
            user_id = ''.join(choice((string.digits + string.ascii_letters)) for _ in range(16))
            json.dump({"id": user_id, "score": 0}, data_file, indent=1)
        send_email(EmailLogin, EmailPassword, EmailSubject, "New user!")
        print("[!]Data file was created. App restarting")
        subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])
        sys.exit(0)


ScreenWidth_X = 1000
ScreenHeight_Y = 500
ScreenMaxWidth_X, ScreenMaxHeight_Y = 1000, 500
ScreenMinWidth_X, ScreenMinHeight_Y = 500, 250
Screen = pygame.display.set_mode((ScreenWidth_X, ScreenHeight_Y), pygame.RESIZABLE)
Pixel_X = ScreenWidth_X / 64
Pixel_Y = ScreenHeight_Y / 32
GlobalRunFlag = True
MerpWidth_X = 75
MerpHeight_Y = 100

IconImg = pygame.image.load(resource_path("data/icon.ico"))
MerpImg1 = pygame.transform.scale(pygame.image.load(resource_path("data/merp.png")), (MerpWidth_X, MerpHeight_Y))
MerpImg2 = pygame.transform.scale(pygame.image.load(resource_path("data/merp2.png")), (MerpWidth_X, MerpHeight_Y))
MerpImg3 = pygame.transform.scale(pygame.image.load(resource_path("data/merp3.png")), (MerpWidth_X, MerpHeight_Y))
MerpImg4 = pygame.transform.scale(pygame.image.load(resource_path("data/merp4.png")), (MerpWidth_X, MerpHeight_Y))
MerpImg5 = pygame.transform.scale(pygame.image.load(resource_path("data/merp5.png")), (MerpWidth_X, MerpHeight_Y))
MerpImg6 = pygame.transform.scale(pygame.image.load(resource_path("data/merp6.png")), (MerpWidth_X, MerpHeight_Y))
MerpImg7 = pygame.transform.scale(pygame.image.load(resource_path("data/merp7.png")), (MerpWidth_X, MerpHeight_Y))
LobbyBackground = pygame.image.load(resource_path("data/LobbyBackground.png"))
GameEscapeMenu = pygame.transform.scale(pygame.image.load(resource_path("data/GameEscapeMenu.png")),
                                        (ScreenWidth_X, ScreenHeight_Y))
GameEscapeUnMute = pygame.transform.scale(pygame.image.load(resource_path("data/UnMuteButton.png")),
                                          (Pixel_X * 12, Pixel_Y * 5))
LobbyMute = pygame.transform.scale(pygame.image.load(resource_path("data/MuteLobbyButton.png")),
                                   (Pixel_X * 5, Pixel_Y * 5))
LobbyUnMute = pygame.transform.scale(pygame.image.load(resource_path("data/UnMuteLobbyButton.png")),
                                     (Pixel_X * 5, Pixel_Y * 5))

MusicButton1 = pygame.mixer.Sound(resource_path("data/PressedButton_1.mp3"))
MusicButton2 = pygame.mixer.Sound(resource_path("data/PressedButton_2.mp3"))
MusicButton3 = pygame.mixer.Sound(resource_path("data/PressedButton_3.mp3"))
MusicClick1 = pygame.mixer.Sound(resource_path("data/Click1.mp3"))
MusicClick2 = pygame.mixer.Sound(resource_path("data/Click2.mp3"))
MusicClick3 = pygame.mixer.Sound(resource_path("data/Click3.mp3"))
MusicTheme = pygame.mixer.Sound(resource_path("data/Theme.mp3"))

pygame.display.set_caption("Clicker", "icon")
pygame.display.set_icon(IconImg)

checking_file()
with open("data.json", 'r') as DataFile:
    UserId = json.load(DataFile)["id"]
with open("data.json", 'r') as DataFile:
    Score = json.load(DataFile)["score"]

MuteFlag = False


def random_music_button():
    global MuteFlag
    if not MuteFlag:
        random_music = choice((1, 2, 3))
        match random_music:
            case 1:
                MusicButton1.play()
            case 2:
                MusicButton2.play()
            case 3:
                MusicButton3.play()


def random_music_click():
    global MuteFlag
    if not MuteFlag:
        random_music = choice((1, 2, 3))
        match random_music:
            case 1:
                MusicClick1.play()
            case 2:
                MusicClick2.play()
            case 3:
                MusicClick3.play()


def game_update():
    global GameEscapeMenu, GameEscapeUnMute, ScreenWidth_X, ScreenHeight_Y, Pixel_X, Pixel_Y
    ScreenWidth_X, ScreenHeight_Y = pygame.display.get_window_size()
    Pixel_X = ScreenWidth_X / 64
    Pixel_Y = ScreenHeight_Y / 32
    GameEscapeMenu = pygame.transform.scale(pygame.image.load(resource_path("data/GameEscapeMenu.png")),
                                            (ScreenWidth_X, ScreenHeight_Y))
    GameEscapeUnMute = pygame.transform.scale(pygame.image.load(resource_path("data/UnMuteButton.png")),
                                              (Pixel_X * 12, Pixel_Y * 5))


def lobby_update():
    global LobbyMute, LobbyUnMute
    LobbyMute = pygame.transform.scale(pygame.image.load(resource_path("data/MuteLobbyButton.png")),
                                       (Pixel_X * 5, Pixel_Y * 5))
    LobbyUnMute = pygame.transform.scale(pygame.image.load(resource_path("data/UnMuteLobbyButton.png")),
                                         (Pixel_X * 5, Pixel_Y * 5))


def game(game_run_flag):
    global Screen, ScreenWidth_X, ScreenHeight_Y, Score, GlobalRunFlag, MuteFlag
    global MusicButton1, MusicButton2
    merp_transformed_img = None
    merp_position = [0, 0]
    random_background = (randint(1, 255), randint(1, 255), randint(1, 255))

    first_click_flag = False
    escape_flag = False

    font = pygame.font.SysFont(resource_path("data/font.ttf"), 64)
    score_text = font.render(f"{Score}", True, (250, 250, 250))
    score_text_size = score_text.get_size()

    while game_run_flag:
        pygame.time.Clock().tick(120)
        pygame.display.update()
        mouse_position = pygame.mouse.get_pos()

        if escape_flag:
            game_update()
            Screen.fill(random_background)
            Screen.blit(GameEscapeMenu, (0, 0))
            if MuteFlag:
                Screen.blit(GameEscapeUnMute, (Pixel_X * 33, Pixel_Y * 17))
        else:
            Screen.fill(random_background)
            Screen.blit(score_text, ((ScreenWidth_X / 2) - score_text_size[0], ScreenHeight_Y / 10))
            if first_click_flag:
                Screen.blit(merp_transformed_img, merp_position)

        ScreenWidth_X, ScreenHeight_Y = pygame.display.get_window_size()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_run_flag = False
                GlobalRunFlag = False
            elif event.type == pygame.VIDEORESIZE:
                width = min(ScreenMaxWidth_X, max(ScreenMinWidth_X, event.w))
                height = min(ScreenMaxHeight_Y, max(ScreenMinHeight_Y, event.h))
                if (width, height) != event.size:
                    Screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            elif not escape_flag and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    random_music_click()
                    random_background = (randint(1, 255), randint(1, 255), randint(1, 255))
                    first_click_flag = True
                    if first_click_flag:
                        merp_position = [choice((0, ScreenWidth_X - MerpHeight_Y)),
                                         randint(0, ScreenHeight_Y - MerpHeight_Y)]
                        merp_look = choice(("up", "down"))
                        merp_img = choice((MerpImg1, MerpImg2, MerpImg3, MerpImg4, MerpImg5, MerpImg6, MerpImg7))
                        if merp_position[0] == 0:
                            if merp_look == "up":
                                merp_transformed_img = pygame.transform.flip(
                                    pygame.transform.rotate(merp_img, 90), True, False)
                            elif merp_look == "down":
                                merp_transformed_img = pygame.transform.rotate(merp_img, -90)
                        else:
                            if merp_look == "up":
                                merp_transformed_img = pygame.transform.flip(
                                    pygame.transform.rotate(merp_img, 90), False, True)
                            elif merp_look == "down":
                                merp_transformed_img = pygame.transform.rotate(merp_img, 90)

                    Score += 1
                    score_text = font.render(f"{Score}", True, (250, 250, 250))
                    score_text_size = score_text.get_size()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    escape_flag = not escape_flag

            if escape_flag:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if Pixel_X * 19 < mouse_position[0] < Pixel_X * 45 and \
                                Pixel_Y * 10 < mouse_position[1] < Pixel_Y * 15:
                            random_music_button()
                            escape_flag = False
                        elif Pixel_X * 19 < mouse_position[0] < Pixel_X * 32 and \
                                Pixel_Y * 17 < mouse_position[1] < Pixel_Y * 22:
                            random_music_button()
                            escape_flag = False
                            game_run_flag = False
                        elif Pixel_X * 33 < mouse_position[0] < Pixel_X * 45 and \
                                Pixel_Y * 17 < mouse_position[1] < Pixel_Y * 22:
                            MuteFlag = not MuteFlag


def lobby(run_lobby_flag):
    global Screen, ScreenWidth_X, ScreenHeight_Y, Pixel_X, Pixel_Y, GlobalRunFlag, MuteFlag
    MusicTheme.play()
    timer = time.time()
    while run_lobby_flag:
        pygame.display.flip()
        pygame.time.Clock().tick(120)

        if time.time() - timer >= MusicTheme.get_length():
            timer = time.time()
            MusicTheme.play()

        lobby_update()
        Screen.blit(pygame.transform.scale(LobbyBackground, (ScreenWidth_X, ScreenHeight_Y)), (0, 0))
        if MuteFlag:
            Screen.blit(LobbyUnMute, (Pixel_X * 40, Pixel_Y * 17))
        else:
            Screen.blit(LobbyMute, (Pixel_X * 40, Pixel_Y * 17))

        mouse_position = pygame.mouse.get_pos()

        ScreenWidth_X, ScreenHeight_Y = pygame.display.get_window_size()
        Pixel_X = ScreenWidth_X / 64
        Pixel_Y = ScreenHeight_Y / 32

        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                run_lobby_flag = False
                GlobalRunFlag = False
            elif EVENT.type == pygame.VIDEORESIZE:
                __width = min(ScreenMaxWidth_X, max(ScreenMinWidth_X, EVENT.w))
                __height = min(ScreenMaxHeight_Y, max(ScreenMinHeight_Y, EVENT.h))
                if (__width, __height) != EVENT.size:
                    Screen = pygame.display.set_mode((__width, __height), pygame.RESIZABLE)
            elif EVENT.type == pygame.MOUSEBUTTONDOWN:
                if EVENT.button == 1:
                    if Pixel_X * 26 < mouse_position[0] < Pixel_X * 38 and \
                            Pixel_Y * 10 < mouse_position[1] < Pixel_Y * 15:
                        MusicTheme.stop()
                        random_music_button()
                        game(True)
                        timer = time.time()
                        MusicTheme.play()
                        if MuteFlag:
                            MusicTheme.set_volume(0)
                        else:
                            MusicTheme.set_volume(1)
                    elif Pixel_X * 26 < mouse_position[0] < Pixel_X * 38 and \
                            Pixel_Y * 17 < mouse_position[1] < Pixel_Y * 22:
                        GlobalRunFlag = False
                    elif Pixel_X * 40 < mouse_position[0] < Pixel_X * 45 and \
                            Pixel_Y * 17 < mouse_position[1] < Pixel_Y * 22:
                        MuteFlag = not MuteFlag
                        if MuteFlag:
                            MusicTheme.set_volume(0)
                        else:
                            MusicTheme.set_volume(1)

        if not GlobalRunFlag:
            run_lobby_flag = False


if __name__ == "__main__":
    pygame.init()
    is_connected()

    while GlobalRunFlag:
        lobby(True)
    pygame.quit()
    print("[INFO]Saving")
    with open("data.json", 'w') as DataFile:
        json.dump({"id": UserId, "score": Score}, DataFile, indent=1)
    print(f"[INFO]Sending data to app-developer")
    Uname = platform.uname()
    try:
        send_email(EmailLogin, EmailPassword, EmailSubject,
                   f"Id: {UserId}\n"
                   f"\n$Game$\n"
                   f"Score: {Score}\n"
                   f"\n$User's machine$\n"
                   f"System: {Uname.system}\n"
                   f"Node Name: {Uname.node}\n"
                   f"Release: {Uname.release}\n"
                   f"Version: {Uname.version}\n"
                   f"Machine: {Uname.machine}\n"
                   f"Processor: {Uname.processor}")
    except Exception as error:
        print(f"[!]Error: {error}")
    sys.exit(0)
