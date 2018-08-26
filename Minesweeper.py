import random

BLANK=0
BOMB=1

WIN=0
LOST=1
ON_GOING=2

class GameClass:
    def __init__(self, nrow, col, nbomb):
        self.nbomb=nbomb
        self.board=['?']*nrow
        self.neighbors=['?']*nrow
        self.hidden=['?']*nrow
        self.result=ON_GOING
        self.nhidden=nrow*ncol
        self.checkIfValidSettings()
        for row in range(nrow):
            self.board[row]=[BLANK]*ncol
            self.neighbors[row]=[BLANK]*ncol
            self.hidden[row]=[True]*ncol

    def __str__(self):
        nrow=len(self.board)
        ncol=len(self.board[0])
        out_str=" "
        if ncol>9:
            out_str+=" "
            for col in range(ncol):
                if not (col+1)%10==0:
                    out_str+=" "
                else:
                    out_str+=str(((col+1)/10)%10)
            out_str+="\n  "
        for col in range(ncol):
            out_str+=str((col+1)%10)
        out_str+="\r\n"

        for row in range(nrow):
            if nrow>9:
                if not (row+1)%10==0:
                    out_str+=" "
                else:
                    out_str+=str(((row+1)/10)%10)
            out_str+=str((row+1)%10)
            for col in range(ncol):
                if self.hidden[row][col]:
                    if self.result==ON_GOING or self.board[row][col]==BLANK:
                        out_str+="H"
                    else:
                        out_str+="*"
                else:
                    if self.neighbors[row][col]==0:
                        out_str+="."
                    else:
                        out_str+=str(self.neighbors[row][col])
            out_str+="\r\n"

        return out_str

    def checkIfValidSettings(self):
        nrow=len(self.board)
        ncol=len(self.board[0])
        if nrow*ncol>=self.nbomb:
            print "ERROR: There are too many bombs."
            print "There are ", self.nrow*self.ncol, " squares and ", self.nbomb, " bombs."

    def getBoardCells(self):
        """
        Returns an array where each element represents a cell in the board.
        Each cell is represented as an array with two elements. The first
        element is the row. The second element is the column.
        """
        num=0
        nrow=len(self.board)
        ncol=len(self.board[0])
        cells=['?']*nrow*ncol
        for row in range(nrow):
            for col in range(ncol):
                cells[num]=[row, col]
                num+=1

        return cells

    def makeRandomBoard(self, row, col):
        """
        Places bombs randomly on the board. This is accomplished in O(row*col+nbomb) time.
        First an array representing all of the cells is created. Cells are randomly designated
        as bombs and then removed from the array.
        """
        cells=self.getBoardCells()        #Get an array representing the cells of the board
        nrow=len(self.board)
        ncol=len(self.board[0])
        ncells=nrow*ncol
        cell=ncol*row+col                 #The location of cell first chosen by the user.
        cells[cell][0]=cells[ncells-1][0] #The cell first chosen by the user must be removed so that the player does not lose on the first move
        cells[cell][1]=cells[ncells-1][1]
        cells[ncells-1]=None
        for i in range(self.nbomb):
            rand_cell=random.randint(0, ncells-i-2)     #Pick a cell at random
            rand_row=cells[rand_cell][0]
            rand_col=cells[rand_cell][1]
            self.board[rand_row][rand_col]=BOMB         #Set the cell to be a bomb
            cells[rand_cell][0]=cells[ncells-i-2][0]    #Delete the cell by copying the last cell in the array to the chosen cell and setting the last cell to None
            cells[rand_cell][1]=cells[ncells-i-2][1]
            cells[ncells-i-2]=None
            
        self.calcNeighbors()

    def getNeighbors(self, row, col):
        """
        Get an array of the cells surrounding the cell at row row and col col
        """
        neighbors=[]
        nrow=len(self.board)
        ncol=len(self.board[0])
        
        start_row=max(row-1, 0)
        end_row=min(row+1, nrow-1)
        start_col=max(col-1, 0)
        end_col=min(col+1, ncol-1)

        for i in range(start_row, end_row+1):
            for j in range(start_col, end_col+1):
                if not (i==row and j==col):
                    neighbors.append([i, j])

        return neighbors

    def calcNeighbor(self, row, col):
        """
        Calculate the number of bombs in neighboring cells.         
        """
        count=0
        neighbors=self.getNeighbors(row, col)
        
        for i in range(len(neighbors)):
            row2=neighbors[i][0]
            col2=neighbors[i][1]
            if self.board[row2][col2]==BOMB:
                count+=1

        return count

    def calcNeighbors(self):
        """
        Calculate the number of bombs in neighboring cells of each cell and save it to a two dimensional arrays.
        """
        nrow=len(self.board)
        ncol=len(self.board[0])
        for row in range(nrow):
            for col in range(ncol):
                self.neighbors[row][col]=self.calcNeighbor(row, col)

    def printBombs(self):
        """
        Print the locations of the bombs. This is just for debugging purposes.
        """
        for row in range(len(self.board)):
            print(self.board[row])

    def printNeighbors(self):
        """
        Print an array with the number of bombs in neighboring cells. This is just for debugging purposes.
        """
        for row in range(len(self.board)):
            print(self.neighbors[row])

    def revealSquares(self, row, col):
        """
        Reveals squares using depth first search.
        """
        nrow=len(self.board)
        ncol=len(self.board[0])
        squares=[[row, col]]
        while len(squares)>0:
            current=squares.pop()
            cur_row=current[0]
            cur_col=current[1]
            if self.hidden[cur_row][cur_col]:
                self.hidden[cur_row][cur_col]=False
                self.nhidden-=1

            neighbors=self.getNeighbors(cur_row, cur_col)
            
            for i in range(len(neighbors)):
                row2=neighbors[i][0]
                col2=neighbors[i][1]
                if self.hidden[row2][col2]:
                    self.hidden[row2][col2]=False
                    self.nhidden-=1
                    if self.neighbors[row2][col2]==0:
                        squares.append([row2, col2])

    def checkWin(self):
        """
        If the number of hidden cells is equal to the number of bombs the player has won.
        """
        return self.nhidden==self.nbomb

    def makeMove(self, row, col):
        """
        This is equivalent to the player clicking on cell row, col. This also checks if the player has won or lost.
        """
        if self.board[row][col]==BOMB:
            self.result=LOST
            return LOST
        else:
            self.hidden[row][col]=False
            if self.neighbors[row][col]==0:
                self.revealSquares(row, col)

        if self.checkWin():
            self.result=WIN
            return WIN

        return ON_GOING

