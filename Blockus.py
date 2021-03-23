from math import floor
import pygame
from pygame.locals import *
from tkinter import *

def convertToHexRGB(rgb):
    #takes in an an int rgb array and returns the color in format #rrggbb
    value = "#"
    for val in rgb:
        value = value + (hex(val).split("x")[1] if len(hex(val).split("x")[1]) == 2 else ("0" + hex(val).split("x")[1]))
    return(value)

class PIECE_SHAPES:
    #one size piece
    SMALL_SQUARE = [[0,0]]
    #two size piece
    TWO_BAR = [[0,0],[1,0]]
    #three size pieces
    SMALL_CORNER = [[0,0],[0,1],[1,0]]
    THREE_BAR = [[0,0],[-1,0],[1,0]]
    #four Size Pieces
    SQUARE = [[0,0],[1,0],[1,1],[0,1]]
    FOUR_BAR = [[0,0],[-1,0],[1,0],[2,0]]
    SMALL_L = [[0,0],[1,0],[0,1],[0,2]]
    HALF_PLUS = [[0,0],[1,0],[-1,0],[0,1]]
    SMALL_Z = [[0,0],[0,-1],[1,0],[-1,-1]]
    #Five size pieces
    LARGE_L = [[0,0],[-1,1],[-1,0],[1,0],[2,0]]
    LARGE_T = [[0,0],[-1,0],[1,0],[0,1],[0,2]]
    LARGE_CORNER = [[0,0],[0,1],[0,2],[1,0],[2,0]]
    OFFSET_Z = [[0,0],[0,-1],[-1,-1],[1,0],[2,0]]
    BIG_Z = [[0,0],[-1,0],[-1,-1],[1,0],[1,1]]
    FIVE_BAR = [[0,0],[-1,0],[-2,0],[1,0],[2,0]]
    TRAPEZOID = [[0,0],[0,1],[1,-1],[1,0],[0,-1]]
    DOUBLE_U = [[0,0],[0,1],[1,1],[-1,0],[-1,-1]]
    BIG_C = [[0,0],[1,0],[-1,0],[1,1],[-1,1]]
    CACTUS = [[0,0],[0,-1],[-1,0],[0,1],[1,1]]
    PLUS = [[0,0],[1,0],[-1,0],[0,1],[0,-1]]
    LOPSIDED_HALF_PLUS = [[0,0],[-1,0],[0,1],[1,0],[2,0]]

class Piece:
    def __init__(self, piece_shape):
        self.shape = piece_shape
    
    def rotateCC(self):
        for part in self.shape:
            tmpX = part[0]
            part[0] = part[1]
            part[1] = -tmpX
    def rotateCW(self):
        for part in self.shape:
            tmpX = part[0]
            part[0] = -part[1]
            part[1] = tmpX

    def flip(self):
        for part in self.shape:
            part[0] = -part[0]
    def flipV(self):
        for part in self.shape:
            part[1] = -part[1]


    def createCanvas(self, top, color):
        c = Canvas(top, width= 50, height=50)
        xOffset = 2
        yOffset = 2
        for part in self.shape:
            partlocation = [part[0] + xOffset, part[1]+ yOffset]
            c.create_rectangle((partlocation[0] * 10) + 1, (partlocation[1] * 10) + 1, (partlocation[0] * 10) + 11, (partlocation[1] * 10) + 11, fill=color)
        return c

