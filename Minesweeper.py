from Tkinter import *
import tkFont

import random

BLANK=0
BOMB=1

WIN=0
LOST=1
ON_GOING=2

class MainApp(Tk):
    """
    The GUI
    """
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.settings_frame=Frame(self)
        self.game_frame=Frame(self)
        
        self.settings_frame.grid()
        self.game_frame.grid()

        self.nrow=9
        self.ncol=9
        self.nbomb=10

        self.game=GameClass(self.nrow, self.ncol, self.nbomb)

        self.nrowLabel=Label(self.settings_frame, text="Rows: ")
        self.nrowLabel.grid(column=0, row=0)

        self.nrowEntryVar=StringVar()
        self.nrowEntry=Entry(self.settings_frame, width=3, textvariable=self.nrowEntryVar)
        self.nrowEntry.grid(column=1, row=0)
        self.nrowEntryVar.set(str(self.nrow))


        self.ncolLabel=Label(self.settings_frame, text="Columns: ")
        self.ncolLabel.grid(column=2, row=0)

        self.ncolEntryVar=StringVar()
        self.ncolEntry=Entry(self.settings_frame, width=3, textvariable=self.ncolEntryVar)
        self.ncolEntry.grid(column=3, row=0)
        self.ncolEntryVar.set(str(self.ncol))


        self.nbombLabel=Label(self.settings_frame, text="Bombs : ")
        self.nbombLabel.grid(column=4, row=0)

        self.nbombEntryVar=StringVar()
        self.nbombEntry=Entry(self.settings_frame, width=3, textvariable=self.nbombEntryVar)
        self.nbombEntry.grid(column=5, row=0)
        self.nbombEntryVar.set(str(self.nbomb))

        action=lambda: self.newGame()
        self.newGameButton=Button(self.settings_frame, text="New Game", command=action)
        self.newGameButton.grid(column=6, row=0)

        self.createField()

    def destroyField(self):
        """
        Destroys the buttons representing the minefield as well as the text field displaying the result of the game.
        """
        button_rows=len(self.buttons)
        button_cols=len(self.buttons[0])
        for row in range(button_rows):
            for col in range(button_cols):
                self.buttons[row][col].destroy()

        self.gameStateLabel.destroy()

    def createField(self):
        """
        Creates the buttons representing the minefield as well as the text field displaying the result of the game.
        """
        self.buttons=[['?' for col in range(self.ncol)] for row in range(self.nrow)]
        self.btn_text=[['?' for col in range(self.ncol)] for row in range(self.nrow)]
        
        w=1
        for row in range(self.nrow):
            for col in range(self.ncol):
                self.btn_text[row][col]=StringVar()
                action=lambda x=row, y=col: self.onButtonClick(x, y)
                self.buttons[row][col]=Button(self.game_frame, textvariable=self.btn_text[row][col], width=w, command=action)
                self.buttons[row][col].grid(column=col, row=row)

        resultFont=tkFont.Font(family='Helvetica', size=18, weight='bold')

        self.gameStateLabelVar=StringVar()
        self.gameStateLabel=Label(self.game_frame, textvariable=self.gameStateLabelVar, font=resultFont)
        self.gameStateLabel.grid(column=0, row=self.nrow, columnspan=self.ncol)
        self.gameStateLabelVar.set("")
        

    def newGame(self):
        """
        Starts a new game. First checks if the settings are valid, then destroys the old game and then creates a new game.
        """
        tempRow=int(self.nrowEntryVar.get())
        tempCol=int(self.ncolEntryVar.get())
        tempBomb=int(self.nbombEntryVar.get())

        if checkIfValidGame(tempRow, tempCol, tempBomb):
            self.nrow=tempRow
            self.ncol=tempCol
            self.nbomb=tempBomb
            self.game=GameClass(self.nrow, self.ncol, self.nbomb)
            self.destroyField()
            self.createField()
            self.updateDisplay()
        else:
            self.gameStateLabelVar.set("INVALID\nSETTINGS!")

    def onButtonClick(self, row, col):
        """
        The minefield is represented by a grid of buttons. The game is played by pressing the buttons.
        """
        if self.game.nhidden==self.nrow*self.ncol: #Is this the first move
            self.game.makeRandomBoard(row, col)

        if self.game.result==ON_GOING:
            result=self.game.makeMove(row, col)
            self.updateDisplay()

        if result==LOST:
            self.gameStateLabelVar.set("YOU LOST!")
        if result==WIN:
            self.gameStateLabelVar.set("YOU WON!")

    def updateDisplay(self):
        """
        Updates the display of the minefield after a cell has been selected.
        """
        for row in range(self.nrow):
            for col in range(self.ncol):
                if self.game.hidden[row][col]:
                    if not (self.game.result==ON_GOING or self.game.board[row][col]==BLANK):
                        self.btn_text[row][col].set("*")
                    else:
                        self.btn_text[row][col].set(" ")
                else:
                    self.btn_text[row][col].set(str(self.game.neighbors[row][col]))

class GameClass:
    def __init__(self, nrow, ncol, nbomb):
        self.nbomb=nbomb
        self.board=['?']*nrow
        self.neighbors=['?']*nrow
        self.hidden=['?']*nrow
        self.result=ON_GOING
        self.nhidden=nrow*ncol
        for row in range(nrow):
            self.board[row]=[BLANK]*ncol
            self.neighbors[row]=[BLANK]*ncol
            self.hidden[row]=[True]*ncol

        self.checkIfValidSettings()

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
        if nrow*ncol<=self.nbomb:
            print "ERROR: There are too many bombs."
            print "There are", nrow, "rows and", ncol, "cols."
            print "There are", nrow*ncol, "squares and", self.nbomb, "bombs."
            return False

        if nrow<2 or ncol<2 or self.nbomb<2:
            print "ERROR: There must be at least two rows, columns, and bombs."
            print "There are", nrow, "rows,", ncol, "cols, and", nbomb, "bombs."
            return False

        return True

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
            if self.hidden[row][col]:
                self.nhidden-=1
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

def checkIfValidGame(nrow, ncol, nbomb):
    if nrow*ncol<=nbomb:
        print "ERROR: There are too many bombs."
        print "There are", nrow, "rows and", ncol, "cols."
        print "There are", nrow*ncol, "squares and", nbomb, "bombs."
        return False

    if nrow<2 or ncol<2 or nbomb<2:
        print "ERROR: There must be at least two rows, columns, and bombs."
        print "There are", nrow, "rows,", ncol, "cols, and", nbomb, "bombs."
        return False

    return True

if __name__=="__main__":
    app=MainApp()
    app.title('Minesweeper')
    app.geometry('300x450')
    app.mainloop()
    
