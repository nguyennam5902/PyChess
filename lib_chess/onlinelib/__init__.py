from lib_chess.lib import *
from lib_chess.onlinelib.utils import (
    bgThread,
    read,
    readable,
    flush,
    write,
    getPlayers,
    showUpdateList,
    showLoading,
    popup,
    request,
    draw,
    draw_win,
    showLobby,
)


def lobby(win, sock, key, load):
    clock = pygame.time.Clock()
    playerList = getPlayers(sock)
    while True:
        clock.tick(10)
        if playerList is None:
            return 2
        showLobby(win, key, playerList)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                write(sock, "quit")
                return 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 460 < x < 500 and 0 < y < 50:
                    write(sock, "quit")
                    return 1

                if 390 < x < 420 and 85 < y < 115:
                    playerList = getPlayers(sock)

                if 300 < x < 475:
                    for i in range(len(playerList)):
                        if 122 + 30 * i < y < 148 + 30 * i:
                            write(sock, "rg" + playerList[i][:4])

                            msg = read()
                            if msg == "close":
                                return 2

                            elif msg == "msgOk":
                                ret = request(win, sock)
                                if ret in [0, 1, 2]:
                                    return ret

                                elif ret == 4:
                                    newret = chess_func(win, sock, 0, load)
                                    if newret in [0, 1, 2]:
                                        return newret

                            elif msg.startswith("err"):
                                showUpdateList(win)

                            playerList = getPlayers(sock)
                            break

        if readable():
            msg = read()
            print(f"1_{msg}")  # Tai sao lai chay toi day
            if msg == "close":
                return 2

            elif msg.startswith("gr"):
                ret = request(win, sock, msg[2:])
                if ret == 4:
                    write(sock, "gmOk" + msg[2:])
                    newret = chess_func(win, sock, 1, load)
                    if newret in [0, 1, 2]:
                        return newret

                else:
                    write(sock, "gmNo" + msg[2:])
                    if ret == 2:
                        return ret
                playerList = getPlayers(sock)

# This is called when user enters chess match, handles online chess.


def chess_func(win, sock, player, load):
    start(win, load)
    print("ONLINE")
    side, board, flags = initBoardVars()
    chess_board = chess.Board()
    clock = pygame.time.Clock()
    sel = prevsel = [0, 0]
    while True:
        clock.tick(25)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                write(sock, "quit")
                return 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 460 < x < 500 and 0 < y < 50:
                    write(sock, "end")
                    return 3

                if 50 < x < 450 and 50 < y < 450:
                    x, y = x // 50, y // 50
                    if load["flip"] and player:
                        x, y = 9 - x, 9 - y

                    if isOccupied(side, board, [x, y]) and side == player:
                        sound.play_click(load)

                    prevsel = sel
                    sel = [x, y]

                    if (side == player
                            and isValidMove(side, board, flags, prevsel, sel)):
                        promote = getPromote(win, player, board, prevsel, sel)
                        write(sock, "mov" + encode(prevsel, sel, promote))
                        makeOkMove(board, chess_board, prevsel, side, sel)
                        animate(win, player, board, prevsel, sel, load, player)
                        side, board, flags = makeMove(
                            side, board, prevsel, sel, flags, promote) # type: ignore
                    if chess_board.is_checkmate():
                        write(sock, "win")
                        ret = draw_win(win, sock)
                        return ret
                elif not chess_board.is_checkmate():
                    if 0 < x < 70 and 0 < y < 50:
                        write(sock, "draw?")
                        ret = draw(win, sock)
                        if ret in [0, 2, 3]:
                            return ret

                    if 400 < x < 500 and 450 < y < 500:
                        write(sock, "resign")
                        return 3

        showScreen(win, side, board, flags, sel, load,
                   player, True, chess_board=chess_board)
        if readable():
            msg = read()
            if msg == "close":
                return 2
            elif msg == "quit" or msg == "resign":
                return popup(win, sock, msg)

            elif msg == "end":
                msg = "end" if isEnd(side, board, flags) else "abandon"
                return popup(win, sock, msg)

            elif msg == "draw?":
                ret = draw(win, sock, False)
                if ret in [2, 3]:
                    return
            elif msg == "win":
                ret = draw_win(win, sock, False)
                if ret in [2, 3]:
                    return
            elif msg.startswith("mov") and side != player:
                fro, to, promote = decode(msg[3:])
                if isValidMove(side, board, flags, fro, to):
                    makeOkMove(board, chess_board, fro, side, to)
                    animate(win, side, board, fro, to, load, player)

                    side, board, flags = makeMove(
                        side, board, fro, to, flags, promote) # type: ignore
                    sel = [0, 0]
                else:
                    return 2
