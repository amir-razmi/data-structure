operator_priority = {"-": 1 , "+": 1, "*" : 2, "/": 2, "^": 3 , "(": 4}
operators = ["-","+","*","/","^","(",")"]

def infix_to_postfix(infix):
  postfix = ""
  stack = []
  for item in infix:
    if operators.count(item) == 0:
      postfix += item
    elif item == ")":
      while True:
        if len(stack) == 0:
          break
        last_stack = stack.pop()
        if last_stack == "(":
          break
        postfix += last_stack
    else:
      while True:
        if len(stack) == 0 or stack[-1] == "(" or operator_priority[item] > operator_priority[stack[-1]] or item == "^":
          stack.append(item)
          break
        postfix += stack.pop()

  for _ in range(len(stack)):
    postfix += stack.pop()

  return postfix
def postfix_to_infix(postfix):
  stack = []
  for item in postfix:
    if operators.count(item) == 0:
      stack.append(item)
    else:
      l = stack.pop()
      ll = stack.pop()
      stack.append(f"({ll}{item}{l})")

  return stack[0]

def infix_to_prefix(infix):
  prefix = ""
  stack = []
  for item in infix[::-1]:
    if operators.count(item) == 0:
      prefix = item + prefix
    elif item == "(":
      while True:
        if len(stack) == 0:
          break
        last_stack = stack.pop()
        if last_stack == ")":
          break
        prefix = last_stack + prefix
    else:
      while True:
        if len(stack) == 0 or stack[-1] == ")" or (operator_priority[item] >= operator_priority[stack[-1]] and stack[-1] != "^"):
          stack.append(item)
          break
        prefix = stack.pop() + prefix

  for _ in range(len(stack)):
    prefix = stack.pop() + prefix

  return prefix
def prefix_to_infix(prefix):
  stack = []
  for item in prefix[::-1]:
    if operators.count(item) == 0:
      stack.append(item)
    else:
      l = stack.pop()
      ll = stack.pop()
      stack.append(f"({l}{item}{ll})")

  return stack[0]

def postfix_to_prefix(postfix):
  infix = postfix_to_infix(postfix)
  return infix_to_prefix(infix)
def prefix_to_postfix(prefix):
  infix = prefix_to_infix(prefix)
  return infix_to_postfix(infix)
