class Stack:
    def __init__(self):
        self.elements = []

    def length(self):
        return len(self.elements)

    def push(self, element):
        self.elements.append(element)

    def push_arr(self, element_arr):
        for i in range(len(element_arr) - 1, -1, -1):
            self.push(element_arr[i])

    def pop(self):
        if self.length() == 0:
            return None
        return self.elements.pop()

    def peek(self):
        element = self.pop()
        self.push(element)
        return element

    def is_exist(self, item):
        is_found = False
        tmp_stack = Stack()

        while self.length() != 0:
            element = self.pop()
            tmp_stack.push(element)

            if element == item:
                is_found = True
                break
        self.__upgrade_stack(tmp_stack)

        return is_found

    def __upgrade_stack(self, stack):
        while stack.length() != 0:
            self.push(stack.pop())

    def show(self):
        tmp_stack = Stack()
        while self.length() != 0:
            tmp_stack.push(self.pop())

        while tmp_stack.length() != 0:
            element = tmp_stack.pop()
            if tmp_stack.length() != 0:
                print(f'{element} -> ', end='')
            else:
                print(f'{element}')