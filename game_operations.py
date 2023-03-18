import random

def printGame(board): 
    # For Printing the game line-wise .
    for line in board:
        print(line)

def placeRandom(board, pieces, pieceNames): 
    # Choosing a piece at random, then placing it on the board.
    pieceName = pieceNames[random.randint(1, len(pieces)) - 1]
    piece = pieces[pieceName]
    for i in range(len(piece)):
        line = piece[i]
        if line[0] == " ":
            line = line[1:]
            boardLine = list(board[i + 1])
            boardLine[4:4 + len(line)] = line
            board[i + 1] = "".join(boardLine)
        else:
            boardLine = list(board[i + 1])
            boardLine[3:3 + len(line)] = line
            board[i + 1] = "".join(boardLine)
    return board, pieceName

def dash_function(board): 
    # Turning the active (movable) piece to dashes.
    for i in range(len(board)):
        line = list(board[i])
        while "*" in line:
            line[line.index("*")] = "-"
        while "x" in line:
            line[line.index("x")] = "-"
        board[i] = "".join(line)
    return board

def rotate(board, dir, pieceName): 
    # Rotate the active piece in the direction specified
    if pieceName == "4":
        return board
    if dir.lower().strip() == "r":
        turnRight = True
    elif dir.lower().strip() == "l":
        turnRight = False
    else:
        return board

    # Finding the coords for the active piece, relative to (0, 0) and remove all instances of *
    coords = []
    occord = []
    for i in range(len(board)):
        filler = " "
        if i == 0:
            filler = "/"
        line = list(board[i])
        while "*" in line:
            coords.append([line.index("*"), i])
            line[line.index("*")] = filler
        if "x" in line:
            ocoord = [line.index("x"), i]
        board[i] = "".join(line)

    # Finding the coords for the active piece
    originCoords = []
    for coord in coords:
        originCoords.append([(coord[0] - ocoord[0]), (coord[1] - ocoord[1])])

    # Edit the coords to rotate in the direction
    if not turnRight:
        for i in range(len(originCoords)):
            coord = originCoords[i]
            originCoords[i] = [coord[1], - coord[0]]
    else:
        for i in range(len(originCoords)):
            coord = originCoords[i]
            originCoords[i] = [- coord[1], coord[0]]

    # Translate the coords back to (0, 0) as origin
    coords = []
    for coord in originCoords:
        coords.append([(coord[0] + ocoord[0]), (coord[1] + ocoord[1])])

    # Place each * back, rotated
    for coord in coords:
        line = list(board[coord[1]])
        line[coord[0]] = "*"
        board[coord[1]] = "".join(line)
    return board

def drop(board):
    # Drops the active piece by 1.
    preProcessBoard = []
    for i in board:
        preProcessBoard.append(i)

    # Finding lines where piece is located
    pieceLines = []
    for i in range(len(board)):
        line = board[i]
        if "*" in line or "x" in line:
            pieceLines.append(i)

    piece = {}
    for i in pieceLines:
        line = board[i]
        if "x" in line:
            if not "*" in line:
                firstInstance = line.index("x")
                lastInstance = line.index("x")
            else:
                firstInstance = None
                if line.index("*") < line.index("x"):
                    firstInstance = line.index("*")
                else:
                    firstInstance = line.index("x")

                lastInstance = None
                if line[::-1].index("*") < line[::-1].index("x"):
                    lastInstance = 9 - line[::-1].index("*")
                else:
                    lastInstance = line.index("x")
        else:
            firstInstance = line.index("*")
            lastInstance = 9 - line[::-1].index("*")
        piece[i] = [firstInstance, lastInstance]

    # Detecting which spots the piece will fall into and validate
    pieceBot = piece[pieceLines[-1]]
    coordsCheck = []
    left = None
    right = None
    for i in pieceLines:
        if left != None:
            if left[0] >= piece[i][0]:
                left = [piece[i][0], i]
            if right[0] <= piece[i][1]:
                right = [piece[i][1], i]
        else:
            left = [piece[i][0], i]
            right = [piece[i][1], i]
    for i in range(pieceBot[0], pieceBot[1] + 1):
        coordsCheck.append([i, pieceLines[-1] + 1])
    if left[0] < coordsCheck[0][0]:
        coordsCheck.append([left[0], left[1] + 1])
    if right[0] > sorted(i[0] for i in coordsCheck)[-1]:
        coordsCheck.append([right[0], right[1] + 1])

    futurePiece = []
    for i in coordsCheck:
        futurePiece.append(board[i[1]][i[0]])

    # Drop the piece
    if "-" in futurePiece:
        # Denying to drop if it is the last possible drop
        last = True
    else:
        last = False
        for line in pieceLines[::-1]:
            linePiece = piece[line]
            if linePiece[0] != linePiece[1]:
                toDrop = preProcessBoard[line][linePiece[0]:linePiece[1] + 1]
                heal = list(board[line])
                heal[linePiece[0]:linePiece[1] + 1] = " " * (linePiece[1] + 1 - linePiece[0])
                board[line] = "".join(heal)
            else:
                toDrop = preProcessBoard[line][linePiece[0]]
                heal = list(board[line])
                heal[linePiece[0]] = " "
                board[line] = "".join(heal)
            lineList = list(board[line + 1])
            lineList[linePiece[0]:linePiece[1] + 1] = toDrop
            board[line + 1] = "".join(lineList)
        ## Heal line above dropped piece
        prevline = list(preProcessBoard[pieceLines[0]])
        pieceTop = piece[pieceLines[0]]

        prevline[pieceTop[0]:pieceTop[1] + 1] = " " * (pieceTop[1] + 1 - pieceTop[0])
        board[pieceLines[0]] = "".join(prevline)
    return board, last

