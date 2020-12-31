from node import Node
import matplotlib.pyplot as plt
import numpy as np

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

def getDancingLinkList(grid, triominoePlacements):
    triomineFieldsList = triominoePlacements

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

    # initialize column headers, these dont hold the amount of 1's, just the column id
    colHeaders = [Node(col, isColHeader=True) for col in range(len(validFields))]
    linkHorizontalCircular([Node(isOrigin=True), *colHeaders])

    previousNodeCol = colHeaders.copy()

    for rowIndex, triomineFields in enumerate(triomineFieldsList):
        doubleLinkNodesRow = []
        for field in triomineFields:
            colIndex = colIndexPerField[field[0]][field[1]]

            node = Node([rowIndex, colIndex])

            #vertical
            node.prev_v = previousNodeCol[colIndex]
            node.prev_v.next_v = node

            previousNodeCol[colIndex] = node

            doubleLinkNodesRow.append(node)

        #horizontal double link
        linkHorizontalCircular(doubleLinkNodesRow)

        dancingLinkList.extend(doubleLinkNodesRow)

    for colIndex, node in enumerate(colHeaders):
        node.prev_v = previousNodeCol[colIndex]
        previousNodeCol[colIndex].next_v = node

    return dancingLinkList, colHeaders, colHeaders[0].prev_h

def linkHorizontalCircular(nodeList):
    for nodeIndex in range(len(nodeList)):
        prev = (nodeIndex - 1) % len(nodeList)
        next = (nodeIndex + 1) % len(nodeList)

        nodeList[nodeIndex].prev_h = nodeList[prev]
        nodeList[nodeIndex].next_h = nodeList[next]

def algorithmX(nodeOrigin):
    partialSolution = []
    while True:
        print("LOOP:")
        print(getMatrixString(nodeOrigin, colHeaders, linkedList))


        #if empty, solution was found
        if nodeOrigin.next_h is nodeOrigin:
            print("array has no more columns")
            print([i.val[0] for i in partialSolution])
            break
        else:
            invalid = False
            for node in origin:
                if node is origin:
                    break
                if node.next_v is node:
                    invalid = True
                    break
            if invalid:
                print("Combination:")
                print(partialSolution)
                print("does not work")
        col = nodeOrigin.next_h
        row = col.next_v

        partialSolution.append(row) # fork is created

        # go through columns that have a 1 in this row and delete
        lastCol = row.prev_h
        currentCol = row
        while True:
            #go through rows that have a 1 in this column and delete
            lastRow = currentCol.prev_v
            currentRow = currentCol
            while True:
                removeRow(currentRow)
                if currentRow is lastRow:
                    break
                currentRow = currentRow.next_v

            removeCol(currentCol)
            if currentCol is lastCol:
                break
            currentCol = currentCol.next_h
    return partialSolution

def removeRow(node):
    if node.isColHeader:
        return
    initial = node
    current = node

    while True:
        current.prev_v.next_v = current.next_v
        current.next_v.prev_v = current.prev_v

        current = current.next_h
        if initial is current:
            break
    return

def removeCol(node):
    initial = node.prev_v
    current = node.prev_v

    while True:
        current.prev_h.next_h = current.next_h
        current.next_h.prev_h = current.prev_h

        current = current.next_v
        if initial is current:
            break
    return


#region visualisation

def getMatrixString(origin, colHeaders, linkedList):
    width = len(colHeaders)

    height = 0
    for node in linkedList:
        height = max(node.val[0], height)
    height += 1

    consideredRows = [0] * height
    for node in origin:
        if node is origin:
            break

        while True:
            node = node.next_v
            if node.isColHeader:
                break
            consideredRows[node.val[0]] = 1

    consideredColumns = [0] * width
    for node in origin:
        if node is origin:
            break
        consideredColumns[node.val] = 1

    display = [[0] * height for _ in range(width)]
    string = ""

    for node in linkedList:
        display[node.val[1]][node.val[0]] = 1


    for i in range(height):
        if consideredRows[i] == 1:
            for j in range(width):
                if consideredColumns[j] == 1:
                    string += str(display[j][i]) + " "
            string += "\n"
    return string

def drawSolution(grid, triominoeList):
    # Make a 9x9 grid...
    nrows, ncols = len(grid), len(grid[1])
    image = np.zeros(nrows * ncols)

    # Set every other cell to a random number (this would be your data)
    for index, triominoe in enumerate(triominoeList):
        for point in triominoe:
            image[point[0] * ncols + point[1]] = index%20

    # Reshape things into a 9x9 grid.
    image = image.reshape((nrows, ncols))

    row_labels = range(nrows)
    col_labels = range(ncols)
    plt.matshow(image, cmap='tab20')
    plt.xticks(range(ncols), col_labels)
    plt.yticks(range(nrows), row_labels)
    plt.show()

#endregion

grid = getGeneratedGrid([9, 2])

triominoePlacements = getPossibleTriominoePlacements(grid, triominoes)

linkedList, colHeaders, origin = getDancingLinkList(grid, triominoePlacements)

sol = algorithmX(origin)

triominoeList = []
for i in sol:
    triominoeList.append(triominoePlacements[i.val[0]])

drawSolution(grid, triominoeList)
