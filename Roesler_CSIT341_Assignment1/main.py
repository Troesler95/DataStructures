import random


def pause():
    cont = input('Press <ENTER> to contine...')


class Stack:
    def __init__(self, maxS=100):
        self.prevLocation = []
        self.size = 0
        self.maxSize = maxS
        self.top = -1

    def isEmpty(self):
        return self.prevLocation == []

    def isFull(self):
        return self.size > (self.maxSize-1)

    def push(self, item):
        print("pushing value {} to stack".format(item))
        if self.size < self.maxSize:
            self.top = self.top + 1
            self.size = self.size + 1
            print("beenStack size and top: {}, {}".format(self.size, self.top))
            self.prevLocation.append(item)
        else:
            raise ValueError("Could not add item to stack!")

    def pop(self):
        if self.size > 0:
            self.size = self.size - 1
            item = self.prevLocation[self.top]
            del self.prevLocation[self.top]
            self.top = self.top - 1
            return item
        else:
            raise ValueError("Could not pop from stack!")

    def peek(self):
        if self.size > 0:
            item = self.prevLocation[self.top]
            return item
        else:
            raise ValueError("Could not pop item from stack!")

    def sizeOf(self):
        return self.size


class Runner:
    def __init__(self, filePath):
        self.curPos = []
        self.start = []
        self.destination = []
        self.beenStack = Stack(100)
        self.mazeFilePath = filePath
        self.maze = [[]]
        self.totalMoves = 0

    def addMaze(self):
        file = open(self.mazeFilePath, "r")
        """
            read each line into a multi-dimensional
            array named maze to create the maze matrix

            find x which marks the destination
            find s which marks the start
            store both in the Runner object
        """
        i = 0
        for line in file:
            for c in line:
                self.maze[i].append(c.lower())
                if c.lower() == 'x':
                    self.destination.append(i)
                    self.destination.append(len(self.maze[i])-1)
                if c.lower() == 'e':
                    self.start.append(i)
                    self.start.append(len(self.maze[i])-1)
            if line != '':
                self.maze.append([])
                i += 1
        print(self.maze)
        print(self.destination)
        print(self.start)
        print("Maze added successfully.\n")
        file.close()

    def createMazeCopy(self):
        file1 = open(self.mazeFilePath, "r")
        self.mazeFilePath = (self.mazeFilePath[:-4])+'-SOLVED.txt'
        file2 = open(self.mazeFilePath, "a")

        file2.write(file1.read()+"\n\nLegend:\n-------\ne = entrance\nx = destination\nW = wall\n-/| = path in stack"+
                                 "\n* = path travelled")

        print("Look for solved maze in {}\n".format(self.mazeFilePath))

    def backTrack(self, filePath, beenTo=False):
        print("starting backtrack")
        # if the current location isn't the last intersection...
        if self.maze[self.curPos[0]][self.curPos[1]] != '+' or beenTo:
            # write an asterisk to mark where we've been
            filePath.seek((self.curPos[0]*(len(self.maze[0])+1))+self.curPos[1])
            filePath.write(b'*')
            self.maze[self.curPos[0]][self.curPos[1]] = '*'

            # store the list item in a temp var
            # change current position to each value of list item from the stack
            temp = self.beenStack.pop()
            print("moving to: {}".format(temp))
            i = 0
            for value in temp:
                self.curPos[i] = value
                i += 1

            self.totalMoves += 1
            # recursively call until the intersection is met
            self.backTrack(filePath)
        else:
            print("finished backtracking")
            print("current position: {}".format(self.curPos))
            return True

    # move the fileObject to the left and mark the path it traveled
    def moveLeft(self, fileObject):
        # special case for first move
        print("moving left")
        if self.totalMoves == 0:
            print("first move")
            fileObject.seek(((self.curPos[0]*(len(self.maze[0])+1))-2) + (self.curPos[1]))
            fileObject.write(b"-")
            self.curPos[1] = self.curPos[1] - 1
            self.maze[self.curPos[0]][self.curPos[1]] = '-'
            self.totalMoves += 1
        # move the file reader to location, write, add location to been, and update location one step to the left
        else:
            fileObject.seek(((self.curPos[0]*(len(self.maze[0])+1))-1) + (self.curPos[1]))
            fileObject.write(b"-")
            self.beenStack.push([self.curPos[0], self.curPos[1]])
            self.curPos[1] = self.curPos[1] - 1
            self.maze[self.curPos[0]][self.curPos[1]] = '-'
            self.totalMoves += 1
            print("current position: {}".format(self.curPos))
            print("beenStack value: {}".format(self.beenStack.peek()))

    def moveRight(self, fileObject):
        print("moving right")
        if self.totalMoves == 0:
            print("first move")
            fileObject.seek(((self.curPos[0]*(len(self.maze[0])+1))+2) + (self.curPos[1]))
            fileObject.write(b"-")
            self.curPos[1] = self.curPos[1] + 1
            self.maze[self.curPos[0]][self.curPos[1]] = '-'
            self.totalMoves += 1
        # move the file reader to location, write, add location to been, and update location one step to the right
        else:
            fileObject.seek(((self.curPos[0]*(len(self.maze[0])+1))+1) + (self.curPos[1]))
            fileObject.write(b"-")
            self.beenStack.push([self.curPos[0], self.curPos[1]])
            self.curPos[1] += 1
            self.maze[self.curPos[0]][self.curPos[1]] = '-'
            self.totalMoves += 1
            print("current position: {}".format(self.curPos))
            print("beenStack value: {}".format(self.beenStack.peek()))

    def moveUp(self, fileObject):
        print("moving up")
        if self.totalMoves == 0:
            print("first move")
            fileObject.seek((self.curPos[0]*(len(self.maze[0])+1)) + (self.curPos[1])-(len(self.maze[0])+1))
            fileObject.write(b"|")
            self.beenStack.push([self.curPos[0], self.curPos[1]])
            self.curPos[0] = self.curPos[0] - 1
            self.maze[self.curPos[0]][self.curPos[1]] = '|'
            self.totalMoves += 1
            print("current position: {}".format(self.curPos))
            print("beenStack value: {}".format(self.beenStack.peek()))
        else:
            # move the file reader to location, write, add location to been, and update location one step up
            fileObject.seek((self.curPos[0]*(len(self.maze[0])+1)) + (self.curPos[1])-(len(self.maze[0])+1))
            fileObject.write(b"|")
            self.beenStack.push([self.curPos[0], self.curPos[1]])
            self.curPos[0] = self.curPos[0] - 1
            self.maze[self.curPos[0]][self.curPos[1]] = '|'
            self.totalMoves += 1
            print("current position: {}".format(self.curPos))
            print("beenStack value: {}".format(self.beenStack.peek()))

    def moveDown(self, fileObject):
        print("moving down")
        if self.totalMoves == 0:
            print("first move")
            fileObject.seek((self.curPos[0]*(len(self.maze[0])+1)) + (self.curPos[1])+(len(self.maze[0])+1))
            fileObject.write(b"|")
            self.beenStack.push([self.curPos[0], self.curPos[1]])
            self.curPos[0] = self.curPos[0] + 1
            self.maze[self.curPos[0]][self.curPos[1]] = '|'
            self.totalMoves += 1
            print("current position: {}".format(self.curPos))
            print("beenStack value: {}".format(self.beenStack.peek()))
        else:
            fileObject.seek((self.curPos[0]*(len(self.maze[0])+1)) + (self.curPos[1])+(len(self.maze[0])+1))
            fileObject.write(b"|")
            self.beenStack.push([self.curPos[0], self.curPos[1]])
            self.curPos[0] = self.curPos[0] + 1
            self.maze[self.curPos[0]][self.curPos[1]] = '|'
            self.totalMoves += 1
            print("current position: {}".format(self.curPos))
            print("beenStack value: {}".format(self.beenStack.peek()))

    def traverse(self):
        try:
            print("Starting move()...")
            #open file and place file reader at the s
            mazeFile = open(self.mazeFilePath, "br+")

            #initiate current position and the stack
            self.curPos = self.start
            self.beenStack.push([self.curPos[0], self.curPos[1]])

        except:
            print("There was an error moving the avatar within the file")

        # while the current position is not the x...
        while self.maze[self.curPos[0]][self.curPos[1]] != 'x':
            # reset random decision
            decision = None

            # avoid out-of range check
            if self.totalMoves > 1:
                # if end is found...
                if self.maze[self.curPos[0]][self.curPos[1]-1] == 'x' \
                        or self.maze[self.curPos[0]][self.curPos[1]+1] == 'x' \
                        or self.maze[self.curPos[0]-1][self.curPos[1]] == 'x' \
                        or self.maze[self.curPos[0]+1][self.curPos[1]] == 'x':
                    print("The end was found!")
                    # if left
                    if self.maze[self.curPos[0]][self.curPos[1]-1] == 'x':
                        self.beenStack.push([self.curPos[0], self.curPos[1]])
                        self.curPos[1] = self.curPos[1] - 1
                        self.totalMoves += 1
                        break
                    # if right
                    elif self.maze[self.curPos[0]][self.curPos[1]+1] == 'x':
                        self.beenStack.push([self.curPos[0], self.curPos[1]])
                        self.curPos[1] = self.curPos[1] - 1
                        self.totalMoves += 1
                        break
                    # if top
                    elif self.maze[self.curPos[0]-1][self.curPos[1]] == 'x':
                        self.beenStack.push([self.curPos[0], self.curPos[1]])
                        self.curPos[1] = self.curPos[1] - 1
                        self.totalMoves += 1
                        break
                    # if below
                    elif self.maze[self.curPos[0]+1][self.curPos[1]] == 'x':
                        self.beenStack.push([self.curPos[0], self.curPos[1]])
                        self.curPos[1] = self.curPos[1] - 1
                        self.totalMoves += 1
                        break

            ################# logic: #######################

            # if we've been to the right...
            if self.beenStack.peek() == [self.curPos[0], (self.curPos[1]+1)]:
                print("we've been to the right")
                # test to see if all three options haven't been visited
                if self.maze[self.curPos[0]][self.curPos[1]-1] == ' ' \
                        and self.maze[self.curPos[0]-1][self.curPos[1]] == ' ' \
                        and self.maze[self.curPos[0]+1][self.curPos[1]] == ' ':
                    # find location in file and write a +
                    mazeFile.seek((self.curPos[0]*(len(self.maze[0])+1)) + self.curPos[1])
                    mazeFile.write(b'+')
                    self.maze[self.curPos[0]][self.curPos[1]] = '+'
                    print("three way intersection marked")

                    decision = random.randint(0, 2)
                    if decision == 0:
                        self.moveUp(mazeFile)
                    elif decision == 1:
                        self.moveDown(mazeFile)
                    elif decision == 2:
                        self.moveLeft(mazeFile)
                    else:
                        break

                # check if left and top have never been to before
                elif self.maze[self.curPos[0]][self.curPos[1]-1] == ' ' \
                        and self.maze[self.curPos[0]-1][self.curPos[1]] == ' ':
                    # find location in file and write a +
                    mazeFile.seek((self.curPos[0]*(len(self.maze[0])+1)) + self.curPos[1])
                    mazeFile.write(b'+')
                    self.maze[self.curPos[0]][self.curPos[1]] = '+'
                    print("left and top intersection marked")


                    # generate randomly either 0 or 1
                    decision = random.randint(0, 1)
                    # go up
                    if decision == 0:
                        self.moveUp(mazeFile)

                    # let's go left!
                    elif decision == 1:
                        self.moveLeft(mazeFile)

                    else:
                        self.backTrack(mazeFile)

                # check if left and bottom have not been to before
                elif self.maze[self.curPos[0]][self.curPos[1]-1] == ' ' \
                        and self.maze[self.curPos[0]+1][self.curPos[1]] == ' ':
                    # find location in file and write a +
                    mazeFile.seek((self.curPos[0]*(len(self.maze[0])+1)) + self.curPos[1])
                    mazeFile.write(b'+')
                    self.maze[self.curPos[0]][self.curPos[1]] = '+'
                    print("left and bottom intersection marked")


                    # generate randomly either 0 or 1
                    decision = random.randint(0, 1)

                    # go down
                    if decision == 0:
                        self.moveDown(mazeFile)
                    # let's go left!
                    elif decision == 1:
                        self.moveLeft(mazeFile)
                    else:
                        break

                # check if bottom and top are open
                elif self.maze[self.curPos[0]-1][self.curPos[1]] == ' ' \
                        and self.maze[self.curPos[0]+1][self.curPos[1]] == ' ':
                    # find location in file and write a +
                    mazeFile.seek((self.curPos[0]*(len(self.maze[0])+1)) + self.curPos[1])
                    mazeFile.write(b'+')
                    self.maze[self.curPos[0]][self.curPos[1]] = '+'
                    print("bottom and top intersection marked")

                    # generate randomly either 0 or 1
                    decision = random.randint(0, 1)
                    # go down
                    if decision == 0:
                        self.moveDown(mazeFile)

                    # let's go up!
                    elif decision == 1:
                        self.moveUp(mazeFile)

                    else:
                        print("I got confused!")
                        raise ValueError

                elif self.maze[self.curPos[0]][self.curPos[1]-1] == '*' \
                        and self.maze[self.curPos[0]-1][self.curPos[1]] == '*' \
                        and self.maze[self.curPos[0]+1][self.curPos[1]] == '*':
                    print("been to all options, attempting backtrack...")
                    self.backTrack(mazeFile)

                # else find which is open and move there
                else:
                    print("only one way to go")
                    # find which direction it is
                    # left
                    if self.maze[self.curPos[0]][self.curPos[1]-1] == ' ':
                        self.moveLeft(mazeFile)
                    # up
                    elif self.maze[self.curPos[0]-1][self.curPos[1]] == ' ':
                        self.moveUp(mazeFile)
                    # down
                    elif self.maze[self.curPos[0]+1][self.curPos[1]] == ' ':
                        self.moveDown(mazeFile)
                    else:
                        print("cant figure where to go, backtracking...")
                        self.backTrack(mazeFile, True)

            # check if last position was to the left
            elif self.beenStack.peek() == [self.curPos[0], (self.curPos[1]-1)]:
                print("We've been to the left")
                # test to see if all three options haven't been visited
                if self.maze[self.curPos[0]+1][self.curPos[1]] == ' ' \
                        and self.maze[self.curPos[0]-1][self.curPos[1]] == ' ' \
                        and self.maze[self.curPos[0]][self.curPos[1]+1] == ' ':
                    # find location in file and write a +
                    mazeFile.seek((self.curPos[0]*(len(self.maze[0])+1)) + self.curPos[1])
                    mazeFile.write(b'+')
                    self.maze[self.curPos[0]][self.curPos[1]] = '+'
                    print("three way intersection marked")

                    decision = random.randint(0, 2)
                    if decision == 0:
                        self.moveUp(mazeFile)
                    elif decision == 1:
                        self.moveDown(mazeFile)
                    elif decision == 2:
                        self.moveRight(mazeFile)
                    else:
                        print("I got confused.")
                        raise ValueError

                # check if bottom and top have never been to before
                elif self.maze[self.curPos[0]+1][self.curPos[1]] == ' ' \
                        and self.maze[self.curPos[0]-1][self.curPos[1]] == ' ':
                    # find location in file and write a +
                    mazeFile.seek((self.curPos[0]*(len(self.maze[0])+1)) + self.curPos[1])
                    mazeFile.write(b'+')
                    self.maze[self.curPos[0]][self.curPos[1]] = '+'
                    print("bottom and top intersection marked")

                    # generate randomly either 0 or 1
                    decision = random.randint(0, 1)
                    # go up
                    if decision == 0:
                        self.moveUp(mazeFile)

                    # let's go down!
                    elif decision == 1:
                        self.moveDown(mazeFile)

                    else:
                        print("I got confused!")
                        break

                # check if bottom and right have not been to before
                elif self.maze[self.curPos[0]+1][self.curPos[1]] == ' ' \
                        and self.maze[self.curPos[0]][self.curPos[1]+1] == ' ':
                    # find location in file and write a +
                    mazeFile.seek((self.curPos[0]*(len(self.maze[0])+1)) + self.curPos[1])
                    mazeFile.write(b'+')
                    self.maze[self.curPos[0]][self.curPos[1]] = '+'
                    print("bottom and right intersection marked")

                    # generate randomly either 0 or 1
                    decision = random.randint(0, 1)
                    # go right
                    if decision == 0:
                        self.moveRight(mazeFile)

                    # let's go down!
                    elif decision == 1:
                        self.moveDown(mazeFile)

                    else:
                        print("I got confused!")
                        break

                # check if right and top are open
                elif self.maze[self.curPos[0]-1][self.curPos[1]] == ' ' \
                        and self.maze[self.curPos[0]][self.curPos[1]+1] == ' ':
                    # find location in file and write a +
                    mazeFile.seek((self.curPos[0]*(len(self.maze[0])+1)) + self.curPos[1])
                    mazeFile.write(b'+')
                    self.maze[self.curPos[0]][self.curPos[1]] = '+'
                    print("right and top intersection marked")

                    # generate randomly either 0 or 1
                    decision = random.randint(0, 1)
                    # go up
                    if decision == 0:
                        self.moveUp(mazeFile)

                    # let's go right!
                    elif decision == 1:
                        self.moveRight(mazeFile)

                    else:
                        print("I got confused!")
                        raise ValueError

                elif self.maze[self.curPos[0]+1][self.curPos[1]] == '*' \
                        and self.maze[self.curPos[0]-1][self.curPos[1]] == '*' \
                        and self.maze[self.curPos[0]][self.curPos[1]+1] == '*':
                    print("all paths tried, attempting back track...")
                    self.backTrack(mazeFile, True)

                # else find which is open and move there
                else:
                    # find which direction it is
                    # Down
                    if self.maze[self.curPos[0]+1][self.curPos[1]] == ' ':
                        self.moveDown(mazeFile)
                    # up
                    elif self.maze[self.curPos[0]-1][self.curPos[1]] == ' ':
                        self.moveUp(mazeFile)
                    # right
                    elif self.maze[self.curPos[0]][self.curPos[1]+1] == ' ':
                        self.moveRight(mazeFile)
                    else:
                        print("couldn't figure where to go, backtracking...")
                        self.backTrack(mazeFile, True)

            # check to see if last pos was below
            elif self.beenStack.peek() == [self.curPos[0]+1, (self.curPos[1])]:
                print("we've been below")

                # test to see if all three options haven't been visited
                if self.maze[self.curPos[0]][self.curPos[1]-1] == ' ' \
                        and self.maze[self.curPos[0]-1][self.curPos[1]] == ' ' \
                        and self.maze[self.curPos[0]][self.curPos[1]+1] == ' ':
                    # find location in file and write a +
                    mazeFile.seek((self.curPos[0]*(len(self.maze[0])+1)) + self.curPos[1])
                    mazeFile.write(b'+')
                    self.maze[self.curPos[0]][self.curPos[1]] = '+'
                    print("three way intersection marked")

                    decision = random.randint(0, 2)
                    if decision == 0:
                        self.moveUp(mazeFile)
                    elif decision == 1:
                        self.moveLeft(mazeFile)
                    elif decision == 2:
                        self.moveRight(mazeFile)
                    else:
                        print("I got confused")
                        raise ValueError

                # check if left and top have never been to before
                elif self.maze[self.curPos[0]][self.curPos[1]-1] == ' ' \
                        and self.maze[self.curPos[0]-1][self.curPos[1]] == ' ':
                    # find location in file and write a +
                    mazeFile.seek((self.curPos[0]*(len(self.maze[0])+1)) + self.curPos[1])
                    mazeFile.write(b'+')
                    self.maze[self.curPos[0]][self.curPos[1]] = '+'
                    print("left and top intersection marked")

                    # generate randomly either 0 or 1
                    decision = random.randint(0, 1)
                    # go up
                    if decision == 0:
                        self.moveUp(mazeFile)

                    # let's go left!
                    elif decision == 1:
                        self.moveLeft(mazeFile)

                    else:
                        print("I got confused!")
                        raise ValueError

                # check if left and right have not been to before
                elif self.maze[self.curPos[0]][self.curPos[1]-1] == ' ' \
                        and self.maze[self.curPos[0]][self.curPos[1]+1] == ' ':
                    # find location in file and write a +
                    mazeFile.seek((self.curPos[0]*(len(self.maze[0])+1)) + self.curPos[1])
                    mazeFile.write(b'+')
                    self.maze[self.curPos[0]][self.curPos[1]] = '+'
                    print(" left and right intersection marked")

                    # generate randomly either 0 or 1
                    decision = random.randint(0, 1)
                    # go right
                    if decision == 0:
                        self.moveRight(mazeFile)

                    # let's go left!
                    elif decision == 1:
                        self.moveLeft(mazeFile)

                    else:
                        print("I got confused!")
                        raise ValueError

                # check if right and top are open
                elif self.maze[self.curPos[0]-1][self.curPos[1]] == ' ' \
                        and self.maze[self.curPos[0]][self.curPos[1]+1] == ' ':
                    # find location in file and write a +
                    mazeFile.seek((self.curPos[0]*(len(self.maze[0])+1)) + self.curPos[1])
                    mazeFile.write(b'+')
                    self.maze[self.curPos[0]][self.curPos[1]] = '+'
                    print("right and top intersection marked")

                    # generate randomly either 0 or 1
                    decision = random.randint(0, 1)
                    # go up
                    if decision == 0:
                        self.moveUp(mazeFile)

                    # let's go right!
                    elif decision == 1:
                        self.moveRight(mazeFile)

                    else:
                        print("I got confused!")
                        raise ValueError

                elif self.maze[self.curPos[0]][self.curPos[1]-1] == '*' \
                        and self.maze[self.curPos[0]-1][self.curPos[1]] == '*' \
                        and self.maze[self.curPos[0]][self.curPos[1]+1] == '*':
                    print("All paths been to, trying to back track...")
                    self.backTrack(mazeFile, True)

                # else find which is open and move there
                else:
                    print("only one way to go")
                    # find which direction it is
                    # left
                    if self.maze[self.curPos[0]][self.curPos[1]-1] == ' ':
                        self.moveLeft(mazeFile)
                    # up
                    elif self.maze[self.curPos[0]-1][self.curPos[1]] == ' ':
                        self.moveUp(mazeFile)
                    # right
                    elif self.maze[self.curPos[0]][self.curPos[1]+1] == ' ':
                        self.moveRight(mazeFile)
                    else:
                        print("couldn't figure out where to go, attempting backtrack")
                        self.backTrack(mazeFile, True)

            # check if last position was above
            elif self.beenStack.peek() == [self.curPos[0]-1, (self.curPos[1])]:
                print("last been above us")

                # test to see if all three options haven't been visited
                if self.maze[self.curPos[0]][self.curPos[1]-1] == ' ' \
                        and self.maze[self.curPos[0]+1][self.curPos[1]] == ' ' \
                        and self.maze[self.curPos[0]][self.curPos[1]+1] == ' ':
                    # find location in file and write a +
                    mazeFile.seek((self.curPos[0]*(len(self.maze[0])+1)) + self.curPos[1])
                    mazeFile.write(b'+')
                    self.maze[self.curPos[0]][self.curPos[1]] = '+'
                    print("three way intersection marked")

                    # decide between the three
                    decision = random.randint(0, 2)
                    # moveDown
                    if decision == 0:
                        self.moveDown(mazeFile)
                    # moveLeft
                    elif decision == 1:
                        self.moveLeft(mazeFile)
                    # moveRight
                    elif decision == 2:
                        self.moveRight(mazeFile)
                    else:
                        print("I got confused.")
                        raise ValueError

                # check if left and bottom have never been to before
                elif self.maze[self.curPos[0]][self.curPos[1]-1] == ' ' \
                        and self.maze[self.curPos[0]+1][self.curPos[1]] == ' ':
                    # find location in file and write a +
                    mazeFile.seek((self.curPos[0]*(len(self.maze[0])+1)) + self.curPos[1])
                    mazeFile.write(b'+')
                    self.maze[self.curPos[0]][self.curPos[1]] = '+'
                    print(" left and bottom intersection marked")

                    # generate randomly either 0 or 1
                    decision = random.randint(0, 1)
                    # go down
                    if decision == 0:
                        self.moveDown(mazeFile)

                    # let's go left!
                    elif decision == 1:
                        self.moveLeft(mazeFile)

                    else:
                        print("I got confused!")
                        raise ValueError

                # check if left and right have not been to before
                elif self.maze[self.curPos[0]][self.curPos[1]-1] == ' ' \
                        and self.maze[self.curPos[0]][self.curPos[1]+1] == ' ':
                    # find location in file and write a +
                    mazeFile.seek((self.curPos[0]*(len(self.maze[0])+1)) + self.curPos[1])
                    mazeFile.write(b'+')
                    self.maze[self.curPos[0]][self.curPos[1]] = '+'
                    print("left and right intersection marked")

                    # generate randomly either 0 or 1
                    decision = random.randint(0, 1)
                    # go right
                    if decision == 0:
                        self.moveRight(mazeFile)

                    # let's go left!
                    elif decision == 1:
                        self.moveLeft(mazeFile)

                    else:
                        print("I got confused!")
                        raise ValueError

                # check if right and bottom are open
                elif self.maze[self.curPos[0]+1][self.curPos[1]] == ' ' \
                        and self.maze[self.curPos[0]][self.curPos[1]+1] == ' ':
                    # find location in file and write a +
                    mazeFile.seek((self.curPos[0]*(len(self.maze[0])+1)) + self.curPos[1])
                    mazeFile.write(b'+')
                    self.maze[self.curPos[0]][self.curPos[1]] = '+'
                    print("right and bottom intersection marked")

                    # generate randomly either 0 or 1
                    decision = random.randint(0, 1)
                    # go down
                    if decision == 0:
                        self.moveDown(mazeFile)

                    # let's go right!
                    elif decision == 1:
                        self.moveRight(mazeFile)

                    else:
                        print("I got confused!")
                        raise ValueError

                elif self.maze[self.curPos[0]][self.curPos[1]-1] == '*' \
                        and self.maze[self.curPos[0]+1][self.curPos[1]] == '*' \
                        and self.maze[self.curPos[0]][self.curPos[1]+1] == '*':
                    print("all paths tried, attempting backtrack")
                    self.backTrack(mazeFile, True)

                # else find which is open and move there
                else:
                    print("only one way to go")
                    # find which direction it is
                    # left
                    if self.maze[self.curPos[0]][self.curPos[1]-1] == ' ':
                        self.moveLeft(mazeFile)
                    # bottom
                    elif self.maze[self.curPos[0]+1][self.curPos[1]] == ' ':
                        self.moveDown(mazeFile)
                    # right
                    elif self.maze[self.curPos[0]][self.curPos[1]+1] == ' ':
                        self.moveRight(mazeFile)
                    # else need to backtrack
                    else:
                        print("couldn't figure out where to go, backtracking...")
                        self.backTrack(mazeFile, True)

            # first move
            else:
                if self.totalMoves == 0:
                    if len(self.maze[0])-2 < self.curPos[1] < len(self.maze[0]):
                        self.moveLeft(mazeFile)
                    elif self.start[1]-1 < 0:
                        self.moveRight(mazeFile)
                    elif self.start[0]-1 < 0:
                        self.moveDown(mazeFile)
                    elif self.start[1]+1 > len(self.maze):
                        self.moveUp(mazeFile)
                else:
                    print("stuck thinking it's the first move...")
                    print("current position: {}".format(self.curPos))
                    print("beenStack last value: {}".format(self.beenStack.peek()))
                    raise ValueError


