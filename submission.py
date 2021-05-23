import logic
import random
from AbstractPlayers import *
import time

# commands to use for move players. dictionary : Move(enum) -> function(board),
# all the functions {up,down,left,right) receive board as parameter and return tuple of (new_board, done, score).
# new_board is according to the step taken, done is true if the step is legal, score is the sum of all numbers that
# combined in this step.
# (you can see GreedyMovePlayer implementation for example)
commands = {Move.UP: logic.up, Move.DOWN: logic.down,
            Move.LEFT: logic.left, Move.RIGHT: logic.right}


# generate value between {2,4} with probability p for 4
def gen_value(p=PROBABILITY):
    return logic.gen_two_or_four(p)


class GreedyMovePlayer(AbstractMovePlayer):
    """Greedy move player provided to you (no need to change),
    the player receives time limit for a single step and the board as parameter and return the next move that gives
    the best score by looking one step ahead.
    """
    def get_move(self, board, time_limit) -> Move:
        optional_moves_score = {}
        for move in Move:
            new_board, done, score = commands[move](board)
            if done:
                optional_moves_score[move] = score
                # print("the optional_moves_score: "+str(move)+" in optional move_score[move] "+str(optional_moves_score))
        # print("greedy move : "+str(max(optional_moves_score, key=optional_moves_score.get)))
        return max(optional_moves_score, key=optional_moves_score.get)


class RandomIndexPlayer(AbstractIndexPlayer):
    """Random index player provided to you (no need to change),
    the player receives time limit for a single step and the board as parameter and return the next indices to
    put 2 randomly.
    """
    def get_indices(self, board, value, time_limit) -> (int, int):
        a = random.randint(0, len(board) - 1)
        b = random.randint(0, len(board) - 1)
        while board[a][b] != 0:
            a = random.randint(0, len(board) - 1)
            b = random.randint(0, len(board) - 1)
        return a, b


# part A
class ImprovedGreedyMovePlayer(AbstractMovePlayer):
    """Improved greedy Move Player,
    implement get_move function with greedy move that looks only one step ahead with heuristic.
    (you can add helper functions as you want).
    """
    def __init__(self):
        AbstractMovePlayer.__init__(self)



        # TODO: add here if needed

    def log2(self, number):
        counter = 0
        n = number
        while int(n/2) != 0:
            counter = counter+1
            n = n/2
        return counter


    def smoothness(self,board):

        copy_board = board

        counter = 0
        for row in range(4):
            for col in range(4):
                if copy_board[row][col] != 0:
                    if copy_board[row][3] != 0:
                        counter += abs((copy_board[row][col]) - (
                            copy_board[row][3]))
                    if copy_board[3][col] != 0:
                        counter += abs((copy_board[row][col]) - (
                            copy_board[3][col]))
        print('smoothness score '+str(counter))
        return counter

    def fragmentation(self, board):
        copy_board = board
        counter = 0
        max_seq = 0
        curr_seq = 0
        visited = []
        finished = []
        queue = []
        counter = 0
        for row in range(4):
            for col in range(4):
                if copy_board[row][col] == 0:
                    queue.append([row, col])
                    counter += 1
        if counter == 0:
            return 0
        for index in queue:
            i = 0
            while [index[0]+i, index[1]] in queue:
                j = 0
                while [index[0]+i, index[1]+j] in queue:
                    if [index[0]+i, index[1]+j] not in visited:
                        curr_seq += 1
                        visited.append([index[0]+i, index[1]+j])
                    j += 1
                i += 1

            if curr_seq > max_seq:
                max_seq = curr_seq
            curr_seq = 0
        print ('frag: '+ str(16*(1 - max_seq/counter))+' empty cells: '+str(counter)+'  max block size: '+str(max_seq))
        return 16*(1 - max_seq/counter)

    def monotonus(self, board):

        copy_board = board
        asndud = 0
        dsndud = 0
        asndlr = 0
        dsndlr = 0
        for row in range(4):
            for col in range(4):
                if col + 1 < 4:
                    if copy_board[row][col] > copy_board[row][col + 1]:
                        dsndlr += copy_board[row][col] - copy_board[row][col + 1]
                    else:
                        asndlr += copy_board[row][col+1] - copy_board[row][col]
                if row + 1 < 4:
                    if copy_board[row][col] > copy_board[row + 1][col]:
                        dsndud += copy_board[row][col] - copy_board[row + 1][col]
                    else:
                        asndud += copy_board[row+1][col] - copy_board[row][col]
        print('monoton: '+str(max(dsndlr, asndlr) + max(dsndud, asndud)))
        return max(dsndlr, asndlr) + max(dsndud, asndud)

    def logBoard(self, board):
        copy_board = board
        for row in range(4):
            for col in range(4):
                if board[row][col] != 0:
                    copy_board[row][col] = self.log2(copy_board[row][col])
                else:
                    copy_board[row][col] = 0
        return copy_board