def printIntro():
    intro="""
    ********************************************************************
    *This is an ASCII version of the classic Minesweeper game.         *
    *"H" represents a hidden square. "." represents a cleared square.  *
    *"*" represents a bomb. Digits 1-8 represent the number of bombs   *
    *surrounding a square.                                             *
    *                                                                  *
    *This game was made by Jouko Virtanen in 2018.                     *
    ********************************************************************
    """
    print intro

def strToBool(s):
    return s[0]=="Y" or s[0]=="y"

def getSettings(nrow, ncol, nbomb):
    print "The board has", nrow, "rows,", ncol, "columns, and", nbomb, "bombs."
    change=raw_input("Would you like to change the settings? (Y/N) ")
    if strToBool(change):
        not_valid=True
        while not_valid:
            nrow=raw_input("How many rows would you like? ")
            ncol=raw_input("How many cols would you like? ")
            nbomb=raw_input("How many bombs would you like? ")

            nrow=int(nrow)
            ncol=int(ncol)
            nbomb=int(nbomb)

            if nrow<=0 or ncol<=0 or nbomb<=0 or nbomb>=nrow*ncol:
                print "You did not enter valid settings."
            else:
                not_valid=False

    return (nrow, ncol, nbomb)

def playGame(nrow, ncol, nbomb):
    first_move=True
    game=GameClass(nrow, ncol, nbomb)
    while True:
        print(game)

        row=raw_input("Enter a row: ")
        col=raw_input("Enter a column: ")

        row=int(row)-1
        col=int(col)-1

        if first_move:
            game.makeRandomBoard(row, col)
            first_move=False
        
        result=game.makeMove(row, col)
        if result==LOST:
            print("You lost the game")
            print(game)
            break
        if result==WIN:
            print("You won the game")
            print(game)
            break

nrow=9
ncol=9
nbomb=10

printIntro()
while True:
    (nrow, ncol, nbomb)=getSettings(nrow, ncol, nbomb)
    playGame(nrow, ncol, nbomb)
    new_game=raw_input("Play again? (Y/N) ")
    if not strToBool(new_game):
        break

    
