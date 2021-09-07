from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import random
                                                                        #STARTING NOTES:
                            # YOU NEED TO PRESS THE MINES TO GET THE RED LIGHT IN ORDER TO START A NEW GAME

spriteBomb = QImage("./minesweepgraphics/mine.jpeg")
spriteFlag = QImage("./minesweepgraphics/redFlag.jpeg")
spriteStart = QImage("./minesweepgraphics/startImage.jpg")

spriteBegin= "./minesweepgraphics/Topbegin.jpeg"
spriteIngame= "./minesweepgraphics/Topingame.jpg"
spriteEndgame= "./minesweepgraphics/Topend.jpg"


gameColors = {
    
    1: QColor('#da0020'),2: QColor('#703500'),3: QColor('#dec829'), #ROY
    4: QColor('#1ee116'),                                           #G
    5: QColor('#315ee1'),6: QColor('#310e2d'),7: QColor('#c238b1'), #BIV

              }
# -------------------------------------------------------------------------------------------------------------- Game Interface class --------------#
class gameInterface(QMainWindow):
    # -------------------------------------------------------------------------------------------------------------- Initialization ----------------#
                                # Class for Designing the Game Interface
                                # Initialization of Class variables first
    def __init__(self):
        super(gameInterface, self).__init__()   # Creation of Super Class for easy reference throughout file

        self.board = 10         # Intialize both the board and bomb size by the 10x10 grid
        self.bombsNum = 10

        self.bombs = QLabel()                                   # Create label contained in bombs
        self.bombs.setAlignment(Qt.AlignHCenter | Qt.AlignLeft) # Align on GUI

        gameFont = self.bombs.font()             # Create a new variable mineFont made for storing the font of widget                                       
        gameFont.setPointSize(50)                # Set fixed size and weight for use on GUI   
        gameFont.setWeight(50)
       
        self.bombs.setFont(gameFont)             # Display towards top of screen
        self.bombs.setText("MINESWEEPER")

        self.button = QPushButton()              # Creation of button
        self.button.setIcon(QIcon(spriteIngame)) # Interactive button icon set to green light icon    
        self.button.setFixedSize(QSize(50, 50))  # Fix size and weight of Icon
        self.button.setIconSize(QSize(50, 50))
        self.button.setFlat(True)                # button does not have a frame designed for it, so we make it flat
        self.button.clicked.connect(self.processStat)           # Connect this button to always refresh our current status

        self.gameBoard = QGridLayout()           # The game board follows a grid layout
        self.gameBoard.setSpacing(3)             # Leave some spacing in between tiles for clean design
   

        interfaceWidget = QWidget()              # Create widget for our grid interface encompassing game items
        interfaceBox = QHBoxLayout()             # Create encompassing horizontal box to contain our bombs and button widget
        interfaceLabel = QLabel()                # interactive label created to correspond to our buttons made
        gameBox = QVBoxLayout()                  # gameBox creates a vertical box designed to encompass our bomb & button widget                    

        interfaceLabel.setAlignment(Qt.AlignRight | Qt.AlignLeft)
        interfaceBox.addWidget(interfaceLabel)      # Add Label and button widgets
        interfaceBox.addWidget(interfaceLabel)      # Align label on GUI as well (above)
        interfaceBox.addWidget(self.bombs)
        interfaceBox.addWidget(self.button)
        interfaceBox.addWidget(interfaceLabel)

        
        gameBox.addLayout(interfaceBox)         # Add interface to vertical box layout
        gameBox.addLayout(self.gameBoard)       # Add board of game as well
        
        interfaceWidget.setLayout(gameBox)
        self.setCentralWidget(interfaceWidget)  # Assign interface to widget

        self.drawBoard()                        # Grid System initalized here
        self.refreshStat(spriteBegin)           # Status refresh

        self.clearBoard()                       # Clear board and initialize individual game components
        self.refreshStat(spriteBegin)           # Status refresh again

        self.show()                             # Display Game
    # ----------------------------------------------------------------------------------------------------------------------------------------------#      
    #
    # -------------------------------------------------------------------------------------------------------------- Game Indicators----------------#
    #
    ## ---------------------------------------- Process Status --------------------------- ##
    def processStat(self):
        if self.status == spriteIngame:         # Check if currently in game, if so, set Status to In game
            self.refreshStat(spriteEndgame)
            self.display()                      

        elif self.status == spriteEndgame:      # Else check if the game has ended, if so, clear Board and initialize new game
            self.refreshStat(spriteBegin)
            self.clearBoard()
    ## ----------------------------------------------------------------------------------- ##        
    #
    ## ------------------------------------------- Start Game ---------------------------- ##
    def start(self):                            # Refresh Status to start icon
        if self.status != spriteIngame:
            self.refreshStat(spriteIngame)
    ## ----------------------------------------------------------------------------------- ##        
    #
    ## ---------------------------------------- Refresh Status --------------------------- ##
    def refreshStat(self, status):              # reassigns provided status to class var, button assigns correct icon
        self.status = status
        self.button.setIcon(QIcon(self.status))
    ## ----------------------------------------------------------------------------------- ##    
    #
    ## ---------------------------------------- End Game --------------------------------- ##
    def endGame(self):
        self.display()                          # Display entirety of map
        self.refreshStat(spriteEndgame)         # Refresh the status to current (lost)
    ## ----------------------------------------------------------------------------------- ##    
    #
    ## ---------------------------------------- Locate Bombs ----------------------------- ##
    def findBombs(self, i, j):
        bombSpots = []                          # Store our spots in growing array

        for ii in range(max(0, i - 1), min(i + 2, self.board)):     # For Indexes in board
            for jj in range(max(0, j - 1), min(j + 2, self.board)): # Containing Bombs
                bombSpots.append(self.gameBoard.itemAtPosition(jj, ii).widget())
                                                # Append to arr and Return to function caller
        return bombSpots
    ## ----------------------------------------------------------------------------------- ##
    #
    # ----------------------------------------------------------------------------------------- Visual Element Functions ---------------------------#
    #
    ## ------------------------------------ Display the Map ------------------------------ ##
    def display(self):                          # Display the whole map
        for i in range(0, self.board):
            for j in range(0, self.board):
                interfaceWidget = self.gameBoard.itemAtPosition(j, i).widget()
                interfaceWidget.found()         # Display on Position ^ Update Status and show the tile
    ## ----------------------------------------------------------------------------------- ##
    #
    ## -------------------------------- Expand Display of Map----------------------------- ##
    def displayFurther(self, i, j):             # Expand board tiles (revealed)
        for ii in range(max(0, i - 1), min(i + 2, self.board)):
            for jj in range(max(0, j - 1), min(j + 2, self.board)):
                interfaceWidget = self.gameBoard.itemAtPosition(jj, ii).widget()
                if not interfaceWidget.minePos: # If position of interfaced (clicked) is not a mine
                    interfaceWidget.pressIn()   # Click and proceed throughout game
    ## ----------------------------------------------------------------------------------- ##
    #                                                                    
    ## ---------------------------- Initialize Game Functions and Buttons ---------------- ##
    def drawBoard(self):                        
        for i in range(0, self.board):
            for j in range(0, self.board):          # Initialize game functions for each tile
                interfaceWidget = gameTile(i, j, False, False, 0, False, False)
                self.gameBoard.addWidget(interfaceWidget, j, i)
                interfaceWidget.gbutton.connect(self.start)     # Assign buttons to widget for each tile
                interfaceWidget.tileReveal.connect(self.displayFurther)
                interfaceWidget.end.connect(self.endGame)
    ## ----------------------------------------------------------------------------------- ##
    #
    ## ------------------------------Clear All Board Tiles-------------------------------- ##            
    def clearBoard(self):           # function contains definition within
        for i in range(0, self.board):      # Clear tiles throughout map
            for j in range(0, self.board):
                interfaceWidget = self.gameBoard.itemAtPosition(j, i).widget()
                interfaceWidget.newTile()   # call newTile to refresh for each indice

        ## -----------------------(sub func) Locate and Append Bombs Nearby -------------- ##        
        bombSpots = []
        def addNear(i, j):          # Create locations adjacent to bombs
            bombSpots = self.findBombs(i, j)    # Return found bombs to bombSpot arr
            bombsNum = sum(1 if interfaceWidget.minePos     # 1 if location is mine else 0 for bombsNum var
                else 0 for interfaceWidget in bombSpots)

            return bombsNum         #return number of bombs to function caller

        while len(bombSpots) < self.bombsNum:   # Append bombs loop
            i = random.randint(0, self.board - 1)
            j = random.randint(0, self.board - 1)        
            if (i, j) not in bombSpots:         # If location through tiles is not a bomb
                interfaceWidget = self.gameBoard.itemAtPosition(j, i).widget()
                interfaceWidget.minePos = True  # Make it a bomb
                bombSpots.append((i, j))        # Append bomb to list


        for i in range(0, self.board):          # After appending bombs, we can find locations adjacent
            for j in range(0, self.board):      # to bombs. Traverse game board
                interfaceWidget = self.gameBoard.itemAtPosition(j, i).widget()
                interfaceWidget.adjNum = addNear(i, j)  

        while True:                             # Finally, check to make sure start pos is not bomb
            i = random.randint(0, self.board - 1) 
            j = random.randint(0, self.board - 1)
            interfaceWidget = self.gameBoard.itemAtPosition(j, i).widget()
                                                # Create Widget on item position
            
            if (i, j) not in bombSpots:         # If position is not on a bomb spot
                interfaceWidget = self.gameBoard.itemAtPosition(j, i).widget()
                interfaceWidget.startPos = True # It is valid to start on

                                                # Reveal nearby mines relative to start location
                for interfaceWidget in self.findBombs(i, j):    
                    if interfaceWidget.minePos == False:
                        interfaceWidget.pressIn()                                
                break
        ## ------------------------------------------------------------------------------- ##        
        ##
