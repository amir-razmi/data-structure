operator_priority = {"-": 1 , "+": 1, "*" : 2, "/": 2, "^": 3 , "(": 4, ")": 4}
operators = ["-","+","*","/","^","(",")"]
main_operators = ["-","+","*","/","^"]

def is_operation(value):
  operator_count = 0
  variable_count = 0
  for c in value:
    if main_operators.count(c) != 0:
      operator_count += 1
    elif operators.count(c) == 0:
      variable_count += 1
  if operator_count + 1 != variable_count:
    show_error("Not an operation")
    raise ValueError("Not an operation")

def is_infix(value):
  value = value.replace(" " , "")
  is_operation(value)
  if main_operators.count(value[0]) != 0 or main_operators.count(value[-1]) != 0:
    show_error("Value is not infix")
    raise ValueError("Value is not infix")
  hide_error()

def is_postfix(value):
  value = value.replace(" " , "")
  is_operation(value)
  if main_operators.count(value[0]) != 0 or main_operators.count(value[-1]) == 0:
    show_error("Value is not postfix")
    raise ValueError("Value is not postfix")
  hide_error()

def is_prefix(value):
  value = value.replace(" " , "")
  is_operation(value)
  if main_operators.count(value[0]) == 0 or main_operators.count(value[-1]) != 0:
    show_error("Value is not pretfix")
    raise ValueError("Value is not pretfix")
  hide_error()


def infix_to_postfix(infix):
  is_infix(infix)

  postfix = ""
  stack = []
  for char in infix:
    if operators.count(char) == 0:
      postfix += char
    elif char == ")":
      while True:
        if len(stack) == 0:
          break
        last_stack = stack.pop()
        if last_stack == "(":
          break
        postfix += last_stack
    else:
      while True:
        if len(stack) == 0 or stack[-1] == "(" or operator_priority[char] > operator_priority[stack[-1]] or char == "^":
          stack.append(char)
          break
        postfix += stack.pop()
  for _ in range(len(stack)):
    postfix += stack.pop()
  result_label.config(text=postfix) 

def postfix_to_infix(postfix, return_value = False):
  is_postfix(postfix)

  stack = []
  for char in postfix:
    if operators.count(char) == 0:
      stack.append(char)
    else:
      l = stack.pop()
      ll = stack.pop()
      stack.append(f"({ll}{char}{l})")

  if return_value:
    return stack[0]
  result_label.config(text=stack[0]) 


def infix_to_prefix(infix):
  is_infix(infix)

  prefix = ""
  stack = []
  for char in infix[::-1]:
    if operators.count(char) == 0:
      prefix = char + prefix
    elif char == "(":
      while True:
        if len(stack) == 0:
          break
        last_stack = stack.pop()
        if last_stack == ")":
          break
        prefix = last_stack + prefix
    else:
      while True:
        if len(stack) == 0 or stack[-1] == ")" or (operator_priority[char] >= operator_priority[stack[-1]] and stack[-1] != "^"):
          stack.append(char)
          break
        prefix = stack.pop() + prefix
  for _ in range(len(stack)):
    prefix = stack.pop() + prefix
  result_label.config(text=prefix)

def prefix_to_infix(prefix, return_value=False):
  is_prefix(prefix)

  stack = []
  for char in prefix[::-1]:
    if operators.count(char) == 0:
      stack.append(char)
    else:
      l = stack.pop()
      ll = stack.pop()
      stack.append(f"({l}{char}{ll})")

  if return_value:
    return stack[0]
  result_label.config(text=stack[0]) 


def postfix_to_prefix(postfix):
  infix = postfix_to_infix(postfix, True)
  infix_to_prefix(infix)

def prefix_to_postfix(prefix):
  infix = prefix_to_infix(prefix, True)
  infix_to_postfix(infix)




import tkinter as tk

root = tk.Tk()
root.title("Function Interface")
root.geometry("600x400")
root.configure(bg="#F0F0F0")

text_entry = tk.Entry(root, width=50, font=("Arial", 14))
text_entry.pack(pady=20)

button_frame = tk.Frame(root, bg="#F0F0F0")
button_frame.pack(pady=10)

buttons = [
    ("Infix to Postfix", infix_to_postfix),
    ("Postfix to Infix", postfix_to_infix),
    ("Infix to Prefix", infix_to_prefix),
    ("Prefix to Infix", prefix_to_infix),
    ("Postfix to Prefix", postfix_to_prefix),
    ("Prefix to Postfix", prefix_to_postfix),
]
for i, (text, func) in enumerate(buttons):
    row, col = divmod(i, 2)
    button = tk.Button(
        button_frame,
        text=text,
        width=20,
        height=2,
        font=("Arial", 12),
        bg="#4CAF50",
        fg="white",
        command=lambda f=func: f(text_entry.get())
    )
    button.grid(row=row, column=col, padx=10, pady=10)
result_label = tk.Label(root, text="", font=("Arial", 14), bg="#F0F0F0", fg="#333333")
result_label.pack(pady=20)

def show_error(message):
    error_label.place(x=25, y =50)
    error_label.config(text=message)
def hide_error():
    error_label.config(text="")
    error_label.place_forget()
error_label = tk.Label(root, text="", font=("Arial", 12), fg="red", bg="#F0F0F0", )

def copy_to_clipboard():
    result_text = result_label.cget("text")
    root.clipboard_clear()
    root.clipboard_append(result_text)
    root.update()
copy_button = tk.Button(root, text="Copy Result", command=copy_to_clipboard, bg="#007BFF", fg="white", font=("Arial", 12))
copy_button.place(x=250, y=350)
hide_error()

root.mainloop()
