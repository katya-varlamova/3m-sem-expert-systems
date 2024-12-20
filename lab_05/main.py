import copy

class Atom:
    def __init__(self, name, terminals):
        self.name = name
        self.terminals = terminals

    def __str__(self):
        strterms = ""
        for term in self.terminals:
            strterms += str(term) + ", "
        return self.name + '(' + strterms.strip(", ") + ')'

    def __repr__(self):
        return self.__str__()


class Constant:
    def __init__(self, value):
        self.value = value
        self.variable = False

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()


class Variable:
    def __init__(self, name):
        self.name = name
        self.variable = True

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Table:
    def __init__(self):
        self.variables = dict()
        self.links = dict()

    def reset(self, other):
        self.variables = other.variables
        self.links = other.links

    def val(self, var):
        return self.variables[var.name]

    def var_links(self, var):
        return self.links[self.variables[var.name]]

    def __str__(self):
        res = ""
        for const in self.links.keys():
            res += str(self.links[const]) + ": " + str(const) + "\n"
        return res



def unification(table, p1, p2):
    print(p1, " and ", p2)
    if p1.name != p2.name:
        print('Имена не совпадают')
        return False

    if len(p1.terminals) != len(p2.terminals):
        print('Длины не совпадают')
        return False

    original = copy.deepcopy(table)
    for t1, t2 in zip(p1.terminals, p2.terminals):
        if t1.variable:
            if t2.variable:
                y = True

                if t1.name not in table.variables and t2.name not in table.variables:
                    table.variables[t1.name] = t2.name
                    table.variables[t2.name] = t1.name

                elif t1.name not in table.variables:
                    table.variables[t1.name] = table.variables[t2.name]

                elif t2.name not in table.variables:
                    table.variables[t2.name] = table.variables[t1.name]

                elif set([t1.name, table.variables[t1.name]]) != set([table.variables[t2.name], t2.name]):
                    y = False
    
                if y == False:
                    print("Переменная ", t1.name, " не соответствует другой переменной ", t2.name, ": ", table.val(t1),
                          " != ", table.val(t2), sep='')
                    table.reset(original)
                    return False

            else:
                y = True
                if t1.name in table.variables and type(table.variables[t1.name]) is not str:
                    if table.variables[t1.name].value != t2.value:
                        y = False

                if t1.name not in table.variables:
                    table.variables[t1.name] = t2

                if type(table.variables[t1.name]) is str:
                    k = table.variables[t1.name]
                    table.variables[t1.name] = t2
                    table.variables[k] = t2
                    table.links[t2.value] = {k}

                if t2.value not in table.links:
                    table.links[t2.value] = {t1.name}
                else:
                    table.links[t2.value].add(t1.name)

                if y == False:
                    print("Несоответствующее значение переменной константе: ", t1.name, " = ", table.val(t1),
                          "константа", t2.value)
                    table.reset(original)
                    return False
        else:
            if t2.variable:
                y = True

                if t2.name in table.variables and type(table.variables[t2.name]) is not str:
                    if table.variables[t2.name].value != t1.value:
                        y = False

                if t2.name not in table.variables:
                    table.variables[t2.name] = t1

                if type(table.variables[t2.name]) is str:
                    k = table.variables[t2.name]
                    table.variables[t2.name] = t1
                    table.variables[k] = t1
                    table.links[t1.value] = {k}

                if t1.value not in table.links:
                    table.links[t1.value] = {t2.name}
                else:
                    table.links[t1.value].add(t2.name)

                if y == False:
                    print("Несоответствующее значение переменной константы:", t2.name, "=", table.val(t2),
                          "константа", t1.value)
                    table.reset(original)
                    return False
            else:
                if t1.value != t2.value:
                    print("Константы не соответствуют:", t1.value, "!=", t2.value)
                    table.reset(original)
                    return False
    return True

def test_unif():
    c_N = Constant('N')
    c_M1 = Constant('M1')
    c_W = Constant('W')
    c_A1 = Constant('A1')

    v_x = Variable("x")
    v_y1 = Variable("y1")
    v_y3 = Variable("y3")
    v_y4 = Variable("y4")
    v_y2 = Variable("y2")
    v_z = Variable("z")
    v_x1 = Variable("x1")
    v_x2 = Variable("x2")
    v_x3 = Variable("x3")
    v_x4 = Variable("x4")

    node1 = Atom("A", [c_M1, c_W])
    node2 = Atom("A", [c_M1, c_W])
    table = Table()
    print("Результат: ", unification(table, node1, node2))
    print("----------")

    node1 = Atom("R", [c_M1, c_W])
    node2 = Atom("A", [c_M1, c_W])
    table = Table()
    print("Результат: ", unification(table, node1, node2))
    print("----------")

    node1 = Atom("A", [c_M1, c_N])
    node2 = Atom("A", [c_M1, c_W])
    table = Table()
    print("Результат: ", unification(table, node1, node2))
    print("----------")

    node1 = Atom("A", [v_x3, v_y2, v_y2])
    node2 = Atom("A", [v_x1, v_y1, v_y1])
    table = Table()
    print("Результат: ", unification(table, node1, node2))
    print("Ссылки:" , table.links)
    print("Переменные: ", table.variables)
    print("----------")

    node1 = Atom("A", [v_x4, v_y3, v_y3])
    node2 = Atom("A", [v_x2, v_y4, v_y4])
    table = Table()
    print("Результат: ", unification(table, node1, node2))
    print("Ссылки:" , table.links)
    print("Переменные: ", table.variables)
    print("----------")

    node1 = Atom("A", [v_x1, v_y3, v_y3])
    node2 = Atom("A", [v_x2, c_A1, c_A1])
    table = Table()
    print("Результат: ", unification(table, node1, node2))
    print("Ссылки:" , table.links)
    print("Переменные: ", table.variables)
    print("----------")

    node1 = Atom("A", [v_x1, v_y3, v_y3])
    node2 = Atom("A", [v_x2, c_A1, c_N])
    table = Table()
    print("Результат: ", unification(table, node1, node2))
    print("Ссылки:" , table.links)
    print("Переменные: ", table.variables)
    print("----------")

    node1 = Atom("A", [v_x1, v_y3, v_y3])
    node2 = Atom("A", [v_x2, c_A1, v_y4])
    table = Table()
    print("Результат: ", unification(table, node1, node2))
    print("Ссылки:" , table.links)
    print("Переменные: ", table.variables)
    print("----------")

if __name__ == "__main__":
    test_unif()