# --------------Greedy func that return score --------------

    def score(self, board):
        copy_board = board
        cells_sum = 0
        for row in range(4):
            for col in range(4):
                cells_sum += copy_board[row][col]
        print('greedy score value: ' + str(cells_sum))
        return cells_sum

    def maxCellValue(self, board):
        copy_board = board
        # print(copy_board)
        max_value = 0
        for row in range(4):
            for col in range(4):
                # print(copy_board[row][col])
                if copy_board[row][col] > max_value:
                    max_value = copy_board[row][col]
        print('cell_max_value: ' + str(max_value))
        return max_value

    def calculateNewHScore(self, board):
        save_board = [row[:] for row in board]
        # for i in range(4):
        #     save_board.append(board[i])
        logged_board = self.logBoard(save_board)
        greedy_score = self.score(logged_board)
        max_value_cell = self.maxCellValue(logged_board)
        fragmantation_value = self.fragmentation(logged_board)
        smoothness_score = self.smoothness(logged_board)
        monoton_score = self.monotonus(logged_board)
        return float(greedy_score)*0.5+max_value_cell*0.5+smoothness_score*0.2+monoton_score*0.2-fragmantation_value*0.2
# ---------------- GET MOVE USING NEW HEURISTICS ---------------

    def get_move(self, board, time_limit) -> Move:
        optional_moves_score = {}
        for move in Move:
            new_board, done, score = commands[move](board)
            if done:
                optional_moves_score[move] = self.calculateNewHScore(board)
                print("move: "+move.value+' heuristic count: '+str(optional_moves_score[move]))

        return max(optional_moves_score, key=optional_moves_score.get)












        # print(board)
        # optional_moves_score = {}
        # for move in Move:
        #     new_board, done, score = commands[move](board)
        #     if done:
        #         optional_moves_score[move] = score
        #         # print("the optional_moves_score: " + str(move) + " in optional move_score[move] " + str(
        #         #     optional_moves_score))
        # print("greedy move : " + str(max(optional_moves_score, key=optional_moves_score.get)))
        # # max_compare = optional_moves_score.get
        # max_value = max(optional_moves_score, key=optional_moves_score.get)
        # max_value = optional_moves_score[max_value]
        #
        # total_list = []
        # scores_sum = []
        # for move in optional_moves_score:
        #     print("the current move: "+str(move)+" move score: " + str(optional_moves_score[move]) + " max_value: " + str(max_value))
        #     if optional_moves_score[move] == max_value:
        #         total_list.append(move)
        #
        #
        # print("total list: "+str(total_list))
        # return max(optional_moves_score, key=optional_moves_score.get)


    # TODO: add here helper functions in class, if needed


# part B
class MiniMaxMovePlayer(AbstractMovePlayer):
    """MiniMax Move Player,
    implement get_move function according to MiniMax algorithm
    (you can add helper functions as you want).
    """
    def __init__(self):
        AbstractMovePlayer.__init__(self)
        # TODO: add here if needed

    def get_move(self, board, time_limit) -> Move:
        # TODO: erase the following line and implement this function.
        raise NotImplementedError

    # TODO: add here helper functions in class, if needed


class MiniMaxIndexPlayer(AbstractIndexPlayer):
    """MiniMax Index Player,
    this player is the opponent of the move player and need to return the indices on the board where to put 2.
    the goal of the player is to reduce move player score.
    implement get_indices function according to MiniMax algorithm, the value in minimax player value is only 2.
    (you can add helper functions as you want).
    """
    def __init__(self):
        AbstractIndexPlayer.__init__(self)
        # TODO: add here if needed

    def get_indices(self, board, value, time_limit) -> (int, int):
        # TODO: erase the following line and implement this function.
        raise NotImplementedError

    # TODO: add here helper functions in class, if needed


# part C
class ABMovePlayer(AbstractMovePlayer):
    """Alpha Beta Move Player,
    implement get_move function according to Alpha Beta MiniMax algorithm
    (you can add helper functions as you want)
    """
    def __init__(self):
        AbstractMovePlayer.__init__(self)
        # TODO: add here if needed

    def get_move(self, board, time_limit) -> Move:
        # TODO: erase the following line and implement this function.
        raise NotImplementedError

    # TODO: add here helper functions in class, if needed


# part D
class ExpectimaxMovePlayer(AbstractMovePlayer):
    """Expectimax Move Player,
    implement get_move function according to Expectimax algorithm.
    (you can add helper functions as you want)
    """
    def __init__(self):
        AbstractMovePlayer.__init__(self)
        # TODO: add here if needed

    def get_move(self, board, time_limit) -> Move:
        # TODO: erase the following line and implement this function.
        raise NotImplementedError

    # TODO: add here helper functions in class, if needed


class ExpectimaxIndexPlayer(AbstractIndexPlayer):
    """Expectimax Index Player
    implement get_indices function according to Expectimax algorithm, the value is number between {2,4}.
    (you can add helper functions as you want)
    """
    def __init__(self):
        AbstractIndexPlayer.__init__(self)
        # TODO: add here if needed

    def get_indices(self, board, value, time_limit) -> (int, int):
        # TODO: erase the following line and implement this function.
        raise NotImplementedError

    # TODO: add here helper functions in class, if needed


# Tournament
class ContestMovePlayer(AbstractMovePlayer):
    """Contest Move Player,
    implement get_move function as you want to compete in the Tournament
    (you can add helper functions as you want)
    """
    def __init__(self):
        AbstractMovePlayer.__init__(self)
        # TODO: add here if needed

    def get_move(self, board, time_limit) -> Move:
        # TODO: erase the following line and implement this function.
        raise NotImplementedError

    # TODO: add here helper functions in class, if needed

