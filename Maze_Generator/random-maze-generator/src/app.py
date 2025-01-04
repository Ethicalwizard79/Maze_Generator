import streamlit as st
import numpy as np
import random
from queue import PriorityQueue

class MazeGenerator:
    """
    A class to generate random mazes using recursive backtracking algorithm.
    
    Attributes:
        width (int): Width of the maze
        height (int): Height of the maze
        maze (numpy.ndarray): 2D array representing the maze
        visited (numpy.ndarray): Tracking visited cells during maze generation
        start (tuple): Starting point coordinates
        end (tuple): Ending point coordinates
    """
    
    def __init__(self, width=21, height=21):
        """
        Initialize the MazeGenerator with specified dimensions.
        
        Args:
            width (int, optional): Maze width. Defaults to 21.
            height (int, optional): Maze height. Defaults to 21.
        """
        self.width = width
        self.height = height
        self.maze = np.zeros((height, width), dtype=int)
        self.visited = np.zeros((height, width), dtype=bool)
        self.start = (0, 0)
        self.end = (height-1, width-1)

    def generate_maze(self):
        """
        Generate a random maze using recursive backtracking.
        
        Returns:
            numpy.ndarray: Generated maze
        """
        # Reset maze and visited arrays
        self.maze = np.zeros((self.height, self.width), dtype=int)
        self.visited = np.zeros((self.height, self.width), dtype=bool)
        
        random.seed(42)  # Consistent random generation
        self.visited[0, 0] = True
        self._carve_passages_from(0, 0)
        
        # Ensure start and end are paths
        self.maze[self.start[0], self.start[1]] = 1
        self.maze[self.end[0], self.end[1]] = 1
        
        return self.maze

    def _carve_passages_from(self, cx, cy):
        """
        Recursive method to carve passages in the maze.
        
        Args:
            cx (int): Current x-coordinate
            cy (int): Current y-coordinate
        """
        # Possible movement directions with step size 2
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            
            # Check if the new cell is within maze bounds and unvisited
            if (0 <= nx < self.width and 
                0 <= ny < self.height and 
                not self.visited[ny, nx]):
                
                self.visited[ny, nx] = True
                self.maze[cy + dy // 2, cx + dx // 2] = 1
                self.maze[ny, nx] = 1
                
                self._carve_passages_from(nx, ny)

    def visualize_maze(self, solution=None):
        """
        Convert maze to a visual representation using emojis.
        
        Args:
            solution (list, optional): Path solution. Defaults to None.
        
        Returns:
            str: Emoji-based maze visualization
        """
        # Create a copy of the maze for visualization
        visual_maze = self.maze.copy()
        
        # Mark start and end points
        visual_maze[self.start[0], self.start[1]] = 3  # Start point
        visual_maze[self.end[0], self.end[1]] = 4      # End point
        
        if solution:
            # Mark solution path
            for x, y in solution:
                if (x, y) != self.start and (x, y) != self.end:
                    visual_maze[x, y] = 2
        
        # Emoji mapping for different cell types
        emoji_map = {
            0: "🧱",  # Wall
            1: "⬜",  # Path
            2: "🟢",  # Solution Path
            3: "🟥",  # Start Point
            4: "🏁"   # End Point
        }
        
        # Convert maze to visual representation
        maze_visual = [
            " ".join(emoji_map[cell] for cell in row)
            for row in visual_maze
        ]
        
        return "\n".join(maze_visual)

class MazeSolver:
    """
    A class to solve mazes using the A* pathfinding algorithm.
    
    Attributes:
        maze (numpy.ndarray): Input maze
        height (int): Maze height
        width (int): Maze width
    """
    
    def __init__(self, maze):
        """
        Initialize the MazeSolver with a given maze.
        
        Args:
            maze (numpy.ndarray): Input maze
        """
        self.maze = maze
        self.height, self.width = maze.shape

    def heuristic(self, a, b):
        """
        Calculate Manhattan distance between two points.
        
        Args:
            a (tuple): First point coordinates
            b (tuple): Second point coordinates
        
        Returns:
            int: Manhattan distance
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, current):
        """
        Find valid neighboring cells for a given cell.
        
        Args:
            current (tuple): Current cell coordinates
        
        Returns:
            list: List of valid neighboring cell coordinates
        """
        x, y = current
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.height and 
                0 <= ny < self.width and 
                self.maze[nx, ny] != 0):  # Can move through paths
                neighbors.append((nx, ny))
        
        return neighbors

    def a_star_solve(self, start=(0, 0), end=None):
        """
        Solve maze using A* pathfinding algorithm.
        
        Args:
            start (tuple, optional): Starting point. Defaults to (0, 0).
            end (tuple, optional): Ending point. Defaults to bottom-right corner.
        
        Returns:
            list: Optimal path from start to end
        """
        if end is None:
            end = (self.height - 1, self.width - 1)

        # Priority queue for A* algorithm
        open_set = PriorityQueue()
        open_set.put((0, start))
        
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, end)}

        while not open_set.empty():
            current = open_set.get()[1]

            if current == end:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path

            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, end)
                    open_set.put((f_score[neighbor], neighbor))

        return None

def main():
    """
    Main function to run the Maze Generator and Solver Streamlit app.
    """
    st.title("🧩 Interactive Maze Generator & Solver")
    
    # Sidebar Configuration
    st.sidebar.header("🎮 Maze Settings")
    width = st.sidebar.slider("Maze Width", 5, 30, 15)
    height = st.sidebar.slider("Maze Height", 5, 30, 15)

    # Initialize session state
    if 'maze_generator' not in st.session_state:
        st.session_state.maze_generator = MazeGenerator(width, height)
        st.session_state.maze = None
        st.session_state.solution = None

    # Generate Maze Button
    if st.sidebar.button("🔀 Generate New Maze"):
        st.session_state.maze_generator = MazeGenerator(width, height)
        st.session_state.maze = st.session_state.maze_generator.generate_maze()
        st.session_state.solution = None

    # Display Generated Maze
    if st.session_state.maze is not None:
        st.subheader("🗺️ Generated Maze")
        maze_visualization = st.session_state.maze_generator.visualize_maze()
        st.text(maze_visualization)

        # Solve Maze Button
        if st.sidebar.button("🧭 Find Optimal Solution"):
            solver = MazeSolver(st.session_state.maze)
            solution = solver.a_star_solve()
            
            if solution:
                st.session_state.solution = solution
                st.success("Optimal path found!")
                
                # Display Solution
                solution_visualization = st.session_state.maze_generator.visualize_maze(solution)
                st.subheader("🏁 Maze Solution")
                st.text(solution_visualization)
                
                # Display Path Length
                st.info(f"Path Length: {len(solution)} steps")
            else:
                st.error("No solution found!")

if __name__ == "__main__":
    main()
