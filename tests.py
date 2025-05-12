import unittest
from main import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
    
    def test_maze_create_cells_2(self):
        num_cols = 10
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 20, 20)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_cell_initialization(self):
        m1 = Maze(0, 0, 2, 2, 10, 10)
        for col in range(2):
            for row in range(2):
                cell = m1._cells[col][row]
                self.assertTrue(cell.has_top_wall)
                self.assertTrue(cell.has_right_wall)
                self.assertTrue(cell.has_bottom_wall)
                self.assertTrue(cell.has_left_wall)

    def test_maze_dimensions(self):
        m1 = Maze(5, 5, 3, 4, 20, 20)
        self.assertEqual(len(m1._cells), 4)
        self.assertEqual(len(m1._cells[0]), 3)

    def test_maze_unique_cells(self):
        m1 = Maze(0, 0, 3, 3, 10, 10)
        cell_ids = set()
        for col in range(3):
            for row in range(3):
                cell_ids.add(id(m1._cells[col][row]))
        self.assertEqual(len(cell_ids), 9)

if __name__ == "__main__":
    unittest.main()
