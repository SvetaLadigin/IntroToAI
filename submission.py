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


###### reference
    # def smoothness(self,board):
    #     grade = 0
    #     for row in range(4):
    #         for col in range(4):
    #             if board[row][col] is not 0:
    #                 if board[row][3] is not 0:
    #                     grade += abs(self.log2(board[row][col]) - self.log2(board[row][3]))
    #                 if board[3][col] is not 0:
    #                     grade += abs(self.log2(board[row][col]) - self.log2(board[3][col]))
    #
    #     return -grade

    def monotonus(self,board):
        ascending_up_to_down = 0
        descending_up_to_down = 0
        ascending_left_to_right = 0
        descending_left_to_right = 0
        for row in range(4):
            for col in range(4):
                if col + 1 < 4:
                    if board[row][col] > board[row][col + 1]:
                        descending_left_to_right -= board[row][col] - board[row][col + 1]
                    else:
                        ascending_left_to_right += board[row][col] - board[row][col + 1]
                if row + 1 < 4:
                    if board[row][col] > board[row + 1][col]:
                        descending_up_to_down -= board[row][col] - board[row + 1][col]
                    else:
                        ascending_up_to_down += board[row][col] - board[row + 1][col]
        return max(descending_left_to_right, ascending_left_to_right) + max(descending_up_to_down, ascending_up_to_down)
###########################################################################


    def smoothness(self,board):
        counter = 0
        for row in range(4):
            for col in range(4):
                if board[row][col] != 0:
                    i = 1
                    while col+i < 4:
                        if board[row][col + i] == 0:
                            i += 1
                            continue
                        if board[row][col+i] == board[row][col]:
                            counter += board[row][col]
                        break

                    i = 1
                    while row+i < 4:
                        if board[row + i][col] == 0:
                            i += 1
                            continue
                        if board[row+i][col] == board[row][col]:
                            counter += board[row][col]
                        break
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
        return 16*(1 - max_seq/counter)

    # def monotonus(self, board):
    #     ascending_up_to_down = 0
    #     descending_up_to_down = 0
    #     ascending_left_to_right = 0
    #     descending_left_to_right = 0
    #     for row in range(4):
    #         for col in range(4):
    #             if board[row][col] == 0:
    #                 continue
    #             i = 1
    #             while col + i < 4:
    #                 if board[row][col + i] == 0:
    #                     i += 1
    #                     continue
    #                 if board[row][col] > board[row][col + 1]:
    #                     descending_left_to_right += board[row][col] - board[row][col + 1]
    #                 else:
    #                     ascending_left_to_right += board[row][col + 1] - board[row][col]
    #                 break
    #             i = 1
    #             while row + i < 4:
    #                 if board[row + i][col] == 0:
    #                     i += 1
    #                     continue
    #                 if board[row][col] > board[row + 1][col]:
    #                     descending_up_to_down += board[row][col] - board[row + 1][col]
    #                 else:
    #                     ascending_up_to_down += board[row + 1][col] - board[row][col]
    #                 break
    #     return max(descending_left_to_right , ascending_left_to_right) + max(descending_up_to_down , ascending_up_to_down)

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


    def calcCellScore(self,value):
        if value <=2:
            return 0
        return 2*self.calcCellScore(value/2) + 2**self.log2(value)

    def score(self, board):
        cells_sum = 0
        for row in range(4):
            for col in range(4):
                 cells_sum += self.calcCellScore(board[row][col])
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
        return max_value

    def hotCorners(self, board):
        max_value = self.maxCellValue(board)
        grade = 0
        for row in range(4):
            for col in range(4):
                if board[row][col] == max_value:
                    if (row == 0 and col == 0) or (row == 3 and col == 3) or (row == 0 and col == 3) or (row == 3 and col == 0):
                        grade += 2*(max_value)
                        continue
                    if (row == 1 and col == 1) or (row == 2 and col == 2) or (row == 1 and col == 2) or (row == 2 and col == 1):
                        grade -= (max_value)
                        continue
                    grade -= (max_value)

        return grade

    def emptyCells(self,board):
        counter = 0
        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    counter += 1
        return counter



    def calculateNewHScore(self, board):
        save_board = [row[:] for row in board]
        # for i in range(4):
        #     save_board.append(board[i])
        logged_board = self.logBoard(save_board)

        greedy_score = self.score(board)
        max_value_cell = self.maxCellValue(board)
        fragmantation_value = self.fragmentation(board)
        empty_value = self.emptyCells(board)
        smoothness_score = self.smoothness(board)
        monoton_score = self.monotonus(board)
        hot_corners = self.hotCorners(board)
        # return float(greedy_score)*0.5+max_value_cell*0.5+smoothness_score*0.2+monoton_score*0.2-fragmantation_value*0.2

        score_fac = 15
        max_value_cell_fac = 10
        fragmantation_value_fac = 10
        empty_value_fac = 20
        hot_corners_fac = 10
        smoothness_score_fac = 40
        monoton_score_fac =40
        print("*************  START   *************")
        print("score: "+str(greedy_score)+'fac:' + str(score_fac))
        print("max_value_cell: "+str(max_value_cell)+'fac:' + str(max_value_cell_fac))
        print("emptyCells: "+str(empty_value)+'fac:' + str(empty_value_fac))
        print("fragmantation: "+str(fragmantation_value)+'fac:' + str(fragmantation_value_fac))
        print("smoothness_score: "+str(smoothness_score)+'fac:' + str(hot_corners_fac))
        print("monoton_score: "+str(monoton_score)+'fac:' + str(smoothness_score_fac))
        print("hot_corners: "+str(hot_corners)+'fac:' + str(monoton_score_fac))
        print("*************   END    *************")

        return float(greedy_score)*score_fac\
               + max_value_cell*max_value_cell_fac\
               + fragmantation_value*fragmantation_value_fac\
               + empty_value*empty_value_fac\
               + hot_corners*hot_corners_fac\
               + smoothness_score*smoothness_score_fac\
               + monoton_score*monoton_score_fac
# ---------------- GET MOVE USING NEW HEURISTICS ---------------

    def get_move(self, board, time_limit) -> Move:
        optional_moves_score = {}
        for move in Move:
            new_board, done, score = commands[move](board)
            if done:
                optional_moves_score[move] = self.calculateNewHScore(new_board)
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