def move(board, direction): 
    # Move the active piece by 1 in direction specified
    # Finding lines of piece
    pieceLines = []
    for i in range(len(board)):
        line = board[i]
        if "*" in line or "x" in line:
            pieceLines.append(i)
    piece = {}
    for i in pieceLines:
        o = None
        line = board[i]
        if "x" in line:
            if not "*" in line:
                firstInstance = line.index("x")
                lastInstance = line.index("x")
            else:
                firstInstance = None
                if line.index("*") < line.index("x"):
                    firstInstance = line.index("*")
                else:
                    firstInstance = line.index("x")

                lastInstance = None
                if line[::-1].index("*") < line[::-1].index("x"):
                    lastInstance = 9 - line[::-1].index("*")
                else:
                    lastInstance = line.index("x")
            o = line.index("x")
        else:
            firstInstance = line.index("*")
            lastInstance = 9 - line[::-1].index("*")
        piece[i] = [firstInstance, lastInstance, o]

    # Heal parts of board where current piece is
    for i in pieceLines:
        line = list(board[i])
        cols = piece[i]
        line[cols[0]:cols[1] + 1] = " " * (cols[1] + 1 - cols[0])
        board[i] = "".join(line)

    # Numerically move 
    if direction == "l":
        for i in pieceLines:
            piece[i][:2] = [m - 1 for m in piece[i][:2]]
            if piece[i][2] != None:
                piece[i][2] -= 1
    else:
        for i in pieceLines:
            piece[i][:2] = [m + 1 for m in piece[i][:2]]
            if piece[i][2] != None:
                piece[i][2] += 1

    # "Render" moved piece on to board
    for i in pieceLines:
        line = list(board[i])
        line[piece[i][0]:piece[i][1] + 1] = "*" * (piece[i][1] + 1 - piece[i][0])
        board[i] = "".join(line)

    # Replace anchor point
    for i in pieceLines:
        if piece[i][2] != None:
            line = list(board[i])
            line[piece[i][2]] = "x"
            board[i] = "".join(line)

    return board

def is_move_valid(board, command, direction = None): 
    # Verify a move for preventing errors.
    valid = True

    pieceLines = []
    for i in range(len(board)):
        line = board[i]
        if "*" in line or "x" in line:
            pieceLines.append(i)

    piece = []
    for i in pieceLines:
        line = board[i]
        if "x" in line:
            if not "*" in line:
                firstInstance = line.index("x")
                lastInstance = line.index("x")
            else:
                firstInstance = None
                if line.index("*") < line.index("x"):
                    firstInstance = line.index("*")
                else:
                    firstInstance = line.index("x")

                lastInstance = None
                if line[::-1].index("*") < line[::-1].index("x"):
                    lastInstance = 9 - line[::-1].index("*")
                else:
                    lastInstance = line.index("x")
        else:
            firstInstance = line.index("*")
            lastInstance = 9 - line[::-1].index("*")
        piece.append([i, firstInstance, lastInstance])

    if command == "move":
        # Validate Move
        # Finding copords of moved piece
        if direction == "r":
            piece = [[i[0], i[1] + 1, i[2] + 1] for i in piece]
        else:
            piece = [[i[0], i[1] - 1, i[2] - 1] for i in piece]

        # Checking if any of the coords are out of bounds
        for point in piece:
            for coord in point[1:]:
                if coord < 0 or coord > 9:
                    valid = False
                    break

        ## Check for existing "-" characters in board
        if valid:
            for point in piece:
                toCheck = board[point[0]][point[1]:point[2] + 1]
                if "-" in toCheck:
                    valid = False
                    break
    elif command == "rotate":
        # Validate rotation
        coords = []
        for point in piece:
            for coord in range(point[1], point[2] + 1):
                if board[point[0]][coord] == "x":
                    ocoord = [coord, point[0]]
                else:
                    coords.append([coord, point[0]])

        # Finding coords in relation to piece origin
        originCoords = []
        for coord in coords:
            originCoords.append([(coord[0] - ocoord[0]), - (coord[1] - ocoord[1])])

        # Rotation Trigger
        if direction == "r":
            rotated = [[i[1], - i[0]] for i in originCoords]
        else:
            rotated = [[- i[1], i[0]] for i in originCoords]
        piece = [[(ocoord[1] - i[1]) - 1, i[0] + ocoord[0]] for i in rotated]
        ocoord[1] -= 1
        piece.append(ocoord[::-1])

        # Check for out of bounds coords
        for point in piece:
            if point[0] <= -1 or point[0] >= 17:
                valid = False
                break
            if point[1] > 9 or point[1] < 0:
                valid = False
                break

        # Check for "-"
        if valid:
            for point in piece:
                if "-" in board[point[0] + 1][point[1]]:
                    valid = False
                    break
    else:
        valid = False
    return valid