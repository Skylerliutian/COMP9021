import copy


x_player = "X"
o_player = "O"
dot_player = "."

minimax_depth = 3


# in order to create a nine-board tic-tac-toe board
class Board(object):
    boards = [[dot_player for i in range(1, 10)] for j in range(1, 10)]
    player = ""
    current_board = 0
    last_move = 0
    last_board = 0
    x_grade = 0
    o_grade = 0

    def __init__(self, player):
        self.player = player

    def __copy__(self):
        board_copy = Board(copy.deepcopy(self.player))
        board_copy.boards = copy.deepcopy(self.boards)
        board_copy.last_move = copy.deepcopy(self.last_move)
        board_copy.x_grade = copy.deepcopy(self.x_grade)
        board_copy.o_grade = copy.deepcopy(self.o_grade)
        board_copy.current_board = copy.deepcopy(self.current_board)
        return board_copy

    # to add one move in this board at current state
    def add_move(self, move, current_board=None, flag=True):
        """Add a move to the board."""
        if current_board is None:
            current_board = self.current_board

        previous_x = self.calculate_board_grade(current_board, x_player)
        previous_o = self.calculate_board_grade(current_board, o_player)

        if flag:
            self.boards[current_board-1][move-1] = self.player
        elif self.player == x_player:
            self.boards[current_board-1][move-1] = o_player
        elif self.player == o_player:
            self.boards[current_board-1][move-1] = x_player

        new_x = self.calculate_board_grade(current_board, x_player)
        new_o = self.calculate_board_grade(current_board, o_player)
        self.x_grade = self.x_grade - previous_x + new_x
        self.o_grade = self.o_grade - previous_o + new_o
        self.last_move = move
        self.last_board = current_board
        self.current_board = move

    # compute board grade and return grade
    def calculate_board_grade(self, current_board, player):
        grade = 0
        win_list = []
        for a in range(0, 3):
            win_list.append(range(a*3, a*3+3))
            win_list.append(range(a, 9, 3))
        win_list.append(range(2, 8, 2))
        win_list.append(range(0, 9, 4))
        for w in win_list:
            num = 0
            for i in w:
                if self.boards[current_board-1][i] == player:
                    num += 1
                elif self.boards[current_board-1][i] != dot_player:
                    num -= 3
            if num == 3:
                grade += 1000000
            elif num == 2:
                grade += 10
            elif num == 1:
                grade += 1
        return grade

    # check whether player can do this move, this step is depend by player
    def can_move(self, step):
        return self.boards[self.current_board-1][step-1] == dot_player

    # compute the grade of this board for this player
    def get_score(self):
        if self.player != x_player:
            return self.o_grade - self.x_grade
        else:
            return self.x_grade - self.o_grade

    # update the boards after player finish this legal move
    def next_boards(self, flag):
        new_boards = []
        for i in range(1, 10):
            if self.can_move(i):
                new_board = copy.copy(self)

                new_board.add_move(i, self.current_board, not flag)

                new_boards.append(new_board)
        return new_boards

    # override __str__ in order to print a visual board at current state
    def __str__(self):
        boards = [self.boards[:3], self.boards[3:6], self.boards[6:9]]
        string = '\n'
        for j in range(0, 3):
            string += ' '
            for i in range(0, len(boards[j])):
                string += ' '.join(boards[j][i][:3])
                if i != len(boards[j])-1:
                    string += ' | '
            string += '\n '
            for i in range(0, len(boards[j])):
                string += ' '.join(boards[j][i][3:6])
                if i != len(boards[j])-1:
                    string += ' | '
            string += '\n '
            for i in range(0, len(boards[j])):
                string += ' '.join(boards[j][i][6:9])
                if i != len(boards[j])-1:
                    string += ' | '
            if j != len(boards)-1:
                string += '\n ------+-------+------ '
            string += '\n'

        return string

