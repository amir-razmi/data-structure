
rows = int(input("Enter rows : "))
square_size = 50
colors = ['#F0D9B5', '#B58863']

from tkinter import Canvas, Tk, PhotoImage
from PIL import Image, ImageTk

w = Tk()
w.title("Pomodoro")
canvas = Canvas(w, width=square_size * rows, height=square_size * rows, bg="white")
canvas.pack()
original_image = Image.open("queen.png").convert("RGBA").resize((int(square_size*0.8), int(square_size*0.8)), 1)
tk_image = ImageTk.PhotoImage(original_image)
for row in range(rows):
  for col in range(rows):
    x1 = col * square_size
    y1 = row * square_size
    x2 = x1 + square_size
    y2 = y1 + square_size
    color = colors[(row + col) % 2]
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)


generated = False
def generate_queens(posses):
  global generated
  if generated == True:
    return
  generated = True

  for p in range(len(posses)):
    canvas.create_image(square_size * posses[p][0], square_size * posses[p][1], anchor='nw', image=tk_image)

def loop(row , logs = "", l = 1 , posses = []):
  for col in range(rows):
    if(row >= 0):
      is_wrong_pos_exists = False
      for p in range(len(posses)):
        pv = posses[p]
        if pv[0] == col or pv[1] == row or abs(pv[0] - col) == abs(pv[1] - row):
          is_wrong_pos_exists = True
          break
      if is_wrong_pos_exists == True:
        continue
      new_posses = posses.copy()
      new_posses.append([col,row])
      loop(row - 1 , l=l + 1 , logs=f"{logs} -> {l}({col})", posses=new_posses)
      if(l == rows):
        print(new_posses)
        generate_queens(new_posses)
        return 

loop(rows -1)
w.mainloop()
