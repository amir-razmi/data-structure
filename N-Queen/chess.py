# Starts from top row to bottom
# On each row, loops on all columns(squares)
# It checks if this square is compatible with previously selected squares
# If it does not, then it will continue to next column
# And if it was ok, then it will go to next row
# If it reaches to the last row, the first compatible square will be selected
# Then it will go to the top row again and tries all this with the next square in top row

rows_count = int(input("How many rows? "))
all_possible_solutions = []

def tree(row , coords = []):
  for col in range(rows_count):
    if len([x for [x,y]in coords if x==col or abs(x-col)==abs(y-row)])!=0:
      continue
    new_coords = [[col,row]] + coords
    if row == 0:
      all_possible_solutions.append(new_coords)
      return
    tree(row - 1 , coords=new_coords)
tree(rows_count - 1)



from PIL import Image, ImageTk
from tkinter import Canvas, Tk
square_size = 80
colors = ['#F0D9B5', '#B58863']

w = Tk()
w.title("N-Queen")
canvas = Canvas(w, width=square_size * rows_count, height=square_size * rows_count, bg="white")
canvas.pack()
original_image = Image.open("queen.png").convert("RGBA").resize((int(square_size*0.8), int(square_size*0.8)), 1)
tk_image = ImageTk.PhotoImage(original_image)
for row in range(rows_count):
  for col in range(rows_count):
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