#
# -------------------------------------------------------------------------------------------------------------- Game Tile Class -------------------#
class gameTile(QWidget):                   
# -------------------------------------------------------------------------------------------------------------- Initialization --------------------#
               # Create a class for each instance of a tile of Minesweeper and logic
                # Variables initialized within super class for easy reference throughout
                 # definitions contained within gameTile class
    gbutton = pyqtSignal()
    end = pyqtSignal() 
    tileReveal = pyqtSignal(int, int)                        

    def __init__(self, rowPos, colPos, startPos, minePos, adjNum, shownStat, flagStat):
        super(gameTile, self).__init__()
                                        # we make this class as well as our interface class Super classes
                                        # for easy reference to self initialized vars,
                   

        self.setFixedSize(QSize(50, 50))    # Set Size of window to be static on each run 50 x 50 (setGeomtry, initially)

        self.rowPos = rowPos            # parameters initialized within class for reference
        self.colPos = colPos

        self.start = startPos
        self.minePos = minePos
        self.adjNum = adjNum

        self.shownStat = shownStat
        self.flagStat = flagStat

# ------------------------------------------------------------------------------------------------------ Inner game mechanics --------------------- #
#
    ## ----------------------------------------Flag Tiles--------------------------------- ##
    def flagTile(self):                 
        self.flagStat = True            # Flag tile and update. Emit this to pyqt signal gbutton var
        self.update()
        self.gbutton.emit()
    ## ---------------------------------------Display a Tile------------------------------ ##
    ##
    ## ----------------------------------------------------------------------------------- ##   
    def found(self):
        self.shownStat = True           # show tile and update. same process as above
        self.update()
        self.gbutton.emit()
    ## ----------------------------------------------------------------------------------- ##
    ##
    ## -------------------------------------Reset a Tile---------------------------------- ##
    def newTile(self):
        self.startPos = False           # intialize all parameter given class vars to False / 0 values
        self.minePos = False
        self.adjNum = 0

        self.shownStat = False
        self.flagStat = False
        self.update()                   # Update to reflect changes
    ## ----------------------------------------------------------------------------------- ##
    ##
    ## ----------------------------------User Press Functionality------------------------- ##
    def pressIn(self):                  # Button to traverse through game
        if self.shownStat == False:     #If not shown, reveal
            self.found()

            if self.adjNum == 0:        # Reveal tiles given no adjacent bombs
                self.tileReveal.emit(self.rowPos, self.colPos)

        self.gbutton.emit()             # emit to signal var
    ## ----------------------------------------------------------------------------------- ##
    ##