class Player:
    def __init__(self, my_number, fake = False):
        self.numb = my_number
        self.color = [int(val) for val in open("config.txt", 'r').readlines()[self.numb].strip("\n").split(",")]
        self.pieces = [Piece(PIECE_SHAPES.SMALL_SQUARE),
                        Piece(PIECE_SHAPES.TWO_BAR),
                        Piece(PIECE_SHAPES.SMALL_CORNER),
                        Piece(PIECE_SHAPES.THREE_BAR),
                        Piece(PIECE_SHAPES.SQUARE),
                        Piece(PIECE_SHAPES.FOUR_BAR),
                        Piece(PIECE_SHAPES.SMALL_L),
                        Piece(PIECE_SHAPES.HALF_PLUS),
                        Piece(PIECE_SHAPES.SMALL_Z),
                        Piece(PIECE_SHAPES.LARGE_L),
                        Piece(PIECE_SHAPES.LARGE_T),
                        Piece(PIECE_SHAPES.LARGE_CORNER),
                        Piece(PIECE_SHAPES.OFFSET_Z),
                        Piece(PIECE_SHAPES.BIG_Z),
                        Piece(PIECE_SHAPES.FIVE_BAR),
                        Piece(PIECE_SHAPES.TRAPEZOID),
                        Piece(PIECE_SHAPES.DOUBLE_U),
                        Piece(PIECE_SHAPES.BIG_C),
                        Piece(PIECE_SHAPES.CACTUS),
                        Piece(PIECE_SHAPES.PLUS),
                        Piece(PIECE_SHAPES.LOPSIDED_HALF_PLUS)]
        self.blockused = False
        self.lastPlayed = Piece([])
    def __int__(self):
        return self.numb

class Board:
    def __init__(self):
        self.state = []
        for ii in range(0,20):
            self.state.append([])
            for jj in range(0,20):
                self.state[ii].append(0)

    def placePiece(self,location,piece, player):
        #returns false if the requested location is not valid for that piece
        #returns true and updates the game board if it is a valid play
        hasNeighbor = False
        for part in piece.shape:
            partLocation = [part[0] + location[0], part[1] + location[1]]
            
            #checks if the piece is on the board
            if not(partLocation[0] < len(self.state) and partLocation[0] >= 0 and partLocation[1] < len(self.state[0]) and partLocation[1] >= 0):
                return False
            
            #checks if there is already a piece at in the location
            if self.state[partLocation[0]][partLocation[1]] != 0:
                return False
            
            #checks for if there is a piece of it's color already adjacent to the piece
            if partLocation[0] < len(self.state) - 1:
                if self.state[partLocation[0] + 1][partLocation[1]] == player:
                    return False
            
            if partLocation[0] > 0:
                if self.state[partLocation[0] -1][partLocation[1]] == player:
                    return False
            
            if partLocation[1] < len(self.state[0]) - 1:
                if self.state[partLocation[0]][partLocation[1] + 1] == player:
                    return False
            
            if partLocation[1] > 0:
                if self.state[partLocation[0]][partLocation[1] - 1] == player:
                    return False
            
            #checks for pieces of the same color diagonally adjacent to the piece
            if partLocation[0] < len(self.state) - 1 and partLocation[1] < len(self.state[0]) - 1:
                if self.state[partLocation[0] + 1][partLocation[1] + 1] == player:
                    hasNeighbor = True
            
            if partLocation[0] < len(self.state) - 1 and partLocation[1] > 0:
                if self.state[partLocation[0] + 1][partLocation[1] - 1] == player:
                    hasNeighbor = True
            
            if partLocation[0] > 0 and partLocation[1] < len(self.state[0]) - 1:
                if self.state[partLocation[0] - 1][partLocation[1] + 1] == player:
                    hasNeighbor = True
            
            if partLocation[0] > 0 and partLocation[1] > 0:
                if self.state[partLocation[0] - 1][partLocation[1] - 1] == player:
                    hasNeighbor = True
            
        
        if hasNeighbor:
            for part in piece.shape:
                partLocation = [part[0] + location[0], part[1] + location[1]]
                self.state[partLocation[0]][partLocation[1]] = player
            return True
        else:
            return False

    def placeFirstPiece(self,location, piece, player):
        #same as the check for the place piece, but modifying the check for neighbors to checking if it is in a corner, also returns false if it is not a valid move, returns true if successful
        hasNeighbor = False
        for part in piece.shape:
            partLocation = [part[0] + location[0], part[1] + location[1]]
            #checks if the piece is on the board
            if not(partLocation[0] < len(self.state) and partLocation[0] >= 0 and partLocation[1] < len(self.state[0]) and partLocation[1] >= 0):
                return False
            #checks if the piece is in a corner
            if partLocation[0] == len(self.state) - 1 and partLocation[1] == len(self.state[0]) - 1:
                hasNeighbor = True
            if partLocation[0] == len(self.state) - 1 and partLocation[1] == 0:
                hasNeighbor = True
            if partLocation[0] == 0 and partLocation[1] == len(self.state[0]) - 1:
                hasNeighbor = True
            if partLocation[0] == 0 and partLocation[1] == 0:
                hasNeighbor = True
        if hasNeighbor:
            for part in piece.shape:
                partLocation = [part[0] + location[0], part[1] + location[1]]
                self.state[partLocation[0]][partLocation[1]] = player
            return True
        else:
            return False



