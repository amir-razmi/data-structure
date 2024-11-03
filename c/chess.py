from PIL import Image, ImageTk
from tkinter import Canvas, Tk

rows = int(input("Enter rows : "))
square_size = 80
colors = ['#F0D9B5', '#B58863']

w = Tk()
w.title("N-Queen")
canvas = Canvas(w, width=square_size * rows, height=square_size * rows, bg="white")
canvas.pack()
original_image = Image.open("queen.png").convert("RGBA").resize((int(square_size*0.8), int(square_size*0.8)), 1)
tk_image = ImageTk.PhotoImage(original_image)
for row in range(rows):
  for col in range(rows):
    x1,y1 = col * square_size, row * square_size
    x2,y2 = x1 + square_size, y1 + square_size
    color = colors[(row + col) % 2]
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)



def generate_queens(coords, page):
  ids = []
  for [x,y] in coords:
    id = canvas.create_image(square_size * x, square_size * y, anchor='nw', image=tk_image)
    ids.append(id)
  text = canvas.create_text(20,20, font=50, text=f"{page}",)
  ids.append(text)
  return ids

all_possible_solutions = []
def tree(row , coords = []):
  if(row < 0):
    return
  for col in range(rows):
    is_column_used = False
    for [x,y] in coords:
      if x == col or abs(x - col) == abs(y - row):
        is_column_used = True
        break
    if is_column_used == True:
      continue

    new_coords = coords.copy()
    new_coords.append([col,row])
    if row == 0:
      all_possible_solutions.append(new_coords)
      return
    tree(row - 1 , coords=new_coords)
tree(rows -1)

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