# -------------------------------------------------------------------------------------------------------PyQt Events------------------------------- # 
    ##          ** SPECIAL pyqt5 Events **  -    Mouse Release
    ## ----------------------------------------Mouse Release Event------------------------ ## 
                        
    def mouseReleaseEvent(self, event): # MOUSE RELEASE allows GUI to pick up mouse events
                                        # Created Widget releases events with this function

        if (event.button() == Qt.RightButton and (self.shownStat == False)):
            self.flagTile()             # Given the tile is not shown and right mouse is pressed, reveal flag

        elif (event.button() == Qt.LeftButton):
            self.pressIn()              # Given the tile is not shown and left mouse is pressed, reveal tile

            if self.minePos==True:      # If a mine exists on tile, GAME OVER
                self.end.emit()

    ## ----------------------------------------------------------------------------------- ##  
    ##          ** SPECIAL pyqt5 Events **  -    Paint game
    ## -----------------------------------------Paint Tiles Event------------------------- ##           
    
    def paintEvent(self, event):       # PAINT EVENT allows us to update our GUI whenever called   
                                       # Gives our Qpainter Items functionality to paint and repaint when supposed to
        
        gameCube = QPainter(self)                       # Create Q painter var                   
        gameCube.setRenderHint(QPainter.Antialiasing)   # Anti Alias text for cleaner Display
        gameEvent = event.rect()                        # Create rectangle for event and store in var           


        if self.shownStat == True:     # if tile is revealed    
            color = self.palette().color(QPalette.Background)   # Assign background color using QPalette.Background to local var
            outer, inner = color, color                     # inner and outer color utilize background 
        else:                   
            outer, inner = Qt.black, Qt.black               # when tile not shown, color is BLACK

        appendage = QPen(outer)        # pen between tiles assignment         
        appendage.setWidth(3)          # keep decent width per tile
        gameCube.fillRect(gameEvent, QBrush(inner))         # file qpainter Var with event and color
        gameCube.drawRect(gameEvent)   # assign gameEvent rectangle to qpainter gameCube
        gameCube.setPen(appendage)     # Assign pen spacing to gameCube for painting                                                      

        if self.shownStat == True:     # If Tile is revealed and it is the start
            if self.startPos == True:  # draw game Event rectangle and start icon
                gameCube.drawPixmap(gameEvent, QPixmap(spriteStart))

            elif self.minePos == True: # if Tile is mine, draw game Event rectangle and mine sprite
                gameCube.drawPixmap(gameEvent, QPixmap(spriteBomb))

            elif self.adjNum > 0:      # If there are adjacencies 
                
                gameFont = gameCube.font()  # Font serves as label for qpainter var

                appendage = QPen(gameColors[self.adjNum])   # appendage assigned gameColors
                gameCube.setPen(appendage)                  # colors change depending on # of bombs adjacent
                gameCube.setFont(gameFont)                  # to location
                gameCube.drawText(gameEvent, Qt.AlignHCenter | Qt.AlignVCenter, str(self.adjNum))
                                                                      # draw text and align                      
        elif self.flagStat == True:                         # if tile is flagged, display flag sprite
            gameCube.drawPixmap(gameEvent, QPixmap(spriteFlag))      

## -------------------------------------------------------------------------------------------- ## 
#
# -----------------------------------------------------------------------------------------------' Main ' of Program ------------------------------ #

app = QApplication([])       
window = gameInterface()         
window.show()
app.exec_()

# ------------------------------------------------------------------------------------------------------------------------------------------------- #

