import pygame
import random

width, height = 1200,750
tile = 50
cols,rows = width // tile, height // tile 
wall_color = pygame.Color('darkorange')
screen_color = pygame.Color('darkslategray')
current_cell_color = pygame.Color("saddlebrown")
black = pygame.Color("black")
white = pygame.Color("white")

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

class Cell:
  def __init__(self, x , y):
    self.col = x
    self.row = y
    self.generator_visited = False
    self.walls = self.generate_walls()
    self.solver_visited = False
    self.solver_walls = self.generate_walls()

  def generate_walls(self):
    x,y = self.col * tile, self.row * tile
    return {
      "top": {"s": (x, y), "e": (x + tile , y )},
      "right": {"s": (x + tile, y), "e": (x + tile, y + tile)},
      "bottom": {"s": (x, y + tile), "e": (x + tile, y + tile)},
      "left": {"s": (x, y), "e": (x, y + tile)}
    }

  def draw_as_current_cell(self):
    x,y = self.col * tile, self.row * tile
    pygame.draw.rect(screen, current_cell_color, (x + 2, y + 2 , tile - 2, tile - 2))

  def draw(self):
    x,y = self.col * tile, self.row * tile
    if self.solver_visited:
      pygame.draw.rect(screen, black, (x, y, tile, tile))
      pygame.draw.rect(screen, white, pygame.Rect(x + tile/4, y + tile/4 , tile/2 , tile/2 ))
    elif self.generator_visited:
      pygame.draw.rect(screen, black, (x, y, tile, tile))

    for wall in self.walls.values():
      if wall != None:
        pygame.draw.line(screen , wall_color, wall["s"], wall["e"])

  def get_all_neighbor_cells(self):
    return {
      "top": maze.get_cell_by_coords(self.col , self.row - 1),
      "bottom": maze.get_cell_by_coords(self.col, self.row + 1),
      "right": maze.get_cell_by_coords(self.col + 1, self.row),
      "left": maze.get_cell_by_coords(self.col - 1, self.row)
    }


class Maze:
  def __init__(self, hard_mode = False):
    self.hard_mode = hard_mode
    self.cells = [Cell(col , row) for col in range(cols) for row in range(rows)]
    self.stacks = [[self.cells[0]]]
    self.doubled_rows = []
    self.doubled_cols = []

  def select_next_cell(self, cur_cell):
    all_neighbors = cur_cell.get_all_neighbor_cells()
    unvisited_neighbors = [n for n in all_neighbors.values() if n and not n.generator_visited]

    if len(unvisited_neighbors) > 0:
      next_cell = random.choice(unvisited_neighbors)
      self.remove_walls(cur_cell, next_cell)
      next_cell.generator_visited = True
      return next_cell

  def remove_walls(self, cell_1 , cell_2):
    for nw in cell_2.walls:
      for cw in cell_1.walls:
        if cell_2.walls[nw] != None and cell_2.walls[nw] == cell_1.walls[cw]:
          pygame.draw.line(screen , screen_color, cell_2.walls[nw]["s"], cell_2.walls[nw]["e"])
          cell_2.walls[nw] = None 
          cell_1.walls[cw] = None
          cell_2.solver_walls[nw] = None 
          cell_1.solver_walls[cw] = None

  def draw_cells(self):
    for c in self.cells:
      c.draw()

  def move_generators(self):
    for stack in self.stacks:
      if len(stack) <= 0:
        continue

      cur_cell = stack.pop()
      cur_cell.generator_visited = True
      cur_cell.draw_as_current_cell()

      next_cell = self.select_next_cell(cur_cell)
      if next_cell:
        stack.append(cur_cell)
        stack.append(next_cell)
      if self.hard_mode:
        if cur_cell.row % 4 == 0 and cur_cell.row not in self.doubled_rows:
          another_cell = self.select_next_cell(cur_cell)
          if another_cell:
            self.doubled_rows.append(cur_cell.row)
            self.stacks.append([another_cell])
        elif cur_cell.col % 3 == 0 and cur_cell.col not in self.doubled_cols:
          another_cell = self.select_next_cell(cur_cell)
          if another_cell:
            self.doubled_cols.append(cur_cell.col)
            self.stacks.append([another_cell])

  def is_maze_created(self):
    empty_stacks = [s for s in self.stacks if len(s) <= 0]
    return len(empty_stacks) == len(self.stacks)
  
  def is_cell_exists(self, x, y):
    return y < rows and y >= 0 and x < cols and x >= 0

  def get_cell_by_coords(self, x, y):
    if self.is_cell_exists(x, y):
      return self.cells[x * rows + y]

