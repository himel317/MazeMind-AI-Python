import heapq


class AStarSolver:

    def __init__(self, maze, start, goal):

        self.maze = maze

        self.start = start

        self.goal = goal

        self.rows = len(maze)

        self.cols = len(maze[0])

    # =======================================

    def heuristic(self, current, goal):

        """
        Manhattan Distance
        """

        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    # =======================================

    def valid(self, row, col):

        return (

            0 <= row < self.rows

            and

            0 <= col < self.cols

            and

            self.maze[row][col] == 0

        )

    # =======================================

    def neighbors(self, node):

        row, col = node

        directions = [

            (-1, 0),

            (1, 0),

            (0, -1),

            (0, 1)

        ]

        result = []

        for dr, dc in directions:

            nr = row + dr

            nc = col + dc

            if self.valid(nr, nc):

                result.append((nr, nc))

        return result
        # =======================================

    def solve(self):

        open_list = []

        heapq.heappush(
            open_list,
            (0, self.start)
        )

        came_from = {}

        g_score = {
            self.start: 0
        }

        f_score = {
            self.start: self.heuristic(
                self.start,
                self.goal
            )
        }

        visited = set()

        while open_list:

            current = heapq.heappop(open_list)[1]

            if current == self.goal:

                return self.reconstruct_path(
                    came_from,
                    current
                )

            visited.add(current)

            for neighbor in self.neighbors(current):

                if neighbor in visited:
                    continue

                tentative_g = g_score[current] + 1

                if (
                    neighbor not in g_score
                    or
                    tentative_g < g_score[neighbor]
                ):

                    came_from[neighbor] = current

                    g_score[neighbor] = tentative_g

                    f_score[neighbor] = (
                        tentative_g
                        +
                        self.heuristic(
                            neighbor,
                            self.goal
                        )
                    )

                    heapq.heappush(
                        open_list,
                        (
                            f_score[neighbor],
                            neighbor
                        )
                    )

        return None
        # =======================================

    def reconstruct_path(self, came_from, current):

        """
        Reconstruct the shortest path
        from goal to start.
        """

        path = [current]

        while current in came_from:

            current = came_from[current]

            path.append(current)

        path.reverse()

        return path