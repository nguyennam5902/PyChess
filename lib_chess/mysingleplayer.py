from lib_chess.lib import *
import chess


def main(win, player, load, movestr=""):
    start(win, load)
    moves = movestr.split()
    side, board, flags = convertMoves(moves)
    chess_board = chess.Board()
    clock = pygame.time.Clock()
    sel = prevsel = [0, 0]
    while True:
        clock.tick(25)
        end = isEnd(side, board, flags)
        for event in pygame.event.get():
            if event.type == pygame.QUIT and prompt(win):
                return 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 460 < x < 500 and 0 < y < 50 and prompt(win):
                    return 1

                if 50 < x < 450 and 50 < y < 450:
                    x, y = x // 50, y // 50
                    if load["flip"] and player:
                        x, y = 9 - x, 9 - y

                    if isOccupied(side, board, [x, y]):
                        sound.play_click(load)

                    prevsel = sel
                    sel = [x, y]

                    if (side == player
                            and isValidMove(side, board, flags, prevsel, sel)):
                        promote = getPromote(win, side, board, prevsel, sel)
                        # START HERE
                        piece = str(getType(side, board, prevsel)
                                    ).replace('p', '').upper()
                        if isOccupied(not side, board, sel):
                            print("TAKE BY HUMAN")
                            human = 'x' + \
                                chr(ord('a') + sel[0] - 1)+str(9 - sel[1])
                            if len(piece) == 0:
                                human = chr(ord('a') + prevsel[0] - 1)+human
                            else:
                                human = piece + human
                            try:
                                chess_board.parse_san(human)
                            except chess.AmbiguousMoveError:
                                print("AmbiguousMoveError")
                        else:
                            if piece == "K" and abs(sel[0] - prevsel[0]) != 1:
                                human = "0-0" if sel[0] > prevsel[0] else "0-0-0"
                            else:
                                human = piece + \
                                    chr(ord('a') + sel[0] - 1)+str(9 - sel[1])
                            try:
                                chess_board.parse_san(human)
                            except chess.AmbiguousMoveError:
                                print("AmbiguousMoveError")
                                human = piece + \
                                    chr(ord(
                                        'a') + prevsel[0] - 1) + chr(ord('a') + sel[0] - 1)+str(9 - sel[1])
                                print("NEW MOVE:", human)
                                try:
                                    chess_board.parse_san(human)
                                except chess.AmbiguousMoveError:
                                    human = piece + \
                                        str(9 - prevsel[1]) + chr(ord('a') +
                                                                  sel[0] - 1)+str(9 - sel[1])
                                print("NEW BETTER MOVE:", human)

                        print(human)
                        chess_board.push_san(human)
                        print(chess_board.is_checkmate())
                        # FINISH HERE
                        animate(win, side, board, prevsel, sel, load, player)

                        side, board, flags = makeMove(
                            side, board, prevsel, sel, flags, promote)  # type: ignore
                        moves.append(encode(prevsel, sel, promote))
                elif side == player or end:
                    sel = [0, 0]
                    if 350 < x < 500 and 460 < y < 490:
                        if prompt(win, saveGame(moves, "mysingle", player)):
                            return 1
                    elif 0 < x < 80 and 0 < y < 50 and load["allow_undo"]:
                        moves = undo(
                            moves, 2) if side == player else undo(moves)
                        side, board, flags = convertMoves(moves)

        showScreen(win, side, board, flags, sel, load,
                   player, chess_board=chess_board)

        end = chess_board.is_checkmate()
        if side != player and not end:
            fro, to = miniMax(side, board, flags)  # type: ignore
            piece = str(getType(side, board, fro)
                        ).replace('p', '').upper()
            if isOccupied(not side, board, [to[0], to[1]]):
                print("TAKE BY MACHINE")
                machine = 'x' + \
                    chr(ord('a') + to[0] - 1)+str(9 - to[1])
                if len(piece) == 0:
                    machine = chr(ord('a') + fro[0] - 1)+machine
                else:
                    machine = piece + machine
            else:
                # print("ERROR:", side, to[0], to[1])
                # print("board:", board[not side])
                if piece == "K" and abs(to[0] - fro[0]) != 1:
                    machine = "0-0" if to[0] > fro[0] else "0-0-0"
                else:
                    machine = piece + \
                        chr(ord('a') + to[0] - 1)+str(9 - to[1])

            print(machine)
            chess_board.push_san(machine)
            animate(win, side, board, fro, to, load, player)
            promote = getPromote(win, side, board, fro, to, True)
            side, board, flags = makeMove(side, board, fro, to, flags)

            moves.append(encode(fro, to, promote))
            sel = [0, 0]
