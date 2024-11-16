import pygame
import random

width, height = 1200,900
tile = 100
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

  def draw_current_cell(self):
    x,y = self.col * tile, self.row * tile
    pygame.draw.rect(screen, pygame.Color("saddlebrown"), (x + 2, y + 2 , tile - 2, tile - 2))

  def draw(self):
    x,y = self.col * tile, self.row * tile
    if self.visited:
      pygame.draw.rect(screen, pygame.Color("black"), (x, y, tile, tile))

    for wall in self.walls.values():
      if wall != None:
        pygame.draw.line(screen , wall_color, wall["s"], wall["e"])

  def is_neibor_cell_exists(self, x, y):
    return y < rows and y >= 0 and x < cols and x >= 0

  def get_neibor_cell(self, x, y):
    if self.is_neibor_cell_exists(x, y):
      cell = cells[x * rows + y]
      return cell
  def get_all_neibor_cells(self):
    return {
      "top": self.get_neibor_cell(self.col , self.row - 1),
      "bottom": self.get_neibor_cell(self.col, self.row + 1),
      "right": self.get_neibor_cell(self.col + 1, self.row),
      "left": self.get_neibor_cell(self.col - 1, self.row)
    }

  def select_next_cell(self):
    all_neibors = self.get_all_neibor_cells()
    not_visited_neibors = [neibor for neibor in all_neibors.values() if neibor and not neibor.visited]
    
    if len(not_visited_neibors) > 0:
      next_cell = random.choice(not_visited_neibors)
      self.remove_walls(next_cell)
      next_cell.visited = True
      return next_cell


  def remove_walls(self, next_cell):
    for nw in next_cell.walls:
      for cw in self.walls:
        if next_cell.walls[nw] != None and next_cell.walls[nw] == self.walls[cw]:
          pygame.draw.line(screen , screen_color, next_cell.walls[nw]["s"], next_cell.walls[nw]["e"])
          next_cell.walls[nw] = None 
          self.walls[cw] = None
          next_cell.solver_walls[nw] = None 
          self.solver_walls[cw] = None

cells = [Cell(col , row) for col in range(cols) for row in range(rows)]


stacks = [[cells[0]]]
cells[0].visited = True
# for _ in range(int(len(cells) / 500)):
# for _ in range(1):
#   not_visited_cells = [cell for cell in cells if not cell.visited]
#   if len(not_visited_cells) > 0:
#     random_cell = random.choice(not_visited_cells)
#     random_cell.visited = True
#     stacks.append([random_cell])


while running:
  screen.fill(screen_color)
  for event in pygame.event.get():
    running = event.type != pygame.QUIT

  for c in cells:
    c.draw()

  for stack in stacks:
    if len(stack) <= 0:
      continue

    current_cell = stack.pop()
    current_cell.visited = True
    current_cell.draw_current_cell()

    next_cell = current_cell.select_next_cell()
    if next_cell:
      stack.append(current_cell)
      stack.append(next_cell)

  clock.tick(60)
  pygame.display.flip()

  empty_stacks = [s for s in stacks if len(s) <= 0]
  if len(empty_stacks) == len(stacks):
    break

stack = [cells[0]]
cells[0].solver_visited = True
final_cell = cells[-1]

while running:
  screen.fill(screen_color)
  for event in pygame.event.get():
    running = event.type != pygame.QUIT

  for c in cells:
    c.draw()

  if len(stack) <= 0:
    continue

  current_cell = stack.pop()
  current_cell.solver_visited = True
  current_cell.draw_current_cell()

  clock.tick(3)
  pygame.display.flip()

  if current_cell == final_cell:
    stack.append(current_cell)
    continue


  neibor_cells = current_cell.get_all_neibor_cells()

  possible_neibors = []
  if neibor_cells["top"] and current_cell.solver_walls["top"] == None and neibor_cells["top"].solver_walls["bottom"] == None:
    possible_neibors.append(neibor_cells["top"])
  if neibor_cells["right"] and current_cell.solver_walls["right"] == None and neibor_cells["right"].solver_walls["left"] == None:
    possible_neibors.append(neibor_cells["right"])
  if neibor_cells["bottom"] and current_cell.solver_walls["bottom"] == None and neibor_cells["bottom"].solver_walls["top"] == None:
    possible_neibors.append(neibor_cells["bottom"])
  if neibor_cells["left"] and current_cell.solver_walls["left"] == None and neibor_cells["left"].solver_walls["right"] == None:
    possible_neibors.append(neibor_cells["left"])


  x = [n for n in possible_neibors if not n.solver_visited]
  for i in possible_neibors:
    print("Currnet Cell : " , (current_cell.col, current_cell.row) , " ==> " , (i.col,i.row))
  if len(x) > 0:
    next_cell = random.choice(x)
    stack.append(current_cell)
    stack.append(next_cell)
  else:
    current_cell.solver_walls = current_cell.generate_walls()




pygame.quit()
