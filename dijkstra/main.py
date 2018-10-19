#!/usr/bin/python
from copy import copy
from cell import Cell
import os
from pprint import pprint
import sys
from search import *
import time
import tkinter as tk

#Construct the Cell objects
def translate(i, j, char):
    if char == 'X':
        return Cell(i, j, 9999)
    elif char == 'O':
        return Cell(i, j, 1)
    elif char == 'F':
        return Cell(i, j, 2)
    elif char == 'E':
        global start_point
        start_point = Cell(i, j, 1)
        return start_point
    elif char == 'S':
        global end_point
        end_point = Cell(i, j, 1)
        return end_point
    else:
        return Cell(i, j, 50)

#Transform the file of char into a double D array of Cells
def read_file(f):
    buttons = []
    file_map = []
    with open(f) as file:
        for i, line in enumerate(file):
            line_map = []
            for j, char in enumerate(line):
                if char != '\n':
                    b = tk.Button(root, text=char)
                    buttons.append(b)
                    buttons[-1].grid(row=i, column=j)
                    line_map.append(translate(i, j, char))
            file_map.append(line_map)
    return file_map

#Init a 2D vector representing the distance needed to go on each cells (set at infinity at first)
def init(lines, collumns):
    dist = []
    for i in range(0, lines):
        sec_d = []
        for j in range(0, collumns):
            if i == start_point.x and j == start_point.y:
                sec_d.append(list((0, 0, 0)))
            else:
                sec_d.append(list((0, 0, 9999)))
        dist.append(sec_d)
    return dist

#Update the dist of cells at each iteration
def update(dist, board):
    #We could also take the starting cell it would be the same
    curr = min_cell(dist, board)
    while curr:
        neighbourhood = get_neighbour(curr, board)
        for neighbour in neighbourhood:
            if dist[curr.x][curr.y][2] + neighbour.dist < dist[neighbour.x][neighbour.y][2]:
                dist[neighbour.x][neighbour.y][2] = dist[curr.x][curr.y][2] + neighbour.dist
                dist[neighbour.x][neighbour.y][0] = curr.x
                dist[neighbour.x][neighbour.y][1] = curr.y
        curr = min_cell(dist, board)
    return dist

#Init the dist array and update it at the end each cell would've a value
#representing the "mouvement" needed to get on it
def find_path(board):
    dist = init(len(board), len(board[0]))
    dist = update(dist, board)
    return dist

#From the end point to the starting point going through the smallest valued neighbours
def get_shortest(dist, board):
    path = []
    curr = end_point
    while curr != start_point:
        path.append((curr.x, curr.y))
        curr = board[dist[curr.x][curr.y][0]][dist[curr.x][curr.y][1]]
    path.append((start_point.x, start_point.y))
    path.reverse()
    return path


def update_ground(i, j):
    letter = root.grid_slaves(row=start_point.x, column=start_point.y)[0]['text']
    if letter != 'E' and letter != 'S':
       root.grid_slaves(row=i, column=j)[0]['text'] = '*'
    root.grid_slaves(row=i, column=j)[0]['bg'] = 'green'

#Draw the path founded with '*', the map is unchanged apart from the solution drawn on it
def draw_ground(path, board):
    root.grid_slaves(row=start_point.x, column=start_point.y)[0]['text'] = 'E'
    root.grid_slaves(row=end_point.x, column=end_point.y)[0]['text'] = 'S'

    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if (i, j) in path:
                root.after(1000, update_ground(i, j))
                root.update()

def run(board):
    dist = find_path(board)
    path = get_shortest(dist, board)
    draw_ground(path, board)


#Main function, create a tk window each time we change file, yes it's dirty but it works
def dijkstra(file):
    global root
    root = tk.Tk()
    board = read_file(file)
    Launch = tk.Button(root, text="Start", command=lambda : run(board))
    Launch.place(relx=0.25, rely=0.5,anchor=tk.CENTER)
    Quit = tk.Button(root, text="Quit", command=lambda : exit())
    Quit.place(relx=0.75, rely=0.5,anchor=tk.CENTER)
    Next = tk.Button(root, text="Next", command=lambda : root.destroy())
    Next.place(relx=0.5, rely=0.5,anchor=tk.CENTER)
    root.mainloop()

#Check the input, if folder run on all files else run file
if __name__ == '__main__':
    input = sys.argv[1]
    if os.path.isdir(input):
        for test in os.listdir(input):
            dijkstra(input + test)
    else:
        dijkstra(input)
