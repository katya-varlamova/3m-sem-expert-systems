class Atom:
    def __init__(self, name: str, sign: int):
        self.name = name
        self.sign = sign
    def print(self):
        t = ""
        if self.sign == -1:
            t = "-"
        print(f"{t}{self.name}", end = " ")

class Clause:
    def __init__(self, atoms: list):
        self.atoms = atoms
    def print(self):
        l = len(self.atoms)
        print("(", end = "")
        for i in range(l):
            self.atoms[i].print()
            if i != l - 1:
                print("+", end = " ")
        print(")", end = "")
        
class KNF:
    def __init__(self, clauses: list, label="KNF: "):
        self.clauses = clauses
        self.label = label
    def print(self):
        print(self.label, "")
        for c in self.clauses:
            c.print()
        print()
        
class Resolution:
    @staticmethod
    def resolve(c1: Clause, c2: Clause) -> Clause:
        new_atoms = []
        n_c1 = c1.atoms
        n_c2 = c2.atoms
        change = False
        for atom1 in c1.atoms:
            for atom2 in c2.atoms:
                if atom1.name == atom2.name and atom1.sign != atom2.sign:
                    n_c1 = [a for a in n_c1 if a != atom1]
                    n_c2 = [a for a in n_c2 if a != atom2]
                    change = True
        if change:
            return Clause(n_c1 + n_c2)
        return None

    @staticmethod
    def run_full(axioms: list, target: list):
        clauses = axioms + target
        new_clauses = axioms + target
        while True:
            found = False
            
            for i in range(len(clauses)):
                if found:
                    break
                for j in range(i + 1, len(clauses)):
                    resolvent = Resolution.resolve(clauses[i], clauses[j])
                    if not resolvent:
                        continue
                    if not resolvent.atoms:
                        print("Доказано противоречие.")
                        return
                    KNF([resolvent], "resolvent: ").print()
                    new_clauses = clauses[:i] + clauses[i + 1:j] + clauses[j + 1:] + [resolvent]
                    found = True
                    break
            KNF(clauses, "old: ").print()
            KNF(new_clauses, "new: ").print()
            if new_clauses == clauses:
                print("Доказана истинность  предположения")
                return
            clauses = new_clauses
                

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
    ]


    Resolution.run_full(axioms, target)
def test2():
    axioms = [    Clause([Atom("Z", -1), Atom("P", 1)]),
        Clause([Atom("S", -1), Atom("M", 1)]),
        Clause([Atom("Z", 1), Atom("S", 1)]),
        Clause([Atom("Z", -1), Atom("M", -1)]),
        Clause([Atom("S", -1), Atom("P", -1)])
    ]


    target = [    Clause([Atom("P", 1), Atom("M", -1)]),
        Clause([Atom("P", -1), Atom("M", 1)])
    ]


    Resolution.run_full(axioms, target)
# дописать тест
test2()
