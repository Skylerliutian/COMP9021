#!/usr/bin/python
# use the sample provide by Zac Partridge
# Thanks very much!

import socket
import sys
import numpy as np
import copy

# a board cell can hold:
#   0 - Empty
#   1 - I played here
#   2 - They played here

# the boards are of size 10 because index 0 isn't used
boards = np.zeros((10, 10), dtype="int8")
s = [".","X","O"]
curr = 0 # this is the current board to play in

# print a row
# This is just ported from game.c
def print_board_row(board, a, b, c, i, j, k):
    print(" "+s[board[a][i]]+" "+s[board[a][j]]+" "+s[board[a][k]]+" | " \
             +s[board[b][i]]+" "+s[board[b][j]]+" "+s[board[b][k]]+" | " \
             +s[board[c][i]]+" "+s[board[c][j]]+" "+s[board[c][k]])

# Print the entire board
# This is just ported from game.c
def print_board(board):
    print_board_row(board, 1,2,3,1,2,3)
    print_board_row(board, 1,2,3,4,5,6)
    print_board_row(board, 1,2,3,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 4,5,6,1,2,3)
    print_board_row(board, 4,5,6,4,5,6)
    print_board_row(board, 4,5,6,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 7,8,9,1,2,3)
    print_board_row(board, 7,8,9,4,5,6)
    print_board_row(board, 7,8,9,7,8,9)
    print()


def win_situation(board0, n):
    board = copy.deepcopy(board0)
    board[n] = 1
    # 1,2,3 all 1
    if (board[1]==1)and(board[2]==1)and(board[3]==1):
        return True
    # 1,4,7 all 1
    if (board[1]==1)and(board[4]==1)and(board[7]==1):
        return True
    # 1,5,9 all 1
    if (board[1]==1)and(board[5]==1)and(board[9]==1):
        return True
    # 2,5,8 all 1
    if (board[2]==1)and(board[5]==1)and(board[8]==1):
        return True
    # 3,5,7 all 1
    if (board[3]==1)and(board[5]==1)and(board[7]==1):
        return True
    # 3,6,9 all 1
    if (board[3]==1)and(board[6]==1)and(board[9]==1):
        return True
    # 4,5,6 all 1
    if (board[4]==1)and(board[5]==1)and(board[6]==1):
        return True
    # 7,8,9 all 1
    if (board[7]==1)and(board[8]==1)and(board[9]==1):
        return True
    return False


def lose_situation(board):
    for n in range(1, 9):
        if board[n] == 0:
            board[n] = 2
            # 1,2,3 all 2
            if (board[1] == 2) and (board[2] == 2) and (board[3] == 2):
                return True
            # 1,4,7 all 2
            if (board[1] == 2) and (board[4] == 2) and (board[7] == 2):
                return True
            # 1,5,9 all 2
            if (board[1] == 2) and (board[5] == 2) and (board[9] == 2):
                return True
            # 2,5,8 all 2
            if (board[2] == 2) and (board[5] == 2) and (board[8] == 2):
                return True
            # 3,5,7 all 2
            if (board[3] == 2) and (board[5] == 2) and (board[7] == 2):
                return True
            # 3,6,9 all 2
            if (board[3] == 2) and (board[6] == 2) and (board[9] == 2):
                return True
            # 4,5,6 all 2
            if (board[4] == 2) and (board[5] == 2) and (board[6] == 2):
                return True
            # 7,8,9 all 2
            if (board[7] == 2) and (board[8] == 2) and (board[9] == 2):
                return True
            board[n] = 0

# choose a move to play
def play():
    # print_board(boards)
    for n in range(1, 10):
        if win_situation(boards[curr], n)and(boards[curr][n] == 0):
            place(curr, n, 1)
            return n
    for n in range(1, 10):
        board = boards[n]
        if len(board[board==1])>len(board[board==2]) and (not lose_situation(board)):
            place(curr, n, 1)
            return n
    for n in range(1, 10):
        board = boards[n]
        if not lose_situation(board):
            place(curr, n, 1)
            return n


# place a move in the global boards
def place(board, num, player):
    global curr
    curr = num
    boards[board][num] = player

# read what the server sent us and
# only parses the strings that are necessary
def parse(string):
    if '(' in string:
        command, args = string.split('(')
        args = args.split(')')[0]
        args = args.split(',')
    else:
        command, args = string, []

    if command == 'second_move':
        place(int(args[0]), int(args[1]), 2)
        return play()
    elif command == 'third_move':
        # place the move that was generated for us
        place(int(args[0]), int(args[1]), 1)
        # place their last move
        place(curr, int(args[2]), 2)
        return play()
    elif command == 'next_move':
        place(curr, int(args[0]), 2)
        return play()
    elif command == 'win':
        print('Congratulations!! We win!!')
        return -1
    elif command == 'loss':
        print("We lost... Don't give up")
        return -1
    return 0

# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    while True:
        text = s.recv(1024).decode()
        if not text:
            continue
        for line in text.split('\n'):
            response = parse(line)
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())

if __name__ == "__main__":
    main()
