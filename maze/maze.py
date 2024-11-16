import pygame
import random

width, height = 1200,900
tile = 10
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
    x,y = x * tile, y * tile
    self.walls = {
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

  def get_neibor_cell(self, x, y):
    if self.col == 0 and self.row == 0:
      print(x,y)
    if y < rows and y >= 0 and x < cols and x >= 0:
      cell = cells[x * rows + y]
      if not cell.visited:
        return cell

  def select_next_cell(self):
    top = self.get_neibor_cell(self.col , self.row + 1)
    bottom = self.get_neibor_cell(self.col, self.row - 1)
    right = self.get_neibor_cell(self.col + 1, self.row)
    left = self.get_neibor_cell(self.col - 1, self.row)

    all_neibor_coords = []
    if top != None:
      all_neibor_coords.append(top)
    if bottom != None:
      all_neibor_coords.append(bottom)
    if right != None:
      all_neibor_coords.append(right)
    if left != None:
      all_neibor_coords.append(left)
    if self.col == 0 and self.row == 0:
      print(all_neibor_coords)
    if len(all_neibor_coords) > 0:
      next_cell = random.choice(all_neibor_coords)
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

cells = [Cell(col , row) for col in range(cols) for row in range(rows)]


stacks = [[cells[0]]]
cells[0].visited = True
for _ in range(int(len(cells) / 500)):
  not_visited_cells = [cell for cell in cells if not cell.visited]
  if len(not_visited_cells) > 0:
    random_cell = random.choice(not_visited_cells)
    random_cell.visited = True
    stacks.append([random_cell])


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



pygame.quit()
