import pygame
from ext.pyBox import TextBox
from tools.loader import ONLINEMENU, BACK, FONT, LOGINBOARD
from tools.utils import rounded_rect


def showScreen(win, sel):
    win.fill((0, 0, 0))

    rounded_rect(win, (255, 255, 255), (120, 10, 260, 70), 20, 4)
    rounded_rect(win, (255, 255, 255), (20, 90, 460, 400), 14, 4)
    win.blit(ONLINEMENU.HEAD, (175, 15))
    win.blit(BACK, (460, 0))

    for cnt, i in enumerate(ONLINEMENU.TEXT):
        win.blit(i, (40, 100 + cnt*18))

    rounded_rect(win, (255, 255, 255), (300, 350, 110, 30), 10, 3)
    win.blit(ONLINEMENU.CONNECT, (300, 350))

    pygame.draw.rect(win, (255, 255, 255), (130 + sel*160, 460, 40, 20), 3)


def loginScreen(win):
    win.fill((0, 0, 0))

    rounded_rect(win, (255, 255, 255), (120, 10, 260, 70), 20, 4)
    rounded_rect(win, (255, 255, 255), (20, 90, 460, 400), 14, 4)
    win.blit(LOGINBOARD.HEAD, (133, 15))
    win.blit(BACK, (460, 0))

    for cnt, i in enumerate(LOGINBOARD.TEXT):
        win.blit(i, (40, 100 + cnt*18))

    rounded_rect(win, (255, 255, 255), (300, 350, 110, 30), 10, 3)
    win.blit(LOGINBOARD.CONNECT, (313, 355))


def main(win):
    clock = pygame.time.Clock()
    sel = 0

    username_box = TextBox(FONT, (0, 0, 0), (65, 350, 200, 35))
    password_box = TextBox(FONT, (0, 0, 0), (65, 400, 200, 35))
    username_box.text = ""
    password_box.text = ""
    while True:
        clock.tick(24)
        loginScreen(win)

        pygame.draw.rect(win, (255, 255, 255), (63, 348, 204, 39))
        username_box.draw(win)

        pygame.draw.rect(win, (255, 255, 255), (63, 398, 204, 39))
        password_box.draw(win)

        for event in pygame.event.get():
            username_box.push(event)
            password_box.push(event)

            if event.type == pygame.QUIT:
                return 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 460 < x < 500 and 0 < y < 50:
                    return 1
                if 300 < x < 410 and 350 < y < 380:
                    return username_box.text, password_box.text, bool(sel)
        pygame.display.update()
