from items import *
from search import Search


def show(arr: list):
    if arr is None:
        print("Not found")
        return
    for i in range(len(arr) - 1, -1, -1):
        if i != 0:
            print(f'{arr[i]} <- ', end='')
        else:
            print(f'{arr[i]}')


def test_1():
    c_N = Constant('N')
    c_M1 = Constant('M1')
    c_W = Constant('W')
    c_A1 = Constant('A1')

    v_x = Variable("x")
    v_y = Variable("y")
    v_z = Variable("z")
    v_x1 = Variable("x1")
    v_x2 = Variable("x2")
    v_x3 = Variable("x3")
    v_x4 = Variable("x4")
    v_x5 = Variable("x5")
    v_x6 = Variable("x6")
    v_x7 = Variable("x7")
    v_x8 = Variable("x8")
    v_x9 = Variable("x9")
    v_x10 = Variable("x10")
    v_x11 = Variable("x11")
    v_x12 = Variable("x12")


    rule_arr = [
        Rule(1, Node("C", [v_x]), [Node("W1", [v_y]), Node("A", [v_x]), Node("S", [v_x, v_y, v_z]), Node("H", [v_z])]),
        Rule(2, Node("S", [c_W, v_x1, c_N]), [Node("M", [v_x1]), Node("O", [c_N, v_x1])]),
        Rule(3, Node("W1", [v_x2]), [Node("M", [v_x2])]),
        Rule(4, Node("H", [v_x3]), [Node("E", [v_x3, c_A1])]),

    ]
    facts = [Node("O", [c_N, c_M1]), Node("M", [c_M1]), Node("A", [c_W]), Node("E", [c_N, c_A1])]
    Search(rule_arr).run(Node("C", [c_W]), facts)

def test_2():
    c_N = Constant('N')
    c_M1 = Constant('M1')
    c_W = Constant('W')
    c_A1 = Constant('A1')

    v_x = Variable("x")
    v_y = Variable("y")
    v_z = Variable("z")
    v_x1 = Variable("x1")
    v_x2 = Variable("x2")
    v_x3 = Variable("x3")
    v_x4 = Variable("x4")
    v_x5 = Variable("x5")
    v_x6 = Variable("x6")
    v_x7 = Variable("x7")
    v_x8 = Variable("x8")
    v_x9 = Variable("x9")
    v_x10 = Variable("x10")
    v_x11 = Variable("x11")
    v_x12 = Variable("x12")


    rule_arr = [
        Rule(1, Node("C", [v_x]), [Node("W1", [v_y]),
                                   Node("A", [v_x]),
                                   Node("S", [v_x, v_y, v_z]),
                                   Node("H", [v_z])]),
        Rule(2, Node("S", [c_W, v_x1, c_N]), [Node("M", [v_x1]),
                                              Node("O", [c_N, v_x1])]),
        Rule(3, Node("W1", [v_x2]), [Node("M", [v_x2])]),
        Rule(4, Node("H", [v_x3]), [Node("E", [v_x3, c_A1])]),

    ]
    facts = [Node("O", [c_N, c_M1]),
             Node("M", [c_M1]),
             Node("A", [c_W]),
             Node("E", [c_N, c_A1])]
    Search(rule_arr).run(Node("C", [c_W]), facts)


    
if __name__ == "__main__":
    test_1()
