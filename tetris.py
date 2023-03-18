import game_operations
if 1 == 1:
    RandomNames = ["1", "2", "3", "4", "5"]
    pieces = {}
    # Initializing empty list
    for na in RandomNames:
        pieces[na] = []

    # Choosing one random name from the RandomNames List
    for n in RandomNames:
        with open("./random_pieces/" + n + ".txt") as fileName:
            for line in fileName:
                pieces[n].append(line.strip("\n"))

    # Building the board for the game
    game = ["|        |"] * 11 + ["----------"]

    # Main Logic for the game 
    isTop = False 
    # Will Change when a "-" is found at the top line
    while not isTop:
        ## Place piece on the board 
        game, pieceName = game_operations.placeRandom(game, pieces, RandomNames)
        game_operations.printGame(game)

        last = False
        while not last:
            # Taking input from user
            instruct = False
            while not instruct:
                # Rotate/move piece
                command = input("Command (type \"h\" for help): ").lower().strip()
                if not command:
                    print("Please enter a valid command to continue")

                # ONE ROW DOWN
                elif command == "space":
                    instruct = True

                # HELP
                elif command == "h":
                    print("Tetris Game Instructions:")
                    print()
                    print("Move piece left and one row down: type \"a\"")
                    print()
                    print("Move piece right and one row down: type \"d\"")
                    print()
                    print("Rotate piece counter clockwise and one row down: type \"w\"")
                    print()
                    print("Rotate piece clockwise and one row down: type \"s\"")
                    print()
                    print("No action and one row down: type \"space\"")
                    print()

                # ROTATE CLOCKWISE
                elif command == "s":
                    direction = "r"
                    if game_operations.is_move_valid(game, "rotate", direction):
                        instruct = True
                        game = game_operations.rotate(game, direction, pieceName)
                    else:
                        print("Your move is invalid . Please enter a valid move to continue .")

                # ROTATE COUNTER CLOCKWISE
                elif command == "w":
                    direction = "l"
                    if game_operations.is_move_valid(game, "rotate", direction):
                        instruct = True
                        game = game_operations.rotate(game, direction, pieceName)
                    else:
                        print("Your move is invalid . Please enter a valid move to continue .")

                # MOVE RIGHT
                elif command == "d":
                    direction = "r"
                    if game_operations.is_move_valid(game, "move", direction):
                        instruct = True
                        game = game_operations.move(game, direction)
                    else:
                        print("Your move is invalid . Please enter a valid move to continue .")

                # MOVE LEFT
                elif command == "a":
                    direction = "l"
                    if game_operations.is_move_valid(game, "move", direction):
                        instruct = True
                        game = game_operations.move(game, direction)
                    else:
                        print("Your move is invalid . Please enter a valid move to continue .")

                else:
                    print("Your move is invalid . Please enter a valid move to continue .")

            # Drop piece by one move
            game, last = game_operations.drop(game)
            game_operations.printGame(game)

        # When piece cannot be dropped, render it as hashes and continue
        game = game_operations.dash_function(game)

        ## Check for line clears
        while "----------" in game[:-1]:
            no = game[:-1].index("------------")
            del game[no]
            game.insert(1, "          ")

        # Display game over
        if "-" in game[1]:
            isTop = True
    game_operations.printGame(game)
    print("-*- Game over! -*-")
    print("Thanks for playing !!")