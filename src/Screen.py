import pygame as pg
import sys

class Screen:
    def __init__(self):    
        pg.init()
        pg.display.set_caption('Tic Tac Toe')
        
        self.screen = pg.display.set_mode((500, 700))
        
        self.font = pg.font.SysFont("Arial", 30)
        self.restartText = self.font.render("Restart", True, (255, 255, 255))
        self.quitText = self.font.render("Home", True, (255, 255, 255))
        self.font2 = pg.font.SysFont("Arial", 50)
        
    """
        Update screen
    """
    def update(self):
        pg.display.update()    
    
    """
        Draw a menu creen 
    """
    def menu(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render("SELECT THE BOARD SIZE", True, (255, 255, 255))
        self.screen.blit(text, (100, 50))
        
        # Draw the button
        text1 = self.font.render("3x3", True, (0, 0, 0))
        text2 = self.font.render("5x5", True, (0, 0, 0))
        pg.draw.rect(self.screen, (255, 255, 255), [150, 200, 200, 100])
        pg.draw.rect(self.screen, (255, 255, 255), [150, 400, 200, 100])
        self.screen.blit(text1, (230, 230))
        self.screen.blit(text2, (230, 430))
        self.update()
        
        # Get player's clicked event
        while True:
            mouse = pg.mouse.get_pos()
            for event in pg.event.get():
                # Click exit button
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                # Click game size button
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if 150 < mouse[0] < 350 and 200 < mouse[1] < 300:
                        self.size = 3
                        return 3
                    elif 150 < mouse[0] < 350 and 400 < mouse[1] < 500:
                        self.size = 5
                        return 5
    
    # Draw the board
    def draw_board(self, signs):
        self.screen.fill((255, 255, 255))
        # Draw board
        n = int(420 / self.size)
        for i in range(self.size + 1):
            pg.draw.line(self.screen, (0, 0, 0), (40 + i*n, 140), (40 + i*n, 560), 3)
            pg.draw.line(self.screen, (0, 0, 0), (40, 140 + i*n), (460, 140 + i*n), 3)
            
        # Draw button
        pg.draw.rect(self.screen, (0, 0, 0), [0, 0, 500, 100])
        pg.draw.rect(self.screen, (0, 0, 0), [0, 600, 500, 100])
        pg.draw.rect(self.screen, (100, 100, 100), [100, 625, 100, 50])
        pg.draw.rect(self.screen, (100, 100, 100), [300, 625, 100, 50])
        self.screen.blit(self.restartText, (110, 630))
        self.screen.blit(self.quitText, (320, 630))
        
        # Draw player's sign
        playerText = self.font.render("You: "+ signs[0], True, (255, 255, 255))
        botText = self.font.render("Bot: "+ signs[1], True, (255, 255, 255))
        self.screen.blit(playerText, (100, 65))
        self.screen.blit(botText, (300, 65))
        self.update()
    
    """
        Draw the sign on the board
    """
    def draw_sign(self, sign, move):
        x, y = move
        n = int(420 / self.size)
        if sign == 'X':
            # Draw X
            pg.draw.line(self.screen, (0, 0, 255), (50 + n*y, 150 + n*x), (30 + n*(y+1), 130 + n*(x+1)), 10)
            pg.draw.line(self.screen, (0, 0, 255), (30 + n*(y+1), 150 + n*x), (50 + n*y, 130 + n*(x+1)), 10)
        else:
            # Draw O
            pg.draw.circle(self.screen, (255, 0, 0), (40 + int(n*(y+0.5)), 140 + int(n*(x+0.5))), int(n*0.45), 3)
        self.update()
    
    """
        Draw the player's turn
    """
    def draw_turn_title(self, turn):
        name = ["Your turn", "Bot turn"]
        pg.draw.rect(self.screen, (0, 0, 0), [0, 0, 500, 70])
        turnText = self.font2.render(name[turn], True, (255, 255, 255))
        self.screen.blit(turnText, (180, 10))
        self.update()
    
    """
        Draw the ending title
    """
    def draw_end_title(self, text, pos):
        pg.draw.rect(self.screen, (0, 0, 0), [0, 0, 500, 100])
        endText = self.font2.render(text, True, (255, 255, 255))
        self.screen.blit(endText, pos)
        self.update()
    
    """
        Get player's clicked event
    """
    def get_player_move(self, board, size):
        #Player's turn
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                # Click restart button
                if 100 < mouse[0] < 200 and 625 < mouse[1] < 675:
                    return "restart"
                # Click home button
                elif 300 < mouse[0] < 400 and 625 < mouse[1] < 675:
                    return "home"
                elif 40 < mouse[0] < 460 and 140 < mouse[1] < 560:
                    n = int(420 / size)
                    x, y = int((mouse[1] - 140) / n), int((mouse[0] - 40) / n)
                    if x < 0 or x > size or y < 0 or y > size or board[x, y] != -1:
                        return 0
                    return [x, y]
        return 0