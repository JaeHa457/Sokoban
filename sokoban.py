"""
Name: Jae Ha
UPI: jha286
Description: Sokoban Game Program written in Python. The aim of the game is for
             the player 'P', to push the crates '#', into the holes 'o'. 
"""


class Sokoban:
    def __init__(self, board = []):
        self.__board = board
        self.__steps = 0
        self.__moves = [list(row) for row in board]
        self.__restart = [list(row) for row in board]
        for row in self.__board:
            self.__column_length = len(row) - 1
        self.__row_length = len(self.__board) - 1
    
    def find_player(self):
        for row_index in range (len(self.__board)):
            for column_index in range(len(self.__board[row_index])):
                if self.__board[row_index][column_index] == "P":
                    position = (row_index, column_index)
        return position

    def complete(self):
        for row in self.__board:
            for column in row:
                if column == "o":
                    return False 
        return True

    def get_steps(self):
        return self.__steps

    def restart(self):
        self.__board = [list(row) for row in self.__restart]
        self.__steps = 0
        return self.__board

    def undo(self):
        self.__steps -= 1
        self.__moves = self.__moves[:-1]
        self.__board = self.__moves[-1]
        if self.__steps <= 0:
            self.__board = [list(row) for row in self.__restart]
            self.__steps = 0
        return self.__board
        
    def find_next_pos_player(self, row, column, direction):
        if direction == "a" and column != 0:
            return [row, column - 1]
        elif direction == "a" and column == 0:
            return [row, self.__column_length]
        elif direction == "d" and column != self.__column_length:
            return [row, column + 1]
        elif direction == "d" and column == self.__column_length:
            return [row, 0]
        elif direction == "w" and row != 0:
            return [row - 1, column]
        elif direction == "w" and row == 0:
            return [self.__row_length, column]
        elif direction == "s" and row != self.__row_length:
            return [row + 1, column]
        elif direction == "s" and row == self.__row_length:
            return [0, column]

    def next_pos_horizon(self, row, column, direction):
        if direction == "a" and column > 1:
            return [row, column - 2]
        elif direction == "a" and column == 1:
            return [row, self.__column_length]
        elif direction == "a" and column == 0:
            return [row, self.__column_length - 1]
        elif direction == "d" and column < self.__column_length - 1:
            return [row, column + 2]
        elif direction == "d" and column == self.__column_length - 1:
            return [row, 0]
        elif direction == "d" and column == self.__column_length:
            return [row, 1]

    def next_pos_vertical(self, row, column, direction):        
        if direction == "w" and row > 1:
            return [row - 2, column]
        elif direction == "w" and row == 1:
            return [self.__row_length, column]
        elif direction == "w" and row == 0:
            return [self.__row_length - 1, column]
        elif direction == "s" and row < self.__row_length - 1:
            return [row + 2, column]
        elif direction == "s" and row == self.__row_length - 1:
            return [0, column]
        elif direction == "s" and row == self.__row_length:
            return [1, column]
    
    def player_or_box(self, row, column, direction):
        if direction == "a" and column != 0:
            return (self.__board[row][column - 1] == "#")
        elif direction == "a" and column == 0:
            return (self.__board[row][self.__column_length] == "#")
        elif direction == "d" and column != self.__column_length:
            return (self.__board[row][column + 1] == "#")
        elif direction == "d" and column == self.__column_length:
            return (self.__board[row][0] == "#")
        elif direction == "w" and row != 0:
            return (self.__board[row - 1][column] == "#")
        elif direction == "w" and row == 0:
            return (self.__board[self.__row_length][column] == "#")
        elif direction == "s" and row != self.__row_length:
            return (self.__board[row + 1][column] == "#")
        elif direction == "s" and row == self.__row_length:
            return (self.__board[0][column] == "#")

    def move_player (self, row, column, row_after, column_after):
        if self.__board[row_after][column_after] not in "o*":
            self.__board[row_after][column_after] = "P"
            self.__board[row][column] = " "
            self.__steps += 1
            self.__moves.append([list(row) for row in self.__board])
            
    def move_box (self, row, column, row_box, col_box, row_after, col_after):
        if self.__board[row_after][col_after] == "o":
            self.__board[row_after][col_after] = " "
            self.__board[row_box][col_box] = "P"
            self.__board[row][column] = " "
            self.__steps += 1
            self.__moves.append([list(row) for row in self.__board])
        elif self.__board[row_after][col_after] == " ":
            self.__board[row_after][col_after] = "#"
            self.__board[row_box][col_box] = "P"
            self.__board[row][column] = " "
            self.__steps += 1
            self.__moves.append([list(row) for row in self.__board])

    def move(self, direction):
        p_loc = self.find_player()
        row = p_loc[0]
        col = p_loc[1]
        p_or_b = self.player_or_box(row, col, direction)
        box = self.find_next_pos_player(row, col, direction)
        if p_or_b == True:
            if direction in "ad":
                next_pos = self.next_pos_horizon(row, col, direction)
            else:
                next_pos = self.next_pos_vertical(row, col, direction)
            self.move_box(row, col, box[0], box[1], next_pos[0], next_pos[1])
        else:
            next_pos = self.find_next_pos_player(row, col, direction)
            self.move_player(row, col, next_pos[0], next_pos[1])
        return self.__board
                             
    def __str__(self):
        board = ""
        for row in self.__board:
            for column in row:
                for element in column:
                    board += element
                    board += " "
            board += "\n"
        board = board[:-1]
        return board

def main(board):
    game = Sokoban(board)
    message = 'Press w/a/s/d to move, r to restart, or u to undo'
    print(message)
    while not game.complete():
        print(game)
        move = input('Move: ').lower()
        while move not in ('w', 'a', 's', 'd', 'r', 'u'):
            print('Invalid move.', message)
            move = input('Move: ').lower()
        if move == 'r':
            game.restart()
        elif move == 'u':
            game.undo()
        else:
            game.move(move)
 
    print(f'Game won in {game.get_steps()} steps!')

test_board = [
    ['*', '*', '*', '*', '*', '*', '*', '*'],
    ['*', ' ', ' ', ' ', ' ', ' ', ' ', '*'],
    ['*', 'P', ' ', '#', ' ', ' ', ' ', '*'],
    ['*', '*', '*', '*', '*', ' ', '#', '*'],
    ['*', 'o', ' ', ' ', ' ', ' ', ' ', '*'],
    ['*', ' ', ' ', ' ', ' ', ' ', 'o', '*'],
    ['*', '*', '*', '*', '*', '*', '*', '*']]

print(main(test_board))
