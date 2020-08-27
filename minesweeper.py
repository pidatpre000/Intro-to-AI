import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
  
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        mines= set()
        for cell in self.cells:
            if cell in self.mines:
                mines.add(cell)
        return mines

        raise NotImplementedError

    def known_safes(self):
        mines= set()
        for cell in self.cells:
            if cell in self.safes:
                mines.add(cell)
        return mines
        raise NotImplementedError

    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
        #implement represents a logically correct sentence given that cell is known to be safe.
        

    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
        #implement sentence logic
       


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
 
    def safe_cells(self,cells,count):
        safe_cells=set()
        print ("cells passed to safe cells: ", cells)
        localcells= copy.deepcopy(cells)
        if count==0:
            for cell in localcells:
                self.mark_safe(cell)
                print ("marking safe: ", cell)
        return safe_cells
 
    def mine_cells(self,cells,count):
        mine_cells=set()
        print ("cells passed to mine cells: ", cells)
        localcells= copy.deepcopy(cells)
       
        print ("length of cells and count", len(cells), count)
        if len(cells)==count:
            for cell in localcells:
                self.mark_mine(cell)
        return mine_cells
           
    def inferences(self):
        for each in range(len(self.knowledge)):
            cells = self.knowledge[each].cells
            for ind in range(each):
                other = self.knowledge[ind].cells        
                if ((len(cells) is not 0) and (len(other) is not 0) and (sorted(cells) != sorted(other))): 
                    if cells.issubset(other):
                        self.knowledge.append(Sentence(other-cells, self.knowledge[ind].count-self.knowledge[each].count))
                        self.info()
                    elif other.issubset(cells):
                        self.knowledge.append(Sentence(cells-other, self.knowledge[each].count-self.knowledge[ind].count))
                        self.info()


    def neighbors(self,cell):
        (i, j)= cell
        neighbors= set()
        for x in range (2):

            if i-x >= 0:
                #left cell
                neighbors.add((i-x,j))
                if j-x >= 0:
                    #top left diagonal
                    neighbors.add((i-x,j-x))
                if j+x < self.height:
                    #bottom left diagonal
                    neighbors.add((i-x,j+x))
            if i+x < self.height:
                #right cell
                neighbors.add((i+x,j))
                if j-x >= 0:
                    #top right diagonal
                    neighbors.add((i+x,j-x))
                if j+x < self.width:
                    #bottom right diagonal
                    neighbors.add((i+x,j+x))
            if j-x >= 0:
                #top cell
                neighbors.add((i,j-x))
            if j+x < self.width:
                #bottom cell
                neighbors.add((i,j+x))
                            
        neighbors.remove(cell)
        known=set()
        for cell in neighbors:
            if cell in self.mines or cell in self.safes:
                known.add(cell)
        return neighbors-known

    def info(self):
        for sentence in self.knowledge:
            safecells= self.safe_cells(sentence.cells,sentence.count)
            minecells= self.mine_cells(sentence.cells,sentence.count)
            for xcell in safecells:
                self.mark_safe(xcell)
                
            for xcell in minecells:
                self.mark_mine(xcell)
                print ("marking as mine: ", xcell)
        
            

             

    def add_knowledge(self, cell, count):
        self.moves_made.add(cell)
        self.mark_safe(cell)
        self.knowledge.append(Sentence(self.neighbors(cell),count))
        self.inferences()
        self.info()
        

    def make_safe_move(self):
        moves= []
        for cell in self.safes:
            if cell not in self.moves_made:
                moves.append(cell)

        if len(moves) == 0:
            return None 
        else:
            move= random.choice(moves)
            print ("safe move: ", move)
            return move
        

    def make_random_move(self):
        for x in range(8):
            for y in range(8):
                move=(x, y)
                if move not in self.mines and move not in self.moves_made:
                    print ("random move: ", move)
                    return move
        return None


