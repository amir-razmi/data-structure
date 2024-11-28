import time

N = int(input("How many rows? "))
columns_set = set(range(N))
all_possible_solutions = []


def tree(row=N-1, queens=[]):
  if N > 13 and len(all_possible_solutions): return

  avail_squares = columns_set.copy()
  for [_x,_y] in queens:
    row_distance = abs(_y - row)
    avail_squares.discard(_x - row_distance)
    avail_squares.discard(_x + row_distance)
    avail_squares.discard(_x)

  for x in avail_squares:
    new_queens = [[x,row]] + queens
    if row == 0:
      all_possible_solutions.append(new_queens)
      return
    tree(row - 1, new_queens)

s = time.time()
tree()
e = time.time()

print("Time(s): ", e-s)



##############################################################################
##############################################################################
##############################################################################



from PIL import Image, ImageTk
from tkinter import Canvas, Tk
square_size = 800 // N
colors = ['#F0D9B5', '#B58863']

w = Tk()
w.title("N-Queen")
canvas = Canvas(w, width=square_size * N, height=square_size * N, bg="white")
canvas.pack()
original_image = Image.open("queen.png").convert("RGBA").resize((int(square_size*0.8), int(square_size*0.8)), 1)
tk_image = ImageTk.PhotoImage(original_image)
for row in range(N):
  for col in range(N):
    x1,y1 = col * square_size, row * square_size
    x2,y2 = x1 + square_size, y1 + square_size
    color = colors[(row + col) % 2]
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

def generate_queens(coords, page):
  ids = []
  for [x,y] in coords:
    id = canvas.create_image(square_size * x, square_size * y, anchor='nw', image=tk_image)
    ids.append(id)
  text = canvas.create_text(30,30, font=50, text=f"{page}",)
  ids.append(text)
  return ids

last_generated_index = 0
queens_id = generate_queens(all_possible_solutions[last_generated_index], 1)
def change_slide(event):
  global queens_id,last_generated_index
  for id in queens_id:
    canvas.delete(id)

  if event.keysym == 'Left':
    last_generated_index = (last_generated_index - 1) % len(all_possible_solutions)
  elif event.keysym == 'Right':
    last_generated_index = (last_generated_index + 1) % len(all_possible_solutions)

  queens_id = generate_queens(all_possible_solutions[last_generated_index], last_generated_index + 1)

w.bind("<Left>", change_slide)
w.bind("<Right>", change_slide)

w.mainloop()
