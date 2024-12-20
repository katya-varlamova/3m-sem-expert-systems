import copy

def unification(table, p1, p2):
    if p1.name != p2.name:
        #print('Имена не совпадают')
        return False

    if len(p1.terminals) != len(p2.terminals):
        #print('Длины не совпадают')
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
                    #print("Переменная ", t1.name, " не соответствует другой переменной ", t2.name, ": ", table.val(t1),
                    #      " != ", table.val(t2), sep='')
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
                    #print("Несоответствующее значение переменной константе: ", t1.name, " = ", table.val(t1),
                    #      "константа", t2.value)
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
                    #print("Несоответствующее значение переменной константы:", t2.name, "=", table.val(t2),
                    #      "константа", t1.value)
                    table.reset(original)
                    return False
            else:
                if t1.value != t2.value:
                    #print("Константы не соответствуют:", t1.value, "!=", t2.value)
                    table.reset(original)
                    return False
    return True

class Atom:
    def __init__(self, name, terminals, sign):
        self.name = name
        self.terminals = terminals
        self.sign = sign

    def __str__(self):
        strterms = ""
        for term in self.terminals:
            strterms += str(term) + ", "
        return self.name + '(' + strterms.strip(", ") + ')'

    def __repr__(self):
        a = self.__str__()
        return f"{self.sign}{a}"

    def print(self):
        t = ""
        if self.sign == -1:
            t = "-"
        a = self.__str__()
        print(f"{t}{a}", end = " ")

    def __eq__(self, other):
        if isinstance(other, Atom):
            return self.__hash__() == other.__hash__() # unification(table, self, other)
        return False

    def __hash__(self):
        objs = []
        for val in self.terminals:
            if type(val) is Constant:
                objs.append(val.value)
            else:
                objs.append(val.name)
        return hash((self.name, self.sign, *objs))

    
class Constant:
    def __init__(self, value):
        self.value = value
        self.variable = False

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()
    def __hash__(self):
        return hash((self.value))

class Variable:
    def __init__(self, name):
        self.name = name
        self.variable = True

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
    def __hash__(self):
        return hash((self.name, self.variable))


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

class Clause:
    def __init__(self, atoms: list):
        self.atoms = atoms
        self.seen = []
    def add_seen(self, seen_id):
        self.seen.append(seen_id)
    def get_seen(self):
        return self.seen
    def get_atoms(self):
        return self.atoms
    def print(self):
        l = len(self.atoms)
        print("(", end = "")
        for i in range(l):
            self.atoms[i].print()
            if i != l - 1:
                print("+", end = " ")
        print(")", end = "\n")
    def __eq__(self, other):
        if isinstance(other, Clause):
            return set(self.atoms) == set(other.atoms)
        return False
        
class KNF:
    def __init__(self, clauses: list, label="KNF: "):
        self.clauses = clauses
        self.label = label
    def print(self):
        print(self.label, "")
        for c in self.clauses:
            c.print()
        print()
var_count = 5        
class Resolution:
    @staticmethod
    def resolve(c1: Clause, c2: Clause) -> Clause:
        new_atoms = []
        n_c1 = c1.atoms
        n_c2 = c2.atoms
        change = False
        for atom1 in c1.atoms:
            for atom2 in c2.atoms:
                table = Table()
                if unification(table, atom1, atom2) and atom1.sign != atom2.sign:
                    n_c1_ = []
                    for a in n_c1:
                        if a != atom1:
                            new_terms = []
                            for term in a.terminals:
                                if term.variable:
                                    if type(table.variables[term.name]) is str:
                                        new_terms.append(Variable(table.variables[term.name]))
                                    else:
                                        new_terms.append(table.variables[term.name])
                                else:
                                    new_terms.append(term)
                            n_c1_.append(Atom(a.name, new_terms, a.sign))
                    n_c2_ = []
                    for a in n_c2:
                        if a != atom2:
                            new_terms = []
                            for term in a.terminals:
                                if term.variable:
                                    if type(table.variables[term.name]) is not str:
                                        new_terms.append(table.variables[term.name])
                                    else:
                                        new_terms.append(Variable(term.name))
                                else:
                                    new_terms.append(term)
                            n_c1_.append(Atom(a.name, new_terms, a.sign))
                    global var_count
                    
                    atoms = list(set(n_c1_ + n_c2_))
                    
                    replaced = {}
                    clause = []
                    for a in atoms:
                        new_terms = []
                        for term in a.terminals:
                            if term.variable:
                                if term.name not in replaced:
                                    replaced[term.name] = Variable(f"x{var_count}")
                                    var_count += 1
                                new_terms.append(replaced[term.name])
                            else:
                                new_terms.append(term)
                        clause.append(Atom(a.name, new_terms, a.sign))
                                    
                    return Clause(clause)
        return None

    @staticmethod
    def run_full(axioms: list, target: list):
        clauses = [Clause(list(set(a.get_atoms()))) for a in target + axioms]
        
        new_clauses = [Clause(list(set(a.get_atoms()))) for a in target + axioms]
        KNF(new_clauses, "дизъюнкты: ").print()
        iters = 200
        while True and iters:
            found = False
            
            for i in range(len(clauses)):
                if found:
                    break
                for j in range(i + 1, len(clauses)):
                    if i in clauses[j].get_seen() or j in clauses[i].get_seen():
                        continue
                    resolvent = Resolution.resolve(clauses[i], clauses[j])
                    if not resolvent:
                        continue
                    if not resolvent.atoms:
                        KNF([clauses[i]], "первый дизъюнкт: ").print()
                        KNF([clauses[j]], "второй дизъюнкт: ").print()
                        KNF([resolvent], "резольвента: ").print()
                        print("Доказана истинность  предположения")
                        return
                    if resolvent in clauses:
                        continue
                    KNF([clauses[i]], "первый дизъюнкт: ").print()
                    KNF([clauses[j]], "второй дизъюнкт: ").print()
                    KNF([resolvent], "резольвента: ").print()
                    clauses[j].add_seen(i)
                    clauses[i].add_seen(j)
                    new_clauses = clauses + [resolvent]                                                                           # clauses[:i] + clauses[i + 1:j] + clauses[j + 1:] + [resolvent] #
                    found = True
                    break
            print("-------------------------------------")
            KNF(new_clauses, "дизъюнкты: ").print()
            if new_clauses == clauses:
                print("Доказано противоречие.")
                return
            clauses = new_clauses
            iters -= 1
                

