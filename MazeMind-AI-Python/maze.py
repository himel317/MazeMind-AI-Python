import tkinter as tk
from constants import *


class MazeGrid:

    def __init__(self, parent, rows=ROWS, cols=COLS):

        self.parent = parent

        self.rows = rows
        self.cols = cols

        self.current_tool = "Wall"

        self.start = None
        self.goal = None

        self.cells = []

        self.create_grid()

    # ===========================================

    def create_grid(self):

        for row in range(self.rows):

            current_row = []

            self.parent.grid_rowconfigure(row, minsize=CELL_SIZE)

            for col in range(self.cols):

                self.parent.grid_columnconfigure(col, minsize=CELL_SIZE)

                cell = tk.Button(

                    self.parent,

                    width=1,

                    height=1,

                    bg=EMPTY,

                    relief="flat",

                    bd=1,

                    highlightthickness=0,

                    activebackground="#E2E8F0",

                    activeforeground=TEXT,

                    cursor="hand2",

                    command=lambda r=row, c=col: self.cell_clicked(r, c)

                )

                cell.grid(
                    row=row,
                    column=col,
                    padx=2,
                    pady=2,
                    sticky="nsew"
                )

                current_row.append(cell)

            self.cells.append(current_row)

    # ===========================================

    def set_tool(self, tool):

        self.current_tool = tool

            # ===========================================

    def cell_clicked(self, row, col):

        cell = self.cells[row][col]

        # -------- Wall --------

        if self.current_tool == "Wall":

            if self.start == (row, col) or self.goal == (row, col):
                return

            cell.configure(bg=WALL)

        # -------- Erase --------

        elif self.current_tool == "Erase":

            cell.configure(bg=EMPTY)

            if self.start == (row, col):
                self.start = None

            if self.goal == (row, col):
                self.goal = None

        # -------- Start --------

        elif self.current_tool == "Start":

            if self.start is not None:

                old_row, old_col = self.start

                self.cells[old_row][old_col].configure(bg=EMPTY)

            if self.goal == (row, col):
                self.goal = None

            self.start = (row, col)

            cell.configure(bg=START)

        # -------- Goal --------

        elif self.current_tool == "Goal":

            if self.goal is not None:

                old_row, old_col = self.goal

                self.cells[old_row][old_col].configure(bg=EMPTY)

            if self.start == (row, col):
                self.start = None

            self.goal = (row, col)

            cell.configure(bg=GOAL)

                # ===========================================

    def reset_grid(self):

        """
        Reset the complete maze.
        """

        for row in range(self.rows):

            for col in range(self.cols):

                self.cells[row][col].configure(bg=EMPTY)

        self.start = None
        self.goal = None

    # ===========================================

    def get_start(self):

        """
        Return Start Position
        """

        return self.start

    # ===========================================

    def get_goal(self):

        """
        Return Goal Position
        """

        return self.goal

    # ===========================================

    def get_maze(self):

        """
        Convert GUI grid into 2D matrix.

        0 = Empty
        1 = Wall
        """

        maze = []

        for row in range(self.rows):

            current = []

            for col in range(self.cols):

                color = self.cells[row][col]["bg"]

                if color == WALL:
                    current.append(1)
                else:
                    current.append(0)

            maze.append(current)

        return maze

    # ===========================================

    def color_path(self, path):

        """
        Highlight the shortest path.
        """

        if path is None:
            return

        self.clear_path()

        for row, col in path:

            if (row, col) == self.start:
                continue

            if (row, col) == self.goal:
                continue

            self.cells[row][col].configure(bg=PATH)

    # ===========================================

    def clear_path(self):

        """
        Remove any previous path markings.
        """

        for row in range(self.rows):

            for col in range(self.cols):

                if self.cells[row][col]["bg"] == PATH:
                    self.cells[row][col].configure(bg=EMPTY)

    # ===========================================

    def rebuild(self, rows, cols):

        """
        Rebuild the grid when maze size changes.
        """

        for row in self.cells:

            for cell in row:
                cell.destroy()

        self.rows = rows
        self.cols = cols

        self.start = None
        self.goal = None

        self.cells = []
        self.create_grid()
