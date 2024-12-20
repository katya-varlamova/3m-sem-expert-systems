from items import *
from stack import Stack
import copy
class Search:
    def __init__(self, rule_arr: [Rule]):
        self.rule_arr = rule_arr

        self.goal_node = None
        self.table = Table()
        self.solution_flg = 1
        self.no_solution_flg = 1
        self.closed_arr = []

    def run(self, goal_node: Node, in_node_arr: [Node]):
        self.goal_node = goal_node
        self.set_nodes_closed(in_node_arr)

        while self.solution_flg and self.no_solution_flg:
            rule_cnt = self.parent_search()

            if self.solution_flg == 0:
                return

            if rule_cnt == 0:
                self.no_solution_flg = 0
                print("Решение не найдено")


    def parent_search(self):
        cnt_rules = 0
        
        for rule in self.rule_arr:
            if self.solution_flg:
                if rule.label != Label.OPEN:
                    continue
                print("\n")
                print(rule, " сейчас обрабатывается")
                if self.close_goal_if_close_nodes_cover(rule.node_arr, rule.out_node):
                    print(f'Правило {rule.number}: все вершины закрыты')
                    rule.label = Label.CLOSE

                    if unification(self.table, rule.out_node, self.goal_node):
                        self.solution_flg = 0
                        print(f'Правило {rule.number} имеет выходную вершину равную целевой')
                        
                    cnt_rules += 1
            else:
                break
 
        print(f'Закрытые правила сейчас: ', end='')
        self.print_closed_rules()
        return cnt_rules

    def close_goal_if_close_nodes_cover(self, in_node_arr: [Node], goal_node):
        print("доказанные факты: ", self.closed_arr)
        print("в процессе доказательства: ", in_node_arr, " -> ", goal_node)
        
        table = Table() #copy.deepcopy(self.table)
        for node in in_node_arr:
            found = False
            for node_closed in self.closed_arr:
                if unification(table, node, node_closed):
                    found = True
                    break
            
            if not found:
                print("Не удалось унифицировать: ", node)
                return False
        self.table = table

        new_terminals = []
        for term in goal_node.terminals:
            if term.variable:
                new_terminals.append(self.table.variables[str(term)])
            else:
                new_terminals.append(term)
        goal_node.terminals = new_terminals
        self.closed_arr.append(goal_node)
        print("Удалось унифицировать; доказанные факты сейчас: ", self.closed_arr)
        return True

    def set_nodes_closed(self, node_arr):
        for node in node_arr:
            self.closed_arr.append(node)

    def print_closed_rules(self):
        for rule in self.rule_arr:
            if rule.label == Label.CLOSE:
                print(rule.number, end=' ')
        print()

    def print_nodes(self, node_arr: [Node]):
        for node in node_arr:
            print(node, end=' ')
        print()