def main(numOfPlayers):
    


    
    pygame.init()
    clock = pygame.time.Clock()
    mousePos = [0,0]
    
    players = []
    playerIndicators = []

    #sets up an array for the canvases for peices 
    pieceCanvases = []
    #sets up tkinter windows for player indicators
    for ii in range(numOfPlayers):
        if ii == 0:
            playerIndicators.append(Tk())
        else:
            playerIndicators.append(Toplevel())
        
        playerIndicators[ii].title("Player %d\'s pieces" % (ii + 1))
    #creates the actual player objects
        players.append(Player(ii + 1))
    
    for c in pieceCanvases:
        c.destroy()
    pieceCanvases = []
    #tkinter drawing stuff
    for ii in range(len(playerIndicators)):
        for piece in players[ii].pieces:
            pieceCanvases.append(piece.createCanvas(playerIndicators[ii], convertToHexRGB(players[ii].color)))
    for c in pieceCanvases:
        c.pack(side = LEFT)
        
    board = Board()
    windowWidth = 600
    windowHight = 400
    screen = pygame.display.set_mode((windowWidth, windowHight), pygame.RESIZABLE)
    currentPlayerIndex = 0
    currentPieceIndex = 0
    currentGridSpace = [0, 0]
    gameOver = False
    
    def set_Piece_Index(event):
        global currentPieceIndex
        #currentPieceIndex = int(c.gettags())
        print("doing a thing")
        

    while pygame.get_init() and (not gameOver):
        
        
        #limeting the framerate
        clock.tick(60)
        
        #checking for game ending conditions
        #all players have declared blockus
        count = 0
        while players[currentPlayerIndex].blockused:
            count += 1
            currentPlayerIndex += 1
            currentPlayerIndex = currentPlayerIndex % numOfPlayers
            if count >= numOfPlayers:
                gameOver = True
                break
        #checks if a player has run out of pieces
        if len(players[currentPlayerIndex].pieces) == 0:
            gameOver = True
        if gameOver:
            pygame.display.set_caption("Blockus -- Game over")
            continue
        
        
        currentPieceIndex = currentPieceIndex % len(players[currentPlayerIndex].pieces)
        currentPiece = players[currentPlayerIndex].pieces[currentPieceIndex]
        pygame.display.set_caption("Blockus -- Player %d's turn" % (players[currentPlayerIndex].numb))
        
        
        #pygame drawing on main screen
        #draws gameboard
        padding = int(abs(windowWidth - windowHight)/2)
        screen.fill((255,0,0))
        gridSize = int(windowWidth/20 if windowWidth < windowHight else windowHight/20)
        for ii in range(len(board.state)):
                for jj in range(len(board.state[1])):
                    pygame.draw.rect(screen, (255,255,255) if board.state[ii][jj] == 0 else ([player.color for player in players][board.state[ii][jj] - 1]), (ii*gridSize + (padding if windowWidth > windowHight else 0), jj*gridSize + (padding if windowWidth < windowHight else 0), gridSize, gridSize))
        
        #draws where the current piece is being held
        if mousePos[0] < 20*gridSize + (padding if windowWidth > windowHight else 0) and mousePos[0] > (padding if windowWidth > windowHight else 0) and mousePos[1] < 20*gridSize + (padding if windowWidth < windowHight else 0) and mousePos[1] > (padding if windowWidth < windowHight else 0):
            currentGridSpace = [int(floor((mousePos[0] - (padding if windowWidth > windowHight else 0)) / gridSize)), int(floor((mousePos[1] - (padding if windowWidth < windowHight else 0)) / gridSize))]
            
            partSize = int(0.5 * gridSize) if (gridSize - int(0.5 * gridSize)) % 2 == 0 else int(0.5 * gridSize) + 1
            partBuffer = int((gridSize - partSize) / 2)
            for part in currentPiece.shape:
                partLocation = [currentGridSpace[0] + part[0], currentGridSpace[1] + part[1]]
                if partLocation[0] >= 0 and partLocation[1] >= 0 and partLocation[0] < len(board.state) and partLocation[1] < len(board.state[0]):
                    xLocation = int((partLocation[0] * partSize) + ((partLocation[0] * 2) + 1) * partBuffer + (padding if windowWidth > windowHight else 0))
                    yLocation = int((partLocation[1] * partSize) + ((partLocation[1] * 2) + 1) * partBuffer + (padding if windowWidth < windowHight else 0))
                    rect = Rect(xLocation, yLocation, partSize, partSize)
                    color = pygame.Color(players[currentPlayerIndex].color[0],players[currentPlayerIndex].color[1],players[currentPlayerIndex].color[2] , 10)
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, (0,0,0,), rect, 1)
        
        #draws the gridlines on the board
        for ii in range(len(board.state) + 1):
            pygame.draw.line(screen, (0,0,0), (0 + (padding if windowWidth > windowHight else 0), ii * gridSize + (padding if windowWidth < windowHight else 0)), (20*gridSize + (padding if windowWidth > windowHight else 0), ii * gridSize + (padding if windowWidth < windowHight else 0)))
            pygame.draw.line(screen, (0,0,0), (ii * gridSize + (padding if windowWidth > windowHight else 0), 0 + (padding if windowWidth < windowHight else 0)), (ii * gridSize + (padding if windowWidth > windowHight else 0), 20*gridSize + (padding if windowWidth < windowHight else 0)))
        
        #actually updates the screen
        pygame.display.flip()
        
        #if pygame window is focused bring the tkinter windows to the front
        for indicator in playerIndicators:
            indicator.attributes("-topmost", pygame.mouse.get_focused())
        
        
        
        #updates tkinter stuff
        playerIndicators[0].update_idletasks()
        playerIndicators[0].update()
        
        
        #game logic stuff
        for event in pygame.event.get():
            #exits the program if when the program is closed
            if event.type == QUIT:
                pygame.quit()
                break
            
            #gets the mouse position and assigns it to a variable
            elif event.type == 4:
                mousePos = [event.pos[0], event.pos[1]]
            
            #resizes the gameboard to fit the window when the window is resized
            elif event.type == VIDEORESIZE:
                windowHight = event.h
                windowWidth = event.w
                screen = pygame.display.set_mode((windowWidth, windowHight), pygame.RESIZABLE)
            
            elif event.type == 5:
                #changes the currently selected piece when the scroll wheel is turned
                if event.button == 4:
                    currentPieceIndex += 1
                    currentPieceIndex = currentPieceIndex % len(players[currentPlayerIndex].pieces)
                elif event.button == 5:
                    currentPieceIndex -= 1
                    currentPieceIndex = currentPieceIndex % len(players[currentPlayerIndex].pieces)
                
                #tries to place the current piece when the left mouse button is pressed
                elif event.button == 1:
                    if len(players[currentPlayerIndex].pieces) == 21:
                        if board.placeFirstPiece(currentGridSpace, currentPiece, players[currentPlayerIndex].numb):
                            players[currentPlayerIndex].lastPlayed = currentPiece
                            players[currentPlayerIndex].pieces.remove(currentPiece)
                            currentPlayerIndex += 1
                            currentPlayerIndex = currentPlayerIndex % numOfPlayers
                            for c in pieceCanvases:
                                c.destroy()
                            pieceCanvases = []
                            #tkinter drawing stuff
                            for ii in range(len(playerIndicators)):
                                for piece in players[ii].pieces:
                                    pieceCanvases.append(piece.createCanvas(playerIndicators[ii], convertToHexRGB(players[ii].color)))
                                    pieceCanvases[ii].addtag_all("%d" % (ii))
                                    pieceCanvases[ii].bind("<Button>", set_Piece_Index(event))
                            for c in pieceCanvases:
                                c.pack(side = LEFT)
                    else:
                        if board.placePiece(currentGridSpace, currentPiece, players[currentPlayerIndex].numb):
                            players[currentPlayerIndex].lastPlayed = currentPiece
                            players[currentPlayerIndex].pieces.remove(currentPiece)
                            currentPlayerIndex += 1
                            currentPlayerIndex = currentPlayerIndex % numOfPlayers
                        for c in pieceCanvases:
                            c.destroy()
                        pieceCanvases = []
                        #tkinter drawing stuff
                        for ii in range(len(playerIndicators)):
                            for piece in players[ii].pieces:
                                pieceCanvases.append(piece.createCanvas(playerIndicators[ii], convertToHexRGB(players[ii].color)))
                                pieceCanvases[ii].addtag_all("%d" % (ii))
                                pieceCanvases[ii].bind("<Button>", set_Piece_Index(event))
                        for c in pieceCanvases:
                            c.pack(side = LEFT)
            
            elif event.type == 2:
                #rotates the piece when the r key is pressed
                if pygame.key.get_pressed()[K_LSHIFT] or pygame.key.get_pressed()[K_RSHIFT]:
                    
                    if event.key == K_r:
                        currentPiece.rotateCW()
                    elif event.key == K_f:
                        currentPiece.flipV()
                    elif event.key == K_b:
                        players[currentPlayerIndex].blockused = True
                else:
                    if event.key == K_r:
                        currentPiece.rotateCC()
                    elif event.key == K_f:
                        currentPiece.flip()
                    elif event.key == K_b:
                        players[currentPlayerIndex].blockused = True
    
    #end screen if the board if the game was ended without closing the program
    if pygame.get_init():
        playerOrder = []
        for ii in range(numOfPlayers):
            bestScore = 10000000
            bestPlayer = -1
            for jj in range(len(players)):
                totalScore = 0
                for piece in players[jj].pieces:
                    for part in piece.shape:
                        totalScore += 1
                
                if totalScore == bestScore:
                    if sum([1 for part in players[jj].lastPlayed.shape]) <= sum([1 for part in bestPlayer.lastPlayed.shape]):
                        bestPlayer = players[jj]
                elif totalScore < bestScore:
                    bestPlayer = players[jj]
                    bestScore = totalScore
            if bestPlayer in players:
                players.remove(bestPlayer)
            playerOrder.append([bestPlayer, bestScore])
        playerOrder = [player for player in playerOrder if type(player[0]) != int]  
        screen.fill((0,0,0))
        font = pygame.font.Font('freesansbold.ttf', 26)
        places = ["1st","2nd","3rd","4th"]
        textLines = []
        textRects = []
        for ii in range(len(playerOrder)):
            print(playerOrder[ii][0].color)
            textLines.append(font.render("%s: player %d with %d squares remaining" %(places[ii],playerOrder[ii][0].numb, playerOrder[ii][1]), True, playerOrder[ii][0].color))
            textRects.append(textLines[ii].get_rect())
            textRects[ii].center = (int(windowWidth / 2), int(windowHight / 8) + 32 * ii)
        
        while pygame.get_init():
            for ii in range(len(textLines)):
                screen.blit(textLines[ii], textRects[ii])
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == VIDEORESIZE:
                    windowHight = event.h
                    windowWidth = event.w
                    screen = pygame.display.set_mode((windowWidth, windowHight), pygame.RESIZABLE)


if __name__ == "__main__":
    main(4)