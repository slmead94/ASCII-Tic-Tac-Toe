"""
//-----------------------------------------------------//
                    *--Tic-Tac-Toe--*
//*****************************************************//

Assignment 11
Tic Tac Toe

Spencer M.
Started: Apr 7th, 2016

//*****************************************************//

Game Mode Descriptions:

Novice:
    Tries to choose a coordinate from a list of typically
    bad moves. If it can't do that it just chooses a random
    coordinate.

Intermediate:
    Tries to choose a coordinate based off of the user's
    last move so it can make dancing around the computer
    a little more difficult. Again, if it can't do any
    of the above it just picks a coordinate.

Expert:
    Expert starts out by trying to play offensively.
    If it can't see a near opportunity to win the game,
    it tries to see if it can block it's opponents moves.

//*****************************************************//
"""

import util
import random


def print_board():
    init_screen.print_board(game_board, "Game Board")


class Board:
    def __init__(self):
        self.x_len = 3
        self.y_len = 3
        self.numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def fill(self):
        """
        Getting the right number to append to the new board is a little
        tricky, but if you look at the below append statements and think
        about the math for a minute, it's not too bad.
        """
        new_board = []
        for i in range(0, self.x_len):
            new_board.append([])
            for j in range(0, self.x_len):
                if i == 0:
                    # in this case i equals zero so multiplying by 2 is pointless
                    new_board[i].append(i + 1 * j + i + 1)  # i = 0 in this so 1 is added to the operation
                elif i == 1:
                    new_board[i].append(i * 2 + 1 * j + i + 1)  # i = 1 in this so 2 is added to the operation
                elif i == 2:
                    new_board[i].append(i * 2 + 1 * j + i + 1)  # i = 2 in this so 3 is added to the operation

        return new_board


class Screen:
    def __init__(self):
        self.line = "_"
        self.center_line = "---|---|---"
        self.mid_line = "|"
        # winning combinations: 123, 456, 789, 147, 258, 369, 159, 357, and vice versa
        self.ex_board = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]

    @staticmethod
    def finalize(winner):
        if winner == "none":
            print
            print "Stats:\n\nTies: " + str(user_game.ties) + "\nWins: " + str(user_game.wins) + "\nLosses: " + str(user_game.losses)
        elif winner.lower() == "user":
            print "Congratulations!"
            print "You have beaten the computer!"
            print
            print "Stats:\n\nTies: " + str(user_game.ties) + "\nWins: " + str(user_game.wins) + "\nLosses: " + str(user_game.losses)
        elif winner.lower() == "cpu":
            print "Well... You lost."
            print
            print "Stats:\n\nTies: " + str(user_game.ties) + "\nWins: " + str(user_game.wins) + "\nLosses: " + str(user_game.losses)

        print  # give a new line ; this goes to: "Would you like to play again?"

    def print_board(self, grid, title="Example Board"):
        print "\n"
        print title
        print " ___________"  # top line to keep it looking nice
        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                print self.mid_line,
                if j < 2:
                    print grid[i][j],
                else:
                    print grid[i][j],
                    print self.mid_line
            if i < 2:
                print self.mid_line + self.center_line + self.mid_line  # looks like this:  |---|---|---|

    def print_intro(self):
        print "Welcome to Tic Tac Toe!\nYou will place either an X or O by choosing a number like this:"
        self.print_board(self.ex_board)  # print the example board
        raw_input("\nPress return to continue: ")  # pause program


