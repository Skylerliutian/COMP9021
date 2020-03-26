#!/usr/bin/python
# The agent.py includes two classes, first is class Board which is used to print the current state nine-board tic-tac-toe board,
# and this Board class have some functions like can_move to check weather player can do this move and so on.
# And class Tree is used to create tree with children in order to implement the alpha-beta pruning algorithm.
# Apart from that two classes, I add some functions max_score and min_score to get the alpha and beta.
# Sever code contains functions of move, last_move, nest_move, second_move and third_move.
# Also create a socket and check the port is legal to make sure this program can be execute correctly
import sys
import re
import socket
import random
import copy


x_player = "X"
o_player = "O"
dot_player = "."

minimax_depth = 4


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



current_board = None

# create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# This class is a tree with children which shows a list of trees and a board as the value
class Tree(object):
    children = []  # to append trees
    value = None

    def __init__(self, value):
        self.value = value
        self.children = []

    def append_child(self, child):
        self.children.append(child)

    def add_children(self, children):
        self.children.extend(children)


# build a tree from the current state board
def build_tree(current_board, depth, flag):
    states = Tree(current_board)

    if depth == 0:
        return states

    # build all the next boards
    for next_board in current_board.next_boards(flag):
        states.append_child(build_tree(next_board, depth - 1, not flag))

    return states

# This is the algorithm of alpha - beta minimax
def minimax_move():
    move_tree = build_tree(current_board, minimax_depth, False)  # board.minimax_depth

    best_board = None
    best_score = -1000000

    alpha = -1000000000
    beta = 1000000000
    for chi in move_tree.children:
        child_score = max_score(chi, alpha, beta, current_board.player)
        if child_score > best_score:
            best_board = chi.value
            best_score = child_score
    attempted_move = best_board.last_move
    move(attempted_move)
# to move randomly
def random_move():
    attempted_move = random.randint(1, 9)
    while not current_board.is_legal(attempted_move):
        attempted_move = random.randint(1, 9)
    move(attempted_move)

# return the beta of the current state board by using alpha-beta pruning
def min_score(tree, alpha, beta, original_player):
    tree.value.player = original_player
    if len(tree.children) == 0:
        return tree.value.get_score()

    for child in tree.children:
        beta = min(beta, max_score(child, alpha, beta, original_player))
        if beta <= alpha:
            break
    return beta

# return the alpha of the current state board by using alpha-beta pruning
def max_score(tree, alpha, beta, original_player):
    tree.value.player = original_player
    if len(tree.children) == 0:
        return tree.value.get_score()

    for child in tree.children:
        alpha = max(alpha, min_score(child, alpha, beta, original_player))
        if beta <= alpha:
            break
    return alpha



# sever code..................

# type a positive integer number and add it to the current board, then send it to server
def move(move):
    current_board.add_move(move)
    s.sendall((str(move) + '\n').encode())  # + '\n'

# add the last one move into the current board
def last_move(previous_move):
    current_board.add_move(int(previous_move), current_board.current_board, False)

# execute a move and add previous move into the current board
def next_move(last_move):
    current_board.add_move(int(last_move), current_board.current_board, False)
    minimax_move()
    
# execute the second move and add the first move into the current board
def second_move(first_board, first_move):
    current_board.add_move(int(first_move), int(first_board), False)
    minimax_move()

# execute the third move and add the second move into the current board
def third_move(first_board, first_move, second_move):
    current_board.add_move(int(first_move), int(first_board))
    current_board.add_move(int(second_move), current_board.current_board, False)
    minimax_move()

# guarantee the port
if '-p' in sys.argv:
    portArg = sys.argv.index('-p') + 1
    port = int(sys.argv[portArg])
else:
    error = """Usage: %s -p <port>""" % sys.argv[0]
    sys.exit(error)

# connect to the server
host = socket.gethostname()
s.connect((host, port))

command = 'init.\n'

# check for each command since multiple commands are received at the same moment
while 'end' not in command and command != '':
    command = repr(s.recv(1024))

    # start
    start_sign = re.search(r'start\(([xo])\)', command)
    # initialise the board as the player we're allocated
    if start_sign is not None:
        if start_sign.group(1) == 'x':
            current_board = Board(x_player)
        elif start_sign.group(1) == 'o':
            current_board = Board(o_player)

    # second_move
    second_move_sign = re.search(r'second_move\(([1-9]),([1-9])\)', command)
    if second_move_sign is not None:
        second_move(second_move_sign.group(1), second_move_sign.group(2))

    # third_move
    third_move_sign = re.search(r'third_move\(([1-9]),([1-9]),([1-9])\)',
                                command)
    if third_move_sign is not None:
        first_move = third_move_sign.group(1)
        first_board = third_move_sign.group(2)
        second_move = third_move_sign.group(3)

        third_move(first_move, first_board, second_move)

    # next_move
    next_move_sign = re.search(r'next_move\(([1-9])\)', command)
    if next_move_sign is not None:
        next_move(next_move_sign.group(1))

    # last_move
    last_move_sign = re.search(r'last_move\(([1-9])\)', command)
    if last_move_sign is not None:
        last_move(last_move_sign.group(1))

    number = re.findall(r'\d', command)
    print(number, current_board)

    # result
    game_end_sign = re.search(r'(win|lose|end)', command)
    if game_end_sign is not None:
        break

print("Finished here .")
s.close()
