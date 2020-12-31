from node import Node
#dancing link with backtracking (i think) for euler problem 161

triominoes = [[[0, 0], [0, 1], [1, 0]],
              [[0, 0], [0, 1], [1, 1]],
              [[0, 0], [1, 0], [1, 1]],
              [[0, 1], [1, 0], [1, 1]],
              [[0, 0], [0, 1], [0, 2]],
              [[0, 0], [1, 0], [2, 0]]] #each trimoinoe as list of points from top left, even if that field not set (see 4)



def getGeneratedGrid(dimensions):
    return [[1] * dimensions[1] for _ in range(dimensions[0])]

def getPossibleTriominoePlacements(grid, polyominoes):
    indexList = []

    width = len(grid[0])
    height = len(grid)

    for rowIndex in range(height):
        for colIndex in range(width):
            for pointList in polyominoes:
                indicesTemp = []

                for offsetPoint in pointList:
                    newRow = rowIndex + offsetPoint[0]
                    newCol = colIndex + offsetPoint[1]

                    if newRow < height and newCol < width and grid[newRow][newCol]:
                        indicesTemp.append([newRow, newCol])
                    else:
                        break

                if len(indicesTemp) == 3:
                    indexList.append(indicesTemp)

    return indexList

def getDancingLinkList(grid, triominoes):
    triomineFieldsList = getPossibleTriominoePlacements(grid, triominoes)

    width = len(grid[0])
    height = len(grid)

    # list of column indices, so all available grid fields (fields that are 1)
    validFields = []
    colIndexPerField = [[-1] * width for _ in range(height)]

    for rowIndex in range(height):
        for colIndex in range(width):
            if grid[rowIndex][colIndex]:
                validFields.append([rowIndex, colIndex])
                colIndexPerField[rowIndex][colIndex] = len(validFields) - 1

    # generate the dancing link array as double linked both col and row
    dancingLinkList = []

    previousNodeCol = [None] * len(validFields)

    firstNodeCol = [None] * len(validFields)

    for rowIndex, triomineFields in enumerate(triomineFieldsList):
        doubleLinkNodesRow = []
        for field in triomineFields:
            colIndex = colIndexPerField[field[0]][field[1]]

            node = Node([rowIndex, colIndex])

            #vertical
            if firstNodeCol[colIndex] is None: # if its the first 1 in this column
                firstNodeCol[colIndex] = node
            else:
                node.prev_v = previousNodeCol[colIndex]
                node.prev_v.next_v = node

            previousNodeCol[colIndex] = node

            doubleLinkNodesRow.append(node)

        #horizontal double link
        for nodeIndex in range(len(doubleLinkNodesRow)):
            prev = (nodeIndex - 1) % len(doubleLinkNodesRow)
            next = (nodeIndex + 1) % len(doubleLinkNodesRow)

            doubleLinkNodesRow[nodeIndex].prev_h = doubleLinkNodesRow[prev]
            doubleLinkNodesRow[nodeIndex].next_h = doubleLinkNodesRow[next]

        dancingLinkList.extend(doubleLinkNodesRow)

    for colIndex, node in enumerate(firstNodeCol):
        node.prev_v = previousNodeCol[colIndex]
        previousNodeCol[colIndex].next_v = node

    return dancingLinkList

def algorithmX(dancingLinkList):
    return

def removeRow():
    return

def removeCol():
    return


grid = getGeneratedGrid([9, 2])

print(getPossibleTriominoePlacements(grid, triominoes))

a = getDancingLinkList(grid, triominoes)

display = [[0] * 46 for _ in range(18)]
string = ""


for node in a:
    display[node.val[1]][node.val[0]] = 1

for i in range(46):
    for j in range(18):
        string += str(display[j][i]) + " "
    string += "\n"

print(string)