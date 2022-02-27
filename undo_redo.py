from abc import ABCMeta, abstractmethod
from copy import deepcopy


class Node(object):
    """ A Doubly-linked lists node. """
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList(object):
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def append(self, data):
        """ Append an item to the list. """
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = self.head
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.count += 1


    def deleteLast(self, data):
        """ Delete a node from the end of the list. """
        current = self.tail
        node_deleted = False
        if current is None or data is None:
            node_deleted = False
            print("This Linked List is empty, no element to delete; or the element to delete is not existing")
            return
        elif self.tail.data == data:
            self.tail = self.tail.prev
            self.tail.next = None
            node_deleted = True
        else:
            print("The last node is not the element we want to delete")
            return
        if node_deleted:
            self.count -= 1

    def deleteAllNodes(self):
        """ Clear the list. """
        # 1 & 2. create a temp node, if the head is not
        #   null make temp as head and move head to head
        #   next, then delete the temp, continue the
        #   process till head becomes null
        while (self.head != None):
            temp = self.head
            self.head = self.head.next
            temp = None

    def __getitem__(self, index):
        """ Get node through index. """
        if index > self.count - 1:
            raise Exception("Index out of range.")
        current = self.head  # Note subtle change
        for i in range(index):
            current = current.next
        return current.data

    def reverse(self):
        """ Reverse linked list. """
        current = self.head
        while current:
            temp = current.next
            current.next = current.prev
            current.prev = temp
            current = current.prev
        # Now reverse the order of head and tail
        temp = self.head
        self.head = self.tail
        self.tail = temp

    def sortList(self):
        """ Sort the list in increasing order. """
        # Check whether list is empty
        if (self.head == None):
            return
        else:

            current = self.head
            while (current.next != None):
                # Index will point to node next to current
                index = current.next;
                while (index != None):
                    # If current's data is greater than index's data, swap the data of current and index
                    if (current.data > index.data):
                        temp = current.data;
                        current.data = index.data;
                        index.data = temp;
                    index = index.next
                current = current.next

    def pop(self):
        """ Pop the last node of the list. """
        if self.head != None:
            if self.head.next == None:
                lastNode = self.head
                self.head = None
                return lastNode.data
            else:
                temp = self.head
                while (temp.next.next != None):
                    temp = temp.next
                lastNode = temp.next
                temp.next = None
                return lastNode.data

    def display(self):
        """ Display the list. """
        if self.head != None:
            temp = self.head
            while temp != None:
                #  Display node value
                print(" ", temp.data, end=" ")
                #  Visit to next node
                temp = temp.next

            print(end="\n  ")
        else:
            print("Empty Linked list")
            
            
class SetOperation(object):
    __metaclass__ = ABCMeta

    def __init__(self, _list, element):
        self._list = _list
        self.element = element


    @abstractmethod
    def __call__(self):
        return

    @abstractmethod
    def undo(self):
        return

class ElementAdder(SetOperation):

    def __call__(self):
        self._list.append(self.element)

    def undo(self):
        self._list.deleteLast(self.element)


class ReverseList(SetOperation):
    
    def __call__(self):
        self._list.reverse()

    def undo(self):
        self._list.reverse()

class SortList(SetOperation):

    def __call__(self):
        self.originaldata = deepcopy(self._list)
        self._list.sortList()


    def undo(self):
        temp = self.originaldata
        self._list.deleteAllNodes()
        for i in range(temp.count):
            self._list.append(temp[i])

class CommandManager(object):
    """ Undo Redo Interface """
    def __init__(self):
        self.undo_commands = DoublyLinkedList()
        self.redo_commands = DoublyLinkedList()

    def push_undo_command(self, command):
        """ Push the given command to the undo command list. """
        self.undo_commands.append(command)

    def pop_undo_command(self):
        """ Remove the last command from the undo command list and return it. """
        try:
            last_undo_command = self.undo_commands.pop()
        except IndexError:
            raise EmptyCommandStackError("Nothing to undo")
        return last_undo_command

    def push_redo_command(self, command):
        """ Push the given command to the redo command list. """
        self.redo_commands.append(command)

    def pop_redo_command(self):
        """ Remove the last command from the redo command list and return it. """
        try:
            last_redo_command = self.redo_commands.pop()
        except IndexError:
            raise EmptyCommandStackError("Nothing to redo")
        return last_redo_command

    def do(self, new_command):
        """ Execute the given command. """
        new_command()
        self.push_undo_command(new_command)
        self.redo_commands.deleteAllNodes()


    def undo(self, n=1):
        """ Undo the last n commands. The default is to undo only the last command. """
        for _ in range(n):
            command = self.pop_undo_command()
            command.undo()
            self.push_redo_command(command)


    def redo(self, n=1):
        """ Redo the last n commands which have been undone using the undo method. """
        for _ in range(n):
            command = self.pop_redo_command()
            command()
            self.push_undo_command(command)


def main() :
    dList = DoublyLinkedList()
    dList.append(5)
    dList.append(3)
    dList.append(2)
    dList.append(1)
    dList.append(4)
    dList.append(8)
    manage = CommandManager()
    print("Original list is: ")
    dList.display()
    print("List after sort: ")
    manage.do(SortList(dList, None))
    dList.display()
    print("List after reverse: ")
    manage.do(ReverseList(dList, None))
    dList.display()
    print("List after add 9 to the end of the list: ")
    manage.do(ElementAdder(dList, 9))
    dList.display()
    print("List after undo back to before we reversed the list: ")
    manage.undo(2)
    dList.display()
    print("List after add a 9 to the end again: ")
    manage.do(ElementAdder(dList, 9))
    dList.display()
    print("List after undo back to the original state of the list: ")
    manage.undo()
    dList.display()

if __name__ == "__main__": main()