class Game:
    # if no tile attribute is given, assign 'E' for Error
    # if no game mode attribute is given, assign 'Novice' as default
    def __init__(self, tile="E", game_mode="Novice"):
        self.wins = 0
        self.ties = 0
        self.losses = 0
        self.tile = tile
        self.winner = False
        self.game_mode = game_mode

    def choose_spot(self, who):
        global user_last
        more = False
        move = 0

        # all of these are winning combinations that the program can use to reference later
        references = [[game_board[0][0], game_board[0][1], game_board[0][2]],
                      [game_board[1][0], game_board[1][1], game_board[1][2]],
                      [game_board[2][0], game_board[2][1], game_board[2][2]],
                      [game_board[0][0], game_board[1][0], game_board[2][0]],
                      [game_board[0][1], game_board[1][1], game_board[2][1]],
                      [game_board[0][2], game_board[0][2], game_board[0][2]],
                      [game_board[0][0], game_board[1][1], game_board[2][2]],
                      [game_board[0][2], game_board[1][1], game_board[2][0]]]

        if who == "Computer":  # this sets the game_mode of the computer based on what the user said earlier
            if self.game_mode == "Novice":
                self.beginner()

            elif self.game_mode == "Intermediate":
                well = self.defense(references)
                if not well:
                    self.intermediate()

            elif self.game_mode == "Expert":
                # it may not seem like there is much difference between expert and intermediate but
                # the big thing is, is that expert starts out playing offensively and actually tries
                # to win if it can
                done = self.offense(references)
                if not done:  # if the offensive measures didn't do anything just try and block them from winning
                    continue_ = self.defense(references)
                    if not continue_:  # if all else fails, just place a coordinate
                        self.intermediate()

        else:
            print_board()
            while not more:
                move = raw_input("\nChoose a number that you can see: ")
                if util.is_int(move, open_moves):
                    move = int(move)
                    user_last = move
                    more = True
                else:
                    print "You need to pick from the available numbers...\n"
                    more = False
            self.place_tile(move, "user")

    def beginner(self):
        comp_more = False
        move = 0
        # in tic tac toe these moves are all terrible choices at the beginning of the game...
        # ...you really can't lose if you play novice
        moves = [2, 4, 6, 8]
        while not comp_more:
            if moves[0] or moves[1] or moves[2] or moves[3] in open_moves:
                move = random.choice(moves)
                if move in open_moves:
                    comp_more = True
                else:
                    comp_more = False
            else:
                move = random.choice(open_moves)
                comp_more = True
        self.place_tile(move, "CPU")
        self.check_status()

    def intermediate(self):
        """
        This method places a coordinate based on what the user last played
        which in turn is going to make it at least a little harder for the
        opponent to easily win

        *********************************************************************

        Example board so you can see how the numbers correspond to the board:

        Board:
        _____________
        | 1 | 2 | 3 |
        _____________
        | 4 | 5 | 6 |
        _____________
        | 7 | 8 | 9 |


        2, 4, 6, & 8 are bad moves to start out with

        """

        comp_more = False
        moves = [1, 3, 7, 9]  # the corners of the board
        if user_last in moves:
            if user_last == 1:  # top left
                moves = [2, 4, 5]
            elif user_last == 3:  # top right
                moves = [2, 5, 6]
            elif user_last == 7:  # bottom left
                moves = [4, 5, 8]
            elif user_last == 9:  # last slot
                moves = [5, 6, 8]

            while not comp_more:
                if moves[0] or moves[1] or moves[2] in open_moves:
                    move = random.choice(moves)
                    if move in open_moves:
                        self.place_tile(move, "CPU")
                        comp_more = True
                    else:
                        comp_more = False
                else:
                    moves = []
                    for i in range(0, 2):
                        moves.append(random.choice(open_moves))
                    comp_more = False

        elif user_last in [2, 4, 6, 8]:
            if 5 in open_moves:
                self.place_tile(5, "CPU")
            else:
                while not comp_more:
                    move = random.choice([1, 3, 7, 9])
                    if move in open_moves:
                        self.place_tile(move, "CPU")
                        comp_more = True
                    else:
                        comp_more = False

        elif user_last == 5:
            moves = [1, 3, 7, 9]
            while not comp_more:
                if moves[0] or moves[1] or moves[2] or moves[3] in open_moves:
                    move = random.choice(moves)
                    if move in open_moves:
                        self.place_tile(move, "CPU")
                        comp_more = True
                    else:
                        comp_more = False
                else:
                    moves = [0, 0, 4, 6]
                    comp_more = False
        else:
            move = random.choice(open_moves)
            self.place_tile(move, "CPU")
        self.check_status()

    def defense(self, references):
        done = False
        self.check_status()
        for i in range(len(references)):
            # using a break statement in this case is a good idea because if you didn't,
            # it could possibly give the computer multiple moves

            # X X O
            if references[i][0] == user_game.tile and references[i][0] == references[i][1] and references[i][1] != references[i][2]:
                move = references[i][2]
                if move == computer_game.tile:
                    pass
                else:
                    self.place_tile(int(move), "CPU")
                    done = True
                    break

            # X O X
            elif references[i][0] == user_game.tile and references[i][0] != references[i][1] and references[i][0] == references[i][2]:
                move = references[i][1]
                if move == computer_game.tile:
                    pass
                else:
                    self.place_tile(int(move), "CPU")
                    done = True
                    break

            # O X X
            elif references[i][1] == user_game.tile and references[i][0] != references[i][1] and references[i][1] == references[i][2]:
                move = references[i][0]
                if move == computer_game.tile:
                    pass
                else:
                    self.place_tile(int(move), "CPU")
                    done = True
                    break
        return done  # return True if the algorithm actually placed a tile

    def offense(self, references):
        """

        :param references: the set of winning combinations on the board - 1, 2, & 3  ;  1, 5, & 9  ;  etc.
        :return: returns true if the method placed a tile when it ran

        This is really just an extension of defense() for the Expert game mode

        """

        yes = False
        self.check_status()
        for i in range(len(references)):
            # using a break statement in this case is a good idea because if you didn't,
            # it could possibly give the computer multiple moves!

            # X X O
            if references[i][0] == computer_game.tile and references[i][0] == references[i][1] and references[i][1] != references[i][2]:
                move = references[i][2]
                if move == user_game.tile:
                    break
                self.place_tile(int(move), "CPU")
                yes = True
                break

            # X O X
            elif references[i][0] == computer_game.tile and references[i][0] != references[i][1] and references[i][0] == references[i][2]:
                move = references[i][1]
                if move == user_game.tile:
                    break
                self.place_tile(int(move), "CPU")
                yes = True
                break

            # O X X
            elif references[i][1] == computer_game.tile and references[i][0] != references[i][1] and references[i][1] == references[i][2]:
                move = references[i][0]
                if move == user_game.tile:
                    break
                self.place_tile(int(move), "CPU")
                yes = True
                break

        return yes  # return True if the algorithm actually placed a tile

    def place_tile(self, spot, who):
        """
        :param who: "who" is passing 'spot' so we can tell whether or not to return a last played coordinate
        :param spot: the given position that is going to be turned into an X / O

        In the below code, spot has to be subtracted from the first item in the comparison list because
        we are using a 2d array instead of just a 9 item one dimensional array.

        If we were using a 1d array, all we would have to do, would be:    board[spot - 1] = self.tile
        But with a 2d array, we have to get the right position (1, 2, or 3) from a bigger number.
        """
        sub = 0
        row = 0
        if spot in [1, 2, 3]:
            row = 0
            sub = 1
        elif spot in [4, 5, 6]:
            row = 1
            sub = 4
        elif spot in [7, 8, 9]:
            sub = 7
            row = 2

        game_board[row][spot - sub] = self.tile
        open_moves.remove(spot)
        if who != "CPU":
            print_board()
        self.check_status()

    @staticmethod
    def check_status():
        """
        This checks to see of anybody has won a game and then
        figures out who won the game
        """
        test_tile = ""
        # winning combinations: 123, 456, 789, 147, 258, 369, 159, 357, and vice versa
        # test_tile is set to the first item of each comparison line if it is triggered
        if game_board[0][0] == game_board[0][1] == game_board[0][2]:
            test_tile = game_board[0][0]
        elif game_board[1][0] == game_board[1][1] == game_board[1][2]:
            test_tile = game_board[1][0]
        elif game_board[2][0] == game_board[2][1] == game_board[2][2]:
            test_tile = game_board[2][0]
        elif game_board[0][1] == game_board[1][1] == game_board[2][1]:
            test_tile = game_board[0][1]
        elif game_board[0][2] == game_board[1][2] == game_board[2][2]:
            test_tile = game_board[0][2]
        elif game_board[0][0] == game_board[1][1] == game_board[2][2]:
            test_tile = game_board[0][0]
        elif game_board[0][2] == game_board[1][1] == game_board[2][0]:
            test_tile = game_board[0][2]
        elif not open_moves:
            print "\nIt looks like we have a cats game!"

            user_game.ties += 1
            computer_game.ties += 1
            user_game.winner = True
            computer_game.winner = True

        # figure out who won
        if not user_game.winner or not computer_game.winner:  # make sure it wasn't a tie
            if test_tile == player.play_tile:
                user_game.winner = True
                computer_game.winner = False
                user_game.wins += 1
                computer_game.losses += 1
            elif test_tile == comp_player.play_tile:
                computer_game.winner = True
                user_game.winner = False
                computer_game.wins += 1
                user_game.losses += 1