def test_resolve():
    a = Clause([Atom("A", 1)])
    b = Clause([Atom("D", 1), Atom("C", -1), Atom("B", 1), Atom("F", 1)])
    a.print()
    b.print()
    cl = Resolution.resolve(a, b)
    if cl:
        cl.print()
    else:
        print(None)
#test_resolve()
def test1():
    axioms = [    Clause([Atom("A", 1), Atom("B", 1)]),
        Clause([Atom("A", 1), Atom("C", -1)]),
        Clause([Atom("A", -1), Atom("D", 1)]),
        Clause([Atom("B", -1), Atom("C", 1)]),
        Clause([Atom("C", -1), Atom("D", -1)])
    ]


    target = [    Clause([Atom("A", -1), Atom("C", 1)]),
        Clause([Atom("B", 1), Atom("D", 1)])
    ] ## already with -


    Resolution.run_full(axioms, target)
def test2():
    axioms = [    Clause([Atom("Z", -1), Atom("P", 1)]),
        Clause([Atom("S", -1), Atom("M", 1)]),
        Clause([Atom("Z", 1), Atom("S", 1)]),
        Clause([Atom("Z", -1), Atom("M", -1)]),
        Clause([Atom("S", -1), Atom("P", -1)])
    ]


    target = [    Clause([Atom("M", -1), Atom("P", 1)]),
        Clause([Atom("M", 1), Atom("P", -1)])
    ]


    Resolution.run_full(axioms, target)
    
def test3():
    axioms = [    Clause([Atom("A", -1), Atom("B", -1), Atom("C", 1)]),
        Clause([Atom("C", -1), Atom("D", -1), Atom("M", -1)]),
        Clause([Atom("N", 1), Atom("D", 1)]),
        Clause([Atom("N", 1), Atom("M", 1)])
    ]


    target = [    Clause([Atom("A", 1)]),
                  Clause([Atom("B", 1)]),
                  Clause([Atom("N", -1)]) # Clause([Atom("N", -1)])
    ]


    Resolution.run_full(axioms, target)
def test_4():
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


    
    axioms = [    Clause([Atom("Z", [c_A1], -1), Atom("P", [v_y], 1)]),
        Clause([Atom("S", [c_W], -1), Atom("M", [c_A1], 1)]),
        Clause([Atom("Z", [v_x2], 1), Atom("S", [v_x3], 1)]),
        Clause([Atom("Z", [v_x4], -1), Atom("M", [v_x5], -1)]),
        Clause([Atom("S", [v_x6], -1), Atom("P", [v_x7], -1)])
    ]


    target = [    Clause([Atom("M", [v_x8], -1), Atom("P", [v_x9], 1)]),
        Clause([Atom("M", [v_x10], 1), Atom("P", [v_x11], -1)])
    ]
    
    Resolution.run_full(axioms, target)
def test_5():
    c_lena = Constant('LENA')
    c_rain = Constant('RAIN')
    c_snow = Constant('SNOW')
    c_petya = Constant('PETYA')

    v_x1 = Variable("x1")
    v_x2 = Variable("x2")
    v_x3 = Variable("x3")
    v_x4 = Variable("x4")
    v_y1 = Variable("y1")
    v_y2 = Variable("y2")

    
    axioms = [
        Clause([Atom("L", [c_petya, c_rain], 1)]),
        Clause([Atom("L", [c_petya, c_snow], 1)]),
        Clause([Atom("S", [v_x1], 1), Atom("M", [v_x1], 1)]),
        Clause([Atom("M", [v_x2], -1), Atom("L", [v_x2, c_rain], -1)]),
        Clause([Atom("S", [v_x3], -1), Atom("L", [v_x3, c_snow], 1)]),
        Clause([Atom("L", [c_lena, v_y1], -1), Atom("L", [c_petya, v_y1], -1)]),
        Clause([Atom("L", [c_lena, v_y2], 1), Atom("L", [c_petya, v_y2], 1)]),
    ]


    target = [Clause([Atom("M", [v_x4], -1), Atom("S", [v_x4], 1)])]
    
    Resolution.run_full(axioms, target)
if __name__ == "__main__":
    test_5()
