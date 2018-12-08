import queue
import random
import math
import sys

sys.setrecursionlimit(5000)

class Solver(object):

    def __init__(self, puzzleConfig, method):
        self.configArr = puzzleConfig.split(",")
        self.configArr = list(map(int, self.configArr))
        if not self.isSquare(len(self.configArr)):
            raise Exception ("The configuration is not a square")
        elif not self.isSolvable():
            raise Exception ("The configuration is not solvable")
        else:
            self.n = int(math.sqrt(len(self.configArr)))
            self.method = method
            self.path = []
            self.puzzle = [[0 for x in range(self.n)] for y in range(self.n)]
            k = 0
            for x in range(self.n):
                for y in range(self.n):
                    self.puzzle[x][y] = self.configArr[k]
                    k += 1
            self.rootState = PuzzleState(self.puzzle)
            self.rootState.showPuzzle()
            if method == "bfs":
                self.bfs_search(False)
            elif method == "dfs":
                self.dfs_search()
            elif method == "ast":
                self.ast_search()

    def isSquare(self, num):
        root = math.sqrt(num)
        if (int(root + 0.5) ** 2 == num):
            return True
        else:
            return False

    def isSolvable(self):
        inversions = 0
        arr = self.configArr.copy()
        arr.remove(0)
        for x in range(len(arr)):
            for y in range(x + 1, len(arr)):
                if arr[y] > arr[x]:
                    inversions += 1

        if inversions % 2 == 0:
            return True
        else:
            return False

    def bfs_search(self, ceroUp = True):

        initialState = self.rootState
        q = queue.Queue()
    
        #Save puzzle configurations
        visited = []
        q.put(initialState)

        while not q.empty():
            currentState = q.get()
            if currentState.isSolved(ceroUp):
                print("Solved")
                currentState.showPuzzle()
                self.getPath(currentState)
                return currentState
            else:
                visited.append(currentState.puzzle)
                #currentState.showPuzzle()
                children = currentState.expandNode()
                for c in children:
                    if c.puzzle not in visited:
                        q.put(c)
        return None

    def dfs_search(self, ceroUp = True):

        initialState = self.rootState
        q = queue.LifoQueue()

        visited = []
        q.put(initialState)
        while not q.empty():
            currentState = q.get()
            if currentState.isSolved(ceroUp):
                print("Solved")
                currentState.showPuzzle()
                self.getPath(currentState)
                return currentState
            else:
                visited.append(currentState.puzzle)
                children = currentState.expandNode()
                for c in children:
                    if c.puzzle not in visited:
                        q.put(c)

    def ast_search(self, ceroUp = True):
         
        initialState = self.rootState
        q = queue.PriorityQueue()

        visited = []
        q.put(0, initialState)
        while not q.empty():
            currentState = q.get()
            if currentState.isSolved(ceroUp):
                print("Solved")
                currentState.showPuzzle()
                self.getPath(currentState)
                return currentState
            else:
                visited.append(currentState.puzzle)
                children = currentState.expandNode()
                for c in children:
                    if c.puzzle not in visited:
                        q.put(c.missplacedPieces(ceroUp), c)

    def getPath(self, PuzzleState):
        self.path.append(PuzzleState.action)
        if PuzzleState.parent is not None:
            self.getPath(PuzzleState.parent)
        else:
            self.path.reverse()
            print(self.path)


class PuzzleState(object):

    def __init__(self, puzzle, parent=None, action="Initial", cost = 0, depth = 0):
        self.puzzle = puzzle
        self.parent = parent
        self.action = action
        self.cost = cost
        self.depth = depth
        self.children = [] #Array of other Puzzle States
        for x in range(len(self.puzzle)):
            for y in range(len(self.puzzle)):
                if self.puzzle[x][y] == 0:
                    self.blankRow = x
                    self.blankColumn = y
                    break
        self.n = len(self.puzzle)

    def missplacedPieces(self, ceroUp):
        puzzleArr = []
        for x in range(len(self.puzzle)):
            for y in range(len(self.puzzle)):
                puzzleArr.append(self.puzzle[x][y])
        solvedPuzzle = puzzleArr.copy()
        solvedPuzzle.sort()
        if ceroUp is False:
            solvedPuzzle.remove(0)
            solvedPuzzle.append(0)
        missplacedPieces = 0
        for x in range(len(puzzleArr)):
            if not puzzleArr[x] == solvedPuzzle[x]:
                missplacedPieces += 1
        return missplacedPieces

    
    def isSolved(self, ceroUp = True):
        puzzleArr = []
        for x in range(len(self.puzzle)):
            for y in range(len(self.puzzle)):
                puzzleArr.append(self.puzzle[x][y])
        solvedPuzzle = puzzleArr.copy()
        solvedPuzzle.sort()
        if ceroUp is False:
            solvedPuzzle.remove(0)
            solvedPuzzle.append(0)
        if solvedPuzzle == puzzleArr:
            return True
        else:
            return False

    def showPuzzle(self):
        for x in range(len(self.puzzle)):
            for y in range(len(self.puzzle)):
                print("{:<4}".format(self.puzzle[x][y]), end="")
            print()
        print("--------------")

    def moveLeft(self):
        if self.blankColumn == 0:
            return None
        else:
            newPuzzleState = [row[:] for row in self.puzzle]
            value = newPuzzleState[self.blankRow][self.blankColumn - 1]
            newPuzzleState[self.blankRow][self.blankColumn - 1] = 0
            newPuzzleState[self.blankRow][self.blankColumn] = value
            return PuzzleState(newPuzzleState, self, "Left", self.cost + 1, self.depth + 1)

    def moveRight(self):
        if self.blankColumn == self.n - 1:
            return None
        else:
            newPuzzleState = [row[:] for row in self.puzzle]
            value = newPuzzleState[self.blankRow][self.blankColumn + 1]
            newPuzzleState[self.blankRow][self.blankColumn + 1] = 0
            newPuzzleState[self.blankRow][self.blankColumn] = value
            return PuzzleState(newPuzzleState, self, "Right", self.cost + 1, self.depth + 1)
    
    def moveUp(self):
        if self.blankRow == 0:
            return None
        else:
            newPuzzleState = [row[:] for row in self.puzzle]
            value = newPuzzleState[self.blankRow - 1][self.blankColumn]
            newPuzzleState[self.blankRow - 1][self.blankColumn] = 0
            newPuzzleState[self.blankRow][self.blankColumn] = value
            return PuzzleState(newPuzzleState, self, "Up", self.cost + 1, self.depth + 1)

    def moveDown(self):
        if self.blankRow == self.n - 1:
            return None
        else:
            newPuzzleState = [row[:] for row in self.puzzle]
            value = newPuzzleState[self.blankRow + 1][self.blankColumn]
            newPuzzleState[self.blankRow + 1][self.blankColumn] = 0
            newPuzzleState[self.blankRow][self.blankColumn] = value
            return PuzzleState(newPuzzleState, self, "Down", self.cost + 1, self.depth + 1)

    def expandNode(self):
        if len(self.children) == 0:
            upChild = self.moveUp()
            if upChild is not None:
                self.children.append(upChild)
            downChild = self.moveDown()
            if downChild is not None:
                self.children.append(downChild)
            leftChild = self.moveLeft()
            if leftChild is not None:
                self.children.append(leftChild)
            rightChild = self.moveRight()
            if rightChild is not None:
                self.children.append(rightChild)

        return self.children
            
S = Solver("2,7,4,0,1,5,8,6,3", "bfs")

"""1,4,3,2,0,5,8,7,6"""