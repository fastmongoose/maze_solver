from tkinter import Tk, BOTH, Canvas

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
    def __init__(self, x1, x2, y1, y2, window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_Wall = True
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = window

    def draw(self, fill_color="blue"):
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
        if self.has_bottom_Wall:
            self._win.canvas.create_line(
                self._x1, self._y2, self._x2, self._y2, fill=fill_color
            )



def main():
    win = Window(800, 600)
    # line1 = Line(100, 100, 400, 400)
    # win.draw_line(line1, "red")
    cell_1 = Cell(100, 200, 100, 200, win)
    cell_1.draw()
    win.wait_for_close()

main()