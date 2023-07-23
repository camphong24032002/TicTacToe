from random import randrange
import time
import numpy as np
from Screen import Screen

class Game:
    """
       Initialize the game with the given board size.
    """
    def __init__(self):
        self.screen = Screen()
        
        self.board = []
        self.turn = -1
        self.signs = [] #-1: Player win, 1: AI win, 0: Draw
        self.scores = [-1000, 1000, 0]
    
    """
        Set size of game board. Initialize the winPos which is used to check the goal.
        
        Parameters:
            size: an integer (3, 5), the size of the board.
    """
    def setSize(self, size):
        self.size = size
        self.winPos = []
        # For each size, the game has its winPos.
        if size == 3:
            self.winBlocks = 3
            # Check vertical
            self.winPos += [[i, i+3, i+6] for i in range(3)]
            
            # Check horizontal
            self.winPos += [[i*3, i*3+1, i*3+2] for i in range(3)]
            
            # Check diagonal
            self.winPos += [[0, 4, 8], [2, 4, 6]]
        elif size == 5:
            self.winBlocks = 4
            # Check vertical
            self.winPos += [[i*5+j, i*5+j+5, i*5+j+10, i*5+j+15] for j in range(5) for i in range(2)]
            
            # Check horizontal
            self.winPos += [[j*5+i, j*5+i+1, j*5+i+2, j*5+i+3] for j in range(5) for i in range(2)]
            
            # Check diagonal
            self.winPos += [[i*5+j, i*5+j+6, i*5+j+12, i*5+j+18] for i in range(2) for j in range(2)]
            self.winPos += [[i*5+j+3, i*5+j+7, i*5+j+11, i*5+j+15] for i in range(2) for j in range(2)]
            
    """
        Setup game play. Random choose player's turn. Initialize and draw the board.
    """
    def start(self):
        self.turn = randrange(0, 2)
        self.board = np.array([[-1]*self.size]*self.size, dtype = int)
        if self.turn == 0:
            self.signs = ['X', 'O']
        else:
            self.signs = ['O', 'X']
        self.screen.draw_board(self.signs)
    
    """
        Check if the game is finished.
        
        Returns:
            goal: an integer (-1: not finished, 0: player win, 1: bot win, 2: draw), the status of the game.
    """
    def goal_check(self):
        # Check all cases of winPos
        for case in self.winPos:
            index = case[0]
            x, y = int(index / self.size), index % self.size
            check = True
            sign = self.board[x, y]
            
            for j in range(1, self.winBlocks):
                # Update position to check
                index = case[j]
                x, y = int(index / self.size), index % self.size
                if self.board[x, y] != sign:
                    check = False
                    break
            if check:
                return sign
            
        # Check draw. The game is draw if there is no empty cell
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i, j] == -1:
                    return -1
        return 2
    
    """
        Alpha-beta pruning algorithm.
    """
    
    def max_value(self, depth, alpha, beta):
        maxVal = -1000
        maxPos = None
        result = self.goal_check()

        # If the game is end, stop algorithm
        if result != -1:
            return self.scores[result], (0, 0)
        
        # Only apply heuristic on board 5x5
        if self.size == 5 and depth == 0:
            return self.heuristic(), (0, 0)
        
        # Try filling each cell and calculate the score
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i, j] == -1:
                    self.board[i, j] = 1
                    if self.goal_check() == 1:
                        self.board[i, j] = -1
                        return 100, (i, j)
                    newVal, move = self.min_value(depth - 1, alpha, beta)
                    self.board[i, j] = -1
                    if newVal > maxVal:
                        maxVal = newVal
                        maxPos = (i, j)
                    alpha = max(maxVal, alpha)
                    if alpha >= beta:
                        return alpha, maxPos
        return maxVal, maxPos
    def min_value(self, depth, alpha, beta):
        minVal = 1000
        minPos = None
        result = self.goal_check()
        
        # If the game is end, stop algorithm
        if result != -1:
            return self.scores[result], (0, 0)
        
        # Try filling each cell and calculate the score
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i, j] == -1:
                    self.board[i, j] = 0
                    if self.goal_check() == 0:
                        self.board[i, j] = -1
                        return -100, (i, j)
                    newVal, move = self.max_value(depth - 1, alpha, beta)
                    self.board[i, j] = -1
                    if newVal < minVal:
                        minVal = newVal
                        minPos = (i, j)
                    beta = min(minVal, beta)
                    if beta <= alpha:
                        return beta, minPos
        return minVal, minPos
    
    """
        Heuristic function is used to help program run faster
        
        Returns:
            h: an integer, the heuristic score
    """
    def heuristic(self):
        h = 0
        for i in range(len(self.winPos)):
            a, b = 0, 0
            for j in range(4):
                index = self.winPos[i][j]
                x, y = int(index / 5), index % 5
                if self.board[x, y] == 1:
                    a += 1
                elif self.board[x, y] == 0:
                    b += 1
            if (a == 0 or b == 0) and a != b:
                h += a*10 - b*10 - 1
        return h
    
    """
        Get bot's move
    """
    def move(self):
        val, move = self.max_value(4, -100000, 100000)
        self.board[move] = 1
        self.screen.draw_sign(self.signs[1], move)
    
    """
        The function that executes the game
    """
    def run(self):
        status = 0
        while True:
            # Start at menu screen
            if status == 0:
                self.setSize(self.screen.menu())
                self.start()
                check = -1
                status = 1
                self.screen.draw_turn_title(self.turn)
            else:
                # The game is finished
                if check != -1:
                    self.turn = -1
                    if check == 2:
                        self.screen.draw_end_title("TIE", (220, 15))
                    else:
                        self.screen.draw_end_title(self.signs[check] + " WIN", (180, 15))
                if self.turn == 1:
                    # Bot's turn
                    self.screen.draw_turn_title(self.turn)
                    time.sleep(0.5)
                    self.move()
                    check = self.goal_check()
                    self.turn = 0
                    self.screen.draw_turn_title(self.turn)
                else:
                    # Player's turn
                    result = self.screen.get_player_move(self.board, self.size)
                    # Player hasn't clicked yet or clicked on invalid cell
                    if result == 0:
                        continue
                    # If player click on Restart button
                    elif result == "restart":
                        self.start()
                        check = -1
                    # If player click on Home button
                    elif result == "home":
                        status = 0
                    elif self.turn != -1:
                        x, y = result
                        self.board[x, y] = 0
                        check = self.goal_check()
                        self.screen.draw_sign(self.signs[0], (x, y))
                        self.turn = 1