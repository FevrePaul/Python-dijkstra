#Return an array filled with the 1 cell neighbour of the curr cell
def get_neighbour(curr, board):
    neighbour = []
    x = curr.x
    y = curr.y
    if x - 1 >= 0:
        neighbour.append(board[x-1][y])
    if y - 1 >= 0:
        neighbour.append(board[x][y - 1])
    if x + 1 < len(board):
        neighbour.append(board[x+1][y])
    if y + 1 < len(board[0]):
        neighbour.append(board[x][y+1])
    return neighbour

#Return the cell with the minimum dist which has never been selected before
#Return None if all cells have allready been selected once
def min_cell(dist, board):
    mindist = 9999
    ret = None
    for arr in board:
        for obj in arr:
            if not obj.visited and dist[obj.x][obj.y][2] < mindist:
                mindist = dist[obj.x][obj.y][2]
                ret = obj
    if ret:
        ret.visited = 1
    return ret