class MazeSolver:
  def __init__(self):
    self.cells = maze.cells
    self.stack = [self.cells[0]]
    self.goal = self.cells[-1]
    self.solved = False

  def move_solver(self):
    if self.solved or len(self.stack) <= 0:
      return

    cur_cell = self.stack.pop()
    cur_cell.solver_visited = True
    cur_cell.draw_as_current_cell()

    if cur_cell == self.goal:
      self.stack.append(cur_cell)
      self.solved = True
      return

    next_cell = self.select_next_cell(cur_cell)
    if next_cell:
      self.stack.append(cur_cell)
      self.stack.append(next_cell)
    else:
      cur_cell.solver_visited = False
      cur_cell.solver_walls = cur_cell.generate_walls()

  def select_next_cell(self, cur_cell):
    neighbor_cells = cur_cell.get_all_neighbor_cells()
    possible_neighbors = []
    if neighbor_cells["top"] and cur_cell.solver_walls["top"] == None and neighbor_cells["top"].solver_walls["bottom"] == None:
      possible_neighbors.append(neighbor_cells["top"])
    if neighbor_cells["right"] and cur_cell.solver_walls["right"] == None and neighbor_cells["right"].solver_walls["left"] == None:
      possible_neighbors.append(neighbor_cells["right"])
    if neighbor_cells["bottom"] and cur_cell.solver_walls["bottom"] == None and neighbor_cells["bottom"].solver_walls["top"] == None:
      possible_neighbors.append(neighbor_cells["bottom"])
    if neighbor_cells["left"] and cur_cell.solver_walls["left"] == None and neighbor_cells["left"].solver_walls["right"] == None:
      possible_neighbors.append(neighbor_cells["left"])

    unvisited_neighbors = [n for n in possible_neighbors if not n.solver_visited]
    closest_cell_to_goal = None
    if len(unvisited_neighbors) > 0:
      for cell in unvisited_neighbors:
        if closest_cell_to_goal == None:
          closest_cell_to_goal = cell
        elif (
          abs(cell.col - self.goal.col) <= abs(closest_cell_to_goal.col - self.goal.col) and 
          abs(cell.row - self.goal.row) <= abs(closest_cell_to_goal.row - self.goal.row)
        ):
          closest_cell_to_goal = cell
    return closest_cell_to_goal



maze = Maze(hard_mode=False)
maze_solver = MazeSolver()

# a = True
# while a :
#   maze.move_generators()
#   a = not maze.is_maze_created()
# b = True
# while b:
#   maze_solver.move_solver()
#   b = not maze_solver.solved

generating_maze = True
while generating_maze:
  screen.fill(screen_color)
  for event in pygame.event.get():
    generating_maze = event.type != pygame.QUIT

  maze.draw_cells()
  maze.move_generators()

  clock.tick(60)
  pygame.display.flip()

  generating_maze = not maze.is_maze_created()

solving_maze = True
while solving_maze:
  screen.fill(screen_color)
  for event in pygame.event.get():
    solving_maze = event.type != pygame.QUIT

  maze.draw_cells()
  maze_solver.move_solver()

  clock.tick(60)
  pygame.display.flip()


pygame.quit()
