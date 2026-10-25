import tkinter as tk
from constants import *
from maze import MazeGrid
from astar import AStarSolver

class MazeGUI:

    def __init__(self):

        # ---------------- Window ----------------

        self.window = tk.Tk()

        self.window.title(WINDOW_TITLE)

        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self.window.configure(bg=BACKGROUND)

        self.window.resizable(True, True)

        self.fullscreen = False

        # ---------------- Variables ----------------

        self.current_tool = "Wall"

        self.maze = None

        self.status_label = None

        self.selected_tool_label = None

        self.tool_buttons = {}

        self.maze_size_label = None

        self.path_length_label = None

        self.result_label = None

        # ---------------- Build UI ----------------

        self.create_layout()

    # =====================================================

    def create_layout(self):

        # ---------------- Header ----------------

        header = tk.Frame(
            self.window,
            bg=HEADER,
            height=70,
            bd=0,
            highlightthickness=1,
            highlightbackground=PANEL_BORDER
        )

        header.pack(fill="x", padx=12, pady=(12, 0))

        tk.Label(
            header,
            text="MazeMind AI",
            bg=HEADER,
            fg=TEXT,
            font=TITLE_FONT
        ).pack(pady=(14, 4))

        tk.Label(
            header,
            text="Interactive maze builder with A* pathfinding",
            bg=HEADER,
            fg="#CBD5E1",
            font=SUBTEXT_FONT
        ).pack()

        control_frame = tk.Frame(
            header,
            bg=HEADER
        )

        control_frame.place(relx=0.98, rely=0.5, anchor="e")

        fullscreen_button = tk.Button(
            control_frame,
            text="⛶",
            bg=HEADER,
            fg=TEXT,
            font=("Segoe UI", 10, "bold"),
            bd=0,
            activebackground=HEADER,
            activeforeground=TEXT,
            cursor="hand2",
            command=self.toggle_fullscreen
        )

        fullscreen_button.pack(side="right", padx=(0, 8))

        minimize_button = tk.Button(
            control_frame,
            text="—",
            bg=HEADER,
            fg=TEXT,
            font=("Segoe UI", 10, "bold"),
            bd=0,
            activebackground=HEADER,
            activeforeground=TEXT,
            cursor="hand2",
            command=self.minimize_window
        )

        minimize_button.pack(side="right")

        # ---------------- Main ----------------

        self.main_frame = tk.Frame(
            self.window,
            bg=BACKGROUND
        )

        self.main_frame.pack(
            padx=12,
            pady=12,
            fill="both",
            expand=True
        )

        # ---------------- Left Panel ----------------

        self.left_panel = tk.Frame(
            self.main_frame,
            bg=LEFT_PANEL,
            width=290,
            bd=0,
            highlightthickness=1,
            highlightbackground=PANEL_BORDER
        )

        self.left_panel.pack(
            side="left",
            fill="y"
        )

        self.left_panel.pack_propagate(False)

        # ---------------- Center Panel ----------------

        self.center_panel = tk.Frame(
            self.main_frame,
            bg=CENTER_PANEL,
            bd=1,
            relief="flat",
            highlightthickness=1,
            highlightbackground=PANEL_BORDER
        )

        self.center_panel.pack(
            side="left",
            fill="both",
            expand=True,
            padx=12
        )

        # ---------------- Right Panel ----------------

        self.right_panel = tk.Frame(
            self.main_frame,
            bg=RIGHT_PANEL,
            width=290,
            bd=0,
            highlightthickness=1,
            highlightbackground=PANEL_BORDER
        )

        self.right_panel.pack(
            side="right",
            fill="y"
        )

        self.right_panel.pack_propagate(False)

        self.build_left_panel()

        self.build_center_panel()

        self.build_right_panel()

    # =====================================================

    def build_left_panel(self):

        tk.Label(
            self.left_panel,
            text="CONTROLS",
            bg=LEFT_PANEL,
            fg=TITLE,
            font=SUBTITLE_FONT
        ).pack(pady=(24, 14))

        tk.Label(
            self.left_panel,
            text="Maze Size",
            bg=LEFT_PANEL,
            fg=TEXT,
            font=SECTION_FONT
        ).pack()

        self.size_var = tk.StringVar(value="10 x 10")

        option = tk.OptionMenu(
            self.left_panel,
            self.size_var,
            "5 x 5",
            "8 x 8",
            "10 x 10",
            "12 x 12",
            "15 x 15",
            command=self.update_size
        )

        option.config(
            width=16,
            bg=BUTTON,
            fg="white",
            font=NORMAL_FONT,
            relief="flat",
            activebackground=BUTTON_ACTIVE,
            activeforeground="white",
            highlightthickness=0
        )

        option.pack(pady=12)

        tk.Frame(self.left_panel, bg=GRID, height=1).pack(fill="x", padx=16, pady=10)

        tk.Label(
            self.left_panel,
            text="Choose a tool, set Start and Goal, draw walls, then solve.",
            bg=LEFT_PANEL,
            fg=SECONDARY_TEXT,
            font=SUBTEXT_FONT,
            wraplength=240,
            justify="left"
        ).pack(pady=(0, 20), padx=16)

        tk.Label(
            self.left_panel,
            text="Tools",
            bg=LEFT_PANEL,
            fg=TEXT,
            font=SUBTITLE_FONT
        ).pack(pady=(0, 14))

        self.tool_buttons = {}

        tools = [
            "Start",
            "Goal",
            "Wall",
            "Erase"
        ]

        for tool in tools:

            button = tk.Button(
                self.left_panel,
                text=tool,
                width=18,
                bg=BUTTON,
                fg="white",
                font=BUTTON_FONT,
                relief="flat",
                activebackground=BUTTON_ACTIVE,
                activeforeground="white",
                cursor="hand2",
                command=lambda t=tool: self.select_tool(t)
            )

            button.pack(pady=5)

            self.tool_buttons[tool] = button

        self.update_tool_buttons()

        self.solve_button = tk.Button(
            self.left_panel,
            text="Solve Maze",
            width=18,
            bg="#16A34A",
            fg="white",
            font=BUTTON_FONT,
            relief="flat",
            activebackground="#15803D",
            activeforeground="white",
            cursor="hand2",
            command=self.solve_maze
        )

        self.solve_button.pack(pady=(24, 10))

        self.reset_button = tk.Button(
            self.left_panel,
            text="Reset Maze",
            width=18,
            bg="#2563EB",
            fg="white",
            font=BUTTON_FONT,
            relief="flat",
            activebackground="#1D4ED8",
            activeforeground="white",
            cursor="hand2",
            command=self.reset_maze
        )

        self.reset_button.pack(pady=5)

        self.clear_path_button = tk.Button(
            self.left_panel,
            text="Clear Path",
            width=18,
            bg="#F59E0B",
            fg="white",
            font=BUTTON_FONT,
            relief="flat",
            activebackground="#D97706",
            activeforeground="white",
            cursor="hand2",
            command=self.clear_path
        )

        self.clear_path_button.pack(pady=5)

        tk.Frame(self.left_panel, bg=GRID, height=1).pack(fill="x", padx=16, pady=16)

        tk.Label(
            self.left_panel,
            text="Tip: Use the Erase tool to clear mistakes quickly.",
            bg=LEFT_PANEL,
            fg=SECONDARY_TEXT,
            font=SUBTEXT_FONT,
            wraplength=240,
            justify="left"
        ).pack(padx=16)

            # =====================================================

    def build_center_panel(self):

        tk.Label(
            self.center_panel,
            text="Maze Grid",
            bg=CENTER_PANEL,
            fg=TEXT,
            font=SUBTITLE_FONT
        ).pack(pady=15)

        grid_container = tk.Frame(
            self.center_panel,
            bg=CARD,
            bd=0,
            relief="flat",
            highlightthickness=1,
            highlightbackground=PANEL_BORDER
        )

        grid_container.pack(padx=16, pady=16, fill="both", expand=True)

        self.grid_frame = tk.Frame(
            grid_container,
            bg=CARD
        )

        self.grid_frame.pack(padx=28, pady=28, expand=True)

        tk.Label(
            self.center_panel,
            text="Use Start and Goal tools first, then draw walls and solve.",
            bg=CENTER_PANEL,
            fg=SECONDARY_TEXT,
            font=SUBTEXT_FONT,
            wraplength=520,
            justify="center"
        ).pack(pady=(0, 16))

        # Create Maze Grid
        self.maze = MazeGrid(self.grid_frame)

    # =====================================================

    def build_right_panel(self):

        tk.Label(
            self.right_panel,
            text="STATUS",
            bg=RIGHT_PANEL,
            fg=STATUS,
            font=SUBTITLE_FONT
        ).pack(pady=20)

        self.status_label = tk.Label(
            self.right_panel,
            text="Status : Ready",
            bg=RIGHT_PANEL,
            fg="white",
            font=NORMAL_FONT,
            anchor="w",
            justify="left"
        )

        self.status_label.pack(fill="x", padx=20, pady=10)

        tk.Label(
            self.right_panel,
            text="Algorithm : A* Search",
            bg=RIGHT_PANEL,
            fg="white",
            font=NORMAL_FONT
        ).pack(anchor="w", padx=20, pady=(10, 5))

        self.maze_size_label = tk.Label(
            self.right_panel,
            text=f"Maze Size : {self.size_var.get()}",
            bg=RIGHT_PANEL,
            fg="white",
            font=NORMAL_FONT
        )

        self.maze_size_label.pack(anchor="w", padx=20, pady=5)

        tk.Label(
            self.right_panel,
            text="Legend",
            bg=RIGHT_PANEL,
            fg=TEXT,
            font=SECTION_FONT
        ).pack(anchor="w", padx=20, pady=(10, 6))

        legend_frame = tk.Frame(self.right_panel, bg=RIGHT_PANEL)
        legend_frame.pack(anchor="w", padx=20, pady=(0, 10), fill="x")

        for label_text, color in [
            ("Start", START),
            ("Goal", GOAL),
            ("Path", PATH),
            ("Wall", WALL)
        ]:
            sample = tk.Frame(legend_frame, bg=color, width=18, height=18, bd=1, relief="solid")
            sample.pack(side="left", padx=(0, 6), pady=2)
            tk.Label(
                legend_frame,
                text=label_text,
                bg=RIGHT_PANEL,
                fg="white",
                font=("Segoe UI", 9)
            ).pack(side="left", padx=(0, 18))

        self.selected_tool_label = tk.Label(
            self.right_panel,
            text=f"Selected Tool : {self.current_tool}",
            bg=RIGHT_PANEL,
            fg="white",
            font=NORMAL_FONT
        )

        self.selected_tool_label.pack(anchor="w", padx=20, pady=5)

        self.path_length_label = tk.Label(
            self.right_panel,
            text="Path Length : -",
            bg=RIGHT_PANEL,
            fg="white",
            font=NORMAL_FONT
        )

        self.path_length_label.pack(anchor="w", padx=20, pady=5)

        self.result_label = tk.Label(
            self.right_panel,
            text="Result : Waiting...",
            bg=RIGHT_PANEL,
            fg="white",
            font=NORMAL_FONT
        )

        self.result_label.pack(anchor="w", padx=20, pady=5)

            # =====================================================

    def select_tool(self, tool):

        self.current_tool = tool

        if self.maze is not None:
            self.maze.set_tool(tool)

        self.update_tool_buttons()

        if self.maze is not None:
            self.maze.clear_path()

        if self.status_label is not None:
            self.status_label.config(
                text=f"Status : {tool} Tool Selected"
            )

        if self.selected_tool_label is not None:
            self.selected_tool_label.config(
                text=f"Selected Tool : {tool}"
            )

    # =====================================================

    def update_tool_buttons(self):

        for tool, button in self.tool_buttons.items():

            button.config(bg=BUTTON_ACTIVE if tool == self.current_tool else BUTTON)

    # =====================================================

    def update_size(self, value):

        if not value:
            return

        try:
            rows, cols = map(int, value.split(" x "))
        except ValueError:
            return

        self.maze.rebuild(rows, cols)

        self.maze_size_label.config(text=f"Maze Size : {value}")

        self.selected_tool_label.config(text=f"Selected Tool : {self.current_tool}")

        self.path_length_label.config(text="Path Length : -")

        self.result_label.config(text="Result : Waiting...")

        if self.status_label is not None:
            self.status_label.config(
                text=f"Status : Maze size set to {value}"
            )

    # =====================================================

    def reset_maze(self):

        self.maze.reset_grid()

        self.path_length_label.config(text="Path Length : -")

        self.result_label.config(text="Result : Waiting...")

        if self.status_label is not None:
            self.status_label.config(
                text="Status : Maze reset"
            )

        if self.selected_tool_label is not None:
            self.selected_tool_label.config(
                text=f"Selected Tool : {self.current_tool}"
            )

    # =====================================================

    def clear_path(self):

        self.maze.clear_path()

        self.path_length_label.config(text="Path Length : -")

        self.result_label.config(text="Result : Path cleared")

        if self.status_label is not None:
            self.status_label.config(
                text="Status : Path cleared"
            )

        if self.selected_tool_label is not None:
            self.selected_tool_label.config(
                text=f"Selected Tool : {self.current_tool}"
            )

    # =====================================================

    def solve_maze(self):

        maze = self.maze.get_maze()

        start = self.maze.get_start()

        goal = self.maze.get_goal()

        if start is None or goal is None:

            if self.status_label is not None:
                self.status_label.config(
                    text="Status : Select both Start and Goal"
                )

            if self.result_label is not None:
                self.result_label.config(
                    text="Result : Select both Start and Goal"
                )

            return

        solver = AStarSolver(
            maze,
            start,
            goal
        )

        path = solver.solve()

        self.maze.color_path(path)

        if path is None:
            self.status_label.config(
                text="Status : No path found"
            )
            self.result_label.config(
                text="Result : No path found"
            )
            self.path_length_label.config(text="Path Length : -")
        else:
            self.status_label.config(
                text=f"Status : Path found ({len(path)} steps)"
            )
            self.result_label.config(
                text="Result : Path found successfully"
            )
            self.path_length_label.config(
                text=f"Path Length : {len(path)}"
            )

    # =====================================================

    def toggle_fullscreen(self):

        self.fullscreen = not self.fullscreen

        self.window.attributes("-fullscreen", self.fullscreen)

        if self.status_label is not None:
            self.status_label.config(
                text="Status : Full screen enabled" if self.fullscreen else "Status : Full screen disabled"
            )

    # =====================================================

    def minimize_window(self):

        self.window.iconify()

    # =====================================================

    def run(self):

        self.window.mainloop()


# =====================================================
# Program Entry
# =====================================================

if __name__ == "__main__":

    app = MazeGUI()

    app.run()