class Menu:

    def __init__(self):
        self.choice = 0
        self.mazeRunner = None

    def retChoice(self):
        return self.choice

    def addMaze(self):
        print("Add New Maze:")
        print("--------------------------------------------------------\n")
        print("********************************************************")
        print("WARNING: Please ensure that any previous \"<name>-SOLVED.txt\""+
              "\n         does not exist in the current directory or the"
              "\n         program may produce unexpected behaviour.")
        print("********************************************************")
        filePath = str(input("Please Enter the Path to the Maze File: "+"\nie. C:\\Users\\Your_Name\\Desktop\\maze.txt\n"))

        print("\nAdd New Maze:")
        print("--------------------------------------------------------\n")

        try:
            self.mazeRunner = Runner(filePath)
            self.mazeRunner.addMaze()
            self.mazeRunner.createMazeCopy()

            print("Please choose solve puzzle from the options menu!")
            pause()
        except IOError as e:
            print("There was an error adding the maze. Please try again!")
            print("Error: {}".format(e))

    def solveMaze(self):
        print("Solve Maze:")
        print("--------------------------------------------------------\n\n\n")
        if self.mazeRunner:
            print("Attempting to solve the given maze...\n")

            # try:
            self.mazeRunner.traverse()

            print("Success!")
            print("Steps to x: ([x,y])")
            print("--------------------\n")

            while self.mazeRunner.beenStack.sizeOf() > 1:
                print(self.mazeRunner.beenStack.pop())

            print("\nPlease see {} for a visual represenation!"
                  " Thanks for using my program!".format(self.mazeRunner.mazeFilePath))
            pause()

        else:
            print("There is no maze to solve! Please enter a maze file to solve!")
            pause()

    def options(self):
        print("Menu:")
        print("--------------------------------------------------------")
        print("\t1. Add New Maze")
        print("\t2. Solve Maze")
        print("\t3. Exit Maze Solver")
        print("--------------------------------------------------------")
        self.choice = int(input("Please Enter an Option and Press Enter: "))


print("========================================================")
print("Welcome to the Maze Solver for CSIT 341: Data Structures")
print("========================================================\n")
print("Author: Tyler Roesler")
print("Date Published: 09/08/16\n")
print("**********************************************************")
print("WARNING: This program assumes the user is running Python 3\n"+
      "         Please use Python 3 for assurance that the program\n"+
      "         will run correctly")
print("**********************************************************\n\n")

menu = Menu()

while True:
    menu.options()
    if menu.retChoice() == 1:
        menu.addMaze()
    elif menu.retChoice() == 2:
        menu.solveMaze()
    elif menu.retChoice() == 3:
        break
