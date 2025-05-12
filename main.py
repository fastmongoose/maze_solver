from tkinter import Tk, BOTH, Canvas
import time
import random

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.root = Tk()
        self.root.title("Maze Solver")
        self.canvas = Canvas()
        self.canvas.pack()
        self.running = False

        self.root.protocol("WM_DELETE_WINDOW", self.close)
    
    def redraw(self):
        self.root.update_idletasks()
        self.root.update()
    
    def wait_for_close(self):
        self.running = True
        while self.running is True:
            self.redraw()
    
    def close(self):
        self.running = False
    
    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.x1, self.y1, self.x2, self.y2, fill=fill_color, width=2
        )


class Cell:
    def __init__(self, x1, x2, y1, y2, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = window

        self.visited = False

    def draw(self, fill_color="blue"):
        self._win.canvas.create_line(self._x1, self._y1, self._x1, self._y2, fill="#d9d9d9")
        self._win.canvas.create_line(self._x1, self._y1, self._x2, self._y1, fill="#d9d9d9")
        self._win.canvas.create_line(self._x2, self._y1, self._x2, self._y2, fill="#d9d9d9")
        self._win.canvas.create_line(self._x1, self._y2, self._x2, self._y2, fill="#d9d9d9")

        
        if self.has_left_wall:
            self._win.canvas.create_line(
                self._x1, self._y1, self._x1, self._y2, fill=fill_color
            )
        if self.has_top_wall:
            self._win.canvas.create_line(
                self._x1, self._y1, self._x2, self._y1, fill=fill_color
            )
        if self.has_right_wall:
            self._win.canvas.create_line(
                self._x2, self._y1, self._x2, self._y2, fill=fill_color
            )
        if self.has_bottom_wall:
            self._win.canvas.create_line(
                self._x1, self._y2, self._x2, self._y2, fill=fill_color
            )

    def draw_move(self, to_cell, undo=False):
        fill_color = "gray"
        if undo == None:
            fill_color = "red"
        self._win.canvas.create_line(
            (self._x1 + self._x2)/2, (self._y1 + self._y2)/2, (to_cell._x1 + to_cell._x2)/2, (to_cell._y1 + to_cell._y2)/2
        )

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, window=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_cols
        self.num_cols = num_rows
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = window
        if seed != None:
            random.seed(seed)
        self._create_cells()
        
    
    def _create_cells(self):
        self._cells = []
        x1 = self.x1
        y1 = self.y1
        for i in range(0, self.num_rows):
            inner_list = []
            for j in range(0, self.num_cols):
                inner_list.append(Cell(x1, x1+self.cell_size_x, y1, y1+self.cell_size_y, window=self.win))
                x1 += self.cell_size_x
            x1 = self.x1
            y1 += self.cell_size_y
            self._cells.append(inner_list)

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.win != None:
                    self._draw_cell(i, j)
        
    
    def _draw_cell(self, i, j):
        self._cells[i][j].draw()
        self._animate()
    
    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self.num_rows - 1][self.num_cols - 1].has_bottom_wall = False
        self._draw_cell(self.num_rows - 1, self.num_cols - 1)
    
    def _break_walls_r(self, i, j):
        current = self._cells[i][j]
        current.visited = True

        directions = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
        random.shuffle(directions)

        for ni, nj in directions:
            if 0 <= ni < self.num_rows and 0 <= nj < self.num_cols:
                neighbor = self._cells[ni][nj]
                if not neighbor.visited:
                    if ni == i + 1:  # down
                        current.has_bottom_wall = False
                        neighbor.has_top_wall = False
                    elif ni == i - 1:  # up
                        current.has_top_wall = False
                        neighbor.has_bottom_wall = False
                    elif nj == j + 1:  # right
                        current.has_right_wall = False
                        neighbor.has_left_wall = False
                    elif nj == j - 1:  # left
                        current.has_left_wall = False
                        neighbor.has_right_wall = False

                    if self.win:
                        self._draw_cell(i, j)
                        self._draw_cell(ni, nj)

                    self._break_walls_r(ni, nj)
    
    def _reset_cells_visited(self):
        for cell in self._cells:
            cell.visited = False
            
    def solve(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        current = self._cells[i][j]
        current.visited = True

        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True

        directions = [
            (i - 1, j, current.has_top_wall), 
            (i + 1, j, current.has_bottom_wall), 
            (i, j - 1, current.has_left_wall),   
            (i, j + 1, current.has_right_wall)    
        ]

        for ni, nj, wall in directions:
            if 0 <= ni < self.num_rows and 0 <= nj < self.num_cols and not wall:
                neighbor = self._cells[ni][nj]
                if not neighbor.visited:
                    current.draw_move(neighbor)
                    if self._solve_r(ni, nj):
                        return True
                    else:
                        current.draw_move(neighbor, undo=True) 

        return False

        

def main():
    win = Window(800, 600)
    maze = Maze(10, 10, 6, 8, 30, 30, window=win)
    maze._break_entrance_and_exit()
    maze._break_walls_r(0, 0)
    maze.solve()
    win.wait_for_close()

if __name__ == "__main__":
    main()