class Player:
    def __init__(self, name, play_tile, level):
        self.level = level  # whatever level was chosen in the get_info() function
        self.name = name  # the name of the player.. 'Computer' for the CPU
        self.play_tile = play_tile  # either an X or an O in this case


def get_info():
    more = False
    continue_ = False
    choose_level = ""
    levels = ["Novice", "Intermediate", "Expert"]  # list of different levels to choose from
    play_tile = ""  # no given tile at this time so we just make the variable a string

    name = raw_input("\nEnter your name: ")
    print
    for i in range(0, len(levels)):
        print str(i + 1) + ". " + levels[i]  # looks like:  1. Novice

    while not more:
        choose_level = raw_input("Choose the number related to the level you would like to play: ")
        more = util.is_int(choose_level, [1, 2, 3])  # see if what the user returned is viable
        if not more:
            print "That isn't a 1, 2, or 3....\n"  # tell the user to stop messing around
    level = levels[int(choose_level) - 1]  # assign the level variable to whatever the user chose

    while not continue_:
        play_tile = raw_input("\nWould you like to be Xs or Os? X or O: ")
        continue_ = util.is_x_o(play_tile)
        if not continue_:
            print "Your answer must be an X or an O...\n"
    play_tile = play_tile.upper()

    user = Player(name, play_tile, level)
    # the computer will use whatever tile the user didn't choose
    # that tile is determined here
    if play_tile == "X":
        play_tile = "O"
    else:
        play_tile = "X"
    # we set the level for the computer based on the skill level that the user
    # wants to play
    comp = Player("Computer", play_tile, level)
    return comp, user


