class Node:
  def __init__(self, data):
    self.data = data
    self.prev = None
    self.next = None

class DoublyLinkedList :
  def __init__(self):
    self.head = None
    self.tail = None

  def display(self):
    print("HEAD : " , self.head.data)
    print("TAIL : " , self.tail.data)
    n = self.head
    while n != None:
      print(n.data, end=" => ")
      n = n.next
    print("_")

  def append(self, data):
    node = Node(data)
    if self.head == None:
      self.head = self.tail = node
      return node

    self.tail.next = node
    node.prev = self.tail
    self.tail = node
    return node

  def insert_before(self, p , data):
    node = Node(data)

    if p.prev:
      p.prev.next = node
      node.prev = p.prev
    else:
      self.head = node

    p.prev = node
    node.next = p
    return node

  def delete_prev_node(self, p):
    if p.prev == None:
      return

    if p.prev.prev:
      p.prev.prev.next = p
    else:
      self.head = p
    p.prev = p.prev.prev



list = DoublyLinkedList()

a = list.append("A")
b = list.append("B")
c = list.append("C")
d = list.append("D")
list.display()

list.insert_before(c , 'F')
list.insert_before(a, "$")
list.insert_before(a, "%")
list.display()


list.delete_prev_node(b)
list.display()