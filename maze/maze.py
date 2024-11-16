import pygame
import random

width, height = 1200,900
tile = 30
cols,rows = width // tile, height // tile 
wall_color = pygame.Color('darkorange')
screen_color = pygame.Color('darkslategray')

pygame.init()

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

running = True


class Cell:
  def __init__(self, x , y):
    self.col = x
    self.row = y
    self.visited = False
    self.solver_visited = False
    self.walls = self.generate_walls()
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
    pygame.draw.rect(screen, pygame.Color("saddlebrown"), (x + 2, y + 2 , tile - 2, tile - 2))

  def draw(self):
    x,y = self.col * tile, self.row * tile
    if self.solver_visited:
      pygame.draw.rect(screen, pygame.Color("black"), (x, y, tile, tile))
      pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect(x + tile /4, y + tile /4 , tile / 2 , tile /2 ))
    elif self.visited:
      pygame.draw.rect(screen, pygame.Color("black"), (x, y, tile, tile))

    for wall in self.walls.values():
      if wall != None:
        pygame.draw.line(screen , wall_color, wall["s"], wall["e"])

  def get_all_neibor_cells(self):
    return {
      "top": maze.get_neibor_cell(self.col , self.row - 1),
      "bottom": maze.get_neibor_cell(self.col, self.row + 1),
      "right": maze.get_neibor_cell(self.col + 1, self.row),
      "left": maze.get_neibor_cell(self.col - 1, self.row)
    }


class Maze:
  def __init__(self):
    self.cells = [Cell(col , row) for col in range(cols) for row in range(rows)]
    self.stacks = [[self.cells[0]]]
    self.doubled_rows = []

  def select_next_cell(self, current_cell):
    all_neibors = current_cell.get_all_neibor_cells()
    not_visited_neibors = [n for n in all_neibors.values() if n and not n.visited]

    if len(not_visited_neibors) > 0:
      next_cell = random.choice(not_visited_neibors)
      self.remove_walls(current_cell, next_cell)
      next_cell.visited = True
      return next_cell

  def remove_walls(self, cell1 , cell2):
    for nw in cell2.walls:
      for cw in cell1.walls:
        if cell2.walls[nw] != None and cell2.walls[nw] == cell1.walls[cw]:
          pygame.draw.line(screen , screen_color, cell2.walls[nw]["s"], cell2.walls[nw]["e"])
          cell2.walls[nw] = None 
          cell1.walls[cw] = None
          cell2.solver_walls[nw] = None 
          cell1.solver_walls[cw] = None

  def draw_cells(self):
    for c in self.cells:
      c.draw()

  def move(self):
    for stack in self.stacks:
      if len(stack) <= 0:
        continue

      current_cell = stack.pop()
      current_cell.visited = True
      current_cell.draw_as_current_cell()

      next_cell = self.select_next_cell(current_cell)
      if next_cell:
        stack.append(current_cell)
        stack.append(next_cell)
      # if current_cell.row % 2 == 0 and current_cell.row not in self.doubled_rows:
      #   another_cell = self.select_next_cell(current_cell)
      #   if another_cell:
      #     self.doubled_rows.append(current_cell.row)
      #     self.stacks.append([another_cell])

  def is_maze_complete(self):
    empty_stacks = [s for s in self.stacks if len(s) <= 0]
    return len(empty_stacks) == len(self.stacks)
  
  def is_neibor_cell_exists(self, x, y):
    return y < rows and y >= 0 and x < cols and x >= 0

  def get_neibor_cell(self, x, y):
    if self.is_neibor_cell_exists(x, y):
      cell = self.cells[x * rows + y]
      return cell

maze = Maze()

while running:
  screen.fill(screen_color)
  for event in pygame.event.get():
    running = event.type != pygame.QUIT

  maze.draw_cells()
  maze.move()

  clock.tick(60)
  pygame.display.flip()

  if maze.is_maze_complete():
    break

class MazeSolver:
  def __init__(self):
    self.cells = maze.cells
    self.stack = [self.cells[0]]
    self.final_cell = self.cells[-1]

  def move(self):
    if len(self.stack) <= 0:
      return

    current_cell = self.stack.pop()
    current_cell.solver_visited = True
    current_cell.draw_as_current_cell()


    if current_cell == self.final_cell:
      self.stack.append(current_cell)
      return

    next_cell = self.select_next_cell(current_cell)
    if next_cell:
      self.stack.append(current_cell)
      self.stack.append(next_cell)
    else:
      current_cell.solver_visited = False
      current_cell.solver_walls = current_cell.generate_walls()

  def select_next_cell(self, cur_cell):
    neibor_cells = cur_cell.get_all_neibor_cells()
    possible_neibors = []
    if neibor_cells["top"] and cur_cell.solver_walls["top"] == None and neibor_cells["top"].solver_walls["bottom"] == None:
      possible_neibors.append(neibor_cells["top"])
    if neibor_cells["right"] and cur_cell.solver_walls["right"] == None and neibor_cells["right"].solver_walls["left"] == None:
      possible_neibors.append(neibor_cells["right"])
    if neibor_cells["bottom"] and cur_cell.solver_walls["bottom"] == None and neibor_cells["bottom"].solver_walls["top"] == None:
      possible_neibors.append(neibor_cells["bottom"])
    if neibor_cells["left"] and cur_cell.solver_walls["left"] == None and neibor_cells["left"].solver_walls["right"] == None:
      possible_neibors.append(neibor_cells["left"])

    x = [n for n in possible_neibors if not n.solver_visited]
    closest_cell_to_goal = None
    if len(x) > 0:
      for cell in x:
        if closest_cell_to_goal == None:
          closest_cell_to_goal = cell
        elif (
          abs(cell.col - self.final_cell.col) <= abs(closest_cell_to_goal.col - self.final_cell.col) and 
          abs(cell.row - self.final_cell.row) <= abs(closest_cell_to_goal.row - self.final_cell.row)
        ):
          closest_cell_to_goal = cell
    return closest_cell_to_goal

maze_solver = MazeSolver()

while running:
  screen.fill(screen_color)
  for event in pygame.event.get():
    running = event.type != pygame.QUIT

  maze.draw_cells()
  maze_solver.move()

  clock.tick(30)
  pygame.display.flip()


pygame.quit()