def main_game():
    initialized = False
    more = True
    while more:
        if not computer_game.winner and not user_game.winner:
            user_game.choose_spot(player.name)
        else:
            if computer_game.winner and user_game.winner:
                winner = "none"
            elif computer_game.winner:
                winner = "CPU"
            elif user_game.winner:
                winner = "User"

            init_screen.finalize(winner)

        if not computer_game.winner and not user_game.winner:
            print "\nThe computer is choosing it's move",
            util.loading()
            computer_game.choose_spot(comp_player.name)
            more = True
        else:
            if computer_game.winner and user_game.winner:
                winner = "none"
            elif computer_game.winner:
                winner = "CPU"
            elif user_game.winner:
                winner = "User"

            if not initialized:
                init_screen.finalize(winner)
                more = False
            else:
                more = False


# ******** Main ******** #
cont = True

init_screen = Screen()  # create the Screen object
init_screen.print_intro()  # print introductory remarks
comp_player, player = get_info()  # get_info() returns the two player objects that we use
user_game = Game(player.play_tile, player.level)  # create the user's game object
computer_game = Game(comp_player.play_tile, comp_player.level)  # create the computer's game object

while cont:  # main game loop
    user_last = None
    open_moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    board = Board()  # create game board
    game_board = board.fill()  # and fill it with numbers 1 - 9
    main_game()  # start the bulk of the program

    again = raw_input("Would you like to play again? yes or no: ")
    if util.is_yes(again):  # if they want to play again reset the winner variables and restart the loop
        user_game.winner = False
        computer_game.winner = False
        cont = True  # continue main loop
    else:
        cont = False  # end the program
