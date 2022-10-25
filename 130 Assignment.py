class Sokoban:
    def __init__(self, board = []):
        self.__board = board
        self.__steps = 0
        self.__restart = [list(i) for i in board]
        for row in self.__board:
            self.__column_length = len(row)
        self.__row_length = len(self.__board)
    
    def find_player(self):
        row = 0
        for rows in self.__board:
            for index in range(row):
                if self.__board[row[index]] == "P":
                    column = index
                    row = rows
        return tuple(row, column)

    def complete(self):
        for row in self.__board:
            for column in row:
                if column == "o":
                    return False 
        return True

    def get_steps(self):
        return self.__steps

    def restart(self):
        self.__board = self.__restart
        self.__steps = 0


    def undo(self):
        pass


    def find_next_pos_player(self, row, column, direction):
        if direction == "a" and column != 0:
            return [row, column - 1]
        if direction == "a" and column == 0:
            return [row, self.__column_length]
        if direction == "d" and column != self.__column_length:
            return [row, column + 1]
        if direction == "d" and column == self.__column_length:
            return [row, 0]
        if direction == "w" and row != 0:
            return [row - 1, column]
        if direction == "w" and row == 0:
            return [self.__row_length, column]
        if direction == "s" and row != self.__row_length:
            return [row + 1, column]
        if direction == "s" and row == self.__row_length:
            return [0, column]

    def next_pos_horizon(self, row, column, direction):         # Box
        if direction == "a" and column > 1:
            return [row, column - 2]
        if direction == "a" and column == 1:
            return [row, self.__column_length]
        if direction == "a" and column == 0:
            return [row, self.__column_length - 1]
        
        if direction == "d" and column < self.__column_length - 1:
            return [row, column + 2]
        if direction == "d" and column == self.__column_length - 1:
            return [row, 0]
        if direction == "d" and column == self.__column_length:
            return [row, 1]

    def next_pos_vertical(self, row, column, direction):        
        if direction == "w" and row > 1:
            return [row - 2, column]
        if direction == "w" and row == 1:
            return [self.__row_length, column]
        if direction == "w" and row == 0:
            return [self.__row_length - 1, column]
        
        if direction == "s" and row < self.__row_length - 1:
            return [row + 2, column]
        if direction == "s" and row == self.__row_length - 1:
            return [0, column]
        if direction == "s" and row == self.__row_length:
            return [1, column]
    
    def player_or_box(self, row, column, direction):
        if direction == "a" and column != 0:
            return self.__board[row[column - 1]] == "#"
        if direction == "a" and column == 0:
            return self.__board[row[self.__column_length]] == "#"
        if direction == "d" and column != self.__column_length:
            return self.__board[row[column + 1]] == "#"
        if direction == "d" and column == self.__column_length:
            return self.__board[row[0]] == "#"
        if direction == "w" and row != 0:
            return self.__board[row - 1[column]] == "#"
        if direction == "w" and row == 0:
            return self.__board[self.__row_length[column]] == "#"
        if direction == "s" and row != self.__row_length:
            return self.__board[row + 1[column]] == "#"
        if direction == "s" and row == self.__row_length:
            return self.__board[0[column]] == "#"

    def move_player (self, row, column, row_after, column_after):
        if self.__board[row_after[column_after]] not in "o*":
            self.__board[row_after[column_after]] = "P"
            self.__board[row[column]] = " "
            self.__steps += 1

    def move_box (self, row, column, row_box, column_box, row_after, column_after):
        if self.__board[row_after[column_after]] == "o":
            self.__board[row_after[column_after]] = " "
            self.__board[row_box[column_box]] = "P"
            self.__board[row[column]] = " "
            self.__steps += 1
        if self.__board[row_after[column_after]] == " ":
            self.__board[row_after[column_after]] = "#"
            self.__board[row_box[column_box]] = "P"
            self.__board[row[column]] = " "
            self.__steps += 1

        
    def move(self, direction):
        p_loc = self.find_player()
        p_or_b = self.player_or_box(p_loc[0], p_loc[1], direction)
        box = self.find_next_pos_player(p_loc[0], p_loc[1], direction)
        if p_or_b == True:
            if direction in "ad":
                next_pos = self.next_pos_horizon(p_loc[0], p_loc[1], direction)
            else:
                next_pos = self.next_pos_vertical(p_loc[0], p_loc[1], direction)
            self.move_box(p_loc[0], p_loc[1], box[0], box[1], next_pos[0], next_pos[1]) 
        else:
            next_pos = self.find_next_pos_player(p_loc[0], p_loc[1], direction)
            self.move_player(p_loc[0], p_loc[1], next_pos[0], next_pos[1])
        return self.__board        
            
        
                             
    def __str__(self):
        for row in self.__data:
            print (row + "\n")
        return

def main(board):
    game = Sokoban(board)
    message = "press w/a/s/d to move, r to restart, or u to undo"
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
            print(game)
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


        
